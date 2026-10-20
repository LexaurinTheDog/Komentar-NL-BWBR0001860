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

De XML bevat redactionele notities die als zodanig naast het citaat staan. Die zijn geen eigen commentaar en hun externe wetsverwijzingen zijn niet automatisch afzonderlijk als overgangsrecht geverifieerd. De twee [rechtspraakkaarten](cases/HR-2018-774.md) en [contractenkaart](cases/HR-2013-BY6108.md) bevatten precieze rechtsoverwegingen en toepassingsbeperkingen. Er is geen claim van uitputtende rechtspraakrecherche.

## Aanvullend bewijs: 20 oktober 2026

[Preflight-resultaat](preflight-result.json), [versiecontrole](sources/version-evidence.json) en [verse HTTP-captures](sources/preflight-2026-10-20-fetch.json) leggen de herhaalde broncontrole vast. De actuele route is vastgelegd als [volledige HTML](sources/preflight-2026-10-20-current.html), de geldigheidsinformatie als [informatie-HTML](sources/preflight-2026-10-20-information.html). Alle vier directe officiële verzoeken gaven HTTP 200. De XML is op root, wetidentificatie, datum en hash getoetst; een HTML-respons kan niet als XML worden geaccepteerd.

De [oorspronkelijke verificatie](sources/verification-2026-10-19.json) blijft behouden. De [niet-genummerde tekstinventaris](sources/non-article-text.json) verantwoordt ook het intitulé en de volledige aanhef en sluiting. De [structurele bronnotities](sources/structural-editorial-notes.json) zijn vanaf deze checkpoint zichtbaar in de uitvoer. Er zijn 460 artikelnotities en 21 structurele notities, samen 481; de XML bevat geen afzonderlijke `noot`-elementen.

Reproduceren zonder nieuwe netwerkverzoeken: `python3 -I _parse.py`, `python3 -I _coverage.py`, `python3 -I _preflight_audit.py`. De laatste stap toetst de bewaarde verse captures; de netwerkaanvragen zelf staan in `_preflight_fetch.py`. Voor de volledige boekbuild blijft het gedeelde bouwscript vereist zodra alle commentaren geschreven zijn.
