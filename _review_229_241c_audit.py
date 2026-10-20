from pathlib import Path
import json,sys,re,hashlib,datetime,subprocess,xml.etree.ElementTree as E,shutil,collections
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-229-241c'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W))
ids=['art-'+x for x in '229 230 231 231a 232 233 234 235 236 236a 237 237a 237b 238 239 240 241 241a 241b 241c'.split()]
now=datetime.datetime.now(datetime.timezone.utc).isoformat();before=json.loads((S/(P+'-before-hashes.json')).read_text())
assert all(before[k]==hashlib.sha256(v.encode()).hexdigest() for k,v in cs.items() if k not in ids)
records=json.loads((S/(P+'-fetch.json')).read_text());external=json.loads((S/(P+'-external-fetch.json')).read_text())
assert all(x['accepted'] and sha(W/x['raw_path'])==x['sha256'] for x in records+external)
r=E.parse(S/(P+'-selected.xml')).getroot();expected=['art-'+a.get('label').removeprefix('Artikel ') for a in r.iter('artikel')];parsed=[u['id'] for u in us]
assert expected==parsed and len(expected)==len(set(expected))==639
assert sha(S/(P+'-selected.xml'))==sha(S/'official-2026-09-01.xml')
def flat(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+flat(c)+' '+(c.tail or '') for c in e)
norm=lambda s:re.sub(r'\s+','',s)
for a in r.iter('artikel'):assert norm(flat(a))==norm(by['art-'+a.get('label').removeprefix('Artikel ')]['text'])
assert not [e for e in r.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
wt=E.parse(S/(P+'-wti.xml')).getroot();dates=sorted({e.get('waarde') for e in wt.findall('./wijzigingen/regeling/datum') if e.get('waarde')})
assert max(d for d in dates if d<='2026-10-21')=='2026-09-01';assert not [d for d in dates if '2026-10-01'<d<='2026-10-21']
names=['units.jsonl','meta.json','coverage-evidence.json','completeness-report.json'];hashes={n:sha(W/n) for n in names}
for script in ['_parse.py','_coverage.py']:
 q=subprocess.run([sys.executable,str(W/script)],capture_output=True,text=True);assert q.returncode==0,q.stderr
assert hashes=={n:sha(W/n) for n in names}
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
save(S/(P+'-parser-check.json'),{'ok':True,'expected_ids':expected,'parsed_ids':parsed,'missing':[],'duplicates':[],'all_official_article_texts_equal':True,'annex_disposition':comp['annexes'],'opening_closing':comp['non_article_text'],'reproduced_hashes':hashes,'official_xml_sha256':sha(S/(P+'-selected.xml'))})
pre=json.loads((S/'author-art-229-241c-preflight-result.json').read_text());pre.update(verified_at=now,review_date_local='2026-10-21',parser_evidence='sources/'+P+'-parser-check.json')
pre['version_evidence'].update(fresh_records='sources/'+P+'-fetch.json',future_dates_excluded=[d for d in dates if d>'2026-10-21'],fresh_wti_matches_previous=sha(S/(P+'-wti.xml'))==sha(S/'author-art-229-241c-wti.xml'))
assert pre['version_evidence']['fresh_wti_matches_previous']
for h in pre['historical_versions_checked']:
 assert sha(W/h['path'])==h['sha256'];old=E.parse(W/h['path']).getroot();labels=[a.get('label') for a in old.iter('artikel')];assert len(labels)==len(set(labels));h['assigned_present_ids']=['art-'+a.removeprefix('Artikel ') for a in labels if 'art-'+a.removeprefix('Artikel ') in ids]
pre['limitations']=['Separate external transitional statutes cited in editorial notes were not independently analysed for historical proceedings.','The substantive second pass covers exactly the twenty assigned units; no whole-book review claimed.']
save(S/(P+'-preflight-result.json'),pre)
p=W/'preflight-result.json';j=json.loads(p.read_text());j['bounded_review_art_229_241c']=pre;save(p,j)
comparisons=[]
for year,ecli in [('2023','2023-1135'),('2005','2005-at2650')]:
 a=S/(P+'-hr-'+year+'.xml');b=S/('author-art-229-241c-hr-'+year+'.xml');root=E.parse(a).getroot();u=root.find('{*}uitspraak');t=''.join(u.itertext());assert a.read_bytes()==b.read_bytes();(S/(P+'-hr-'+year+'.txt')).write_text(t)
 local=Path('/Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr/ecli-nl-hr-'+ecli+'.md');dest=S/(P+'-hr-'+year+'-local.md');shutil.copyfile(local,dest)
 paras=u.findall('.//{*}para');miss=[norm(''.join(e.itertext()))[:100] for e in paras if norm(''.join(e.itertext())) not in norm(dest.read_text())]
 comparisons.append({'year':year,'official_sha256':sha(a),'full_text_chars':len(t),'same_as_author_capture':True,'local_corpus_path':str(local),'local_snapshot':str(dest.relative_to(W)),'local_sha256':sha(dest),'official_paragraphs':len(paras),'unmatched_paragraph_prefixes':miss})
save(S/(P+'-case-comparison.json'),comparisons)
log=json.loads((S/'author-art-229-241c-search-log.json').read_text());log['second_pass']={'checked_at':now,'scope':'Existing selective research reviewed, no additional case asserted. Full official judgments freshly fetched and read, corpus snapshots compared.','holdings':'2023 paragraphs3.1.2–3.1.7: actual and constructive knowledge, real rescue prospects;3.2.2: concrete contractual booking qualification;3.3.2–3.3.3 limits bank exception, not blanket approval. 2005 paragraphs3.4.1–3.4.4 and3.6: statutory termination versus contractual dissolution, potential6:248(2)limit and distinct damages.','external_law':'Fresh current BW6:136, BW7:672 and Rv490b read directly; preserve statutory cross-reference numbers, no silent repair. Rv490b(2)condition corrected in241b.','limitations':'No exhaustive new case-law search or universal later-treatment audit claimed.'};save(S/(P+'-search-log.json'),log)
notes=[
'Beide leden en verwijzing61 gecontroleerd: baten en lasten bestaande gemeenschap, afzonderlijk privévermogen partner en terugneming, zonder nieuwe partneraansprakelijkheid.',
'Alle vier leden: afdwingingspauze, schorsing versus verval/onherroepelijkheid, vervroeging, registerverklaring, voorrang beperkt tot belaste goederen. Verwijzing36 uitgewerkt tot zesmaandenverlenging en van rechtswege aanvangende vervaltermijnen; geen algemene stuiting.',
'Alle drie leden: lopende/nieuwe procedure, beperkte discretionaire uitspraakopschorting na erkenning en ontbreken derdenbelang, medewerking bij eis en verweer boedelrechten.',
'Erkenning via19 en5(3), verlies beheer/beschikking en beperking tot vordering over concreet goed/recht gecontroleerd; geen universele bevoegdheid afgeleid.',
'Alle drie uitzonderingen: dekkingsgrens voorrang, wettelijke vastgestelde onderhoudslasten/vooraf vervallen termijnen/rechterlijke vaststelling, huurkooptermijnen tegenover237aafwikkeling gecontroleerd.',
'Gezamenlijke evenredige betaling van overige vooraf bestaande schulden gecontroleerd; numeriek20/80voorbeeld juist, medewerking228 heft verbod niet op;236a/boedelschulden onderscheiden.',
'Alle drie leden en volledige HR2023 gelezen. Berekening261/262 uitgewerkt: voorwaarden, onenigheid, onzekere/periodieke/later opeisbare vorderingen.6:136 rechtstreeks geverifieerd; concrete3.2.2niet tot onbeperkte verrekeningsbevoegdheid uitgebreid.',
'Alle drie leden en55/56 gecontroleerd. HR2023eigen oordeel3.1.2–3.1.7omvat behoren te weten en omstandigheden; financiering geen automatische goede trouw; na aanvang overgenomen posten uitgesloten.',
'Alle drie leden: onvolledige wederzijdse nakoming, schriftelijke redelijke termijn aan beiden, verval eigen nakomingsrecht zonder automatische ontbinding, zekerheid desverlangd, persoonlijke-prestatieuitzondering.',
'Vooraf gesloten overeenkomst versus vooraf verkregen vordering, ontbinding/vernietiging/schadevergoeding en233route gecontroleerd; regel schept materiële aanspraak niet zelf.',
'Beurswaren, leveringstijdstip of termijn na aanvang en236situatie gecontroleerd. Automatische ontbinding door voorlopige verlening en schade beide richtingen onderscheiden.',
'Alle drie leden: beide ontbindingsgerechtigden, huurkoop/scheepshuurkoop, geen automatische ontbinding, gevolgen koperswanprestatie, verkopersclaim233 versus232(3).',
'Alle drie leden: noodzakelijke limitatief beschreven nutslevering, oude betalingsverbintenis, eerdere tekortkoming, insolventie/beslagbeding alleen met goedvinden beiden;2005arrest niet uitgebreid tot andere diensten.',
'Alle drie leden en volledige HR2005gelezen. Plaatselijk eindtijdstip, termijn/vooruitbetaling, boedelhuur/pacht gecontroleerd. Geen schadevergoeding bij wettelijke opzegging en mogelijke6:248(2)grens contractueel beding uit3.4.2/3.6 verduidelijkt; partijstellingen niet als holding gebruikt.',
'Alle vier leden en actuele BW7:672gelezen. Langere werkgeverstermijnen2/3/4maanden per diensttijd uitgewerkt; gewone werknemerstermijn1maand benoemd. Letterlijke239(2)verwijzing behouden, overige voorwaarden niet weggeredeneerd; boedelloon/premies en agentuur onderscheiden.',
'Alle drie leden: bewijspositie voor/na publicatie en werkelijke bekendheid, zelfstandige bevrijding boedelvoordeel. Voorbeeld gewijzigd: gedeeltelijke bevrijding en geen verrekening234.',
'Borgen/andere medeschuldenaren, eigen verweermiddelen/garantieomvang, derdenbelang231(2)en afzonderlijke regresbehandeling gecontroleerd; geen universele opschorting.',
'Alle vier leden: afzonderlijke beschikking, belanghebbende/ambtshalve, uitzondering boedelschuldeisers,2+2maanden, voorwaarden, termijnschorsing en dagaanvang gecontroleerd. Officiële terminologie curator in lid3 zichtbaar gelaten.',
'Beide leden en actuele Rv490bgelezen. Fout hersteld: bewaarstorting is onder verwijzingsvoorwaarden, niet onvoorwaardelijk bij iedere ontvangst. Bij ontbreken verdelingsovereenstemming volledig bedrag i.p.v.overschot; rangregelingroute uitgelegd.',
'Beide leden: bodembeslaguitwinning versus leggen/bestaan, RCuitzondering, vreemd goed op bodem, later beslag en voorafgaand deurwaardersexploot eigenaar/andere pandhouder gecontroleerd. Geen opheffing afkoeling door exploot afgeleid.'
]
rows=[]
for i,n in zip(ids,notes):
 after=hashlib.sha256(cs[i].encode()).hexdigest();rows.append({'id':i,'official_path':by[i]['official_path'],'finding':n,'result':'corrected' if before[i]!=after else 'accepted_without_change','before_sha256':before[i],'after_sha256':after,'statutory_sha256':hashlib.sha256(by[i]['text'].encode()).hexdigest()})
assert len(rows)==20
paras=[p for i in ids for p in cs[i].split('\n\n') if len(p)>200];assert len(paras)==len(set(paras));assert all(len(cs[i])>=700 and not re.search('TODO|FIXME',cs[i]) for i in ids)
for script,suffix in [('build_repo.py','build.txt'),('validate.py','validation.txt')]:
 q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/'+script,str(W)],capture_output=True,text=True);(S/(P+'-'+suffix)).write_text(q.stdout+q.stderr)
 if script=='validate.py':validation=json.loads(q.stdout)
assert validation['verbatim_ratio']==1.0
save(S/(P+'-validation.json'),validation)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[r['id'] for r in rows if r['result']=='corrected'],'checked_at_utc':now,'whole_book_complete':False,'validation_result':validation,'limitations':['Only twenty assigned units reviewed; no external professional approval.','Existing selective judicial research verified; no exhaustive case-law search claimed.','Whole-book authoring remains incomplete; full strict validation failure outside this scope is preserved.','Separate transitional statutes in editorial notes not independently analysed for historical proceedings.']}
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,result)
checks={'ok':True,'reviewed_ids':ids,'unassigned_commentaries_unchanged':True,'duplicate_long_paragraphs':0,'commentary_chars':{i:len(cs[i]) for i in ids},'source_agreement':1.0,'whole_book_complete':False}
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,checks)
p=S/'verification.json';j=json.loads(p.read_text());j['bounded_review_art_229_241c']={'records':records,'external_records':external,'preflight':'sources/'+P+'-preflight-result.json'};save(p,j)
p=W/'status.json';j=json.loads(p.read_text());j['bounded_review_art_229_241c']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/'+P+'-result.json'};save(p,j)
print(json.dumps({'reviewed':20,'changed':result['changed_units'],'verbatim_ratio':1.0,'validation':validation}))
