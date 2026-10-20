from pathlib import Path
import json,hashlib,sys,re,datetime,subprocess,xml.etree.ElementTree as E,html,shutil,urllib.request
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-213aa-214'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W));ids=['art-'+i for i in '213aa 213bb 213cc 213dd 213ee 213ff 213gg 213hh 213ii 213jj 213kk 213kka 213ll 213mm 213nn 213oo 213pp 213qq 213rr 214'.split()];now=datetime.datetime.now(datetime.timezone.utc).isoformat();before=json.loads((S/(P+'-before-hashes.json')).read_text())
assert all(before[k]==hashlib.sha256(v.encode()).hexdigest() for k,v in cs.items() if k not in ids)
records=json.loads((S/(P+'-fetch.json')).read_text());assert all(r['accepted'] and sha(W/r['raw_path'])==r['sha256'] for r in records)
r=E.parse(S/(P+'-selected.xml')).getroot();expected=['art-'+a.get('label').removeprefix('Artikel ') for a in r.iter('artikel')]
toc=['art-'+html.unescape(x).removeprefix('Artikel ') for x in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',(S/(P+'-current.html')).read_text())]
assert expected==toc==[u['id'] for u in us] and len(set(expected))==639
assert sha(S/(P+'-selected.xml'))==sha(S/'official-2026-09-01.xml')
def flat(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+flat(c)+' '+(c.tail or '') for c in e)
norm=lambda s:re.sub(r'\s+','',s)
for a in r.iter('artikel'):assert norm(flat(a))==norm(by['art-'+a.get('label').removeprefix('Artikel ')]['text'])
assert not [e for e in r.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
wt=E.parse(S/(P+'-wti.xml')).getroot();dates=sorted({e.get('waarde') for e in wt.findall('./wijzigingen/regeling/datum') if e.get('waarde')});assert max(d for d in dates if d<='2026-10-21')=='2026-09-01'
assert not [d for d in dates if '2026-10-01'<d<='2026-10-21']
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
names=['units.jsonl','meta.json','coverage-evidence.json','completeness-report.json'];hashes={n:sha(W/n) for n in names}
for script in ['_parse.py','_coverage.py']:
 q=subprocess.run([sys.executable,str(W/script)],capture_output=True,text=True);assert q.returncode==0,q.stderr
assert hashes=={n:sha(W/n) for n in names}
save(S/(P+'-parser-check.json'),{'ok':True,'official_source':{'url':records[1]['url'],'local_raw_evidence_path':records[1]['raw_path'],'sha256':records[1]['sha256']},'expected_ids':expected,'parsed_ids':[u['id'] for u in us],'html_toc_ids':toc,'missing':[],'duplicates':[],'annex_disposition':comp['annexes'],'opening_closing':comp['non_article_text'],'reproduced_hashes':hashes})
pre=json.loads((S/'author-art-213aa-214-preflight-result.json').read_text())
pre.update(verified_at=now,review_date_local='2026-10-21',parser_evidence='sources/'+P+'-parser-check.json')
pre['version_evidence'].update(fresh_records='sources/'+P+'-fetch.json',future_dates_excluded=[d for d in dates if d>'2026-10-21'],fresh_wti_matches_previous=sha(S/(P+'-wti.xml'))==sha(S/'author-art-213aa-214-wti.xml'))
assert pre['version_evidence']['fresh_wti_matches_previous']
for h in pre['historical_versions_checked']:
 assert sha(W/h['path'])==h['sha256']
 old=E.parse(W/h['path']).getroot(); labels=[a.get('label') for a in old.iter('artikel')];assert len(labels)==len(set(labels))
 h['assigned_present_ids']=['art-'+a.removeprefix('Artikel ') for a in labels if 'art-'+a.removeprefix('Artikel ') in ids]
save(S/(P+'-preflight-result.json'),pre)
p=W/'preflight-result.json';j=json.loads(p.read_text());j['bounded_review_art_213aa_214']=pre;save(p,j)
log={'at':now,'queries':['site.uitspraken.rechtspraak.nl "213nn" "213oo"'],'web_result':'No directly relevant primary judgment returned; unrelated legislation and insolvency judgments excluded.','local_query':'rg -l --glob *.md 213nn|213oo|213kk|213bb /Volumes/LaCie/law-intake/eu/nl/rechtspraak','local_hits':['hr/ecli-nl-hr-1968-ac2286.md'],'disposition':'Historical metadata hit excluded; no judicial holding added or relied on in these twenty units. Selective search only.'}
save(S/(P+'-search-log.json'),log)
findings=['Beide leden: herkomstbevoegdheden versus Nederlandse uitoefeningswijze, dwang en rechtspraak uitgezonderd; vertegenwoordigers en bijstand afzonderlijk gecontroleerd.', 'Twee bewijsroutes onderscheiden; onbedoelde extra waarmerkingseis voor verklaring bevoegde instantie verwijderd. Vertaling alleen op verlangen en geen verzonnen beëdigingsvereiste.', 'Verzoek curator, griffier Den Haag en register19(1) gecontroleerd; registratie niet als erkenningsvoorwaarde uitgelegd.', 'Zetel buiten EU, bijkantoren Nederland en andere lidstaat, vergunningstaten en passende autoriteiten gecontroleerd. Beide inspanningsplichten onderscheiden van bevoegdheidsoverdracht.', 'Verslag73a en volledige kring van betrokken of voorheen betrokken derden gecontroleerd; geen algehele geheimhoudingsregel gemaakt.', 'Wettelijke categorie1:1 Wft onderscheiden van feitelijke ondernemingsgrootte; geen ongeverifieerde kwantitatieve drempels toegevoegd.', 'Alle vijf verwijzingen gelezen in huidige XML:213a(1),213abis(3),213b,213i,213k(1). Geen overname van niet-verwezen leden.', 'Onderdelen a/b: afschrift verzekeraar versus kennis inhoud toezichthouders, zetel en dienstverlening vanuit relevante vestigingen gecontroleerd.', 'Beide leden: griffier naar DNB en DNB naar aangewezen buitenlandse toezichthouders, onverwijld en mogelijke gevolgen gecontroleerd.', 'Verzoek buitenlandse toezichthouder als aanleiding, procedureverloop als voorwerp; geen algemeen inzagerecht polishouders afgeleid.', 'Alle vijf leden en a–e gecontroleerd. Onderdeel d aangescherpt tot vestiging in Nederland, niet alleen Nederland. Boedelkosten, zekerheden, jaarlijkse grenzen, toekomstige prestaties, achterstelling overige vorderingen en aparte levens-/schadeverwijzingen kloppen. Officieel defect artikel10 BW7 zichtbaar behouden.', 'Volledige schakel213ma–mk en historische noot gelezen; geen verwarring huidig213ll. Voorschot onderscheiden van definitieve rang.', 'Alle definities a–g gelezen, EU/EER-uitbreiding, verschillende colleges en drie typen afwikkelingsmaatregel gecontroleerd.', 'Beide leden: Amsterdam voor Nederlandse vestiging en verbod bij buitenlandse lidstaatvestiging plus vergunning daar. Geen automatische bevoegdheid bij ontbreken vergunning afgeleid.', 'Alle vier leden: Europese criteria a/b en negatieve algemeenbelangtoets, ontvangers afschrift, monopolie aanvraag en eigen aangifte met horen DNB en75(3) onderscheiden.', 'Beide leden: gelegenheid verweer en redelijkheidstoets, geen volledige beleidssubstitutie. Afzonderlijke rechterlijke toets213pp behouden.', 'Summierlijk blijken van22(1)a/b onderscheiden van afwikkelings- en procedurevoorwaarden213nn; geen gewone betalingsstaking als vervangende norm.', '212he,212hga(1),212i tegen huidige XML gelezen; alleen eerste machtigingslid overgenomen, geen automatische invoeging toestemmingsvrijstelling uit tweede lid.', 'Uitsluitend10 uitgesloten, termijn en gerechtigden tegen artikel10 gecontroleerd. Geen algemene uitsluiting alle rechtsmiddelen geclaimd.', 'Alle vier leden: voorzien probleem, verzoek door schuldenaar met advocaat, staat96 nader gespecificeerd, relatieve bevoegdheid en EU-rechtsmacht gescheiden, akkoord facultatief en alle uitgesloten categorieën gecontroleerd.']
rows=[]
for i,note in zip(ids,findings):
 after=hashlib.sha256(cs[i].encode()).hexdigest();rows.append({'id':i,'official_path':by[i]['official_path'],'effective_from':by[i]['effective_from'],'source_notes_checked':by[i]['notes'],'finding':note,'result':'corrected' if before[i]!=after else 'accepted_without_change','before_sha256':before[i],'after_sha256':after,'statutory_sha256':hashlib.sha256(by[i]['text'].encode()).hexdigest()})
assert len(rows)==20
paras=[p for i in ids for p in cs[i].split('\n\n') if len(p)>200];assert len(paras)==len(set(paras))
assert all(len(cs[i])>=(120 if by[i]['text']=='Vervallen' else 700) and not re.search('TODO|FIXME',cs[i]) for i in ids)
for script,suffix in [('build_repo.py','build.txt'),('validate.py','validation.txt')]:
 q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/'+script,str(W)],capture_output=True,text=True);(S/(P+'-'+suffix)).write_text(q.stdout+q.stderr)
 if script=='validate.py':validation=json.loads(q.stdout)
assert validation['verbatim_ratio']==1.0
save(S/(P+'-validation.json'),validation)
missing=sum(not cs.get(u['id']) for u in us)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[r['id'] for r in rows if r['result']=='corrected'],'checked_at_utc':now,'whole_book_complete':False,'validation_result':validation,'limitations':['Only the assigned twenty units reviewed; project-internal review, no external professional approval.','Selective judicial search; no sufficiently relevant verified judgment added to these twenty units.','Historical versions excluded; current statutory text reviewed.','Defective official BW7 article10 reference in213kk preserved and expressly flagged; no corrected statutory wording invented.',f'{missing} unassigned commentaries absent; whole-book build and strict validation remain unsuccessful.']}
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,result)
checks={'ok':True,'reviewed_ids':ids,'unassigned_commentaries_unchanged':True,'duplicate_long_paragraphs':0,'commentary_chars':{i:len(cs[i]) for i in ids},'source_agreement':1.0,'whole_book_complete':False}
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,checks)
p=S/'verification.json';j=json.loads(p.read_text());j['bounded_review_art_213aa_214']={'records':records,'preflight':'sources/'+P+'-preflight-result.json'};save(p,j)
p=W/'status.json';j=json.loads(p.read_text());j['bounded_review_art_213aa_214']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/'+P+'-result.json'};save(p,j)
print(json.dumps({'reviewed':20,'changed':result['changed_units'],'missing_elsewhere':missing,'verbatim_ratio':1.0}))
