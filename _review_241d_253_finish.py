from pathlib import Path
import json,sys,shutil,subprocess,re,hashlib
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-241d-253';sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);r=json.loads((W/'review-result.json').read_text());ids=r['reviewed_ids'];us=load_units(str(W));cs=load_commentary(str(W));B=W/'batches/art-241d-253';T=O/'batches/art-241d-253'
review='''\n\n## Afgebakende tweede lezing — artikelen 241d–253

Op 21 oktober 2026 zijn exact twintig artikelen beoordeeld: 241d, 241e, 242–247, 247a–247d, 248, 249, 249a, 250, 250a en 251–253. [Exacte reviewed_ids en bevinding per artikel](sources/review-art-241d-253-result.json). Zes toelichtingen zijn verbeterd: de goederen en pandrechtselectie in 241d, het voorlopige verleningstijdstip in 241e, de rechterlijke belangenafweging in 242, de aanvullende positie van DNB bij 246/215, de gewone rechtsmiddelenuitsluiting in 247/282 en de specifieke terugkijktermijnen in 249/43/45. Bij 246 is de onjuiste voorstelling hersteld dat DNB volgens 215 de schuldeisers vervangt. De afwijkende letterlijke formulering van 246 blijft zichtbaar. Veertien andere toelichtingen zijn aanvaard. Niet-toegewezen commentaren zijn hashgelijk gebleven.

De [verse broncaptures](sources/review-art-241d-253-fetch.json) bevatten URL, UTC-ophaaltijd, HTTP200, SHA-256 en formaatcontrole. De [preflight](sources/review-art-241d-253-preflight-result.json) behoudt de oorspronkelijke auteurspeildatum 19 oktober 2026. De actuele officiële route vermeldt gelding vanaf 1 september 2026 tot heden. De lokale reviewdatum, UTC-ophaaltijd en op de officiële pagina vermelde raadpleegdatum zijn afzonderlijke gegevens. Het wijzigingsregister bevat geen ingegane wijziging sinds intake; toekomstige toestanden zijn niet met de geldende tekst vermengd. Historische teksten van 2002 en 2025 zijn op unieke artikelplaatsen en hun uitsluiting uit de extractie gecontroleerd.

De [parsercontrole](sources/review-art-241d-253-parser-check.json) vergelijkt de 639 officiële XML-labels met de volledige verse HTML-inhoudsopgave en de extractie. Geen ontbrekende of dubbele identifiers, volledige tekstovereenkomst, geen onverklaarde juridische tekst. Aanhef, slot, bronnotities en vervallen plaatsen blijven behouden; 250a is een vervallen slot. De volledige XML en HTML-inhoudsopgave bevatten geen operationele bijlagen. Parser en afzonderlijke dekkingscontrole zijn opnieuw uitgevoerd zonder productwijziging. Deze technische controles bewijzen geen inhoudelijke juridische kwaliteit.

Beide volledige Hoge Raad-uitspraken zijn gelezen en opnieuw officieel opgehaald: ECLI:NL:HR:2017:1280 en ECLI:NL:HR:2018:424. [Capturevergelijking en nationale corpusversies](sources/review-art-241d-253-case-comparison.json), [selectief onderzoekslog](sources/review-art-241d-253-search-log.json). Het arrest van 2017 ondersteunt de minimumhoorkring, benadelingsmaatstaf, belangenafweging en het onderscheid tussen een persoonlijk akkoordaanbod en boedelbindende handelingen. Het arrest van 2018 ondersteunt de beperkte verifieerbaarheid van later ontstane aanspraken en het fixatiemoment bij aansluitend faillissement; het verleent geen boedelrang. Partijstellingen, weergegeven hofuitspraken en eigen Hoge Raad-oordelen zijn onderscheiden. Geen uitputtend later-rechtspraakonderzoek of nieuwe autoriteit voor technische bepalingen geclaimd.

De actuele officiële BW7:51 is rechtstreeks gelezen voor de begrippen in 241d/241e. De EUR-Lex-route naar de geconsolideerde insolventieverordening gaf HTTP202 met een lege body en is als onbruikbare bron verworpen. Voor 247d zijn de nationale verwijzingspakketten gecontroleerd; de tekst pretendeert geen zelfstandige behandeling van de Europese materiële omzettingsvoorwaarden. Evenmin worden de volledige Wft-uitkeringsvoorwaarden onder 249a of afzonderlijke externe overgangswetten in bronnotities integraal beoordeeld.

Het afgebakende checkpoint is opnieuw met de ongewijzigde gedeelde bouwer samengesteld en strikt gevalideerd. De volledige boekbouw en validatie zijn daarnaast uitgevoerd; ontbrekende toelichtingen buiten deze batch verhinderen boekvoltooiing. [Validatieresultaten](sources/review-art-241d-253-validation.json). Dit is een projectinterne tweede lezing van uitsluitend twintig artikelen; geen externe professionele goedkeuring en geen voltooid boek.
'''
p=W/'REVIEW.md';assert '## Afgebakende tweede lezing — artikelen 241d–253' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing 241d–253: [bevindingen](sources/'+P+'-result.json), [broncontrole](sources/'+P+'-preflight-result.json), [parsercontrole](sources/'+P+'-parser-check.json), [selectief rechtspraakonderzoek](sources/'+P+'-search-log.json).\n')
intro='''# Faillissementswet — beoordeeld checkpoint artikelen 241d–253

Dit checkpoint bevat uitsluitend de twintig artikelen 241d–253, inclusief de letterartikelen en het vervallen slot 250a. De wettekst geldt vanaf 1 september 2026, naar de oorspronkelijke auteurspeildatum 19 oktober 2026; tweede lezing en nieuwe officiële broncontrole op 21 oktober 2026 lokale tijd. [Officiële tekst](https://wetten.overheid.nl/BWBR0001860/2026-09-01). Zes toelichtingen verbeterd, veertien aanvaard. Het hele boek blijft onvoltooid.

Commentaar © 2026 Vojtěch Říha; Apache-2.0 voor de oorspronkelijke toelichting. Officiële wettekst en rechterlijke uitspraken blijven afzonderlijk bronmateriaal. Concept, geen externe professionele goedkeuring. Selectieve verwerking van twee volledige Hoge Raad-uitspraken; geen uitputtend rechtspraakonderzoek.

[Bevindingen](sources/review-art-241d-253-result.json) · [Broncontrole](sources/review-art-241d-253-preflight-result.json) · [Dekking](sources/review-art-241d-253-parser-check.json) · [Onderzoekslog en beperkingen](sources/review-art-241d-253-search-log.json) · [Tweede lezing](REVIEW.md).
'''
(B/'README.md').write_text(intro);(B/m['intro_file']).write_text(intro);shutil.copyfile(W/'commentary/part-27.md',B/'commentary/part-27.md')
# Bounded expected IDs independently filtered from the official label inventory, not the parser output.
check=json.loads((S/(P+'-parser-check.json')).read_text());ex=check['expected_ids'];ex=ex[ex.index('art-241d'):ex.index('art-253')+1];assert ex==ids
coverage={'official_source':{'url':'https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/2026-09-01_0/xml/BWBR0001860_2026-09-01_0.xml','local_raw_evidence_path':'sources/'+P+'-selected.xml','sha256':sha(S/(P+'-selected.xml'))},'expected_ids':ex,'parsed_ids':[u['id'] for u in us if u['id'] in ids],'annex_disposition':check['annex_disposition'],'scope':'Independently enumerated official contiguous range 241d–253; full 639-ID inventory in parser-check.json.'};save(B/'coverage-evidence.json',coverage)
bm=json.loads((B/'meta.json').read_text());bm['title']='Faillissementswet — beoordeeld checkpoint artikelen 241d–253';save(B/'meta.json',bm)
for year in ['2017','2018']:
 p=S/('author-art-241d-253-case-'+year+'.md');t=p.read_text().replace('author-art-241d-253','review-art-241d-253')
 if year=='2017':t+='\nTweede lezing: rov. 3.7.2–3.7.3 en 3.10.2 laten ruimte voor groepsbelangen bij de belangenafweging, zonder ondergeschiktheid van de Nederlandse surseance aan de buitenlandse herstructurering. Dit ondersteunt de aanvulling bij artikel 242.\n'
 (S/(P+'-case-'+year+'.md')).write_text(t)
# Whole-book builder may refuse missing commentaries. Preserve the exact output without reducing scope.
q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/build_repo.py',str(W)],capture_output=True,text=True);(S/(P+'-build.txt')).write_text(q.stdout+q.stderr)
q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/build_repo.py',str(B)],capture_output=True,text=True);assert q.returncode==0,q.stderr;(S/(P+'-bounded-build.txt')).write_text(q.stdout+q.stderr)
for c in bm['chapters']:
 shutil.copyfile(T/f"{c['n']:02d}-{c['slug']}.md",O/f"{c['n']:02d}-art-241d-253-checkpoint-{c['n']}.md")
for root in [O,B,T]:
 (root/'sources').mkdir(exist_ok=True)
 for p in S.glob(P+'-*'):shutil.copyfile(p,root/'sources'/p.name)
 for name in ['SOURCES.md','REVIEW.md']:shutil.copyfile(W/name,root/name)
for name in ['review-result.json','review-checks.json','preflight-result.json','status.json']:shutil.copyfile(W/name,O/name)
shutil.copyfile(S/'verification.json',O/'sources/verification.json')
for p in W.glob('_review_241d_253_*.py'):shutil.copyfile(p,O/p.name)
checked=0;broken=[]
for p in list(O.glob('*art-241d-253-checkpoint*.md'))+[T/'README.md',T/m['intro_file']]+list(T.glob('*wet*.md'))+[S/(P+'-case-2017.md'),S/(P+'-case-2018.md')]:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',link):continue
  checked+=1
  if not (p.parent/link.split('#')[0]).exists():broken.append([str(p),link])
assert not broken,broken
j=json.loads((W/'review-checks.json').read_text());j.update(local_links_checked=checked,broken_local_links=broken)
for p in [W/'review-checks.json',S/(P+'-checks.json'),O/'review-checks.json',O/'sources'/(P+'-checks.json'),B/'sources'/(P+'-checks.json'),T/'sources'/(P+'-checks.json')]:save(p,j)
print(json.dumps({'reviewed':20,'corrected':6,'links_checked':checked,'whole_book_complete':False}))
