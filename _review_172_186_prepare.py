from pathlib import Path
import json
W=Path(__file__).resolve().parent
ids=['art-172','art-172a','art-173','art-173a','art-173b','art-173c','art-173d']+['art-'+str(n) for n in range(174,187)]
data=[
('ongesplitst','Beide leden171 bij nieuw faillissement, inhaalronde ook nieuwe crediteuren, geen terugvorderingsbevoegdheid.',['171']),
('ongesplitst','Overeenkomstige akkoordafdeling bij EU47lid1, geen nationale pauliana47; expliciete beperking zonder externe EU-certificering.',['5']),
('1–2','Van rechtswege insolventie versus betalingsonmacht, nadere verificatie en einde98/100 afhankelijk voortzetting.',['1','98','100','173a']),
('1–4','Initiatief curator/aanwezige crediteur, commissie- en curatoradvies, verplicht uitstel op verlangen max14dagen, kennisgeving afwezigen114.',['114','145','173b']),
('1–4','Meer dan helft bedragen volledige relevante noemer; geen aanwezigheidsnoemer, geen dubbele meerderheid;75procedure, proces-verbaal en8dageninzage.',['75','145','173d']),
('1–3','Acht dagen na definitieve weigering versus oproeping tien dagen voor zitting;80a-vorm,114 en adviezen173a2/stemming173b.',['80a','114','158','173a','173b']),
('ongesplitst','Acht dagen na vergadering, stukken zelf en correctie in beide richtingen; geen veranderde prognose.',['149','173b','174']),
('1–2','Staking op verzoek; verplichte commissie/curatorhoor versus discretionair overige crediteuren/schuldenaar;67uitzondering.',['67','175']),
('1–3','Onmiddellijke vereffening zonder toestemming schuldenaar; huisraadRC versus21; verkoop overtollige activa ook bij voortzetting.',['21','176']),
('1–2','Openbaar of toestemming onderhands; cumulatief2000 volgens boedelbeschrijving inclusief eerdere verkopen; incourante baten goedkeuring.',['101']),
('ongesplitst','Diensten gefailleerde tegen RC-vergoeding onderscheiden van wettelijke medewerking, opdracht en geen automatische arbeidsovereenkomst.',['105','105a']),
('ongesplitst','Facultatieve raadpleging na insolventie volgens80a, geen overdracht beheertaak of akkoordstemming.',['80a','145','173']),
('ongesplitst','Voldoende gerede middelen volgensRC; geverifieerden plus110lid3-beslissing; tussentijdse uitdeling en lijstprocedure.',['110','180','183']),
('1–2','Inhoud inclsalaris en110lid3; voorrang ook betwist, tekort/nietverkocht concurrent;181 onderscheiden van189 en190correctie.',['57','60','110','181','189','190']),
('ongesplitst','Volle bedrag voorwaardelijk toegelaten claim, geen directe betaling; voorbeeld gecorrigeerd: toelatingsstatus niet gelijk contractvoorwaarde.',['189']),
('1–2','Kostenomslag uitzonderingsbestemmingen volledig benoemd; hoger bevoorrechte crediteur wel omslag; zelfstandige luchtvaartuigverkoop.',['57','59a','60']),
('1–3','Tien dagen inzage, beide overlappende kennisgevingsleden behouden, bedrag en nieuwsbladverwijzing niet eigenmachtig gerepareerd.',['14','110','184']),
('1–2','Gemotiveerd bezwaar griffie binnen inzageperiode, bewijs en bijlage; erkenningsbeschikking67 niet opnieuw via184; HR3.4.2 onderscheiden3.4.3.',['67','183','185','187']),
('1–3','Openbare zitting max14dagen na inzage, griffiemededeling enRCrapport versus rechtbankbeslissing; HRkostenherstel3.5 onderscheiden erkenning.',['183','187']),
('vervallen','Slot behouden en geen huidig extra rechtsmiddel afgeleid; overgangsnotitie2018 behouden.',['184','185','187'])]
notes={k:(p,t,['art-'+r for r in refs],['ECLI:NL:HR:2017:2808'] if k in ['art-184','art-185'] else []) for k,(p,t,refs) in zip(ids,data)}
s=(W/'_review_153_171_audit.py').read_text().replace('153-171','172-186').replace('153_171','172_186')
a=s.index("ids=['art-");b=s.index('\nrecords=[]',a);s=s[:a]+'ids='+repr(ids)+s[b:]
a=s.index('notes={');b=s.index('\nassert list(notes)==ids',a);s=s[:a]+'notes='+repr(notes)+s[b:]
s=s.replace('Full HR2024:210 read and compared to preserved national corpus. Selective research; no exhaustive later-treatment check.','Full HR2017:2808 read and compared to preserved national corpus; the relevant articles67/184 remain operative. Selective research; no exhaustive later-treatment check.')
(W/'_review_172_186_audit.py').write_text(s)
(W/'cases/HR-2017-2808-uitdelingslijst.md').write_text('''# Hoge Raad 3 november 2017 — verzet en erkenningsbeslissing

ECLI:NL:HR:2017:2808; zaak 17/02858. Ondersteunt art-184 en art-185.

[Officiële uitspraak](https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:HR:2017:2808), [volledige XML](../sources/review-art-172-186-case-hr-2017-2808.xml), [leesversie](../sources/review-art-172-186-case-hr-2017-2808.txt), [HTTP, tijdstip en SHA-256](../sources/review-art-172-186-cases-fetch.json), [nationale corpusversie](../sources/review-art-172-186-hr-2017-2808-local.md).

De schuldeisers wilden via verzet de erkenning van een andere vordering corrigeren. De klacht dat zij die vordering eerder als schuldeiser hadden betwist staat in rov. 3.4.1; dit is hun standpunt. In rov. 3.4.2 oordeelt de Hoge Raad dat die feitelijke stelling niet eerst in cassatie kon worden aangevoerd. Aanvullend bepaalt rov. 3.4.3 dat de beslissing van de rechter-commissaris om een vordering op de erkende lijst te plaatsen een beschikking volgens artikel 67 lid 1 is. De betrokken schuldeiser had daartegen hoger beroep moeten instellen. In verzet volgens artikel 184 e.v. kan daarop niet worden teruggekomen.

Rov. 3.5 en het dictum verwerpen het beroep maar wijzen terug voor eventuele aanpassing van de algemene faillissementskosten op de lijst wegens de door cassatie veroorzaakte kosten. Dat beperkte herstel heropent de erkenningsvraag niet. De uitspraak sluit evenmin alle zelfstandige bezwaren tegen de verdeling uit. Historische rechtspraak die de Hoge Raad aanhaalt is niet afzonderlijk onderzocht of als zelfstandige autoriteit gebruikt.

De volledige tekst is gelezen en vergeleken met de nationale corpusversie; de dragende overwegingen komen overeen. De relevante erkennings- en verzetstructuur van artikelen 67 en 184 is in de geselecteerde tekst behouden. Latere wijzigingen van andere procedurele onderdelen en overgangsrecht maken deze beslissing geen zelfstandige bron voor alle huidige proceduretermijnen. Selectieve selectie, geen uitputtend onderzoek naar latere behandeling.
''')
(W/'sources/review-art-172-186-search-log.json').write_text(json.dumps({'queries':['site.rechtspraak.nl "182" "Faillissementswet" "Hoge Raad" omslag','site.rechtspraak.nl "184" "uitdelingslijst" "Hoge Raad"'],'full_decisions_read':['ECLI:NL:HR:2017:2808'],'local_corpus_read':'/Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr/ecli-nl-hr-2017-2808.md','snapshot':'sources/review-art-172-186-hr-2017-2808-local.md','not_used':'PHR opinions, estate-liquidation cases and commercial annotations not used as judgments; no additional sufficiently relevant verified authority added for other assigned units.','limitations':'Selective search; no exhaustive later-treatment review.'},indent=2)+'\n')
