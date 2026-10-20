from pathlib import Path
import json,sys,hashlib,re,collections,datetime,shutil,subprocess
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
c=load_commentary(str(W));r=json.loads((W/'review-result.json').read_text());checks=json.loads((W/'review-checks.json').read_text());ids=r['reviewed_ids'];assert len(ids)==20
before=json.loads((W/'sources/review-art-172-186-before-hashes.json').read_text());assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
pgraphs=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:pgraphs[p].append(k)
assert not [v for v in pgraphs.values() if len(v)>1]
assert all(not re.search(r'TODO|FIXME|to be filled',c[k],re.I) for k in ids)
v=json.loads((W/'sources/review-art-172-186-validation.json').read_text());assert v['verbatim_ratio']==1 and len(v['errors'])==1 and '342' in v['errors'][0]
checks.update(assigned_commentary_count=20,assigned_min_chars=min(len(c[k]) for k in ids),repeated_paragraphs=0,whole_book_complete=False,full_builder_exit_code=1,strict_validator_exit_code=1,strict_validation=v)
r['validation_result']=v
for name,value in [('review-result.json',r),('sources/review-art-172-186-result.json',r),('review-checks.json',checks),('sources/review-art-172-186-checks.json',checks)]:save(W/name,value)
p=W/'status.json';v=json.loads(p.read_text());v['updated_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();v['commentary_characters']=sum(map(len,c.values()));v['bounded_review_art_172_186']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'changed':7,'unassigned_commentaries_unchanged':True,'evidence':'sources/review-art-172-186-result.json','whole_book_complete':False};save(p,v)
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_172_186']={'preflight':'sources/review-art-172-186-preflight-result.json','actual_fetch_records':json.loads((W/'sources/review-art-172-186-fetch.json').read_text()),'case_fetch_records':'sources/review-art-172-186-cases-fetch.json'};save(p,v)
review='''

## Twaalfde afgebakende tweede lezing — artikelen 172 tot en met 186

Op 21 oktober 2026 (Europe/Prague; bronresponsen 20 oktober UTC) zijn exact twintig toegewezen plaatsen gelezen: 172, 172a, 173, 173a–173d en 174–186. Alle leden, voorbeelden en bronnotities zijn gecontroleerd tegen de opnieuw opgehaalde officiële XML, met controle van de aangehaalde interne bepalingen. [Exacte reviewed_ids en individuele bevindingen](sources/review-art-172-186-result.json). Zeven toelichtingen zijn aangepast: 172, 173b, 180, 181, 182, 184 en 185. Alle 277 overige bestaande toelichtingen bleven hashgelijk.

Artikel 172 verduidelijkt beide fasen van de inhaalverdeling, ook voor nieuwe crediteuren. Bij artikel 173b is de bedragmeerderheid berekend over de volledige relevante vorderingen, zonder verlaging wegens afwezigheid; de commissieprocedure is afzonderlijk uitgelegd. Bij artikelen 180 en 181 is voorwaardelijke toelating onderscheiden van een contractuele opschortende voorwaarde en betwiste rang. Artikel 189 lid 2 reserveert bij betwiste voorrang uitsluitend het meerdere boven het concurrente percentage. Artikel 182 noemt ook de beperkte rechten, huurders en pachters binnen de kostenuitzondering. De overlappende actuele leden 2 en 3 van artikel 183 zijn als officiële formulering behouden en niet als vermeende historische versies verwijderd. Artikel 186 blijft de vervallen plaats, met bronnotitie.

De [nieuwe bronopvragingen](sources/review-art-172-186-fetch.json) registreren werkelijke URL, HTTP 200, tijdstip, hash en formaatcontrole. De [preflight](sources/review-art-172-186-preflight-result.json) behoudt de oorspronkelijke beslissende datum 19 oktober en bevestigt de gelding vanaf 1 september 2026, geen effectieve wijziging sinds intake, de uitsluiting van de historische toestand uit 2002 en de toekomstige wijziging in 2027. De XML en onafhankelijke officiële HTML-inhoudsopgave bevatten dezelfde 639 unieke plaatsen; de volledige parserinventaris en wettelijke tekst komen overeen. Aanhef en slot zijn verantwoord, geen operatieve bijlage aangetroffen. Geen reparatie van wettelijke woorden nodig.

De [volledige beslissing HR 2017:2808](cases/HR-2017-2808-uitdelingslijst.md) is gelezen en met het nationale corpus vergeleken. Rov. 3.4.2 betreft de nieuwe feitelijke stelling in cassatie; rov. 3.4.3 begrenst verzet tegen een eerdere erkenningsbeschikking; rov. 3.5 en het dictum laten beperkt kostenherstel na verwerping toe. De kaart onderscheidt deze oordelen van de klacht van partijen. [Selectief onderzoekslog](sources/review-art-172-186-search-log.json). Geen uitputtende inventaris of latere-behandelingscontrole. Voor de andere technische regels is geen aanvullende voldoende relevante geverifieerde uitspraak opgenomen. Externe Europese bepalingen en overgangswetten zijn niet integraal onderzocht; de toelichting bij 172a blijft uitdrukkelijk beperkt en verlangt voor concrete toepassing verificatie van die externe voorwaarden.

De [volledige buildpoging](sources/review-art-172-186-build.txt) en [strikte validator](sources/review-art-172-186-validation.json) geven 100% tekstovereenkomst, maar worden nog geblokkeerd door 342 ontbrekende commentaren buiten deze batch. De checkpoint-export bevat de complete hoofdstukken en 297 bestaande toelichtingen. [Batchcontroles](sources/review-art-172-186-checks.json) leggen behoud van andere commentaren, afwezigheid van exact herhaalde lange alinea's en lokale linkcontrole vast. Lengte- en scriptcontroles bewijzen geen juridische kwaliteit. Dit is een afgebakende tweede lezing binnen het project, geen externe professionele goedkeuring of voltooiing van het hele boek.
'''
p=W/'REVIEW.md';assert 'Twaalfde afgebakende' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing artikelen 172–186: [broncontrole](sources/review-art-172-186-preflight-result.json), [bevindingen](sources/review-art-172-186-result.json), [onderzoekslog](sources/review-art-172-186-search-log.json), [HR 2017:2808](cases/HR-2017-2808-uitdelingslijst.md).\n')
p=W/'source-manifest.json';v=json.loads(p.read_text());v['scope']='Preserved source and bounded-review evidence, including articles 172–186; no new rights claim over official texts.'
def manifest():
 v['files']=[{'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for d in ['sources','cases'] for q in sorted((W/d).rglob('*')) if q.is_file()];save(W/'source-manifest.json',v)
manifest();out=subprocess.run(['python3',str(W/'_checkpoint.py')],capture_output=True,text=True);assert out.returncode==0,out.stderr;print(out.stdout)
for p in W.glob('_review_172_186_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  count+=1
  if not (p.parent/url.split('#')[0]).exists():broken.append((str(p),url))
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=broken)
for p in [W/'review-checks.json',W/'sources/review-art-172-186-checks.json',O/'review-checks.json',O/'sources/review-art-172-186-checks.json']:save(p,checks)
manifest();shutil.copyfile(W/'source-manifest.json',O/'source-manifest.json')
print(json.dumps({'complete':True,'reviewed':20,'corrected':7,'whole_book_complete':False,'links_checked':count}))
