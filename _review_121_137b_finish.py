from pathlib import Path
import json,sys,re,hashlib,datetime,shutil,subprocess,collections
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
c=load_commentary(str(W));r=json.loads((W/'review-result.json').read_text());checks=json.loads((W/'review-checks.json').read_text());ids=r['reviewed_ids'];assert len(ids)==20
before=json.loads((W/'sources/review-art-121-137b-before-hashes.json').read_text());assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
pgraphs=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:pgraphs[p].append(k)
assert not [v for v in pgraphs.values() if len(v)>1]
assert all(not re.search(r'TODO|FIXME|to be filled',c[k],re.I) for k in ids)
v=json.loads((W/'sources/review-art-121-137b-validation.json').read_text());assert v['verbatim_ratio']==1 and len(v['errors'])==1 and '342' in v['errors'][0]
checks.update(assigned_commentary_count=20,assigned_min_chars=min(len(c[k]) for k in ids),repeated_paragraphs=0,whole_book_complete=False,full_builder_exit_code=1,strict_validator_exit_code=1,strict_validation=v,parser_idempotent=True)
r['validation_result']=v
for name,value in [('review-result.json',r),('sources/review-art-121-137b-result.json',r),('review-checks.json',checks),('sources/review-art-121-137b-checks.json',checks)]:save(W/name,value)
p=W/'status.json';v=json.loads(p.read_text());v['updated_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();v['commentary_characters']=sum(map(len,c.values()));v['bounded_review_art_121_137b']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'changed':8,'unassigned_commentaries_unchanged':True,'evidence':'sources/review-art-121-137b-result.json','whole_book_complete':False};save(p,v)
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_121_137b']={'preflight':'sources/review-art-121-137b-preflight-result.json','actual_fetch_records':json.loads((W/'sources/review-art-121-137b-fetch.json').read_text()),'case_fetch_records':'sources/review-art-121-137b-cases-fetch.json'};save(p,v)
review='''

## Negende afgebakende tweede lezing — artikelen 121 tot en met 137b

Op 21 oktober 2026 (Europe/Prague; bronopvragingen op 20 oktober UTC) zijn exact twintig toegewezen plaatsen volledig aan de wettelijke bron getoetst: 121, 122, 122a, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 137a en 137b. Alle leden, letters, bronnotities, interne verwijzingen en fictieve voorbeelden zijn gelezen. [Individuele bevindingen en exacte identifiers](sources/review-art-121-137b-result.json). Acht toelichtingen zijn aangescherpt: 121, 122, 125, 126, 132, 137, 137a en 137b. De overige twaalf zijn ongewijzigd aanvaard. De 277 niet toegewezen bestaande toelichtingen zijn hashgelijk gebleven.

De nieuwe [primaire bronopvragingen](sources/review-art-121-137b-fetch.json) bevatten daadwerkelijke HTTP-200-responsen, tijdstippen, hashes en formaatcontrole voor actuele HTML, geselecteerde XML en wijzigingsinformatie. De ontvangen officiële pagina vermeldt raadpleging op 20 oktober en geldigheid vanaf 1 september 2026 tot heden; deze datum is niet hernoemd naar de lokale reviewdatum. De wijzigingsinformatie toont geen ingegane wijziging sinds de intake tot en met 21 oktober. De oorspronkelijke beslissende redactiedatum 19 oktober blijft behouden. De [preflight](sources/review-art-121-137b-preflight-result.json) sluit historische toestand 2002 en toekomstige gedateerde wijziging 2027 uit, controleert alle 639 unieke officiële identifiers, bijlageafwezigheid, aanhef, slot en volledige wettelijke tokens. Parser opnieuw uitgevoerd zonder wijziging van bron of units; onafhankelijke XML/HTML-dekking opnieuw gecontroleerd.

[HR 28 november 2014, ECLI:NL:HR:2014:3464](cases/HR-2014-3464-verificatie.md) is integraal gelezen en met de nationale corpusversie vergeleken. Het arrest ondersteunt uitsluitend de beschreven herstelcontext bij erkenning en het onderscheid tussen eigen betwisting en toelatingsbezwaar. Processtandpunten en de beslissing van de rechtbank zijn van de conclusies van de Hoge Raad onderscheiden. Het oude uitgangspunt van één verificatievergadering en oude artikelleden worden uitdrukkelijk niet als actueel recht weergegeven. [Onderzoekslog](sources/review-art-121-137b-search-log.json). Geen uitputtend rechtspraakonderzoek of controle van alle latere behandeling; geen zelfstandige volledige toets van externe Rv/BW/Europese instrumenten of de in bronnotities genoemde overgangswetten. De uitleg betreft de geselecteerde actuele toestand.

De [volledige build](sources/review-art-121-137b-build.txt) en [strikte validator](sources/review-art-121-137b-validation.json) zijn uitgevoerd. Wettelijke tekstovereenkomst: 100%. De 342 ontbrekende toelichtingen buiten deze batch verhinderen de volledige build en boekvalidatie. De bestaande checkpoint-export bouwt de 22 complete hoofdstukken opnieuw; er zijn geen lege vervanghoofdstukken gemaakt. Het manuscript blijft een onvoltooide boekopdracht met 297 van 639 toegelichte plaatsen. [Batchcontroles](sources/review-art-121-137b-checks.json) bevestigen de twintig toelichtingen, geen exact herhaalde lange alinea's en behoud van niet toegewezen werk. Lengtecontrole bewijst geen juridische kwaliteit. Deze afgebakende tweede lezing is geen externe professionele goedkeuring en certificeert niet het hele boek.
'''
p=W/'REVIEW.md';assert 'Negende afgebakende' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing artikelen 121–137b: [broncontrole](sources/review-art-121-137b-preflight-result.json), [bevindingen](sources/review-art-121-137b-result.json), [primaire rechtspraak](cases/HR-2014-3464-verificatie.md) en [onderzoekslog](sources/review-art-121-137b-search-log.json).\n')
p=W/'source-manifest.json';v=json.loads(p.read_text());v['scope']='Preserved original, preflight and bounded-review evidence sets, including articles 121–137b. No new rights claim over official texts.'
def manifest():
 v['files']=[{'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for d in ['sources','cases'] for q in sorted((W/d).rglob('*')) if q.is_file()];save(W/'source-manifest.json',v)
manifest();out=subprocess.run(['python3',str(W/'_checkpoint.py')],capture_output=True,text=True);assert out.returncode==0,out.stderr;print(out.stdout)
for p in W.glob('_review_121_137b_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  count+=1
  if not (p.parent/url.split('#')[0]).exists():broken.append((str(p),url))
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=broken)
for p in [W/'review-checks.json',W/'sources/review-art-121-137b-checks.json',O/'review-checks.json',O/'sources/review-art-121-137b-checks.json']:save(p,checks)
manifest();shutil.copyfile(W/'source-manifest.json',O/'source-manifest.json')
print(json.dumps({'complete':True,'reviewed':20,'corrected':8,'whole_book_complete':False,'links_checked':count}))
