from pathlib import Path
import json,hashlib,sys,re,datetime,subprocess,xml.etree.ElementTree as E,shutil,collections
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-215-228'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W))
ids=['art-'+x for x in '215 215a 215b 216 217 218 219 220 221 222 222a 222b 223 223a 223b 224 225 226 227 228'.split()]
now=datetime.datetime.now(datetime.timezone.utc).isoformat();before=json.loads((S/(P+'-before-hashes.json')).read_text())
assert all(before[k]==hashlib.sha256(v.encode()).hexdigest() for k,v in cs.items() if k not in ids)
records=json.loads((S/(P+'-fetch.json')).read_text());assert all(x['accepted'] and sha(W/x['raw_path'])==x['sha256'] for x in records)
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
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
names=['units.jsonl','meta.json','coverage-evidence.json','completeness-report.json'];hashes={n:sha(W/n) for n in names}
for script in ['_parse.py','_coverage.py']:
 q=subprocess.run([sys.executable,str(W/script)],capture_output=True,text=True);assert q.returncode==0,q.stderr
assert hashes=={n:sha(W/n) for n in names}
save(S/(P+'-parser-check.json'),{'ok':True,'expected_ids':expected,'parsed_ids':parsed,'missing':[],'duplicates':[],'all_official_article_texts_equal':True,'annex_disposition':comp['annexes'],'opening_closing':comp['non_article_text'],'reproduced_hashes':hashes,'official_xml_sha256':sha(S/(P+'-selected.xml'))})
pre=json.loads((S/'author-art-215-228-preflight-result.json').read_text());pre.update(verified_at=now,review_date_local='2026-10-21',parser_evidence='sources/'+P+'-parser-check.json')
pre['version_evidence'].update(fresh_records='sources/'+P+'-fetch.json',future_dates_excluded=[d for d in dates if d>'2026-10-21'],fresh_wti_matches_previous=sha(S/(P+'-wti.xml'))==sha(S/'author-art-215-228-wti.xml'))
assert pre['version_evidence']['fresh_wti_matches_previous']
for h in pre['historical_versions_checked']:
 assert sha(W/h['path'])==h['sha256'];old=E.parse(W/h['path']).getroot();labels=[a.get('label') for a in old.iter('artikel')];assert len(labels)==len(set(labels));h['assigned_present_ids']=['art-'+a.removeprefix('Artikel ') for a in labels if 'art-'+a.removeprefix('Artikel ') in ids]
save(S/(P+'-preflight-result.json'),pre)
p=W/'preflight-result.json';j=json.loads(p.read_text());j['bounded_review_art_215_228']=pre;save(p,j)
# Both complete official judgments were read, including facts, complaints, own holdings and disposition.
comparisons=[]
for y in ['2017','2010']:
 a=S/(P+'-hr-'+y+'.xml');b=S/('author-art-215-228-hr-'+y+'.xml');root=E.parse(a).getroot();t=''.join(root.find('{*}uitspraak').itertext());assert a.read_bytes()==b.read_bytes();(S/(P+'-hr-'+y+'.txt')).write_text(t);comparisons.append({'year':y,'sha256':sha(a),'full_text_chars':len(t),'same_as_author_capture':True})
save(S/(P+'-case-comparison.json'),comparisons)
rv=json.loads((S/(P+'-rv-fetch.json')).read_text());assert rv['http_status']==200 and sha(W/rv['raw_path'])==rv['sha256'];html=(W/rv['raw_path']).read_text();assert 'Geldend van 14-07-2026' in html and 't/m heden' in html
log=json.loads((S/'author-art-215-228-search-log.json').read_text());log['review']={'checked_at':now,'scope':'Existing selective research reviewed, no additional case asserted. Existing local corpus hits read in sources/author-art-215-228-local-hits.txt.','case_review':'Both full official judgments read and freshly fetched byte-identically. 2017 paragraphs3.5.2 and3.7.2–3.9.3 support215/218/228; 2010 paragraphs4.1.3–4.1.5 support228. No post-WHOA rule inferred from the older215 formulation.','external_statute':'Current official Rv177 read in separately hashed capture; oath exceptions added to223b.'};save(S/(P+'-search-log.json'),log)
notes=[
'Alle vijf leden en onderdelen gecontroleerd. Uitleg van overeenkomstige toepassing6(1), derde zin, en6(4) toegevoegd: buitenlandse hoofdprocedure, zienswijze en typering procedure. Oi2017 geldt met huidige WHOA-uitzonderingen.',
'Verzettermijn en uitsluitend internationale-bevoegdheidsgrond gecontroleerd. Efficiënt looncriterium en zienswijzemogelijkheid van250(3) uitgewerkt; rechtsmiddelenverbod beperkt tot kostenbeslissing.',
'Alle taken a–g en bijzondere/strafrechtelijke gegevens uitsluitend voor lid2(c) gecontroleerd; huidige ingangsdatum1 september2026 bevestigd.',
'Alle publicatiegegevens, minuutvermelding en eventueel akkoord gecontroleerd; publicatie niet tot constitutief aanvangsmoment gemaakt.',
'Dagaanvangsfictie gecontroleerd; voorbeeld en verhouding228 juist, geen algemene ongeldigheid of derdenbescherming verzonnen.',
'Alle acht leden gecontroleerd. Beide strikte meer-dan-drempels en rekenvoorbeeld juist; verplichte weigering, discretionaire verlening, faillissement,213ar-prioriteit en DNB-hoorrecht onderscheiden. Oi2017 passage gelezen.',
'Alle vier leden: toegang niet-voorstemmers, acht dagen, verzoekschrift en vierdaagse explootplicht, openbare dossierovername gecontroleerd.',
'Beide leden: geen herstemming, deelname iedere schuldeiser, raadkamer en openbare uitspraak onderscheiden.',
'Alle vier leden: cassatietoegang en termijn, verzoekschrift, dossierovername en overeenkomstige exploot/besloten behandeling gecontroleerd.',
'Beide leden: uitvoerbaarheid verlening ondanks rechtsmiddel en publicatie, onderscheiden van voortduring voorlopige voorziening bij afwijzing218(5).',
'Alle vier leden en zes gegevenscategorieën: chronologisch lokaal register, verordeninggegevens, delegatie, gratis inzage/betaald uittreksel en doorgifte gecontroleerd.',
'Alle drie leden: centrale beheerder, verwijzing naar222a, delegatie en inzage/uittreksel gecontroleerd, geen recht op volledige administratie beweerd.',
'Beide leden: maximale duur anderhalf jaar, herhaalde verlengingen, tijdig verzoek, voortduring hangende beslissing en bekendmaking gecontroleerd.',
'Beide leden: verplichte benoeming, advies op verzoek en toezicht, afzonderlijke/gezamenlijke bevoegdheid meerdere RCs gecontroleerd.',
'Alle drie leden: verzoekvereiste, exploot, Rv-verwijzingen en exacte familiekring gecontroleerd. Inhoud Rv177 verduidelijkt met eed en uitzonderingen onder16/ontbrekend begrip.',
'Beide leden: meerderheid, staking en RC-beslissing, ontslag/vervanging/toevoeging en hoorrecht gecontroleerd. Zelfstandige werkkring70(2) preciezer verbonden aan rechterlijke benoemingsbeslissing.',
'Beide leden: bescherming bij verlening en later, alle initiatiefnemers en geen zelfstandig schuldenaarsverzoek in opsomming gecontroleerd.',
'Alle vier leden: benoeming, verlengbare onderzoekstermijn, beredeneerde betrouwbaarheid/prognose/maatregelen, gratis neerlegging/inzage en personeelsregeling gecontroleerd.',
'Beide leden: driemaandelijks verslag, openbaarmaking via226(3), termijnverlenging uitsluitend RC; geen verlenging surseanceduur afgeleid.',
'Beide leden en volledige twee HR-uitspraken gecontroleerd. Gezamenlijk beheer en schadeloosstelling onderscheiden van beperkte aansprakelijkheid voor baat; stilzwijgende toestemming geen gevolg van enkele voortzetting. Oi betreft specifieke groepsboedelbinding/informatieplicht, geen algemeen verbod akkoord252.'
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
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[r['id'] for r in rows if r['result']=='corrected'],'checked_at_utc':now,'whole_book_complete':False,'validation_result':validation,'limitations':['Only twenty assigned units reviewed; no external professional approval.','Existing selective judicial research verified; no exhaustive case-law search claimed.','Whole-book authoring remains incomplete; full strict validation failure outside this scope is preserved.']}
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,result)
checks={'ok':True,'reviewed_ids':ids,'unassigned_commentaries_unchanged':True,'duplicate_long_paragraphs':0,'commentary_chars':{i:len(cs[i]) for i in ids},'source_agreement':1.0,'whole_book_complete':False}
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,checks)
p=S/'verification.json';j=json.loads(p.read_text());j['bounded_review_art_215_228']={'records':records,'preflight':'sources/'+P+'-preflight-result.json'};save(p,j)
p=W/'status.json';j=json.loads(p.read_text());j['bounded_review_art_215_228']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/'+P+'-result.json'};save(p,j)
print(json.dumps({'reviewed':20,'changed':result['changed_units'],'verbatim_ratio':1.0}))
