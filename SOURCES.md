# Bronnen en reproduceerbare controle

Controle- en redactiedatum: 19 oktober 2026. De volledige reikwijdte blijft BWBR0001860; de inhoudelijke checkpoint is nog onvoltooid.

| Bewijs | Betekenis |
|---|---|
| [Officiële toestand](sources/official-2026-09-01.xml) | HTTP 200, root `toestand`, BWBR0001860, inwerkingtreding 2026-09-01; enige geaccepteerde canonieke artikelbron |
| [Informatiepagina met HTML](sources/official-information.json.html) | Expliciet geraadpleegd op 19-10-2026, geldend vanaf 01-09-2026 tot heden; toekomstige en ongedateerde wijzigingen vermeld |
| [WTI](sources/wti.xml) | Dateringen van wijzigingen en toekomstige/ongedateerde records; geen samenvoeging met historische versies |
| [Verificatiemanifest](sources/verification.json) | URL, controletijd, HTTP-resultaat, SHA-256, verworpen responses en reden |
| [Oorspronkelijke intake](sources/intake-original.md) | Ongewijzigde kopie, oorspronkelijke intake blijft onaangeraakt |
| [Wijzigingskaart](sources/change-map.json) | Alle 639 artikelteksten gelijk na witruimtenormalisatie; twee bronrepresentaties bewaard |
| [Dekkingsbewijs](coverage-evidence.json) | Onafhankelijk uit officiële XML-labels afgeleide expected_ids naast parsed_ids, expliciete bijlageafwezigheid |
| [Volledigheidsrapport](completeness-report.json) | Ontbrekende/extra/dubbele identificaties, volgorde, vervallen plaatsen, structuur en volledige tekstcontrole |
| [Rechtspraakcontrole](sources/case-verification.json) | Officiële XML en nationale corpussnapshots, exacte hashes en tekstvergelijking |
| [Recherchespoor](sources/search-log.json) | Werkelijke zoekvragen, selectie en grenzen van het onderzoek |
| [Technische kwaliteitscontrole](quality-report.json) | Commentaardekking, herhaling en lokale linkcontrole; geen onafhankelijke juridische goedkeuring |

De mislukte route voor de exacte datum 19 oktober en de historische XML uit 2002 zijn geen bewijs van huidig recht. HTTP-succes alleen is niet als inhoudsvalidatie gebruikt. Een lege respons en een foutpagina zijn afgewezen. De huidige versie wordt gedragen door de geaccepteerde toestand en de uitdrukkelijke geldigheidsinformatie van de officiële website.

De XML bevat redactionele notities die als zodanig naast het citaat staan. Die zijn geen eigen commentaar en hun externe wetsverwijzingen zijn niet automatisch afzonderlijk als overgangsrecht geverifieerd. De [pluraliteitskaart](cases/HR-2018-774.md), [contractenkaart](cases/HR-2013-BY6108.md) en [cassatiekaart](cases/HR-2018-1100.md) bevatten precieze rechtsoverwegingen en toepassingsbeperkingen. Er is geen claim van uitputtende rechtspraakrecherche.

## Aanvullend bewijs: 20 oktober 2026

[Preflight-resultaat](preflight-result.json), [versiecontrole](sources/version-evidence.json) en [verse HTTP-captures](sources/preflight-2026-10-20-fetch.json) leggen de herhaalde broncontrole vast. De actuele route is vastgelegd als [volledige HTML](sources/preflight-2026-10-20-current.html), de geldigheidsinformatie als [informatie-HTML](sources/preflight-2026-10-20-information.html). Alle vier directe officiële verzoeken gaven HTTP 200. De XML is op root, wetidentificatie, datum en hash getoetst; een HTML-respons kan niet als XML worden geaccepteerd.

De [oorspronkelijke verificatie](sources/verification-2026-10-19.json) blijft behouden. De [niet-genummerde tekstinventaris](sources/non-article-text.json) verantwoordt ook het intitulé en de volledige aanhef en sluiting. De [structurele bronnotities](sources/structural-editorial-notes.json) zijn vanaf deze checkpoint zichtbaar in de uitvoer. Er zijn 460 artikelnotities en 21 structurele notities, samen 481; de XML bevat geen afzonderlijke `noot`-elementen.

Reproduceren zonder nieuwe netwerkverzoeken: `python3 -I _parse.py`, `python3 -I _coverage.py`, `python3 -I _preflight_audit.py`. De laatste stap toetst de bewaarde verse captures; de netwerkaanvragen zelf staan in `_preflight_fetch.py`. Voor de volledige boekbuild blijft het gedeelde bouwscript vereist zodra alle commentaren geschreven zijn.

## Bewijs van de afgebakende tweede lezing

[Eerder review-resultaat](sources/review-art-1-14b-result.json), [eerdere reproduceerbare controles](sources/review-art-1-14b-checks.json) en [HTTP-bronlog](sources/review-art-1-14b-fetch.json) behoren uitsluitend bij de twintig toegewezen plaatsen. De extra uitspraak van 6 juli 2018 is volledig bewaard en met het nationale corpus vergeleken. De officiële XML bevat ook de in het corpus ontbrekende partijcaption. `_review_audit.py` herhaalt bron- en integriteitschecks; de concrete juridische beoordelingen zijn afzonderlijk per eenheid genoteerd en worden niet door de scriptuitslag bewezen. Firecrawl had bij de hercontrole nul beschikbare credits; de bewijsstukken zijn rechtstreeks van de officiële servers opgehaald.

## Tweede batch: artikel 15–27

[Huidig review-resultaat](sources/review-art-15-27-result.json), [integriteitscontroles](sources/review-art-15-27-checks.json), [verse officiële bronnen](sources/review-art-15-27-fetch.json) en [rechtspraakvergelijking](sources/review-art-15-27-case-comparison.json) horen bij exact de twintig nieuwe plaatsen. De [oude toelichting](sources/review-art-15-27-commentary-before.txt) en hashes van alle 297 toen bestaande toelichtingen zijn bewaard; buiten deze opdracht is geen toelichting gewijzigd. Reproduceren: `python3 -I _review_15_27_audit.py`, na de ongewijzigde parser en volledigheidscontrole. Het eerdere script `_review_audit.py` hoort bij de vorige batch; voer dat niet over het actuele batchresultaat heen uit. De twee nieuwe zaakkaarten zijn [2007:BA5197](cases/HR-2007-BA5197.md) en [2017:2564](cases/HR-2017-2564.md). De [metadata-only respons](sources/review-art-15-27-first-fetch.json) is afgewezen. Rechtstreekse HTTP-ophaling verving de door onvoldoende Firecrawl-credits mislukte poging.

## Derde batch: artikel 28–40

[Actueel review-resultaat](sources/review-art-28-40-result.json), [integriteitscontrole](sources/review-art-28-40-checks.json), [bronpreflight](sources/review-art-28-40-preflight-result.json), [HTTP-captures](sources/review-art-28-40-fetch.json) en [volledige rechtspraakvergelijking](sources/review-art-28-40-case-comparison.json) betreffen exact deze twintig plaatsen. De [oorspronkelijke toelichtingen](sources/review-art-28-40-commentary-before.txt) en [hashes van alle bestaande commentaren](sources/review-art-28-40-before-hashes.json) zijn behouden. Vier nieuwe zaakkaarten zijn in REVIEW gekoppeld. Bronnen zijn direct van officiële servers gehaald, omdat Firecrawl nul credits meldde. Reproduceren zonder netwerk: `python3 -I _parse.py`, `python3 -I _coverage.py`, `python3 -I _review_28_40_audit.py`. Alleen dit laatste reviewscript correspondeert met de huidige beperkte scope; eerdere scripts blijven als historisch bewijs bewaard. De canonieke bron en alle wettelijke artikelteksten zijn ongewijzigd.

## Vierde batch: de twintig toegewezen plaatsen artikel 41–60

[Review-resultaat](review-result.json), [controlebewijzen](review-checks.json), [volledige preflight](sources/review-art-41-60-preflight-result.json), [verse wetscaptures](sources/review-art-41-60-fetch.json), [vier eerste HR-captures](sources/review-art-41-60-cases-fetch.json), [arrest uit 2026](sources/review-art-41-60-latest-case-fetch.json) en [beperkte externe BW-controle](sources/review-art-41-60-external-fetch.json). Alle geslaagde bronverzoeken hebben HTTP-status, exact toegangstijdstip, ruwe body, formaatvalidatie en SHA-256. De huidige BWB-route bevestigt op 20 oktober 2026 geldigheid vanaf 1 september 2026 tot heden; de WTI bevestigt de wijzigingsselectie voor de ongewijzigde beslissende datum 19 oktober.

De vijf volledige rechterlijke teksten zijn vergeleken met het lokale nationale corpus. Alle corpuslichamen zijn na witruimtenormalisatie gelijk aan het slot van de volledige officiële uitspraak; de officiële captions zijn aanvullend behouden. Zie [vergelijkingsbewijs](sources/review-art-41-60-case-comparison.json), de afzonderlijke zaakkaarten en de aangevulde [zoeklog](sources/search-log.json). Firecrawl meldde nul credits; directe officiële HTTP-ophaling is gebruikt. Een eerste externe BW-route met een willekeurige datum leverde 404 op en is niet als wetsbron gebruikt; de actuele route leverde de expliciet geldende versie. Een lokaal niet-beschikbare HTML-bibliotheek is niet geïnstalleerd; de bewaarde officiële HTML en de betreffende leden zijn rechtstreeks gelezen.

Reproduceren zonder netwerk: `python3 -I _parse.py`, `python3 -I _coverage.py`, `python3 -I _review_41_60_audit.py`. De nieuwe audit toetst integriteit en registreert de afzonderlijk gemaakte inhoudelijke beoordelingen; zij verricht geen zelfstandige juridische goedkeuring. Eerdere audits blijven historische bewijsstukken en schrijven bij uitvoering hun eigen oude scope. [Voorafgaande commentaren](sources/review-art-41-60-commentary-before.txt) en [alle eerdere commentaarhashes](sources/review-art-41-60-before-hashes.json) bewijzen de beperkte wijzigingsscope. De twaalf gewijzigde toelichtingen bevinden zich uitsluitend in deze reviewopdracht.


## Afgebakende tweede lezing: 60a–72

[Verse officiële bronopvraging](sources/review-art-60a-72-fetch.json), [preflight](sources/review-art-60a-72-preflight-result.json), [volledige zaakbronnen](sources/review-art-60a-72-cases-fetch.json) en [vergelijking nationaal corpus](sources/review-art-60a-72-case-comparison.json). Twee selectieve zaakkaarten: [HR 2016:2997](cases/HR-2016-2997.md), [HR 2018:1799](cases/HR-2018-1799.md). [Zoeklog](sources/review-art-60a-72-search-log.json).

Aanvullende tweede lezing artikelen 73–89: [actuele broncontrole](sources/review-art-73-89-preflight-result.json), [zoeklog](sources/review-art-73-89-search-log.json), [officiële zaakresponses](sources/review-art-73-89-cases-fetch.json), [vergelijking nationaal corpus](sources/review-art-73-89-case-comparison.json), [bevindingen](sources/review-art-73-89-result.json). De vier nieuwe zaaknotities behandelen [curatorontslag](cases/HR-2024-1382.md), [schorsing bewaring](cases/HR-2021-102.md), [extra contactbeperkingen](cases/HR-2026-400.md) en [zelfbelastende inlichtingen](cases/HR-2014-161.md). Selectieve primaire rechtspraak, geen commerciële annotaties.

Tweede lezing artikelen 90–106: [broncontrole](sources/review-art-90-106-preflight-result.json), [bevindingen per artikel](sources/review-art-90-106-result.json), [hercontrole primaire rechtspraak](sources/review-art-90-106-cases-fetch.json). De bestaande zaaknotities voor HR 2014:161 en HR 2026:400 zijn opnieuw getoetst.

Tweede lezing artikelen 106a–120: [broncontrole](sources/review-art-106a-120-preflight-result.json), [bevindingen](sources/review-art-106a-120-result.json), [primaire rechtspraak](cases/RBOVE-2020-1557.md) en [onderzoekslog](sources/review-art-106a-120-search-log.json).

Tweede lezing artikelen 121–137b: [broncontrole](sources/review-art-121-137b-preflight-result.json), [bevindingen](sources/review-art-121-137b-result.json), [primaire rechtspraak](cases/HR-2014-3464-verificatie.md) en [onderzoekslog](sources/review-art-121-137b-search-log.json).

Tweede lezing artikelen 137c–152: [broncontrole](sources/review-art-137c-152-preflight-result.json), [bevindingen](sources/review-art-137c-152-result.json), [onderzoekslog](sources/review-art-137c-152-search-log.json), [HR 2024:210](cases/HR-2024-210-akkoord-reikwijdte.md) en [Rb. Gelderland 2015:5785](cases/RBGEL-2015-5785-akkoordstemming.md).

Tweede lezing artikelen 153–171: [broncontrole](sources/review-art-153-171-preflight-result.json), [bevindingen](sources/review-art-153-171-result.json), [onderzoekslog](sources/review-art-153-171-search-log.json), [HR 2024:210](cases/HR-2024-210-akkoord-reikwijdte.md).

Tweede lezing artikelen 172–186: [broncontrole](sources/review-art-172-186-preflight-result.json), [bevindingen](sources/review-art-172-186-result.json), [onderzoekslog](sources/review-art-172-186-search-log.json), [HR 2017:2808](cases/HR-2017-2808-uitdelingslijst.md).

Tweede lezing artikelen 187–206: [broncontrole](sources/review-art-187-206-preflight-result.json), [bevindingen](sources/review-art-187-206-result.json), [onderzoekslog](sources/review-art-187-206-search-log.json), [HR 2014:1630](cases/HR-2014-1630-buitenlands-verhaal.md), [HR 2016:759](cases/HR-2016-759-verificatietitel.md).

Tweede lezing artikelen 207–212hf: [broncontrole](sources/review-art-207-212hf-preflight-result.json), [bevindingen](sources/review-art-207-212hf-result.json), [overgangsbronnen](sources/review-art-207-212hf-transitional-fetch.json), [onderzoekslog](sources/review-art-207-212hf-search-log.json), [Rotterdam](cases/RBROT-2020-1792-rehabilitatie.md), [Almelo](cases/RBALM-1999-AA3942-rehabilitatie.md).

Tweede lezing 212hg–212l: [bevindingen](sources/review-art-212hg-212l-result.json), [bronpreflight](sources/review-art-212hg-212l-preflight-result.json), [historische officiële tekst](sources/review-art-212hg-212l-historical.xml), [onderzoekslog](sources/review-art-212hg-212l-search-log.json).

Tweede lezing 212m–212ij: [bevindingen](sources/review-art-212m-212ij-result.json), [bronpreflight](sources/review-art-212m-212ij-preflight-result.json), [overgangswetten](sources/review-art-212m-212ij-transition-fetch.json), [onderzoekslog](sources/review-art-212m-212ij-search-log.json).

Tweede lezing 212z–213a: [beoordeling](sources/review-art-212z-213a-result.json), [bronpreflight](sources/review-art-212z-213a-preflight-result.json), [onderzoekslog](sources/review-art-212z-213a-search-log.json).

Tweede lezing213abis–213ap: [beoordeling](sources/review-art-213abis-213ap-result.json), [bronpreflight](sources/review-art-213abis-213ap-preflight-result.json), [volledige uitspraakcontrole](sources/review-art-213abis-213ap-case-check.json).

Tweede lezing 213aq–213md: [beoordeling](sources/review-art-213aq-213md-result.json), [bronpreflight](sources/review-art-213aq-213md-preflight-result.json), [selectief zoeklog](sources/review-art-213aq-213md-search-log.json).


Auteursbatch 213me–213z (inclusief 213ij), 21 oktober 2026: twintig specifieke toelichtingen met voorbeelden en checklists; [bronpreflight](sources/author-art-213me-213z-preflight-result.json), [onafhankelijke identificatievergelijking](sources/author-art-213me-213z-coverage.json), [selectief rechtspraakonderzoek](sources/author-art-213me-213z-search-log.json), [zaakfiche C-724/20](cases/eu-c-724-20-paget.md). De volledige wet blijft buiten deze batch onvoltooid. Dit auteurscheckpoint is nog niet onafhankelijk nagelezen.

Tweede lezing 213me–213z, inclusief 213ij: [beoordeling](sources/review-art-213me-213z-result.json), [bronpreflight](sources/review-art-213me-213z-preflight-result.json), [selectief zoeklog](sources/review-art-213me-213z-search-log.json).


Auteursbatch 213aa–214: twintig specifieke toelichtingen; [broncontrole](sources/author-art-213aa-214-preflight-result.json), [dekking](sources/author-art-213aa-214-coverage.json), [selectief rechtspraakonderzoek](sources/author-art-213aa-214-search-log.json). Geen rechterlijke uitspraak aangehaald in deze batch. Onafhankelijke tweede lezing nog niet uitgevoerd; overige bepalingen vallen buiten deze opdracht.

Tweede lezing 213aa–214: [beoordeling](sources/review-art-213aa-214-result.json), [bronpreflight](sources/review-art-213aa-214-preflight-result.json), [selectief zoeklog](sources/review-art-213aa-214-search-log.json).


Auteursbatch 215–228: twintig specifieke toelichtingen; [broncontrole](sources/author-art-215-228-preflight-result.json), [dekking](sources/author-art-215-228-coverage.json), [selectief rechtspraakonderzoek](sources/author-art-215-228-search-log.json). Twee volledige Hoge Raad-uitspraken selectief verwerkt; zie de bronkaarten. Onafhankelijke tweede lezing nog niet uitgevoerd; overige bepalingen vallen buiten deze opdracht.

Tweede lezing 215–228: [resultaat](sources/review-art-215-228-result.json), [preflight](sources/review-art-215-228-preflight-result.json), [selectief onderzoekslog](sources/review-art-215-228-search-log.json).
