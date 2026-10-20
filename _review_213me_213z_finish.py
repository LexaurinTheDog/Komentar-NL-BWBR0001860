from pathlib import Path
import sys,json,shutil,re,hashlib
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-213me-213z'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);r=json.loads((W/'review-result.json').read_text());ids=r['reviewed_ids'];cs=load_commentary(str(W));us=load_units(str(W))
review='''

## Twintigste afgebakende tweede lezing — artikelen 213me–213z, inclusief 213ij

Op 21 oktober 2026 zijn exact de twintig toegewezen artikelen inhoudelijk gelezen tegen alle leden en onderdelen van de officiële tekst. [Exacte reviewed_ids en bevindingen per artikel](sources/review-art-213me-213z-result.json). Bij artikel 213mf is het toepasselijke overgangsrecht expliciet gemaakt: XIV(4) van Stb. 2018/489 bewaart het eerdere recht voor faillissementen uitgesproken vóór inwerkingtreding van artikel IV. Bij 213s is een grammaticale fout hersteld. Bij 213ij is de uitsluiting van individuele executie uit de uitzondering toegevoegd. De zeventien andere commentaren zijn aanvaard. Alle niet-toegewezen commentaren zijn hashgelijk gebleven.

Voor de voorschotten zijn ontvangerskring, aanvraagverzuim, samenloop voor dezelfde schade, overbetaling, overnemer, goede trouw, wijzigingsbevoegdheid en rechtsmiddelen afzonderlijk gecontroleerd. De internationale bepalingen zijn gelezen op erkenning, werkingstijdstip, herkomstrecht en iedere bijzondere verwijzingsregel. Daarbij zijn goederenrechtelijke rechten van derden onderscheiden van rechten van de verzekeraar, koper van verkoper, schuld van tegenvordering, overeenkomst van beschikkingshandeling en lopend bodemgeding van executie. Voor artikel 213z zijn beide cumulatieve bewijsthema’s gecontroleerd. De officiële defecte richtlijnverwijzing in 213me is behouden en zichtbaar besproken; de editie verzint geen ondernemingsdrempels.

De [verse broncaptures](sources/review-art-213me-213z-fetch.json) bevatten URL, UTC-ophaaltijd, HTTP-resultaat, formaatcontrole en SHA-256. De actuele officiële route verklaart gelding vanaf 1 september 2026 tot heden. De [preflight](sources/review-art-213me-213z-preflight-result.json) onderscheidt die gelding van de raadpleegdatum, behoudt 19 oktober 2026 als auteursdatum en controleert het wijzigingsregister sinds intake. De wijziging van 15 november 2027 en ongedateerde voorstellen zijn uitgesloten. Historische XML-toestanden van 2002 en 2025 zijn afzonderlijk geteld en niet als huidige tekst ingevoegd. Wft 3:241 lid 4 is in de nieuwe officiële HTML gelezen; het bij artikel 213q uitgelegde aanknopingspunt klopt.

De [parsercontrole](sources/review-art-213me-213z-parser-check.json) vergelijkt onafhankelijk officiële XML-labels, HTML-inhoudsopgave en parserproducten: 639 unieke plaatsen, geen ontbrekende of dubbele identificaties. Iedere officiële artikeltekst is vergeleken. Parser en volledigheidsscript zijn opnieuw uitgevoerd met identieke hashes van de producten. De volledige XML bevat geen operationele bijlagen; aanhef, slot en structurele bronnotities blijven afzonderlijk verantwoord.

Het volledige arrest van het Hof van Justitie van 13 januari 2022, C-724/20, ECLI:EU:C:2022:9, is gelezen in de twee bewaarde officiële extracties (punten 1–68 en dictum); de officiële pagina is opnieuw geraadpleegd. De [zaakfiche](cases/eu-c-724-20-paget.md) ondersteunt 213ij. De in punten 63–66 aan de nationale rechter gelaten controle en de voorbehouden bevoegdheden van het liquidatierecht blijven essentieel. Rechtstreekse eerdere downloads waren leeg (HTTP 202) en blijven afgewezen. Het [selectieve zoeklog](sources/review-art-213me-213z-search-log.json) bewaart de herhaalde officiële en lokale zoekvragen; de historische lokale metadatahit is niet als relevante jurisprudentie gebruikt. Voor de overige negentien artikelen is geen voldoende relevante geverifieerde uitspraak toegevoegd. Dit is geen uitputtend rechtspraakonderzoek.

De [bouwpoging](sources/review-art-213me-213z-build.txt) en [strikte validatie](sources/review-art-213me-213z-validation.json) zijn uitgevoerd. De wettekstovereenkomst is 100%; 239 ontbrekende commentaren buiten deze batch verhinderen een volledige boekbouw en validatie. Het bestaande checkpoint is daarom met deze twintig gecontroleerde artikelen opnieuw samengesteld. De linkcontrole en controle op identiek herhaalde lange alinea’s slagen. Dit is een projectinterne afgebakende tweede lezing, geen volledige boekreview of externe professionele goedkeuring.
'''
p=W/'REVIEW.md';s=p.read_text();assert 'Twintigste afgebakende' not in s;p.write_text(s.rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing 213me–213z, inclusief 213ij: [beoordeling](sources/'+P+'-result.json), [bronpreflight](sources/'+P+'-preflight-result.json), [selectief zoeklog](sources/'+P+'-search-log.json).\n')
p=W/'cases/eu-c-724-20-paget.md';s=p.read_text().replace('toepassingscontrole bij onafhankelijk nazicht blijft nodig.','projectinterne tweede lezing op 21 oktober 2026 uitgevoerd voor artikel 213ij. Punten 45–47 sluiten individuele executie uit; punten 63–66 laten de daarin beschreven nationale controles aan de verwijzende rechter. De rechterlijke uitleg van artikel 292 sluit aan bij de huidige tekst van 213ij; geen latere wetsversie als historische norm ingevoegd. [Reviewbewijs](../sources/'+P+'-search-log.json).');p.write_text(s)
parts=['# Artikelen 213me–213z — beoordeeld checkpoint','Twintig toegewezen artikelen, inclusief 213ij, uit een onvoltooid commentaar. Wettekst: 1 september 2026. Projectinterne tweede lezing: 21 oktober 2026; drie commentaren aangescherpt of gecorrigeerd, zeventien aanvaard. [Exacte beoordeling](sources/'+P+'-result.json). [Bronpreflight](sources/'+P+'-preflight-result.json). Tekst commentaar © 2026 Vojtěch Říha; Apache-2.0. Concept; geen externe professionele goedkeuring.']
for u in us:
 if u['id'] in ids:
  parts.extend(['### '+u['label'],'**Wettekst:**',quote(u['text'])]);parts.extend('*Redactionele bronnotitie:* '+n for n in u['notes']);parts.append(cs[u['id']])
(O/'28-art-213me-213z-checkpoint.md').write_text('\n\n'.join(parts)+'\n')
p=O/'INDEX.md';p.write_text(p.read_text().replace('Auteurscheckpoint: artikelen 213me–213z','Beoordeeld checkpoint: artikelen 213me–213z'))
for n in ['REVIEW.md','SOURCES.md','preflight-result.json','status.json','review-result.json','review-checks.json','cases/eu-c-724-20-paget.md']:shutil.copyfile(W/n,O/n)
for p in S.glob(P+'-*'):shutil.copyfile(p,O/'sources'/p.name)
shutil.copyfile(S/'verification.json',O/'sources/verification.json')
for p in W.glob('_review_213me_213z_*.py'):shutil.copyfile(p,O/p.name)
checks=json.loads((W/'review-checks.json').read_text());broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',link):continue
  count+=1
  if not (p.parent/link.split('#')[0]).exists():broken.append([str(p.relative_to(O)),link])
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=[])
for p in [W/'review-checks.json',S/(P+'-checks.json'),O/'review-checks.json',O/'sources'/(P+'-checks.json')]:p.write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
j=json.loads((W/'source-manifest.json').read_text());j['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];j['scope']='Preserved evidence through bounded review213me–213z including213ij; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reviewed':20,'corrected':3,'local_links_checked':count,'whole_book_complete':False}))
