from pathlib import Path
import json,hashlib,sys,re,datetime,subprocess,xml.etree.ElementTree as E,html,shutil,urllib.request
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-213me-213z'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W));ids=['art-'+i for i in '213me 213mf 213mg 213mh 213mi 213mj 213mk 213n 213o 213p 213q 213r 213s 213t 213u 213v 213w 213x 213ij 213z'.split()];now=datetime.datetime.now(datetime.timezone.utc).isoformat();before=json.loads((S/(P+'-before-hashes.json')).read_text())
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
pre=json.loads((S/'author-art-213me-213z-preflight-result.json').read_text())
pre.update(verified_at=now,review_date_local='2026-10-21',parser_evidence='sources/'+P+'-parser-check.json')
pre['version_evidence'].update(fresh_records='sources/'+P+'-fetch.json',future_dates_excluded=[d for d in dates if d>'2026-10-21'],fresh_wti_matches_previous=sha(S/(P+'-wti.xml'))==sha(S/'author-art-213me-213z-wti.xml'))
assert pre['version_evidence']['fresh_wti_matches_previous']
for h in pre['historical_versions_checked']:
 assert sha(W/h['path'])==h['sha256']
 old=E.parse(W/h['path']).getroot(); labels=[a.get('label') for a in old.iter('artikel')];assert len(labels)==len(set(labels))
 h['assigned_present_ids']=['art-'+a.removeprefix('Artikel ') for a in labels if 'art-'+a.removeprefix('Artikel ') in ids]
pre['transition_evidence']={'path':'sources/review-art-207-212hf-stb-2018-489.txt','sha256':sha(S/'review-art-207-212hf-stb-2018-489.txt'),'finding':'XIV(4) preserves former Faillissementswet for insurer bankruptcies before Article IV commencement; text read at line424.'}
save(S/(P+'-preflight-result.json'),pre)
p=W/'preflight-result.json';j=json.loads(p.read_text());j['bounded_review_art_213me_213z']=pre;save(p,j)
log=json.loads((S/'author-art-213me-213z-search-log.json').read_text())
log['review']={'checked_at':now,'web_queries':['site:uitspraken.rechtspraak.nl "213mf" "213mi"','site:uitspraken.rechtspraak.nl "213ij" verzekeraar'],'web_result':'No results returned.','local_search':'rg -l --glob *.md \\b213(mf|mi|ij)\\b|Paget Approbois /Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr','local_hits':['ecli-nl-hr-1968-ac2286.md'],'disposition':'Same irrelevant historical metadata hit as author search; excluded. Existing complete Paget decision paragraphs1–68 and operative part read against both preserved official browser extractions, with fresh official page check. No other judgment added.'}
save(S/(P+'-search-log.json'),log)
findings=[
'Beide leden en bronnoot gelezen: natuurlijke personen, ondernemingsgrootte bij opeisbaarheid, defecte richtlijnverwijzing behouden en uitzondering op verzoek met onaanvaardbaarheidstoets.',
'Alle drie leden: aanvraagverzuim versus bevel tot betaling, curator horen, drie dagen, hoogte/frequentie. Overgangsrecht XIV(4) expliciet toegevoegd en tegen publicatie gecontroleerd.',
'Samenloop vereist twee aanspraken ter zake van dezelfde schade, geen betalingseis toegevoegd; aanspraak zelf blijft onderscheiden van voorschot.',
'Beide leden: periodiek overschot, overdracht vóór verificatie, onverrekenbaar bedrag, afwijkende overeenkomst en daadwerkelijke betaling door overnemer gevolgd door termijnkorting.',
'Nihilstelling beperkt tot overbetaling wegens lagere verificatie, ontbreken goede trouw en causaal verband; verhouding tot213mh correct onderscheiden.',
'RC-toestemming voor beëindiging, hoogte en frequentie afzonderlijk gecontroleerd; geen eenzijdige stop of definitieve vaststelling voorgespiegeld.',
'Alle onderdelen a–c en67 gelezen: drie beroepsgerechtigden, horen/oproepen, rechtbank hoogste ressort; geen ononderzochte cassatie-uitspraak toegevoegd.',
'Beide leden: van rechtswege erkenning en werkingstijdstip herkomststaat; geen Nederlandse publicatie als constitutieve eis.',
'Hoofdregel herkomstrecht en wettelijke uitzonderingen onderscheiden; erkenning en toepasselijk recht niet verward.',
'Alle vier leden en onderdelen gelezen: bestaande rechten, niet-limitatieve categorieën, openbaar derdenwerkend verkrijgingsrecht, registers/ligging/zetel derde-schuldenaar en213s.',
'Alle drie leden: koper versus verkoper verzekeraar, buitenlandse ligging op werkingstijdstip. Wft3:241(4) in verse officiële HTML gelezen en verwijzing klopt.',
'Recht toepasselijk op vordering van verzekeraar als aanknoping gecontroleerd; geen nieuwe verrekeningsbevoegdheid of aantastingsimmuniteit.',
'Nietigheid, vernietiging en niet-tegenwerpelijkheid wegens collectieve benadeling behouden; relatie213z correct. Grammaticale fout hersteld.',
'Arbeidsovereenkomst en overige arbeidsverhouding, toepasselijk recht versus collectieve indiening/rang gescheiden; geen automatische woonplaatsaanknoping.',
'Genot en verkrijging onroerend goed, exclusieve lex situs voor liquidatiegevolgen en scheiding van213v/x gecontroleerd.',
'Rechten van verzekeraar op registergoed, registergezag versus fysieke gegevenslocatie en verschil met derdenrechten213p gecontroleerd.',
'Alle drie leden en onderdelen: marktrecht, voorbehoud213p, benadelingsvordering, derde-landmarkt erkenning/aanwijzing en beide vergelijkbaarheidseisen.',
'Bezwarende beschikking na opening, registergoed/effecten/rekening/depot en bijzondere situs onroerend goed; verwijzing beslist niet zelf geldigheid.',
'Volledig arrest C-724/20 gelezen: verzekeringsclaim inbegrepen, forumrecht voor gedingseffecten, begrenzing liquidatiebevoegdheden. Uitsluiting individuele executie uit punten45–47 toegevoegd.',
'Beide cumulatieve bewijsthema’s: ander lidstaatrecht en concrete afwezigheid aantastingsmogelijkheid. Bewijslast begunstigde en verhouding213s/w gecontroleerd.'
]
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
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[r['id'] for r in rows if r['result']=='corrected'],'checked_at_utc':now,'whole_book_complete':False,'validation_result':validation,'limitations':['Only the assigned twenty units reviewed; project-internal review, no external professional approval.','Selective judicial search; existing C-724/20 full text reviewed, no claim of exhaustive coverage.','Historical versions excluded; transitional applicability explicitly checked.','Defective official directive reference in213me preserved; no quantitative enterprise thresholds invented.',f'{missing} unassigned commentaries absent; whole-book build and strict validation remain unsuccessful.']}
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,result)
checks={'ok':True,'reviewed_ids':ids,'unassigned_commentaries_unchanged':True,'duplicate_long_paragraphs':0,'commentary_chars':{i:len(cs[i]) for i in ids},'source_agreement':1.0,'whole_book_complete':False}
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,checks)
p=S/'verification.json';j=json.loads(p.read_text());j['bounded_review_art_213me_213z']={'records':records,'preflight':'sources/'+P+'-preflight-result.json'};save(p,j)
p=W/'status.json';j=json.loads(p.read_text());j['bounded_review_art_213me_213z']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/'+P+'-result.json'};save(p,j)
print(json.dumps({'reviewed':20,'changed':result['changed_units'],'missing_elsewhere':missing,'verbatim_ratio':1.0}))
