from pathlib import Path
import json,sys,re,hashlib,datetime,shutil,subprocess,collections
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
c=load_commentary(str(W));r=json.loads((W/'review-result.json').read_text());checks=json.loads((W/'review-checks.json').read_text());ids=r['reviewed_ids'];assert len(ids)==20
before=json.loads((W/'sources/review-art-106a-120-before-hashes.json').read_text());assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
pgraphs=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:pgraphs[p].append(k)
assert not [v for v in pgraphs.values() if len(v)>1]
assert all(not re.search(r'TODO|FIXME|to be filled',c[k],re.I) for k in ids)
v=json.loads((W/'sources/review-art-106a-120-validation.json').read_text());assert v['verbatim_ratio']==1 and len(v['errors'])==1 and '342' in v['errors'][0]
checks.update(assigned_commentary_count=20,assigned_min_chars=min(len(c[k]) for k in ids),repeated_paragraphs=0,whole_book_complete=False,full_builder_exit_code=1,strict_validator_exit_code=1,strict_validation=v,parser_idempotent=True)
r['validation_result']=v
for name,value in [('review-result.json',r),('sources/review-art-106a-120-result.json',r),('review-checks.json',checks),('sources/review-art-106a-120-checks.json',checks)]:save(W/name,value)
p=W/'status.json';v=json.loads(p.read_text());v['updated_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();v['commentary_characters']=sum(map(len,c.values()));v['bounded_review_art_106a_120']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'changed':6,'unassigned_commentaries_unchanged':True,'evidence':'sources/review-art-106a-120-result.json','whole_book_complete':False};save(p,v)
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_106a_120']={'preflight':'sources/review-art-106a-120-preflight-result.json','actual_fetch_records':json.loads((W/'sources/review-art-106a-120-fetch.json').read_text()),'case_fetch_records':'sources/review-art-106a-120-cases-fetch.json'};save(p,v)
review='''

## Achtste afgebakende tweede lezing — artikelen 106a tot en met 120

Op 20 oktober 2026 zijn exact twintig toegewezen plaatsen volledig gelezen: 106a, 106b, 106c, 106d, 106e, 107, 108, 109, 110, 110a, 111, 112, 113, 114, 115, 116, 117, 118, 119 en 120. Alle leden, letters, bronnotities en voorbeelden zijn aan de officiële tekst getoetst. [Exacte identifiers en individuele bevindingen](sources/review-art-106a-120-result.json). Zes toelichtingen zijn aangescherpt: 106a (gronden en uitzonderingen), 106b (verbod versus kostenveroordelingen), 106c (procedure en voorlopige maatregelen), 110 (doelgroep, vervalbeding en overeenkomstige bepalingen), 114 (iedereen en kosten) en 119 (eed, rechthebbenden en betwisting). Veertien zijn ongewijzigd aanvaard. De 277 overige bestaande toelichtingen zijn hashgelijk gebleven.

Het volledige [vonnis RBOVE 2020:1557](cases/RBOVE-2020-1557.md) is gelezen, vastgelegd en uitsluitend voor de daarin daadwerkelijk besliste informatieplichtgrond en het dictum gebruikt. De daarnaast gestelde herhalingsgrond liet de rechtbank onbeslist. [HTTP- en hashbewijs](sources/review-art-106a-120-cases-fetch.json), [selectief onderzoek en nationale corpusraadpleging](sources/review-art-106a-120-search-log.json). Geen uitputtend rechtspraakonderzoek, verificatie van latere rechtsmiddelen of volledige zelfstandige toets van de externe BW-, fiscale, Europese en overgangsinstrumenten. De bronnotities over overgangsrecht blijven zichtbaar; de toelichting betreft de geselecteerde actuele toestand.

De [nieuwe broncontrole](sources/review-art-106a-120-preflight-result.json) bevat HTTP-200-bodies van actuele officiële HTML, geselecteerde XML en wijzigingsinformatie. Geldend vanaf 1 september 2026 tot heden bij raadpleging op 20 oktober; oorspronkelijke beslissende redactiedatum 19 oktober behouden. Historische toestand 2002 en toekomstige wijziging 2027 zijn uitgesloten. Alle 639 unieke identifiers en wettelijke tokens komen overeen met de parser. Geen eigen wettelijke bijlagen; aanhef en slot behouden. De parser en onafhankelijke dekkingscontrole zijn opnieuw uitgevoerd.

De [volledige build](sources/review-art-106a-120-build.txt) en [strikte validator](sources/review-art-106a-120-validation.json) zijn uitgevoerd. Wettelijke tekstovereenkomst: 100%. De 342 ontbrekende toelichtingen buiten deze opdracht verhinderen de volledige build en boekvalidatie. De bestaande checkpoint-export bouwt de complete hoofdstukken opnieuw. Het manuscript telt nog steeds 297 van 639 toegelichte plaatsen; deze review claimt geen voltooid boek. [Batchcontroles](sources/review-art-106a-120-checks.json) bevestigen twintig aanwezige toelichtingen en geen exact herhaalde lange alinea's. Lengtecontrole is geen bewijs van juridische kwaliteit. Dit is een afgebakende nieuwe proceslezing, geen externe professionele goedkeuring.
'''
p=W/'REVIEW.md';assert 'Achtste afgebakende' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing artikelen 106a–120: [broncontrole](sources/review-art-106a-120-preflight-result.json), [bevindingen](sources/review-art-106a-120-result.json), [primaire rechtspraak](cases/RBOVE-2020-1557.md) en [onderzoekslog](sources/review-art-106a-120-search-log.json).\n')
p=W/'source-manifest.json';v=json.loads(p.read_text())
def manifest():
 v['files']=[{'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for d in ['sources','cases'] for q in sorted((W/d).rglob('*')) if q.is_file()];save(W/'source-manifest.json',v)
manifest();out=subprocess.run(['python3',str(W/'_checkpoint.py')],capture_output=True,text=True);assert out.returncode==0,out.stderr;print(out.stdout)
for p in W.glob('_review_106a_120_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  count+=1
  if not (p.parent/url.split('#')[0]).exists():broken.append((str(p),url))
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=broken)
for p in [W/'review-checks.json',W/'sources/review-art-106a-120-checks.json',O/'review-checks.json',O/'sources/review-art-106a-120-checks.json']:save(p,checks)
manifest();shutil.copyfile(W/'source-manifest.json',O/'source-manifest.json')
print(json.dumps({'complete':True,'reviewed':20,'corrected':6,'whole_book_complete':False,'links_checked':count}))
