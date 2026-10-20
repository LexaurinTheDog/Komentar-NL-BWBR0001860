from pathlib import Path
import json,sys,re,hashlib,datetime,subprocess,xml.etree.ElementTree as E,shutil,collections,html
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-241d-253'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W))
ids=['art-'+x for x in '241d 241e 242 243 244 245 246 247 247a 247b 247c 247d 248 249 249a 250 250a 251 252 253'.split()]
now=datetime.datetime.now(datetime.timezone.utc).isoformat();before=json.loads((S/(P+'-before-hashes.json')).read_text())
assert set(before)==set(cs) and all(before[k]==hashlib.sha256(v.encode()).hexdigest() for k,v in cs.items() if k not in ids)
records=json.loads((S/(P+'-fetch.json')).read_text());cases=json.loads((S/(P+'-case-fetch.json')).read_text());external=json.loads((S/(P+'-external-fetch.json')).read_text())
assert all(x['accepted'] and sha(W/x['raw_path'])==x['sha256'] for x in records+cases)
assert external[0]['accepted'] and external[1]['http_status']==202 and not external[1]['accepted']
r=E.parse(S/(P+'-selected.xml')).getroot();expected=['art-'+a.get('label').removeprefix('Artikel ') for a in r.iter('artikel')];parsed=[u['id'] for u in us]
assert expected==parsed and len(expected)==len(set(expected))==639
assert ids==expected[expected.index(ids[0]):expected.index(ids[-1])+1]
assert sha(S/(P+'-selected.xml'))==sha(S/'official-2026-09-01.xml')
def flat(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+flat(c)+' '+(c.tail or '') for c in e)
norm=lambda s:re.sub(r'\s+','',s)
for a in r.iter('artikel'):assert norm(flat(a))==norm(by['art-'+a.get('label').removeprefix('Artikel ')]['text'])
assert not [e for e in r.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
ht=(S/(P+'-current.html')).read_text();htmlids=['art-'+html.unescape(t).strip().removeprefix('Artikel ') for t in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',ht)]
assert htmlids==expected
assert not re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>([^<]*(?:Bijlage|Annex)[^<]*)</a>',ht)
wt=E.parse(S/(P+'-wti.xml')).getroot();dates=sorted({e.get('waarde') for e in wt.findall('./wijzigingen/regeling/datum') if e.get('waarde')})
assert max(d for d in dates if d<='2026-10-21')=='2026-09-01';assert not [d for d in dates if '2026-10-01'<d<='2026-10-21']
names=['units.jsonl','meta.json','coverage-evidence.json','completeness-report.json'];hashes={n:sha(W/n) for n in names}
for script in ['_parse.py','_coverage.py']:
 q=subprocess.run([sys.executable,str(W/script)],capture_output=True,text=True);assert q.returncode==0,q.stderr
assert hashes=={n:sha(W/n) for n in names}
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
save(S/(P+'-parser-check.json'),{'ok':True,'expected_ids':expected,'parsed_ids':parsed,'fresh_html_ids':htmlids,'missing':[],'duplicates':[],'all_official_article_texts_equal':True,'annex_disposition':comp['annexes'],'opening_closing':comp['non_article_text'],'reproduced_hashes':hashes,'official_xml_sha256':sha(S/(P+'-selected.xml'))})
pre=json.loads((S/'author-art-241d-253-preflight-result.json').read_text());pre.update(verified_at=now,review_date_local='2026-10-21',parser_evidence='sources/'+P+'-parser-check.json')
pre['version_evidence'].update(fresh_records='sources/'+P+'-fetch.json',future_dates_excluded=[d for d in dates if d>'2026-10-21'],fresh_wti_matches_previous=sha(S/(P+'-wti.xml'))==sha(S/'author-art-241d-253-wti.xml'))
assert pre['version_evidence']['fresh_wti_matches_previous']
for h in pre['historical_versions_checked']:
 assert sha(W/h['path'])==h['sha256'];old=E.parse(W/h['path']).getroot();labels=[a.get('label') for a in old.iter('artikel')];assert len(labels)==len(set(labels));h['assigned_present_ids']=['art-'+a.removeprefix('Artikel ') for a in labels if 'art-'+a.removeprefix('Artikel ') in ids]
pre['limitations']=['Separate external transitional statutes cited in editorial notes were not independently analysed for historical proceedings.','The substantive second pass covers exactly the twenty assigned units; no whole-book review claimed.']
save(S/(P+'-preflight-result.json'),pre)
p=W/'preflight-result.json';j=json.loads(p.read_text());j['bounded_review_art_241d_253']=pre;save(p,j)
comparisons=[]
for year,ecli in [('2017','2017-1280'),('2018','2018-424')]:
 a=S/(P+'-hr-'+year+'.xml');b=S/('author-art-241d-253-hr-'+year+'.xml');root=E.parse(a).getroot();u=root.find('{*}uitspraak');t=''.join(u.itertext());assert a.read_bytes()==b.read_bytes();(S/(P+'-hr-'+year+'.txt')).write_text(t)
 local=Path('/Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr/ecli-nl-hr-'+ecli+'.md');dest=S/(P+'-hr-'+year+'-local.md');shutil.copyfile(local,dest)
 paras=u.findall('.//{*}para');miss=[norm(''.join(e.itertext()))[:100] for e in paras if norm(''.join(e.itertext())) not in norm(dest.read_text())]
 comparisons.append({'year':year,'official_sha256':sha(a),'full_text_chars':len(t),'same_as_author_capture':True,'local_corpus_path':str(local),'local_snapshot':str(dest.relative_to(W)),'local_sha256':sha(dest),'official_paragraphs':len(paras),'unmatched_paragraph_prefixes':miss})
save(S/(P+'-case-comparison.json'),comparisons)
log=json.loads((S/'author-art-241d-253-search-log.json').read_text());log['second_pass']={'checked_at':now,'scope':'Existing selective research independently reviewed, no additional case asserted. Both complete official judgments freshly fetched and read; corpus snapshots compared.','holdings':'2017:3.4.2 minimum hearing circle;3.5.2 and3.6.2 anticipated prejudice and knowledge;3.7.2–3.7.3,3.10.2 discretion and group interests;3.8.2 personal composition offer versus estate-bound act. 2018:3.5.4–3.5.6 restrict broad previous formulations;3.9 fixation at surseance opening;3.12 answers, no estate rank from verifiability.','external_law':'Current official BW7:51 read; goods and transfer/pledge distinction verified. EUR-Lex consolidated endpoint returned HTTP202 with empty body and is rejected; no EU substantive conditions added from memory. Article247d remains a national procedural commentary and expressly refers substantive EU conditions to the Regulation.','limitations':'No exhaustive new case-law search or universal later-treatment audit. EU consolidated response unavailable; no claim to review EU substantive conversion criteria.'};save(S/(P+'-search-log.json'),log)
notes=[
'Afkoelingsuitzondering beperkt tot verpande goederen; BW7:51 rechtstreeks gecontroleerd. Geld/effecten/kredietvorderingen en verschil overdracht/pand toegevoegd zonder alle toepassingsvoorwaarden te pretenderen te behandelen.',
'Beide leden: terugwerking217, werkelijk tijdstip voorlopige verlening, opgesomde handelingen en artikelen, dezelfde dag en bewijslast onbekendheid gecontroleerd. Voorlopige verlening expliciet gemaakt.',
'Alle vijf leden en volledige HR2017 gecontroleerd: vijf verschillende gronden, verplichte verzoeken alleen1/5, minimumhoorkring, faillissement versus voortduren, DNBhoren. Rechterlijke belangenafweging en groepsbelangen uit3.7.2–3.7.3/3.10.2 toegevoegd; verzoekplicht is geen automatische intrekkingsplicht.',
'Alle vier leden: asymmetrisch appelrecht, acht dagen vanaf beschikking, verzoekroute/kennisgeving, minimumhoorkring HR2017:3.4.2 en onderscheid gehoord worden/appelleren gecontroleerd.',
'Alle drie leden: cassatietermijn, in ongelijk gestelde partij, indiening/oproeping/kennisgevingen en verband242(4) gecontroleerd. Feitelijke herwaardering niet als zelfstandige cassatiegrond gepresenteerd.',
'Publicatie na kracht van gewijsde via216 tegenover rechtsmiddelentermijn243 en faillissementspublicatie248/14 gecontroleerd. Geen uitstel van faillissementsbekendmaking afgeleid.',
'Beide leden en volledige215(2) gecontroleerd. Materiële fout hersteld: DNB is in215 aanvullende gehoorde, geen algemene vervanging bekende schuldeisers. Eigen afwijkende246formulering zichtbaar verantwoord, inclusief letterlijke afzeggingsadressaat lid1.',
'Beide leden: herstel betalingsmogelijkheid, steeds bevoegd verzoek, bewindvoerders/definitieve surseance schuldeisers, griffier/termijn. Geen eigen appelregeling;282uitsluiting gewone voorziening expliciet, zonder onbeoordeelde doorbreking uit te sluiten.',
'Alle zes leden: natuurlijke persoon, voorlopige surseance, beide tijdsgrenzen,284verzoek bij dezelfde rechtbank, facultatief horen,6(2)partnerbevoegdheid, definitieve toepassing en gebundelde293publicatie/afzegging255/264 gecontroleerd.',
'Alle vijf leden: uitsluiting schuldeisers/belanghebbenden, afwijzing/acht dagen schuldenaar, twintig dagen behandeling/acht dagen uitspraak, cassatie/kennisgeving, blokkade definitieve verlening/akkoord tijdens verzoek en rechtsmiddelen gecontroleerd.',
'Beide leden/onderdelen: gerichte228(1)tweede volzinbevoegdheid, behoud boedelschuld/indiening zonder erkenning en alleen249(1)onder1/4 overgenomen. Geen algemene overname249.',
'Exacte nationale verwijzingspakketten voor beide omzettingsroutes gecontroleerd:242(3),243–246 versus247a(3–5),247b(1),247c. Geen invoeging termijnen247a(1–2) of beroep247b(2–4). Europese inhoudelijke omzettingscriteria uitdrukkelijk niet zelfstandig behandeld; onbruikbare externe capture verworpen.',
'Beide leden en213ar/13/14/15 gecontroleerd: rauwelijks-verzoekverbod met uitzondering, installatie/publicatie faillissement, geldigheid curatorhandelingen/vernietigingsgevolgen en249aansluiting.',
'Beide leden/alle vier onderdelen en volledige HR2018 gelezen. Aansluitingsvoorwaarde, specifieke termijnverschuiving, bevoegdheid228, met medewerking verrichte handelingen/boedelschulden, boedelbaat en herhaalde surseance.43/45éénjaarspresumpties concreet uitgewerkt; geen verschuiving iedere termijn, geen boedelrang door verificatie.',
'Opgesomde financiële ondernemingen, reeds uitgevoerde vangnetregeling, titelII of éénmaandvoorwaarde en voortzetting viaWft3.5.6 gecontroleerd. Geen nieuwe regeling of zelfstandige uitkeringsaanspraak afgeleid; externe Wftuitkeringsvoorwaarden niet integraal beoordeeld.',
'Alle drie leden: deskundigen226/bewindvoerders, voorrang loon/verschotten inclusief griffier, efficiënte behandeling en gelegenheid zienswijze bij afwijking/niet-instemmingRC gecontroleerd. Geen vaste mondelinge vorm of uitputtende rangregeling afgeleid.',
'Officiële status vervallen en leeg slot behouden; geen huidige bevoegdheid of gereconstrueerd historisch recht. Historische voorbeeldvraag terecht voorbehouden aan oude tekst/overgangsrecht.',
'Alle verwijzingen203–205 gelezen: buitenlands verhaal onbezwaarde goederen, overdrachtsdoel en weerlegbaar wetenschapsvermoeden, overdracht vordering/schuld voor verboden verrekening. Overeenkomstige toepassing met eigen surseancewerking begrensd; checklist gecontroleerd.',
'Aanbiedingsbevoegdheid schuldenaar bij/na verzoek aan geraakte schuldeisers, geen automatische aanvaarding/homologatie; volledige HR2017:3.8.2onderscheid eigen aanbod/ook boedelbindende handeling en fictief groepsvorderingvoorbeeld gecontroleerd.',
'Beide leden: kosteloze inzage ieder, reeds215neergelegd versus alsnog neerleggen, afschrift zodra mogelijk aan bewindvoerders/deskundigen, geen instemming door inzage. Voorbeeld en254onherroepelijkheid gecontroleerd.'
]
rows=[]
for i,n in zip(ids,notes):
 after=hashlib.sha256(cs[i].encode()).hexdigest();rows.append({'id':i,'official_path':by[i]['official_path'],'finding':n,'result':'corrected' if before[i]!=after else 'accepted_without_change','before_sha256':before[i],'after_sha256':after,'statutory_sha256':hashlib.sha256(by[i]['text'].encode()).hexdigest()})
assert len(rows)==20
paras=[p for i in ids for p in cs[i].split('\n\n') if len(p)>200];assert len(paras)==len(set(paras));assert all(len(cs[i])>=700 if i!='art-250a' else len(cs[i])>=120 for i in ids)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[r['id'] for r in rows if r['result']=='corrected'],'checked_at_utc':now,'whole_book_complete':False,'limitations':['Only twenty assigned units reviewed; no external professional approval.','Existing selective judicial research verified; no exhaustive case-law search claimed.','Whole-book authoring remains incomplete.','Separate transitional statutes in editorial notes not independently analysed for historical proceedings.','EU substantive conversion criteria and Wft compensation entitlement conditions are not independently analysed; national procedural references verified. EUR-Lex HTTP202 empty body rejected.']}
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,result)
checks={'ok':True,'reviewed_ids':ids,'unassigned_commentaries_unchanged':True,'duplicate_long_paragraphs':0,'commentary_chars':{i:len(cs[i]) for i in ids},'source_agreement':1.0,'whole_book_complete':False}
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,checks)
p=S/'verification.json';j=json.loads(p.read_text());j['bounded_review_art_241d_253']={'records':records+cases,'external_records':external,'preflight':'sources/'+P+'-preflight-result.json'};save(p,j)
p=W/'status.json';j=json.loads(p.read_text());j['bounded_review_art_241d_253']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/'+P+'-result.json'};save(p,j)
print(json.dumps({'reviewed':20,'changed':result['changed_units'],'all_639_texts_exact':True}))
