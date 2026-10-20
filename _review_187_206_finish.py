from pathlib import Path
import json,sys,hashlib,re,collections,datetime,shutil,subprocess
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
c=load_commentary(str(W));r=json.loads((W/'review-result.json').read_text());checks=json.loads((W/'review-checks.json').read_text());ids=r['reviewed_ids'];assert ids==['art-'+str(n) for n in range(187,207)]
before=json.loads((W/'sources/review-art-187-206-before-hashes.json').read_text());assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
paragraphs=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:paragraphs[p].append(k)
assert not [v for v in paragraphs.values() if len(v)>1]
assert all(not re.search(r'TODO|FIXME|to be filled',c[k],re.I) for k in ids)
# Repeat the required builder and strict validator against the final edited manuscript.
for tool,suffix in [('build_repo.py','build.txt'),('validate.py','validation.json')]:
 proc=subprocess.run(['python3','/Volumes/LaCie/open-commentary/_tools/'+tool,str(W)],capture_output=True,text=True);assert proc.returncode==1
 (W/('sources/review-art-187-206-'+suffix)).write_text(proc.stdout+proc.stderr)
v=json.loads((W/'sources/review-art-187-206-validation.json').read_text());assert v['verbatim_ratio']==1 and len(v['errors'])==1 and '342' in v['errors'][0]
checks.update(assigned_commentary_count=20,assigned_min_chars=min(len(c[k]) for k in ids),repeated_paragraphs=0,whole_book_complete=False,full_builder_exit_code=1,strict_validator_exit_code=1,strict_validation=v,parser_reproduction_evidence='sources/review-art-187-206-parser-check.json')
r['validation_result']=v
for name,value in [('review-result.json',r),('sources/review-art-187-206-result.json',r),('review-checks.json',checks),('sources/review-art-187-206-checks.json',checks)]:save(W/name,value)
p=W/'status.json';st=json.loads(p.read_text());st['updated_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();st['commentary_characters']=sum(map(len,c.values()));st['bounded_review_art_187_206']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'changed':17,'unassigned_commentaries_unchanged':True,'evidence':'sources/review-art-187-206-result.json','whole_book_complete':False,'case_authorities':['ECLI:NL:HR:2014:1630','ECLI:NL:HR:2016:759'],'source_preflight':'sources/review-art-187-206-preflight-result.json'};save(p,st)
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_187_206']={'preflight':'sources/review-art-187-206-preflight-result.json','actual_fetch_records':json.loads((W/'sources/review-art-187-206-fetch.json').read_text()),'case_fetch_records':'sources/review-art-187-206-cases-fetch.json','historical_source':'sources/version-register.xml; official historical toestand 2002-01-01, excluded from current operative text and used solely for explicitly historical explanations of repealed198–202'};save(p,v)
review='''

## Dertiende afgebakende tweede lezing — artikelen 187 tot en met 206

Op 21 oktober 2026 (Europe/Prague; bronresponsen 20 oktober UTC) zijn precies de twintig plaatsen 187–206 inhoudelijk nagelezen tegen de officiële wettelijke tekst. Alle leden, bronnotities, voorbeelden en relevante interne verwijzingen zijn gecontroleerd. [Exacte reviewed_ids en afzonderlijke bevindingen](sources/review-art-187-206-result.json). Zeventien toelichtingen zijn verbeterd; artikelen 189, 191 en 195 zijn zonder wijziging aanvaard. De overige 277 bestaande toelichtingen zijn hashgelijk bewaard. Dit rapport beoordeelt uitsluitend deze batch en vervangt eerdere reviewbevindingen niet.

De behandeling in cassatie moet volgens artikel 187 binnen twintig dagen plaatsvinden; alleen een zittingsdatum bepalen is onvoldoende. De acht dagen lopen vanaf het geven van de beschikking. Artikel 188 legt afgifte van de verklaring op verzoek vast en maakt inschrijving bij of na levering mogelijk. Artikel 190 bevat nu een controleerbaar rekenvoorbeeld met aftrek over hetzelfde gerangschikte bedrag. Bij artikel 193 is de foutieve aanduiding van de persoonlijke aanspraak gecorrigeerd naar een aanspraak tegen de schuldenaar; rekening en verantwoording na een maand en teruggave van boeken zijn afzonderlijke verplichtingen. Artikel 194 onderscheidt het rechtbankbevel van gewone goedkeuring door de rechter-commissaris.

De vervallen artikelen 198–202 zijn elk vergeleken met hun eigen historische tekst in de [officiële toestand uit 2002](sources/version-register.xml): nalatenschapsaanvraag, bevoegde rechtbank en oproeping, vermogensafscheiding, aanvraagtermijnen en beperkingen van akkoord- en achtste afdeling. Die historische bepalingen zijn niet als actueel recht in units.jsonl ingevoegd. De huidige restverwijzing in artikel 5 naar artikel 198 herstelt de vervallen aanvraaggrond niet. De huidige externe erfrechtelijke regeling is niet integraal gecertificeerd. Bij artikel 206 blijven de dubbele bronwoorden en spellingnotitie bewaard; de toelichting verduidelijkt advocatenindiening en het bewijsvereiste van artikel 207.

[Verse HTTP-opvragingen](sources/review-art-187-206-fetch.json) bevatten URL, tijdstip, HTTP 200, SHA-256, geldig XML-formaat en expliciete gelding vanaf 1 september 2026 tot heden. De [preflight](sources/review-art-187-206-preflight-result.json) behoudt de beslissende auteursdatum 19 oktober, controleert de WTI, sluit de historische toestand en toekomstige wijzigingen uit en vindt geen effectieve wijziging sinds intake. De 639 unieke officiële XML-identificatoren stemmen overeen met de onafhankelijke officiële HTML-inhoudsopgave en parseruitvoer. Aanhef, slot en redactionele notities zijn verantwoord; geen operatieve bijlage aangetroffen. [Opnieuw uitgevoerde parser en volledigheidscontrole](sources/review-art-187-206-parser-check.json) leveren dezelfde bytes op; geen wettelijke tekstreparatie nodig.

Drie volledige officiële uitspraken en hun nationale corpusversies zijn gelezen. [HR 2014:1630](cases/HR-2014-1630-buitenlands-verhaal.md) ondersteunt bij artikel 203 de toets van de buitenlandse voorrangspositie naar inhoud of strekking. De oude Europese insolventieverordening in dat arrest is niet als actuele Europese regel overgenomen. [HR 2016:759](cases/HR-2016-759-verificatietitel.md) ondersteunt de verificatietitel en haar beperking door persoonlijke betwisting, met de door het arrest bepaalde executieverjaring. [HR 2016:202](sources/review-art-187-206-case-hr-2016-202.txt) is bewust niet als inhoudelijke autoriteit gebruikt: het dictum verwerpt met artikel 81 RO, terwijl de weergegeven conclusie niet-ontvankelijkheid adviseerde. Dat advies is geen oordeel van de Hoge Raad. [Vergelijking met corpus](sources/review-art-187-206-case-comparison.json): de niet-gematchte alinea's zijn uitsluitend voorwerk dat het corpus weglaat; de inhoudelijke onderdelen stemmen overeen. [Onderzoekslog en grenzen](sources/review-art-187-206-search-log.json). Selectieve rechtspraak, geen uitputtende controle van latere behandeling. Geen andere uitspraak toegevoegd voor de overige technische of vervallen plaatsen. Externe BW-, Rv-, Europese, buitenlandse en overgangsregelingen zijn niet integraal gecertificeerd; de uitleg blijft beperkt tot de gecontroleerde Fw en gelezen oordelen.

De [volledige buildpoging](sources/review-art-187-206-build.txt) stopt op 342 ontbrekende commentaren buiten de batch. De [strikte validator](sources/review-art-187-206-validation.json) bevestigt 100% wettelijke tekstovereenkomst maar meldt diezelfde onvolledigheid. De bestaande checkpoint-export is opnieuw samengesteld. [Batchcontroles](sources/review-art-187-206-checks.json) bevestigen alle twintig commentaren, behoud van andere toelichtingen, geen exact herhaalde lange alinea's en de lokale links. Lengtecontrole bewijst geen juridische kwaliteit. Het boek is onvoltooid; deze tweede lezing binnen het project is geen externe professionele goedkeuring.
'''
p=W/'REVIEW.md';assert 'Dertiende afgebakende' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing artikelen 187–206: [broncontrole](sources/review-art-187-206-preflight-result.json), [bevindingen](sources/review-art-187-206-result.json), [onderzoekslog](sources/review-art-187-206-search-log.json), [HR 2014:1630](cases/HR-2014-1630-buitenlands-verhaal.md), [HR 2016:759](cases/HR-2016-759-verificatietitel.md).\n')
p=W/'source-manifest.json';manifest=json.loads(p.read_text());manifest['scope']='Preserved source and bounded-review evidence, including articles 187–206; no new rights claim over official texts.'
def save_manifest():
 manifest['files']=[{'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for d in ['sources','cases'] for q in sorted((W/d).rglob('*')) if q.is_file()];save(W/'source-manifest.json',manifest)
save_manifest();out=subprocess.run(['python3',str(W/'_checkpoint.py')],capture_output=True,text=True);assert out.returncode==0,out.stderr;print(out.stdout)
for p in W.glob('_review_187_206_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  count+=1
  if not (p.parent/url.split('#')[0]).exists():broken.append((str(p),url))
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=broken)
for p in [W/'review-checks.json',W/'sources/review-art-187-206-checks.json',O/'review-checks.json',O/'sources/review-art-187-206-checks.json']:save(p,checks)
save_manifest();shutil.copyfile(W/'source-manifest.json',O/'source-manifest.json')
print(json.dumps({'complete':True,'reviewed':20,'corrected':17,'whole_book_complete':False,'links_checked':count}))
