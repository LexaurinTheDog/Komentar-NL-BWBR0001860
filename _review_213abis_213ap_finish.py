from pathlib import Path
import sys,json,shutil,re,hashlib
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-213abis-213ap'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);r=json.loads((W/'review-result.json').read_text());ids=r['reviewed_ids'];cs=load_commentary(str(W));us=load_units(str(W))
review='''

## Achttiende afgebakende tweede lezing — artikelen 213abis–213ap

Op 21 oktober 2026 zijn exact twintig toegewezen plaatsen gecontroleerd: 213abis, 213ab–213ad, 213ad1, 213ae–213ag, 213aga–213agc en 213ah–213ap. Alle leden, bronnotities, voorbeelden en gebruikte verwijzingen zijn gelezen tegen de officiële tekst. [Exacte reviewed_ids en bevindingen per plaats](sources/review-art-213abis-213ap-result.json). Bij 213ag is het onderwerp van de beschikking expliciet toegevoegd aan de vereiste aanvullende bekendmakingsgegevens. Bij 213agb is verduidelijkt dat de wijzigingsmachtiging ook tegelijk met het faillissement kan worden verleend. De overige achttien plaatsen zijn zonder tekstwijziging aanvaard. Niet-toegewezen commentaren zijn hashgelijk gebleven. Deze projectinterne tweede lezing betreft uitsluitend deze batch; zij is geen volledige boekreview of externe professionele goedkeuring.

De bijzondere aanvraaggronden, eigen aangifte, vergunninghistorie, inzagebevoegdheid, besloten spoedbehandeling en redelijkheidstoets zijn afzonderlijk beoordeeld. Voor portefeuilleoverdracht zijn de machtiging, wijziging, instemming van de verkrijger, levensverzekeringsgrens, geldigheidsduur en tijdige verlenging onderscheiden van DNB-advies, transactietoestemming en bekendmaking. De huidige Wft-tekst van artikel 3A:85 bevestigt dat 213abis uitsluitend naar lid1, onderdelen a en b verwijst; onderdeel c is geen extra faillissementsvoorwaarde. De vervallen plaatsen zijn als expliciete actuele slots behouden. Artikel XIV(4) van Stb.2018/489 is daadwerkelijk gelezen; historische faillissementen kunnen onder oud recht blijven. CIX van Stb.2016/290 is voor de bronnoot bij213ae gecontroleerd. De wijzigingswet Stb.2023/306, artikelIII C–E, bevestigt de intrekking van213ad, toevoeging van213aga leden3–5 en schrapping van213agb lid6.

[Verse broncaptures](sources/review-art-213abis-213ap-fetch.json) bevatten werkelijke UTC-ophaaltijd, HTTP200, URL, formaatcontrole en SHA-256. De ophaaltijd valt op20 oktober UTC en21 oktober lokale tijd; de getoonde raadpleegdatum is daarvan onderscheiden. De actuele route bevestigt gelding vanaf1 september2026 tot heden. De [preflight](sources/review-art-213abis-213ap-preflight-result.json) bewaart de auteursdatum19 oktober2026, controleert WTI op wijzigingen sinds intake, sluit toekomstige toestanden uit en houdt historische versies apart. De [parsercontrole](sources/review-art-213abis-213ap-parser-check.json) vergelijkt onafhankelijk de639 unieke XML-identificaties met HTML-inhoudsopgave en parserproducten. De parser en volledigheidscontrole zijn opnieuw bytegelijk uitgevoerd; aanhef en slot zijn verantwoord en de volledige XML bevat geen operationele bijlagen.

De volledige uitspraak ECLI:NL:RBAMS:2022:7475 is opnieuw opgehaald, als XML gevalideerd en van1.1 tot6.2 gelezen; zie [controlebewijs](sources/review-art-213abis-213ap-case-check.json) en de behouden [zaakkaart](cases/rbams-2022-7475.md). De procesgang en toestemming in het advies van de rechters-commissarissen zijn onderscheiden van het eigen oordeel in5.2–5.6 en de waarderingsopvatting van DNB in3.1. De85% is een dossierfeit, geen wettelijke grens. De uitspraak beslist niet over verlenging en bewijst niet de toepassing van de later toegevoegde leden van213aga. De inhoud van de niet meegeleverde bijlage8 is niet zelfstandig als geverifieerd behandeld. Het bestaande selectieve onderzoekslog blijft behouden; er wordt geen uitputtend rechtspraakonderzoek geclaimd.

De [volledige bouwpoging](sources/review-art-213abis-213ap-build.txt) en [strikte validatie](sources/review-art-213abis-213ap-validation.json) zijn uitgevoerd:100% wettekstovereenkomst. De279 ontbrekende commentaren buiten de batch verhinderen volledige bouw/validatie. Alle twintig toegewezen plaatsen hebben inhoudelijk commentaar; lange alinea’s zijn niet identiek herhaald. Lengte is geen bewijs van juridische kwaliteit. Het afzonderlijke checkpoint is opnieuw samengesteld en lokaal vastgelegd; het gehele boek blijft onvoltooid.
'''
p=W/'REVIEW.md';s=p.read_text();assert 'Achttiende afgebakende' not in s;p.write_text(s.rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing213abis–213ap: [beoordeling](sources/'+P+'-result.json), [bronpreflight](sources/'+P+'-preflight-result.json), [volledige uitspraakcontrole](sources/'+P+'-case-check.json).\n')
parts=['# Artikelen 213abis–213ap — beoordeeld checkpoint','Twintig toegewezen eenheden van een onvoltooid commentaar. Wettekst:1 september2026. Projectinterne tweede lezing:21 oktober2026; twee commentaren aangevuld, achttien aanvaard. [Exacte beoordeling](sources/'+P+'-result.json). [Bronpreflight](sources/'+P+'-preflight-result.json). Tekst commentaar ©2026 Vojtěch Říha; Apache-2.0. Concept; geen externe professionele goedkeuring.']
for u in us:
 if u['id'] in ids:
  parts.extend(['### '+u['label'],'**Wettekst:**',quote(u['text'])]);parts.extend('*Redactionele bronnotitie:* '+n for n in u['notes']);parts.append(cs[u['id']])
(O/'26-art-213abis-213ap-checkpoint.md').write_text('\n\n'.join(parts)+'\n')
p=O/'INDEX.md';s=p.read_text().replace('Auteurscheckpoint: artikelen 213abis–213ap','Beoordeeld checkpoint: artikelen 213abis–213ap');p.write_text(s)
# Preserve existing exports; replace only the reviewed checkpoint and supporting metadata.
for n in ['REVIEW.md','SOURCES.md','preflight-result.json','status.json','review-result.json','review-checks.json']:
 shutil.copyfile(W/n,O/n)
for p in S.glob(P+'-*'):shutil.copyfile(p,O/'sources'/p.name)
shutil.copyfile(S/'verification.json',O/'sources/verification.json')
for p in W.glob('_review_213abis_213ap_*.py'):shutil.copyfile(p,O/p.name)
checks=json.loads((W/'review-checks.json').read_text());broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',link):continue
  count+=1
  if not (p.parent/link.split('#')[0]).exists():broken.append([str(p.relative_to(O)),link])
assert not broken,broken
checks.update(output_local_links_checked=count,broken_output_local_links=[])
for p in [W/'review-checks.json',S/(P+'-checks.json'),O/'review-checks.json',O/'sources'/(P+'-checks.json')]:p.write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
j=json.loads((W/'source-manifest.json').read_text());j['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];j['scope']='Preserved source and review evidence through assigned articles213abis–213ap; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reviewed':20,'corrected':2,'local_links_checked':count,'whole_book_complete':False}))
