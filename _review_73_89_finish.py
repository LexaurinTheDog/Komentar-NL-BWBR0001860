from pathlib import Path
import json,re,hashlib,datetime,collections,sys,shutil,subprocess
W=Path(__file__).resolve().parent;O=Path('/Volumes/LaCie/open-commentary/nl/Komentar-NL-BWBR0001860');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
c=load_commentary(str(W));result=json.loads((W/'review-result.json').read_text());ids=result['reviewed_ids'];checks=json.loads((W/'review-checks.json').read_text())
assert len(ids)==len(set(ids))==20
repeated=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:repeated[p].append(k)
assert not [v for v in repeated.values() if len(v)>1]
for k in ids:assert not re.search(r'TODO|FIXME|to be filled',c[k],re.I)
found=[]
for p in (W/'commentary').glob('*.md'):found+=re.findall(r'^=== (\S+)',p.read_text(),re.M)
assert len(found)==len(set(found))==297
validation=json.loads((W/'sources/review-art-73-89-validation.json').read_text());assert validation['verbatim_ratio']==1.0 and len(validation['errors'])==1 and '342' in validation['errors'][0]
checks.update(parser_idempotent=True,duplicate_commentary_ids=0,repeated_paragraphs=0,assigned_commentary_count=20,assigned_nonempty=True,assigned_min_chars=min(len(c[k]) for k in ids),whole_book_complete=False,full_builder_exit_code=1,strict_validator_exit_code=1,strict_validation=validation,full_build_limitation='342 missing commentaries outside this assigned review batch; full build stops before chapter rendering. Existing complete-chapter checkpoint exporter used.')
save(W/'review-checks.json',checks);save(W/'sources/review-art-73-89-checks.json',checks)
result['limitations']=[x for x in result['limitations'] if not x.startswith('External Rv')]+['External transitional instruments are preserved as editorial notes; not independently analysed in full. EVRM rules are discussed only to the extent supported by the verified HR holdings.']
result['technical_evidence']='sources/review-art-73-89-checks.json';result['validation_result']=validation
save(W/'review-result.json',result);save(W/'sources/review-art-73-89-result.json',result)
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_73_89']={'verified_at':now,'preflight':'sources/review-art-73-89-preflight-result.json','actual_fetch_records':json.loads((W/'sources/review-art-73-89-fetch.json').read_text()),'case_fetch_records':'sources/review-art-73-89-cases-fetch.json'};save(p,v)
p=W/'status.json';v=json.loads(p.read_text());v['updated_at_utc']=now;v['commentary_characters']=sum(map(len,c.values()));v['bounded_review_art_73_89']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'changed':7,'unassigned_commentaries_unchanged':True,'evidence':'sources/review-art-73-89-result.json','case_sources':['ECLI:NL:HR:'+k.replace('-',':') for k in ['2024-1382','2021-102','2026-400','2014-161']],'whole_book_complete':False,'validation':'100% statutory agreement; only full-book failure is 342 missing unassigned commentaries'};save(p,v)
review='''

## Zesde afgebakende tweede lezing — artikelen 73 tot en met 89

Op 20 oktober 2026 zijn exact twintig toegewezen plaatsen tegen hun volledige officiële bron gelezen: 73, 73a, 74, 75, 75a, 76, 77, 78, 79, 80, 80a, 81, 82, 83, 84, 85, 86, 87, 88 en 89. Alle leden, de verwijzingslijst van 78, bronnotities, voorbeelden en interne verwijzingen zijn betrokken. [Bevindingen per plaats en exacte reviewed_ids](sources/review-art-73-89-result.json). De vijf eerdere reviewbewijzen zijn behouden; dit proces claimt uitsluitend deze twintig plaatsen te hebben beoordeeld.

Zeven toelichtingen zijn aangevuld: 73, 78, 84, 85, 86, 87 en 88. De hoorplicht en concrete toets bij curatorontslag zijn verduidelijkt. Artikel 78 behoudt de werkelijke bronverwijzing naar 73 lid 2; de toelichting verwisselt die niet met de ontslagbeslissing uit lid 1. De oproepregel van 84 richt zich specifiek tot stemgerechtigden. Bij 85 en 86 zijn rechtsmiddelen en de afbakening ten opzichte van bewaring concreter gemaakt. Bij 87 en 88 zijn schorsing, stilstaande dertigdagentermijn, actuele bewaringsgronden, periodieke herbeoordeling, gebruiksbeperking van afgedwongen inlichtingen en het ontbreken van een grondslag voor extra rechterlijke contactbeperkingen toegevoegd. De overige dertien toelichtingen zijn zonder wijziging aanvaard; de vervallen plaats 89 blijft uitdrukkelijk behouden.

Vier volledige primaire beschikkingen zijn gelezen, vers van Rechtspraak opgehaald en met het lokale nationale corpus vergeleken: [HR 2024:1382](cases/HR-2024-1382.md), [HR 2021:102](cases/HR-2021-102.md), [HR 2026:400](cases/HR-2026-400.md) en [HR 2014:161](cases/HR-2014-161.md). De kaarten onderscheiden middelen, lagere oordelen, eigen HR-oordeel en dictum. De 2014-uitspraak wordt alleen voor de gebruikswaarborg bij de daar verlangde wilsafhankelijke inlichtingen gebruikt, niet als volledige beschrijving van het later gewijzigde artikel 105 of van alle strafrechtelijk bewijsrecht. De uitspraken in het belang der wet zijn als zodanig aangeduid. Dit is selectief onderzoek; voor de overige technische commissie- en stemartikelen is geen afzonderlijke zaak geverifieerd en aangehaald. Overgangsinstrumenten zijn niet integraal zelfstandig onderzocht.

De [verse preflight](sources/review-art-73-89-preflight-result.json) berust op daadwerkelijke HTTP-200-responses met bodies, headers en SHA-256 voor huidige officiële HTML, geselecteerde XML en WTI. De huidige geldigheidsmelding bevestigt 1 september 2026 tot heden op 20 oktober. De oorspronkelijke beslissende redactiedatum blijft 19 oktober 2026. De oude toestand uit 2002 is uitgesloten; toekomstige wijzigingen zijn niet ingevoegd. XML en de onafhankelijke HTML-inhoudsopgave bevatten elk 639 unieke huidige plaatsen; eigen bijlagen zijn afwezig en aanhef en sluiting behouden. Alle wettelijke tekst is volledig gelijk buiten witruimte. [Parser- en volledigheidshercontrole](sources/review-art-73-89-parser-check.json).

De volledige builder en strikte validator zijn werkelijk uitgevoerd: beide stoppen uitsluitend wegens de 342 nog ontbrekende commentaren buiten de opdracht. [Buildmelding](sources/review-art-73-89-build.txt), [strikte validatie](sources/review-art-73-89-validation.json), [batchcontroles](sources/review-art-73-89-checks.json). De bestaande checkpointprocedure exporteert de 22 volledig geschreven hoofdstukken opnieuw. Alle 277 niet-toegewezen bestaande commentaren zijn hashgelijk gebleven; dubbele commentaaridentificaties en exact herhaalde lange alinea’s zijn niet aangetroffen. Het boek blijft onvoltooid met 297 van 639 toegelichte plaatsen. Deze tweede lezing is een nieuwe controle binnen het project, geen externe professionele goedkeuring; technische tekstovereenkomst bewijst geen juridische kwaliteit.
'''
p=W/'REVIEW.md';s=p.read_text();assert 'Zesde afgebakende' not in s;p.write_text(s.rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'''\n\nAanvullende tweede lezing artikelen 73–89: [actuele broncontrole](sources/review-art-73-89-preflight-result.json), [zoeklog](sources/review-art-73-89-search-log.json), [officiële zaakresponses](sources/review-art-73-89-cases-fetch.json), [vergelijking nationaal corpus](sources/review-art-73-89-case-comparison.json), [bevindingen](sources/review-art-73-89-result.json). De vier nieuwe zaaknotities behandelen [curatorontslag](cases/HR-2024-1382.md), [schorsing bewaring](cases/HR-2021-102.md), [extra contactbeperkingen](cases/HR-2026-400.md) en [zelfbelastende inlichtingen](cases/HR-2014-161.md). Selectieve primaire rechtspraak, geen commerciële annotaties.\n''')
# Refresh reproducible source manifest before exporting all supporting evidence.
p=W/'source-manifest.json';v=json.loads(p.read_text());v['files']=[]
for d in ['sources','cases']:
 for q in sorted((W/d).rglob('*')):
  if q.is_file():v['files'].append({'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
save(p,v)
r=subprocess.run(['python3',str(W/'_checkpoint.py')],capture_output=True,text=True);assert r.returncode==0,r.stderr;print(r.stdout)
for name in ['_review_73_89_fetch.py','_review_73_89_cases_fetch.py','_review_73_89_prepare.py','_review_73_89_edit.py','_review_73_89_audit.py','_review_73_89_finish.py']:
 shutil.copyfile(W/name,O/name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  target=url.split('#')[0];count+=1
  if not (p.parent/target).exists():broken.append({'file':str(p.relative_to(O)),'target':target})
assert not broken,broken
checks.update(broken_output_local_links=broken,output_local_links_checked=count)
for p in [W/'review-checks.json',W/'sources/review-art-73-89-checks.json',O/'review-checks.json',O/'sources/review-art-73-89-checks.json']:save(p,checks)
# The changed checks file is itself part of the manifest.
v['files']=[]
for d in ['sources','cases']:
 for q in sorted((W/d).rglob('*')):
  if q.is_file():v['files'].append({'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
for p in [W/'source-manifest.json',O/'source-manifest.json']:save(p,v)
print(json.dumps({'review_complete':True,'reviewed_ids':ids,'changed':7,'local_links_checked':count,'unassigned_unchanged':True,'whole_book_complete':False}))
