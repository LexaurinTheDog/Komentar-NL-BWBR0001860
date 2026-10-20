from pathlib import Path
import json,subprocess,sys,shutil,hashlib,re,urllib.request
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
p=W/'sources/review-art-212hg-212l-historical.json';rec=json.loads(p.read_text());r=urllib.request.urlopen(rec['url'],timeout=30);b=r.read();assert hashlib.sha256(b).hexdigest()==rec['sha256'];hp=W/'sources/review-art-212hg-212l-historical.xml.headers';hp.write_text('HTTP status: '+str(r.status)+'\n'+str(r.headers));rec['headers_path']=str(hp.relative_to(W));p.write_text(json.dumps(rec,indent=2)+'\n')
review='''

## Vijftiende afgebakende tweede lezing — artikelen 212hg–212l

Op 21 oktober 2026 zijn exact twintig plaatsen inhoudelijk nagelezen: 212hg, 212hga, 212hgb, 212hgc, 212hgd*, 212hgd, 212hi–212hr en 212i–212l. [Exacte reviewed_ids en bevindingen per eenheid](sources/review-art-212hg-212l-result.json). Dertien toelichtingen zijn verbeterd, zeven zonder wijziging aanvaard. Alle leden, letters, bronnotities, voorbeelden en gebruikte interne verwijzingen zijn tegen de bron gelezen. Alle niet-toegewezen toelichtingen zijn hashgelijk gebleven. Deze review is een projectinterne tweede lezing, geen externe professionele goedkeuring of volledige boekreview.

Artikel 212hgb onderscheidt nu expliciet overgang en wijziging, de vier beschermde categorieën inclusief de beperkte cliëntverplichtingen uit derivatenvermogen, facultatieve uitsluiting van schadevergoeding, behandeling, horen, advies, duur en verlenging. Artikel 212hgc verduidelijkt dat andere bekendmaking bij niet-aangewezen dagbladen de Staatscourant niet overbodig maakt en bewaart het buitenlandse dienstverleningsaanknopingspunt. Artikel 212hgd* werkt alle publicatiegegevens, aantallen, talen en aanvullende buitenlandse gegevens uit. Artikel 212hgd zonder ster onderscheidt de wederzijdse informatie-/bijstandsplicht inclusief verkrijger van de dienstenplicht voor bank en groep ten behoeve van de overnemer.

De negen vervallen plaatsen 212hj–212hr zijn ieder rechtstreeks vergeleken met de [volledige officiële toestand van 1 januari 2018](sources/review-art-212hg-212l-historical.xml). Hun uiteenlopende oude onderwerpen zijn nu afzonderlijk verklaard: externe verwijzingen, planvoorbereiding, informatie/toegang, medewerking, goedkeuringsverzoek, behandeling/prijstoets, uitvoering, aanpassing en derdelandbijkantoren. De oude regels zijn uitsluitend historische uitleg. Het daadwerkelijk gelezen artikel XIV lid 4 van [Stb. 2018/489](sources/review-art-207-212hf-stb-2018-489.xml) behoudt oud recht voor de daar omschreven oudere verzekeraarsfaillissementen; dit is geen algemene herleving van vervallen bankartikelen. De huidige vervallen slots blijven afzonderlijke bronrecords.

De zeven andere toelichtingen zijn op hun eigen inhoud aanvaard: bijzondere summiere grondslag bij 212hg, toestemming derde bij 212hga, limitatieve uitvoerbaarheid en uitsluiting artikel 10 bij 212hi, vertegenwoordiging bij 212i, verschillende buitenlandse informatieplichten bij 212j, vergunningroute bij 212k en verval van eigen aangifte bij 212l. Voor 212k is artikel 1:104 lid 5 in de [opgeslagen officiële Wft-tekst](sources/author-art-212j-212l-wft.html) daadwerkelijk gelezen: ontwerp voor ECB tegenover eigen besluit, met de artikel 3:4-uitzondering. De wijzigingsdatum van 212l is bevestigd in de artikelmetadata. Geen externe Europese regeling is uit het geheugen aangevuld.

[Verse bronresponses](sources/review-art-212hg-212l-fetch.json) geven URL, werkelijke ophaaltijd, HTTP 200, SHA-256 en formaatcontrole. De huidige route vermeldt gelding vanaf 1 september 2026 tot heden. [Preflight](sources/review-art-212hg-212l-preflight-result.json) behoudt de beslissende auteursdatum 19 oktober 2026, controleert de WTI-dateringen, sluit historische en toekomstige teksten uit en vindt geen effectieve wijziging sinds intake. De twee 212hgd-identificaties zijn onderscheiden actuele XML-paden. De [opnieuw uitgevoerde parser en volledigheidscontrole](sources/review-art-212hg-212l-parser-check.json) reproduceren bytegelijk de bestaande producten: 639 unieke plaatsen, alle wettelijke tekst, verantwoorde aanhef/slot en geen operationele bijlage. Geen wettekst gewijzigd.

[Selectief rechtspraakonderzoek](sources/review-art-212hg-212l-search-log.json) leverde geen voldoende relevante geverifieerde volledige uitspraak op; daarom zijn geen holdings of casuskaarten verzonnen. Het lokale HR-corpus is doorzocht. Geen claim op uitputtende rechtspraakdekking of latere behandeling; externe Europese en effectenrechtelijke regimes zijn niet in hun geheel gecertificeerd.

De [volledige build](sources/review-art-212hg-212l-build.txt) is geprobeerd en weigert de 339 ontbrekende commentaren buiten deze batch. De [strikte validator](sources/review-art-212hg-212l-validation.json) bevestigt 100% wettekstovereenkomst en dezelfde onvolledigheid. De twintig toegewezen plaatsen hebben alle inhoudelijk commentaar; geen exact herhaalde lange alinea aangetroffen. De [batchcontroles](sources/review-art-212hg-212l-checks.json) leggen dit vast. De bestaande hoofdstukken en het afzonderlijke checkpoint 212j–212l zijn behouden en opnieuw geëxporteerd. Minimumlengte is geen bewijs van juridische kwaliteit. Het volledige boek blijft onvoltooid.
'''
p=W/'REVIEW.md';s=p.read_text();assert 'Vijftiende afgebakende' not in s;p.write_text(s.rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing 212hg–212l: [bevindingen](sources/review-art-212hg-212l-result.json), [bronpreflight](sources/review-art-212hg-212l-preflight-result.json), [historische officiële tekst](sources/review-art-212hg-212l-historical.xml), [onderzoekslog](sources/review-art-212hg-212l-search-log.json).\n')
# Rebuild completed chapters only after the full builder recorded the out-of-scope missing material.
r=subprocess.run([sys.executable,str(W/'_checkpoint.py')],capture_output=True,text=True);assert r.returncode==0,r.stderr
idx=O/'INDEX.md';s=idx.read_text().replace('van artikel 1 tot en met artikel 212i','van artikel 1 tot en met artikel 212l (inclusief het afzonderlijke checkpoint hieronder)');line='[Afzonderlijk checkpoint: artikelen 212j–212l](23-art-212j-212l-checkpoint.md).';idx.write_text(s+'\n'+line+'\n')
for p in W.glob('_review_212hg_212l_*.py'):shutil.copyfile(p,O/p.name)
broken=[];count=0
for p in list(O.glob('*.md'))+list((O/'cases').glob('*.md')):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',target):continue
  count+=1
  if not (p.parent/target.split('#')[0]).exists():broken.append([str(p.relative_to(O)),target])
assert not broken,broken
checks=json.loads((W/'review-checks.json').read_text());checks['output_local_links_checked']=count;checks['broken_output_local_links']=broken
for dest in [W/'review-checks.json',W/'sources/review-art-212hg-212l-checks.json',O/'review-checks.json',O/'sources/review-art-212hg-212l-checks.json']:dest.write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
manifest=json.loads((W/'source-manifest.json').read_text());manifest['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];manifest['scope']='Preserved sources and bounded review evidence through articles 212hg–212l; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reviewed':20,'corrected':13,'local_links_checked':count,'whole_book_complete':False}))
