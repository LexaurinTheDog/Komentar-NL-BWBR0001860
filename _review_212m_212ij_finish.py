from pathlib import Path
import json,sys,subprocess,shutil,re,hashlib
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir']);prefix='review-art-212m-212ij'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
result=json.loads((W/'review-result.json').read_text());ids=result['reviewed_ids'];cs=load_commentary(str(W));us=load_units(str(W))
review='''

## Zestiende afgebakende tweede lezing — artikelen 212m–212ij

Op 21 oktober 2026 zijn exact twintig plaatsen inhoudelijk vergeleken met de officiële bron: 212m, 212ma, 212n, 212o, 212p, 212q, 212r, 212ra–212rf, 212s, 212t, 212u, 212v, 212w, 212x en 212ij. [Exacte reviewed_ids, leden en bevindingen per plaats](sources/review-art-212m-212ij-result.json). Zeven toelichtingen zijn gecorrigeerd, dertien zonder wijziging aanvaard. Alle toegewezen leden, letters, bronnotities, voorbeelden en gebruikte interne verwijzingen zijn gelezen. Niet-toegewezen commentaren zijn hashgelijk gebleven. Dit is een projectinterne tweede lezing, geen externe professionele goedkeuring of volledige boekreview.

De vervallen artikelen 212m en 212ma zijn afzonderlijk nagelezen in de [officiële historische toestand van 1 januari 2018](sources/review-art-212hg-212l-historical.xml). Hun eigen functies zijn nu concreet toegelicht: overgang uit de noodregeling met faillissementsgrond, beëindiging en zeven categorieën overgangsgevolgen bij 212m; aanvullende vangnetverwijzing in het andere faillissementsscenario bij 212ma. Beide blijven vervallen actuele slots. De verwijzing naar artikel XIV lid 4 van [Stb. 2018/489](sources/review-art-207-212hf-stb-2018-489.xml) is gecorrigeerd: dat lid betreft daar omschreven oudere verzekeraarsfaillissementen, geen algemeen behoud van oud bankrecht. Datzelfde onderscheid is bij 212o verwerkt; 212t en volgende zijn daar slechts een vergelijking met de uitzonderingssystematiek bij inkomende liquidaties.

Bij 212p is de onhandige wettelijke verwijzing naar een termijn in artikel 109 lid 1 niet stilzwijgend gerepareerd in de wettekst. Het commentaar onderscheidt nu de kennisgeving van artikel 109, de veertiendagentermijn en aanpassingsmogelijkheid van artikel 127 leden 1–2 en de consequentie uit lid 3. Bij 212rc en 212rd is artikel III van [Stb. 2022/105](sources/review-art-212m-212ij-stb-2022-105.xml) daadwerkelijk gelezen en de temporele grens verbonden aan het uitspreken van het faillissement vóór inwerkingtreding van artikel II. Bij 212re is artikel III leden 1–3 van [Stb. 2022/22](sources/review-art-212m-212ij-stb-2022-22.xml) gelezen: uitsluiting voor de aangeduide oudere geregistreerde obligaties, met aanvullende overgangscategorie tot en met 7 juli 2024. Alleen de nieuwe ingangsdatum noemen was onvoldoende. [Ophaalgegevens overgangswetten](sources/review-art-212m-212ij-transition-fetch.json).

De overige dertien toelichtingen zijn op hun eigen materie aanvaard: DNB-informatie bij 212n; taalfaciliteiten bij 212q; bewijs van onbekendheid bij betaling onder 212r; depositorang bij 212ra; bijzondere schuldinstrumentenrang en uitgiftemoment bij 212rb; vier afzonderlijke eigenvermogensregels bij 212rf; automatische erkenning en werkingstijdstip bij 212s; hoofdregel van toepasselijk recht bij 212t; beschermde goederenrechten en lokalisatie bij 212u; beide kooprichtingen bij 212v; recht op de vordering van de bank als verrekeningsaanknopingspunt bij 212w; behoud van benadelingsacties bij 212x; arbeidsverhoudingen en beperkte reikwijdte bij 212ij. De datums 25 maart 2026 bij 212ra en 8 juli 2022 bij 212re zijn tegen de officiële artikelmetadata gecontroleerd. De Europese kwalificatiecriteria zijn niet uit geheugen aangevuld of afzonderlijk integraal gecertificeerd.

De [verse officiële responses](sources/review-art-212m-212ij-fetch.json) hebben HTTP 200 en gevalideerde XML/HTML, met URL, werkelijke ophaaltijd en SHA-256. De actuele route vermeldt gelding van 1 september 2026 tot heden; de gecachte raadpleegdatum 20 oktober is onderscheiden van de ophaaltijd. De [preflight](sources/review-art-212m-212ij-preflight-result.json) bewaart de beslissende auteursdatum 19 oktober 2026, vergelijkt de WTI-wijzigingen, sluit historische en toekomstige toestanden uit en stelt geen effectieve wijziging sinds intake vast. De [opnieuw uitgevoerde parser en onafhankelijke volledigheidscontrole](sources/review-art-212m-212ij-parser-check.json) reproduceren bytegelijk de bestaande producten: 639 unieke actuele plaatsen, dezelfde identificaties uit XML en HTML-inhoudsopgave, verantwoorde aanhef en slot, geen operationele bijlagen. De onderscheiden actuele 212hgd-paden zijn geen historische doublure. Geen wettekst is gewijzigd.

[Selectieve officiële webzoekopdrachten en lokale HR-corpuszoekactie](sources/review-art-212m-212ij-search-log.json) leverden geen voldoende relevante geverifieerde volledige uitspraak op. Er is geen holding of casuskaart verzonnen en geen uitputtende rechtspraakdekking geclaimd. De [volledige build](sources/review-art-212m-212ij-build.txt) en [strikte validator](sources/review-art-212m-212ij-validation.json) zijn uitgevoerd: 100% wettekstovereenkomst, maar 319 ontbrekende commentaren buiten deze batch verhinderen een geslaagde volledige boekbouw. De twintig beoordeelde plaatsen hebben ieder inhoudelijk commentaar en geen exact herhaalde lange alinea. Minimumlengte is geen bewijs van juridische kwaliteit. [Batchcontroles](sources/review-art-212m-212ij-checks.json). Het bestaande auteurscheckpoint is met de correcties opnieuw opgebouwd; het volledige boek blijft onvoltooid.
'''
p=W/'REVIEW.md';s=p.read_text();assert 'Zestiende afgebakende' not in s;p.write_text(s.rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing 212m–212ij: [bevindingen](sources/review-art-212m-212ij-result.json), [bronpreflight](sources/review-art-212m-212ij-preflight-result.json), [overgangswetten](sources/review-art-212m-212ij-transition-fetch.json), [onderzoekslog](sources/review-art-212m-212ij-search-log.json).\n')
# The full builder has already recorded the absent out-of-scope commentary.
oldidx=(O/'INDEX.md').read_text();checkpoint_lines=[s for s in oldidx.splitlines() if s.startswith('[') and 'checkpoint.md)' in s]
r=subprocess.run([sys.executable,str(W/'_checkpoint.py')],capture_output=True,text=True);assert r.returncode==0,r.stderr
parts=['# Artikelen 212m–212ij — beoordeeld checkpoint','Twintig toegewezen eenheden van het onvoltooide commentaar. Wettekst: 1 september 2026. Projectinterne tweede lezing op 21 oktober 2026: zeven toelichtingen gecorrigeerd, dertien aanvaard. [Exacte beoordeling](sources/'+prefix+'-result.json). [Bronpreflight](sources/'+prefix+'-preflight-result.json). Tekst commentaar © 2026 Vojtěch Říha; Apache-2.0. Concept; geen externe professionele goedkeuring.']
for u in us:
 if u['id'] in ids:
  parts.extend(['### '+u['label'],'**Wettekst:**',quote(u['text'])]);parts.extend('*Redactionele bronnotitie:* '+n for n in u.get('notes',[]));parts.append(cs[u['id']])
(O/'23-art-212m-212ij-checkpoint.md').write_text('\n\n'.join(parts)+'\n')
idx=O/'INDEX.md';s=idx.read_text();s=re.sub(r'van artikel 1 tot en met artikel 212i','van artikel 1 tot en met artikel 212ij (inclusief de afzonderlijke checkpoints)',s)
for line in checkpoint_lines:
 if line not in s:s+='\n'+line+'\n'
idx.write_text(s)
for p in W.glob('_review_212m_212ij_*.py'):shutil.copyfile(p,O/p.name)
# Verify local evidence links and keep a reproducible inventory.
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',target):continue
  count+=1
  if not (p.parent/target.split('#')[0]).exists():broken.append([str(p.relative_to(O)),target])
assert not broken,broken
checks=json.loads((W/'review-checks.json').read_text());checks['output_local_links_checked']=count;checks['broken_output_local_links']=broken
for p in [W/'review-checks.json',W/f'sources/{prefix}-checks.json',O/'review-checks.json',O/f'sources/{prefix}-checks.json']:p.write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
manifest=json.loads((W/'source-manifest.json').read_text());manifest['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];manifest['scope']='Preserved sources and bounded review evidence through assigned articles 212m–212ij; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reviewed':20,'corrected':7,'local_links_checked':count,'whole_book_complete':False}))
