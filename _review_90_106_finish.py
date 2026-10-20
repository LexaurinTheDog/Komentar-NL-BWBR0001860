from pathlib import Path
import json,sys,re,hashlib,datetime,shutil,subprocess,collections
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
c=load_commentary(str(W));r=json.loads((W/'review-result.json').read_text());checks=json.loads((W/'review-checks.json').read_text());ids=r['reviewed_ids']
assert len(ids)==20 and len(set(ids))==20
before=json.loads((W/'sources/review-art-90-106-before-hashes.json').read_text());assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
pgraphs=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:pgraphs[p].append(k)
assert not [v for v in pgraphs.values() if len(v)>1]
assert all(not re.search(r'TODO|FIXME|to be filled',c[k],re.I) for k in ids)
v=json.loads((W/'sources/review-art-90-106-validation.json').read_text());assert v['verbatim_ratio']==1 and len(v['errors'])==1 and '342' in v['errors'][0]
checks.update(assigned_commentary_count=20,assigned_min_chars=min(len(c[k]) for k in ids),repeated_paragraphs=0,whole_book_complete=False,full_builder_exit_code=1,strict_validator_exit_code=1,strict_validation=v,parser_idempotent=True)
r['validation_result']=v;r['limitations']=[x for x in r['limitations'] if not x.startswith('External Rv')]+['The Awbi authorisation is identified as in the official Fw; no complete independent review of the external entry statute or transitional instruments.','Case selection reuses prior primary-source discovery; both full decisions independently read and fetched again, not a new exhaustive search.']
for name,value in [('review-result.json',r),('sources/review-art-90-106-result.json',r),('review-checks.json',checks),('sources/review-art-90-106-checks.json',checks)]:save(W/name,value)
p=W/'status.json';v=json.loads(p.read_text());v['updated_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();v['commentary_characters']=sum(map(len,c.values()));v['bounded_review_art_90_106']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'changed':7,'unassigned_commentaries_unchanged':True,'evidence':'sources/review-art-90-106-result.json','whole_book_complete':False};save(p,v)
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_90_106']={'preflight':'sources/review-art-90-106-preflight-result.json','actual_fetch_records':json.loads((W/'sources/review-art-90-106-fetch.json').read_text()),'case_fetch_records':'sources/review-art-90-106-cases-fetch.json'};save(p,v)
review='''

## Zevende afgebakende tweede lezing — artikelen 90 tot en met 106

Op 20 oktober 2026 zijn exact twintig toegewezen plaatsen volledig gelezen: 90, 91, 92, 93, 93a, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 105a, 105b en 106. Alle leden, letters, bronnotities en bestaande voorbeelden zijn getoetst. [Exacte identifiers en individuele bevindingen](sources/review-art-90-106-result.json). Zeven toelichtingen zijn aangescherpt: 93 (uitzonderingen verzegeling), 98 (advies en latere voortzettingsprocedure), 100 (commissieadvies), 101 (verkoopvormen en cumulatieve grens van € 2.000), 105 (waarborgen bij informatiedwang), 105a (geen extra contactbeperking op basis van medewerkingsplicht) en 106 (personele reikwijdte en betekenis driejaarstermijn). Dertien toelichtingen zijn zonder wijziging aanvaard. De 277 overige bestaande toelichtingen zijn hashgelijk gebleven.

De volledige beschikkingen [HR 2014:161](cases/HR-2014-161.md) en [HR 2026:400](cases/HR-2026-400.md) zijn opnieuw gelezen en vers opgehaald; de bestaande zaaknotities zijn behouden. [Nieuwe HTTP- en hashbewijzen](sources/review-art-90-106-cases-fetch.json), [vergelijking met nationaal corpus](sources/review-art-90-106-case-comparison.json), [onderzoeksafbakening](sources/review-art-90-106-search-log.json). De oudere beschikking wordt uitsluitend voor de daar beoordeelde wilsafhankelijke informatie en dwangwaarborg gebruikt; de huidige informatieplicht volgt uit de actuele wet. Geen volledige rechtspraakinventaris of zelfstandige volledige analyse van Awbi of overgangsinstrumenten wordt geclaimd.

De [nieuwe broncontrole](sources/review-art-90-106-preflight-result.json) controleert werkelijke HTTP-200-bodies voor huidige officiële HTML, geselecteerde XML en WTI. Geldend vanaf 1 september 2026 tot heden op 20 oktober; de oorspronkelijke beslissende redactiedatum blijft 19 oktober. Historische toestand 2002 en toekomstige wijziging 2027 zijn uitgesloten. Alle 639 unieke XML- en HTML-identifiers komen met de parser overeen; geen wettelijke tekst ontbreekt, eigen bijlagen zijn afwezig en aanhef en sluiting zijn behouden. De parser is opnieuw uitgevoerd en de dekkingscontrole blijft volledig.

De [volledige build](sources/review-art-90-106-build.txt) en [strikte validatie](sources/review-art-90-106-validation.json) zijn uitgevoerd. Wettelijke tekstovereenkomst is 100%; uitsluitend de 342 ontbrekende toelichtingen buiten deze opdracht verhinderen volledige boekvalidatie. De bestaande checkpointprocedure exporteert de reeds complete hoofdstukken. [Batchcontroles](sources/review-art-90-106-checks.json). Er zijn geen exact herhaalde lange alinea’s aangetroffen. Het boek blijft onvoltooid: 297 van 639 plaatsen toegelicht. Deze review geldt uitsluitend de twintig genoemde plaatsen en is geen externe professionele goedkeuring.
'''
p=W/'REVIEW.md';assert 'Zevende afgebakende' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing artikelen 90–106: [broncontrole](sources/review-art-90-106-preflight-result.json), [bevindingen per artikel](sources/review-art-90-106-result.json), [hercontrole primaire rechtspraak](sources/review-art-90-106-cases-fetch.json). De bestaande zaaknotities voor HR 2014:161 en HR 2026:400 zijn opnieuw getoetst.\n')
p=W/'source-manifest.json';v=json.loads(p.read_text())
def manifest():
 v['files']=[{'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for d in ['sources','cases'] for q in sorted((W/d).rglob('*')) if q.is_file()];save(W/'source-manifest.json',v)
manifest();out=subprocess.run(['python3',str(W/'_checkpoint.py')],capture_output=True,text=True);assert out.returncode==0,out.stderr;print(out.stdout)
for p in W.glob('_review_90_106_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  count+=1
  if not (p.parent/url.split('#')[0]).exists():broken.append((str(p),url))
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=broken)
for p in [W/'review-checks.json',W/'sources/review-art-90-106-checks.json',O/'review-checks.json',O/'sources/review-art-90-106-checks.json']:save(p,checks)
manifest();shutil.copyfile(W/'source-manifest.json',O/'source-manifest.json')
print(json.dumps({'complete':True,'reviewed':20,'corrected':7,'whole_book_complete':False,'links_checked':count}))
