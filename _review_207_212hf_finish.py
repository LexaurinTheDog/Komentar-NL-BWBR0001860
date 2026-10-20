from pathlib import Path
import json,sys,hashlib,re,collections,datetime,shutil,subprocess
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
c=load_commentary(str(W));r=json.loads((W/'review-result.json').read_text());checks=json.loads((W/'review-checks.json').read_text());ids=r['reviewed_ids'];assert len(ids)==20
before=json.loads((W/'sources/review-art-207-212hf-before-hashes.json').read_text());assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
paragraphs=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:paragraphs[p].append(k)
assert not [v for v in paragraphs.values() if len(v)>1]
assert all(not re.search(r'TODO|FIXME|to be filled',c[k],re.I) for k in ids)
for tool,suffix in [('build_repo.py','build.txt'),('validate.py','validation.json')]:
 proc=subprocess.run(['python3','/Volumes/LaCie/open-commentary/_tools/'+tool,str(W)],capture_output=True,text=True)
 (W/('sources/review-art-207-212hf-'+suffix)).write_text(proc.stdout+proc.stderr)
 assert proc.returncode==1
v=json.loads((W/'sources/review-art-207-212hf-validation.json').read_text());assert v['verbatim_ratio']==1 and '342' in v['errors'][0]
checks.update(assigned_commentary_count=20,assigned_min_chars=min(len(c[k]) for k in ids),repeated_paragraphs=0,whole_book_complete=False,full_builder_exit_code=1,strict_validator_exit_code=1,strict_validation=v,parser_reproduction_evidence='sources/review-art-207-212hf-parser-check.json')
r['validation_result']=v
for name,value in [('review-result.json',r),('sources/review-art-207-212hf-result.json',r),('review-checks.json',checks),('sources/review-art-207-212hf-checks.json',checks)]:save(W/name,value)
p=W/'status.json';st=json.loads(p.read_text());st['updated_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();st['commentary_characters']=sum(map(len,c.values()));st['bounded_review_art_207_212hf']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'changed':13,'unassigned_commentaries_unchanged':True,'evidence':'sources/review-art-207-212hf-result.json','whole_book_complete':False,'case_authorities':['ECLI:NL:RBROT:2020:1792','ECLI:NL:RBALM:1999:AA3942'],'source_preflight':'sources/review-art-207-212hf-preflight-result.json'};save(p,st)
p=W/'sources/verification.json';verification=json.loads(p.read_text());verification['bounded_review_art_207_212hf']={'preflight':'sources/review-art-207-212hf-preflight-result.json','actual_fetch_records':json.loads((W/'sources/review-art-207-212hf-fetch.json').read_text()),'case_fetch_records':'sources/review-art-207-212hf-cases-fetch.json','transitional_records':'sources/review-art-207-212hf-transitional-fetch.json'};save(p,verification)
review='''

## Veertiende afgebakende tweede lezing — artikelen 207 tot en met 212hf

Op 21 oktober 2026 (Europe/Prague; bronresponsen 20 oktober UTC) zijn precies twintig plaatsen nagelezen: 207–212, 212a–h en 212ha–hf. [Exacte reviewed_ids en afzonderlijke bevindingen](sources/review-art-207-212hf-result.json). Alle leden, subonderdelen, bronnotities, interne verwijzingen en voorbeelden zijn tegen de officiële wettelijke toestand gecontroleerd. Dertien toelichtingen zijn verbeterd; zeven zijn zonder wijziging aanvaard. Alle overige 277 bestaande toelichtingen zijn hashgelijk bewaard. Deze review betreft uitsluitend de batch, geen volledige boekreview of externe professionele goedkeuring.

Artikel 207 verduidelijkt nu met het eigen oordeel van Rechtbank Rotterdam dat nakoming van een akkoord en een curatorverklaring in die zaak het vereiste bewijs niet leverden. Het verzoekersstandpunt is geen rechterlijk oordeel. Het historische Almelose toewijzende vonnis illustreert artikelen 208/210, met de uitdrukkelijke beperking dat de oude dagbladpublicatie geen huidig vereiste is. De centrale registratie onder artikel 212 is bevestigd tegen artikelen 19 en 19a; er was daar geen inhoudelijke fout te herstellen. Bij 212a zijn de eigen deelnemersdrempel en uitsluitingen van de derdelandroute verduidelijkt; bij 212b de niet-tegenwerpelijkheid, toepasselijke leden en goederen waarop de afkoelingsuitzondering ziet. Bij 212d zijn de verschillende telregels, clearing/uitvoering, letterlijk beperkte publicatieverwijzing en afzonderlijke informatieplichten behandeld. Artikel 212g onderscheidt deposito-overeenkomst, in aanmerking komend en gegarandeerd deposito en de verschillende reikwijdten van leden 1 en 2.

Bij 212ha is de zevendagentermijn gecorrigeerd naar dagtekening van de kennisgeving, met de DNB-mededeling als alternatief en zonder automatische toewijzing bij termijnverloop. Artikel 212hd onderscheidt afschrift voor de bank en inhoudskennisgeving voor autoriteiten en bewaart het aanknopingspunt voor dienstverlening vanuit vestigingen in een andere lidstaat. Artikel 212hf ziet op DNB's oordeel over a/b; een uitbreiding naar c of elk Europees oordeel is niet aangenomen. De vervallen plaatsen 212f/212hc blijven leeg als huidige wettelijke tekst. De vroegere effectenrechtelijke conflictenregel van 212f is alleen historisch verklaard tegen de officiële toestand2002; 212hc wordt niet uit een verzekeraars-overgangsregel herleefd.

De drie in de bronnotities genoemde [officiële wijzigingswetten](sources/review-art-207-212hf-transitional-fetch.json) zijn daadwerkelijk opgehaald en gelezen. Artikel III van Stb. 2025/363 behoudt de vroegere afdeling 11A voor de daarin omschreven oudere faillissementen en surseances; de geconsolideerde XML dateert de wijziging op 19 november 2025. Dit is nu bij artikelen 212a–d uitgelegd. Artikel XIV lid 4 van Stb. 2018/489 ziet op oudere faillissementen van verzekeraars. Artikel CIX van Stb. 2016/290 regelt de overgang bij procesrechtelijke digitalisering; geen volledige certificering van alle latere invoeringsbesluiten of externe Rv-bepalingen is verricht.

[Verse bronresponses](sources/review-art-207-212hf-fetch.json) bevatten daadwerkelijke URL, tijdstip, HTTP200, hashes, formaatcontrole en expliciete gelding vanaf1september2026 tot heden. [Preflight](sources/review-art-207-212hf-preflight-result.json) behoudt de beslissende auteursdatum19oktober, vergelijkt WTI en huidige route, vindt geen effectieve wijziging sinds intake en sluit historische en toekomstige versies uit. De officiële XML en onafhankelijke HTML-inhoudsopgave bevestigen639unieke plaatsen, geen operationele bijlage, en verantwoorde aanhef/slottekst. [Opnieuw uitgevoerde parser en volledigheidscontrole](sources/review-art-207-212hf-parser-check.json) produceren dezelfde bestanden. Geen wettelijke tekst aangepast.

Volledige officiële teksten van [Rotterdam2020:1792](cases/RBROT-2020-1792-rehabilitatie.md) en [Almelo1999:AA3942](cases/RBALM-1999-AA3942-rehabilitatie.md) zijn gelezen. Het lokale nationale corpus bevat hogere gerechten, geen collectie van deze lagere gerechten; geen duplicaat aangetroffen. [Onderzoekslog](sources/review-art-207-212hf-search-log.json). Voor de overige plaatsen is geen voldoende relevante geverifieerde uitspraak gebruikt. Dit is selectief onderzoek; latere behandeling en alle externe Europese, Wft-, BW-, Rv- en overgangsregelingen zijn niet uitputtend gecertificeerd. Geen commerciële annotatie gekopieerd.

De volledige build is [daadwerkelijk geprobeerd](sources/review-art-207-212hf-build.txt); de [strikte validator](sources/review-art-207-212hf-validation.json) bevestigt100% wettelijke tekstovereenkomst en meldt342ontbrekende commentaren buiten de batch. Het bestaande onvoltooide checkpoint is opnieuw geëxporteerd. [Batchcontroles](sources/review-art-207-212hf-checks.json) bevestigen20toelichtingen, behoud van andere toelichtingen, geen exact herhaalde lange alinea's en geldige lokale bewijslinks. Minimumlengte bewijst geen juridische kwaliteit. Het boek blijft onvoltooid.
'''
# Keep typography readable in the durable report.
for a,b in [('toestand2002','toestand 2002'),('HTTP200','HTTP 200'),('vanaf1september2026','vanaf 1 september 2026'),('auteursdatum19oktober','auteursdatum 19 oktober'),('bevestigen639unieke','bevestigen 639 unieke'),('Rotterdam2020','Rotterdam 2020'),('Almelo1999','Almelo 1999'),('bevestigt100%','bevestigt 100%'),('meldt342ontbrekende','meldt 342 ontbrekende'),('bevestigen20toelichtingen','bevestigen 20 toelichtingen')]:review=review.replace(a,b)
p=W/'REVIEW.md';assert 'Veertiende afgebakende' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing artikelen 207–212hf: [broncontrole](sources/review-art-207-212hf-preflight-result.json), [bevindingen](sources/review-art-207-212hf-result.json), [overgangsbronnen](sources/review-art-207-212hf-transitional-fetch.json), [onderzoekslog](sources/review-art-207-212hf-search-log.json), [Rotterdam](cases/RBROT-2020-1792-rehabilitatie.md), [Almelo](cases/RBALM-1999-AA3942-rehabilitatie.md).\n')
manifest=json.loads((W/'source-manifest.json').read_text());manifest['scope']='Preserved source and bounded review evidence through articles207–212hf; no new rights claim over official texts.'
def save_manifest():
 manifest['files']=[{'path':str(q.relative_to(W)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for d in ['sources','cases'] for q in sorted((W/d).rglob('*')) if q.is_file()];save(W/'source-manifest.json',manifest)
save_manifest();out=subprocess.run(['python3',str(W/'_checkpoint.py')],capture_output=True,text=True);assert out.returncode==0,out.stderr;print(out.stdout)
for p in W.glob('_review_207_212hf_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  count+=1
  if not (p.parent/url.split('#')[0]).exists():broken.append((str(p),url))
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=broken)
for p in [W/'review-checks.json',W/'sources/review-art-207-212hf-checks.json',O/'review-checks.json',O/'sources/review-art-207-212hf-checks.json']:save(p,checks)
save_manifest();shutil.copyfile(W/'source-manifest.json',O/'source-manifest.json')
print(json.dumps({'complete':True,'reviewed':20,'corrected':13,'whole_book_complete':False,'links_checked':count}))
