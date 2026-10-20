from pathlib import Path
import json,re,sys,subprocess,shutil,hashlib,datetime
W=Path(__file__).resolve().parent;S=W/'sources';prefix='review-art-212z-213a';O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_units,load_commentary,quote
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
for p in [W/'review-result.json',S/(prefix+'-result.json')]:
 j=json.loads(p.read_text());j['limitations']=[x.replace('213a definition','213 definition') for x in j['limitations']];save(p,j)
r=json.loads((W/'review-result.json').read_text());ids=r['reviewed_ids'];cs=load_commentary(str(W));us=load_units(str(W))
log={'searched_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'web_queries':['site.curia.europa.eu C-85/12 LBI judgment 24 October 2013','site:rechtspraak.nl "212ee"','site:rechtspraak.nl "213a" "verzekeraar"'],'web_result':'Official InfoCuria case index identified LBI, C-85/12, ECLI:EU:C:2013:697. Full judgment PDF capture failed: HTTP202 empty body, rejected; web open also cache miss. No judgment holding used.','official_index':'https://infocuria.curia.europa.eu/tabs/redirect/juris/documents.jsf?num=C-85%2F12','local_search':'rg -l -i 212ee|212dd|212oo|213a /Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr --glob *.md','local_matches':[{'file':'ecli-nl-hr-1968-ac2286.md','disposition':'Not adopted as an authority; prior search identified different numbered insurance provisions.'},{'file':'ecli-nl-hr-2006-au7473.md','disposition':'Not adopted; accounting guideline paragraph false positive in earlier search.'},{'file':'ecli-nl-hr-2023-839.md','disposition':'Inspected local text: damages/valuation following forced transfer under old Wft, not adopted for current213a jurisdiction. No holding used.'}],'limits':'Selective research; no exhaustive case-law claim, no new case cards or holdings.'}
save(S/(prefix+'-search-log.json'),log)
review='''

## Zeventiende afgebakende tweede lezing — artikelen 212z–213a

Op 21 oktober 2026 zijn exact de twintig toegewezen plaatsen 212z, 212aa–212nn, 212nna, 212oo, 212pp, 213 en 213a tegen de officiële bron gelezen. [Exacte reviewed_ids en bevindingen per plaats](sources/review-art-212z-213a-result.json). Drie toelichtingen zijn gecorrigeerd en zeventien zonder wijziging aanvaard. De eigen voorwaarden, leden en letters, bronnotities, voorbeelden en gebruikte interne verwijzingen zijn gecontroleerd. Niet-toegewezen commentaren zijn hashgelijk gebleven. Dit is een projectinterne tweede lezing van deze batch, geen volledige boekreview of externe professionele goedkeuring.

Bij 212ff definieert het wettelijk aangehaalde artikel 212a, onderdeel m, in de actuele tekst de afwikkelingsrekening; onderdeel l omschrijft verrekening. Het commentaar verklaart de verwijzing nu niet langer ten onrechte tot sluitende actuele kwalificatievoorwaarde. De letterlijke wettekst is behouden en de interpretatieve moeilijkheid is zichtbaar gemaakt. Voor afzonderlijke verrekeningsbevoegdheden is de verwijzing naar 212w toegevoegd, naast 212x voor benadelingsacties. Bij 213 is de onregelmatigheid van onderdeel a expliciet gemaakt: twee benamingen maar drie verwijzingen, waaronder de herverzekeraarsdefinitie onder f. De betekenis wordt vanuit de samenhang benaderd zonder de officiële tekst stilzwijgend te verbeteren of de Europese kwalificatiecriteria uit geheugen aan te vullen.

Voor het vervallen 212nna is de [historische officiële toestand van 19 november 2025](sources/review-art-212z-213a-historical-2025.xml) daadwerkelijk gelezen. Het commentaar omschrijft nu de vroegere voorwaarde van DNB-bevoegdheidsgebruik onder afdeling 3A.1.5 Wft, de toenmalige entiteitsverwijzing c–g en uitzonderingen 212k en 212r. Dat is onderscheiden van het huidige 212pp. De vervaldatum 25 maart 2026 en de bronverwijzingen Stb. 2026/60 en 61 zijn tegen de actuele artikelmetadata gecontroleerd. Een eerste verzoek om een niet-bestaande toestand 1 januari 2026 leverde een lege301-response op en is afgewezen; die response is geen inhoudelijke bron.

De overige zeventien plaatsen zijn aanvaard op hun eigen onderwerp: ligging bij onroerende contracten; registergezag bij bankrechten; marktrecht en effectendepotvoorbehouden; bezwarende beschikkingen na opening; aanhangige gedingen; cumulatief bewijs bij benadeling; terugoverdrachtscontracten; uitoefening effectenrechten; curatorbevoegdheden en bijstand; benoemingsbewijs en vertaling; Haagse registratie; informatieketen voor derde-landbanken; coördinatie-inspanningen; bescherming van reddingsderden; twee verschillende beleggingsondernemingsroutes; eigen groepsentiteitsregeling; Amsterdamse verzekeraarsbevoegdheid en de vergunning-/bijkantoorscenario’s. De checklists zijn op aansluiting bij deze onderwerpen beoordeeld.

[Verse broncaptures](sources/review-art-212z-213a-fetch.json) bevatten URL, werkelijke ophaaltijd, HTTP200, formaatcontrole en SHA-256. De actuele route bevestigt gelding vanaf 1 september 2026 tot heden. De officiële getoonde raadpleegdatum20 oktober is onderscheiden van de ophaaltijd. De [preflight](sources/review-art-212z-213a-preflight-result.json) bewaart de beslissende auteursdatum19 oktober, sluit historische en toekomstige toestanden uit en stelt via WTI geen effectieve wijziging sinds intake vast. De [parsercontrole](sources/review-art-212z-213a-parser-check.json) reproduceert de bestaande parserproducten bytegelijk: 639 actuele unieke identificaties uit onafhankelijk gelezen XML en HTML-inhoudsopgave, geen ontbrekende eenheden, verantwoorde aanhef en slot, geen operationele bijlagen. De externe Wft-bijlage waarnaar 213 verwijst is geen ontbrekende bijlage van deze wet.

[Selectief rechtspraakonderzoek](sources/review-art-212z-213a-search-log.json) omvat officiële webzoekopdrachten en de lokale HR-corpuszoekactie. LBI is in de officiële index gevonden maar de volledige uitspraakresponse was leeg en is verworpen. Er is geen holding aan toegeschreven. Het lokale Conservatrix-resultaat betreft waardering onder oud interventierecht en is niet als autoriteit voor de actuele bevoegdheidsregel gebruikt. Geen uitputtende dekking geclaimd.

De [volledige bouwpoging](sources/review-art-212z-213a-build.txt) en [strikte validator](sources/review-art-212z-213a-validation.json) zijn uitgevoerd. De wettekstovereenkomst is100%; 299 ontbrekende commentaren buiten de batch verhinderen een geslaagde volledige bouw/validatie. Alle twintig toegewezen plaatsen hebben afzonderlijk inhoudelijk commentaar en geen identieke lange alinea. Lengte bewijst geen juridische kwaliteit. Het beoordeelde checkpoint is opnieuw samengesteld. Het gehele boek blijft onvoltooid.
'''
p=W/'REVIEW.md';assert 'Zeventiende afgebakende' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing212z–213a: [beoordeling](sources/'+prefix+'-result.json), [bronpreflight](sources/'+prefix+'-preflight-result.json), [onderzoekslog](sources/'+prefix+'-search-log.json).\n')
oldidx=(O/'INDEX.md').read_text();lines=[x for x in oldidx.splitlines() if x.startswith('[') and 'checkpoint.md)' in x]
q=subprocess.run([sys.executable,str(W/'_checkpoint.py')],capture_output=True,text=True);assert q.returncode==0,q.stderr
parts=['# Artikelen212z–213a — beoordeeld checkpoint','Twintig toegewezen eenheden van een onvoltooid commentaar. Wettekst:1 september2026. Projectinterne tweede lezing:21 oktober2026; drie toelichtingen gecorrigeerd, zeventien aanvaard. [Exacte beoordeling](sources/'+prefix+'-result.json). [Bronpreflight](sources/'+prefix+'-preflight-result.json). Tekst commentaar ©2026 Vojtěch Říha; Apache-2.0. Concept; geen externe professionele goedkeuring.']
for u in us:
 if u['id'] in ids:
  parts.extend(['### '+u['label'],'**Wettekst:**',quote(u['text'])]);parts.extend('*Redactionele bronnotitie:* '+n for n in u['notes']);parts.append(cs[u['id']])
(O/'24-art-212z-213a-checkpoint.md').write_text('\n\n'.join(parts)+'\n')
p=O/'INDEX.md';s=p.read_text().replace('van artikel 1 tot en met artikel 212i','van artikel 1 tot en met artikel 213a (inclusief afzonderlijke checkpoints)')
for line in lines:
 if line not in s:s+='\n'+line+'\n'
p.write_text(s)
for p in W.glob('_review_212z_213a_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',target):continue
  count+=1
  if not (p.parent/target.split('#')[0]).exists():broken.append([str(p.relative_to(O)),target])
assert not broken,broken
checks=json.loads((W/'review-checks.json').read_text());checks.update(output_local_links_checked=count,broken_output_local_links=[])
for p in [W/'review-checks.json',S/(prefix+'-checks.json'),O/'review-checks.json',O/'sources'/(prefix+'-checks.json')]:save(p,checks)
manifest=json.loads((W/'source-manifest.json').read_text());manifest['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];manifest['scope']='Preserved sources and bounded review evidence through assigned articles212z–213a; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:save(p,manifest)
print(json.dumps({'reviewed':20,'corrected':3,'local_links_checked':count,'whole_book_complete':False}))
