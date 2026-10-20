from pathlib import Path
import json,sys,hashlib,re,collections,datetime,shutil,subprocess
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
c=load_commentary(str(W));r=json.loads((W/'review-result.json').read_text());checks=json.loads((W/'review-checks.json').read_text());ids=r['reviewed_ids'];assert len(ids)==20
before=json.loads((W/'sources/review-art-153-171-before-hashes.json').read_text());assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
pgraphs=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:pgraphs[p].append(k)
assert not [v for v in pgraphs.values() if len(v)>1]
assert all(not re.search(r'TODO|FIXME|to be filled',c[k],re.I) for k in ids)
v=json.loads((W/'sources/review-art-153-171-validation.json').read_text());assert v['verbatim_ratio']==1 and len(v['errors'])==1 and '342' in v['errors'][0]
checks.update(assigned_commentary_count=20,assigned_min_chars=min(len(c[k]) for k in ids),repeated_paragraphs=0,whole_book_complete=False,full_builder_exit_code=1,strict_validator_exit_code=1,strict_validation=v)
r['validation_result']=v
for name,value in [('review-result.json',r),('sources/review-art-153-171-result.json',r),('review-checks.json',checks),('sources/review-art-153-171-checks.json',checks)]:save(W/name,value)
p=W/'status.json';v=json.loads(p.read_text());v['updated_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();v['commentary_characters']=sum(map(len,c.values()));v['bounded_review_art_153_171']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'changed':8,'unassigned_commentaries_unchanged':True,'evidence':'sources/review-art-153-171-result.json','whole_book_complete':False};save(p,v)
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_153_171']={'preflight':'sources/review-art-153-171-preflight-result.json','actual_fetch_records':json.loads((W/'sources/review-art-153-171-fetch.json').read_text()),'case_fetch_records':'sources/review-art-153-171-cases-fetch.json'};save(p,v)
p=W/'cases/HR-2024-210-akkoord-reikwijdte.md';p.write_text(p.read_text().rstrip()+'''\n\nTweede lezing artikelen 153–171: de volledige beslissing is opnieuw gelezen, inclusief het onderscheid tussen partijstandpunten (2.3–2.4) en oordeel (3.1–3.7), en vergeleken met de bewaarde nationale corpusversie. Ondersteunt in deze batch art-157 en de afbakening tot verifieerbare schuld bij art-161a; geen zelfstandig oordeel over de redelijke-onmogelijkheidsexceptie van artikel 161a. [Nieuwe HTTP- en hashregistratie](../sources/review-art-153-171-cases-fetch.json), [volledige XML](../sources/review-art-153-171-case-hr-2024-210.xml), [leesversie](../sources/review-art-153-171-case-hr-2024-210.txt), [corpusversie](../sources/review-art-153-171-hr-2024-210-local.md). De actuele artikelen 128 en 157 behouden de relevante formulering.\n''')
review='''

## Elfde afgebakende tweede lezing — artikelen 153 tot en met 171

Op 21 oktober 2026 (Europe/Prague, bronopvragingen 20 oktober UTC) zijn exact twintig toegewezen artikelen volledig tegen hun bron gelezen: 153–161, 161a en 162–171. Alle leden, bronnotities, voorbeelden en interne verwijzingen zijn betrokken. [Individuele bevindingen en exacte identifiers](sources/review-art-153-171-result.json). Acht toelichtingen zijn aangepast: 155, 156, 157, 161a, 163, 168, 169 en 171. De twaalf andere zijn aanvaard. Alle 277 overige bestaande toelichtingen zijn ongewijzigd, gecontroleerd met hashes.

De materiële aanvulling bij artikel 157 beperkt de akkoordbinding tot verifieerbare concurrente vorderingen en bespreekt natuurlijke verbintenissen en uitgesloten lopende rente. Bij artikel 161a zijn die grens en de aanpasbare indieningstermijn uitgewerkt. De procedurele aanvullingen onderscheiden de acht dagen voor instellen van een rechtsmiddel van de snelle behandeling, en maken openbaarheid en de uitzondering voor de rechter-commissaris expliciet. Bij artikel 163 is de bewaarplicht bij ontbrekende storting én zekerheid verduidelijkt. Artikel 168 noemt de exacte verwijzingsomvang; artikel 169 onderscheidt homologatie van onherroepelijkheid. Artikel 171 bevat een concreet inhaalrekenvoorbeeld en legt uit dat gelijkelijk geen gelijk bedrag per persoon betekent.

De [nieuwe bronresponsen](sources/review-art-153-171-fetch.json) bevatten URL, HTTP-status, tijdstip, hash en formaatcontrole. De [preflight](sources/review-art-153-171-preflight-result.json) toetst de geldende toestand vanaf 1 september 2026, de wijzigingsinformatie sinds intake, de uitgesloten historische versie van 2002 en de toekomstige wijzigingsdatum 2027. De oorspronkelijke beslissende redactiedatum 19 oktober blijft behouden. Alle 639 officiële identifiers zijn met parser en onafhankelijke HTML-inhoudsopgave vergeleken; geen ontbrekende of dubbele plaatsen. Aanhef en slot zijn verantwoord, geen operatieve bijlage aangetroffen. De bestaande volledigheidscontrole is opnieuw uitgevoerd met volledige tekstovereenkomst.

De [volledige HR-beslissing 2024:210](cases/HR-2024-210-akkoord-reikwijdte.md) is gelezen en met de nationale corpusversie vergeleken. De kaart onderscheidt het partijstandpunt van het eigen oordeel en geeft precieze rechtsoverwegingen en beperkingen. [Selectief onderzoekslog](sources/review-art-153-171-search-log.json). Geen uitputtende rechtspraakinventaris of controle van latere behandeling; voor de overige technische regels is geen aanvullende, voldoende relevante geverifieerde uitspraak toegevoegd. De externe overgangswetten en algemene cassatievoorschriften zijn niet integraal gecertificeerd; bronnotities blijven behouden en toepassing op oude procedures vergt afzonderlijk onderzoek.

De [volledige build](sources/review-art-153-171-build.txt) en [strikte validator](sources/review-art-153-171-validation.json) zijn uitgevoerd: 100% wettelijke tekstovereenkomst; 342 ontbrekende commentaren buiten deze batch blijven de volledige build en boekvalidatie blokkeren. De checkpoint-export is opnieuw opgebouwd voor de complete hoofdstukken. Het boek bevat nog steeds 297 van 639 toelichtingen. [Batchcontroles](sources/review-art-153-171-checks.json) verantwoorden twintig gecontroleerde commentaren, behoud van andere teksten, geen exact herhaalde lange alinea's en lokale links. Script- en lengtecontroles bewijzen geen juridische kwaliteit. Dit is een afgebakende tweede lezing binnen het project, geen externe professionele goedkeuring of voltooiing van het hele boek.
'''
p=W/'REVIEW.md';assert 'Elfde afgebakende' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing artikelen 153–171: [broncontrole](sources/review-art-153-171-preflight-result.json), [bevindingen](sources/review-art-153-171-result.json), [onderzoekslog](sources/review-art-153-171-search-log.json), [HR 2024:210](cases/HR-2024-210-akkoord-reikwijdte.md).\n')
p=W/'source-manifest.json';v=json.loads(p.read_text());v['scope']='Preserved source and bounded-review evidence, now including articles 153–171; no new rights claim over official texts.'
def manifest():
 v['files']=[{'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for d in ['sources','cases'] for q in sorted((W/d).rglob('*')) if q.is_file()];save(W/'source-manifest.json',v)
manifest();out=subprocess.run(['python3',str(W/'_checkpoint.py')],capture_output=True,text=True);assert out.returncode==0,out.stderr;print(out.stdout)
for p in W.glob('_review_153_171_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  count+=1
  if not (p.parent/url.split('#')[0]).exists():broken.append((str(p),url))
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=broken)
for p in [W/'review-checks.json',W/'sources/review-art-153-171-checks.json',O/'review-checks.json',O/'sources/review-art-153-171-checks.json']:save(p,checks)
manifest();shutil.copyfile(W/'source-manifest.json',O/'source-manifest.json')
print(json.dumps({'complete':True,'reviewed':20,'corrected':8,'whole_book_complete':False,'links_checked':count}))
