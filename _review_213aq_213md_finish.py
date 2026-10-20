from pathlib import Path
import sys,json,shutil,re,hashlib
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-213aq-213md'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);r=json.loads((W/'review-result.json').read_text());ids=r['reviewed_ids'];cs=load_commentary(str(W));us=load_units(str(W))
review='''

## Negentiende afgebakende tweede lezing — artikelen 213aq–213md

Op 21 oktober 2026 zijn exact de twintig toegewezen plaatsen 213aq, 213ar, 213b–213k, 213ka, 213kaa, 213l, 213m en 213ma–213md gecontroleerd. Alle leden, onderdelen, bronnotities, voorbeelden en gebruikte verwijzingen zijn inhoudelijk gelezen tegen de officiële tekst. [Exacte reviewed_ids en bevindingen per artikel](sources/review-art-213aq-213md-result.json). Bij 213ar is de onjuiste omschrijving van 213ag als rechtsmiddelenregel vervangen door bekendmaking. Bij 213j is verduidelijkt dat lid 2 het Nederlandse bericht met meertalig formulier voorschrijft. Bij 213l is het bereik van lid 1 expliciet beperkt tot na de aanvangsdag vervallende verzekeringsvorderingen. Bij 213mc is een grammaticale fout hersteld. De andere zestien toelichtingen zijn aanvaard. Alle niet-toegewezen commentaren zijn hashgelijk gebleven.

De aanvraag tegen de moeder, toezichtscommunicatie, schuldeisersinformatie en taalregels zijn afzonderlijk gecontroleerd. Voor de polissen zijn termijnpremies, volledige premiebetaling, het nog mogelijke risico, spaarelement, RC-toestemming en beëindiging onderscheiden. Bij de waardering zijn de drie peildata en bij de rangorde alle categorieën gecontroleerd. De voorschotregels zijn getoetst op opeisbaarheid, drempel, risicodatum, afkoopmoment, uitsluitingen, verzoektermijn, prudente prognose en voortzetting van reeds lopende betalingen. Artikel 213md maakt de negentig dagen tot verzoektermijn, niet zonder meer tot uiterste betaaldatum. De checklist is een thematisch hulpmiddel en geen verondersteld einde van de wettelijke afdeling.

De [verse broncaptures](sources/review-art-213aq-213md-fetch.json) bewaren URL, werkelijke UTC-ophaaltijd, HTTP-resultaat, formaatcontrole en SHA-256. De actuele route bevestigt gelding vanaf 1 september 2026 tot heden; de getoonde raadpleegdatum staat los van de capturetijd. De [preflight](sources/review-art-213aq-213md-preflight-result.json) behoudt 19 oktober 2026 als auteursdatum en controleert wijzigingen sinds intake, historische toestanden en toekomstige wijzigingsdata. De actuele Wft-definitie van groep in 3a:77 is afzonderlijk gelezen. Stb. 2023/306 bevestigt de relevante wijzigingen en vervallen plaatsen; XIV(4) van Stb. 2018/489 bewaart oud recht voor eerder uitgesproken verzekeraarsfaillissementen. Er is geen vroegere norm als huidige tekst ingevoegd.

De [parsercontrole](sources/review-art-213aq-213md-parser-check.json) vergelijkt onafhankelijk de officiële XML-identificaties, HTML-inhoudsopgave en parserproducten: 639 unieke plaatsen, geen ontbrekende of dubbele identificaties. De bestaande parser en volledigheidscontrole zijn opnieuw bytegelijk uitgevoerd. Iedere wettelijke artikeltekst stemt overeen; aanhef en slot blijven afzonderlijk verantwoord. De volledige XML bevat geen operationele bijlagen.

Het [selectieve rechtspraakonderzoek](sources/review-art-213aq-213md-search-log.json) is herhaald in de officiële rechtspraakindex en het lokale Hoge Raad-corpus. De gerichte zoekvragen leverden geen voldoende relevante geverifieerde uitspraak op. Er is geen nieuwe uitspraak of onbewezen rechterlijk oordeel toegevoegd. Dit is geen uitputtende rechtspraakdekking; externe garantieregelingen en een concrete uitvoeringsregeling voor waardering zijn niet als zelfstandig onderzocht gepresenteerd.

De [bouwpoging](sources/review-art-213aq-213md-build.txt) en [strikte validatie](sources/review-art-213aq-213md-validation.json) zijn uitgevoerd: 100% wettekstovereenkomst. De 259 ontbrekende toelichtingen buiten deze batch verhinderen volledige bouw en validatie. Daarom is het bestaande checkpoint met precies deze twintig plaatsen opnieuw samengesteld. Lange alinea's zijn niet identiek herhaald; een lengtecontrole bewijst geen juridische kwaliteit. Deze projectinterne tweede lezing is geen volledige boekreview of externe professionele goedkeuring.
'''
p=W/'REVIEW.md';s=p.read_text();assert 'Negentiende afgebakende' not in s;p.write_text(s.rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing 213aq–213md: [beoordeling](sources/'+P+'-result.json), [bronpreflight](sources/'+P+'-preflight-result.json), [selectief zoeklog](sources/'+P+'-search-log.json).\n')
parts=['# Artikelen 213aq–213md — beoordeeld checkpoint','Twintig toegewezen plaatsen van een onvoltooid commentaar. Wettekst: 1 september 2026. Projectinterne tweede lezing: 21 oktober 2026; vier toelichtingen gecorrigeerd of aangescherpt, zestien aanvaard. [Exacte beoordeling](sources/'+P+'-result.json). [Bronpreflight](sources/'+P+'-preflight-result.json). Tekst commentaar © 2026 Vojtěch Říha; Apache-2.0. Concept; geen externe professionele goedkeuring.']
for u in us:
 if u['id'] in ids:
  parts.extend(['### '+u['label'],'**Wettekst:**',quote(u['text'])]);parts.extend('*Redactionele bronnotitie:* '+n for n in u['notes']);parts.append(cs[u['id']])
(O/'27-art-213aq-213md-checkpoint.md').write_text('\n\n'.join(parts)+'\n')
p=O/'INDEX.md';p.write_text(p.read_text().replace('Auteurscheckpoint: artikelen 213aq–213md','Beoordeeld checkpoint: artikelen 213aq–213md'))
for n in ['REVIEW.md','SOURCES.md','preflight-result.json','status.json','review-result.json','review-checks.json']:shutil.copyfile(W/n,O/n)
for p in S.glob(P+'-*'):shutil.copyfile(p,O/'sources'/p.name)
shutil.copyfile(S/'verification.json',O/'sources/verification.json')
for p in W.glob('_review_213aq_213md_*.py'):shutil.copyfile(p,O/p.name)
checks=json.loads((W/'review-checks.json').read_text());broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',link):continue
  count+=1
  if not (p.parent/link.split('#')[0]).exists():broken.append([str(p.relative_to(O)),link])
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=[])
for p in [W/'review-checks.json',S/(P+'-checks.json'),O/'review-checks.json',O/'sources'/(P+'-checks.json')]:p.write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
j=json.loads((W/'source-manifest.json').read_text());j['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];j['scope']='Preserved source and review evidence through assigned articles213aq–213md; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reviewed':20,'corrected':4,'local_links_checked':count,'whole_book_complete':False}))
