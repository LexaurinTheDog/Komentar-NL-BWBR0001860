from pathlib import Path
import json,sys,re,hashlib,datetime,shutil,subprocess,collections
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
c=load_commentary(str(W));r=json.loads((W/'review-result.json').read_text());checks=json.loads((W/'review-checks.json').read_text());ids=r['reviewed_ids'];assert len(ids)==20
before=json.loads((W/'sources/review-art-137c-152-before-hashes.json').read_text());assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
pgraphs=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:pgraphs[p].append(k)
assert not [v for v in pgraphs.values() if len(v)>1]
assert all(not re.search(r'TODO|FIXME|to be filled',c[k],re.I) for k in ids)
v=json.loads((W/'sources/review-art-137c-152-validation.json').read_text());assert v['verbatim_ratio']==1 and len(v['errors'])==1 and '342' in v['errors'][0]
checks.update(assigned_commentary_count=20,assigned_min_chars=min(len(c[k]) for k in ids),repeated_paragraphs=0,whole_book_complete=False,full_builder_exit_code=1,strict_validator_exit_code=1,strict_validation=v,parser_idempotent=True)
r['validation_result']=v
for name,value in [('review-result.json',r),('sources/review-art-137c-152-result.json',r),('review-checks.json',checks),('sources/review-art-137c-152-checks.json',checks)]:save(W/name,value)
p=W/'status.json';v=json.loads(p.read_text());v['updated_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();v['commentary_characters']=sum(map(len,c.values()));v['bounded_review_art_137c_152']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'changed':9,'unassigned_commentaries_unchanged':True,'evidence':'sources/review-art-137c-152-result.json','whole_book_complete':False};save(p,v)
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_137c_152']={'preflight':'sources/review-art-137c-152-preflight-result.json','actual_fetch_records':json.loads((W/'sources/review-art-137c-152-fetch.json').read_text()),'case_fetch_records':'sources/review-art-137c-152-cases-fetch.json'};save(p,v)
review='''

## Tiende afgebakende tweede lezing — artikelen 137c tot en met 152

Op 21 oktober 2026 (Europe/Prague; bronopvragingen 20 oktober UTC) zijn exact twintig toegewezen plaatsen volledig gelezen en tegen de wettelijke bron getoetst: 137c, 137d, 137e, 137f, 137g, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151 en 152. Alle leden, letters, bronnotities, voorbeelden en interne verwijzingen zijn betrokken. [Exacte identifiers en individuele bevindingen](sources/review-art-137c-152-result.json). Negen toelichtingen zijn uitgebreid: 137c–137g, 138, 145, 146 en 149. De elf overige zijn zonder wijziging aanvaard. Alle 277 niet toegewezen bestaande toelichtingen zijn hashgelijk gebleven.

De verduidelijkingen betreffen de afzonderlijke verkoopregels, kostenomslag, openbare verzetbehandeling en cassatie, reservering en beëindiging, en de terugkeer naar gewone verificatie met akkoordmogelijkheid. De akkoorduitleg onderscheidt het totale concurrente vorderingsbedrag van de verschenen personen en onderscheidt een werkelijk causale tegenstem van afwezigheid. De herstelroute is niet tot tel- of typefouten beperkt wanneer een uit de stukken blijkende interpretatiefout wordt gesteld.

Nieuwe [HTTP-responsen met tijdstippen, hashes en formaatcontrole](sources/review-art-137c-152-fetch.json) bevestigen geldigheid vanaf 1 september 2026 tot heden. De officiële pagina zegt raadpleging op 20 oktober; dat is niet veranderd in de lokale reviewdatum. Wijzigingsinformatie bevat geen ingegane wijziging sinds de intake tot 21 oktober. De [preflight](sources/review-art-137c-152-preflight-result.json) behoudt de beslissende redactiedatum 19 oktober, sluit historische 2002-toestand en toekomstige wijzigingsdatum 2027 uit en vergelijkt alle 639 unieke officiële identifiers met parser en onafhankelijke HTML-inhoudsopgave. Aanhef, slot, bijlageafwezigheid en volledige wettelijke tokens zijn gecontroleerd. Parser en dekking zijn opnieuw uitgevoerd zonder bron- of unitwijziging.

Twee volledige primaire uitspraken zijn gelezen: [HR 2024:210](cases/HR-2024-210-akkoord-reikwijdte.md), tevens gelezen in de nationale corpusversie, en [Rb. Gelderland 2015:5785](cases/RBGEL-2015-5785-akkoordstemming.md). De eerste ondersteunt de beperkte reikwijdte van het akkoord bij lopende rente; de tweede de uitleg van artikelen 145, 146 en 149. Processtandpunten en historische citaten zijn van rechterlijke conclusies onderscheiden. De relevante wettelijke formuleringen zijn met de actuele bron vergeleken. De rechtbankbeschikking is niet als Hoge Raad-rechtspraak gepresenteerd. [Onderzoekslog](sources/review-art-137c-152-search-log.json). Selectief onderzoek, geen uitputtend overzicht of volledige controle van latere behandeling. Geen zelfstandige volledige certificering van externe BW/Rv-instrumenten of de overgangswetten in bronnotities; de uitleg betreft de geselecteerde actuele toestand.

De [volledige build](sources/review-art-137c-152-build.txt) en [strikte validator](sources/review-art-137c-152-validation.json) zijn uitgevoerd: wettelijke tekstovereenkomst 100%. De 342 ontbrekende toelichtingen buiten deze batch verhinderen de boekvalidatie en volledige build. De bestaande checkpoint-export bouwt de 22 complete hoofdstukken opnieuw. De opdracht blijft onvoltooid met 297 van 639 toegelichte plaatsen. [Batchcontroles](sources/review-art-137c-152-checks.json) bevestigen alle twintig commentaren, geen exact herhaalde lange alinea's en behoud van ander commentaar. Lengte- en scriptcontroles bewijzen geen juridische kwaliteit. Deze afgebakende tweede lezing is geen externe professionele goedkeuring of certificering van het hele boek.
'''
p=W/'REVIEW.md';assert 'Tiende afgebakende' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing artikelen 137c–152: [broncontrole](sources/review-art-137c-152-preflight-result.json), [bevindingen](sources/review-art-137c-152-result.json), [onderzoekslog](sources/review-art-137c-152-search-log.json), [HR 2024:210](cases/HR-2024-210-akkoord-reikwijdte.md) en [Rb. Gelderland 2015:5785](cases/RBGEL-2015-5785-akkoordstemming.md).\n')
p=W/'source-manifest.json';v=json.loads(p.read_text());v['scope']='Preserved original, preflight and bounded-review evidence sets, including articles 137c–152. No new rights claim over official texts.'
def manifest():
 v['files']=[{'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for d in ['sources','cases'] for q in sorted((W/d).rglob('*')) if q.is_file()];save(W/'source-manifest.json',v)
manifest();out=subprocess.run(['python3',str(W/'_checkpoint.py')],capture_output=True,text=True);assert out.returncode==0,out.stderr;print(out.stdout)
for p in W.glob('_review_137c_152_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  count+=1
  if not (p.parent/url.split('#')[0]).exists():broken.append((str(p),url))
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=broken)
for p in [W/'review-checks.json',W/'sources/review-art-137c-152-checks.json',O/'review-checks.json',O/'sources/review-art-137c-152-checks.json']:save(p,checks)
manifest();shutil.copyfile(W/'source-manifest.json',O/'source-manifest.json')
print(json.dumps({'complete':True,'reviewed':20,'corrected':9,'whole_book_complete':False,'links_checked':count}))
