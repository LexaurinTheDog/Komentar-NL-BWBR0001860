from pathlib import Path
import json,datetime,hashlib,xml.etree.ElementTree as E,re
W=Path(__file__).resolve().parent
keys=['2024-1382','2021-102','2026-400','2014-161']
context={
'2024-1382':('4 oktober 2024','24/00392','3.2 en 3.4','De curator was in drie lopende faillissementen ontslagen omdat hij van de rechtbanklijst was geschrapt. De Hoge Raad oordeelt dat horen of behoorlijke oproeping noodzakelijk is en dat lijstschrapping niet zonder meer ontslag rechtvaardigt: de reden moet kenbaar worden betrokken. Vernietiging en terugwijzing, geen definitief verbod op ontslag.','art-73 en art-85','De relevante hoorplicht van artikel 73 is ook in de huidige tekst aanwezig. De uitspraak is geen erkenning van een recht om op de rechtbanklijst te blijven.'),
'2021-102':('22 januari 2021','20/03587','3.2.1–3.6.2','In cassatie in het belang der wet beoordeelt de Hoge Raad de schorsing van faillissementsbewaring. De rechter moet bij bevel, verlenging en ontslagverzoek onderzoeken of schorsing volstaat. Zonder actuele bewaringsgrond past beëindiging. Tijdens schorsing loopt de dertigdagentermijn niet; wel moet een herbeoordelingstermijn worden gesteld. De betrokkene kan steeds opheffing of aanpassing verzoeken. Bewaring en schorsing vallen buiten artikel 85; hoger beroep en cassatie zijn mogelijk.','art-85, art-86, art-87 en art-88','De geciteerde overwegingen zijn eigen oordelen van de Hoge Raad, niet de geciteerde rechtbankmotivering onder 2.3. Vernietiging in het belang der wet zonder nadeel voor verkregen partijrechten. De huidige artikelen 87 en 88 behouden de relevante regels; voorwaarden vergen een eigen rechtmatige basis en evenredigheid.'),
'2026-400':('13 maart 2026','25/02800','3.2–3.5','De rechtbank had contact tijdens bewaring beperkt tot advocaten, curatoren en rechter-commissaris; het hof had die extra beperking vernietigd. De Hoge Raad verwerpt het daartegen in het belang der wet ingestelde beroep. Artikel 87 en andere wettelijke bepalingen bieden geen grondslag voor het aldus door de rechter opleggen van contactbeperkingen. Het nut voor medewerking maakt het ontbreken van een kenbare en voorzienbare wettelijke grondslag niet goed.','art-87','Het middel onder 3.1 stelde juist dat de bevoegdheid inherent was; dat is niet het oordeel van de Hoge Raad. De Hoge Raad betrekt ook de latere uitbreiding van informatie- en medewerkingsplichten. Dit oordeel maakt niet alle gewone detentieregels ongeldig en betreft geen schorsingsvoorwaarden.'),
'2014-161':('24 januari 2014','13/02780','3.5–3.8 en beslissing','De gefailleerde vroeg ontslag uit bewaring wegens het risico zichzelf door inlichtingen te belasten. De Hoge Raad aanvaardt dwang tot informatie voor de boedelafwikkeling, maar eist bij het niet uit te sluiten strafrechtelijk gebruik van deze wilsafhankelijke inlichtingen een effectieve waarborg. Hij voegt aan de afwijzing de gebruiksrestrictie voor faillissementsafwikkeling toe; de strafrechter beslist over gevolgen van schending.','art-88, met verwijzing vanuit art-87','De Hoge Raad gelastte geen onvoorwaardelijk ontslag. Zijn oordeel betreft de in die zaak verlangde wilsafhankelijke inlichtingen, niet ieder bestaand document. Artikel 105 is later uitgebreid; de informatieplicht wordt daarom ontleend aan de huidige wet, terwijl de uitspraak uitsluitend de dwang- en gebruikswaarborg ondersteunt. Geen claim dat alle latere strafrechtelijke bewijsrechtspraak is onderzocht.')
}
for k in keys:
 date,docket,paras,holding,units,limit=context[k];ec='ECLI:NL:HR:'+k.replace('-',':')
 text=f'''# HR {date} — {ec}

Hoge Raad, Civiele Kamer (in 2014: Eerste Kamer), zaak {docket}. [Officiële volledige beschikking](https://uitspraken.rechtspraak.nl/details?id={ec}). [Ruwe XML](../sources/review-art-73-89-hr-{k}.xml), [volledig leesextract](../sources/review-art-73-89-hr-{k}.txt), [lokale nationale corpusversie](../sources/review-art-73-89-hr-{k}-local.md). [HTTP- en hashregister](../sources/review-art-73-89-cases-fetch.json).

Relevante overwegingen: {paras}. {holding}

Ondersteunt {units}. {limit} Selectieve controle; geen uitputtende rechtspraakinventaris.
'''
 (W/f'cases/HR-{k}.md').write_text(text)
log={'searched_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'queries':['site.rechtspraak.nl faillissementsbewaring Hoge Raad 2013','site.rechtspraak.nl curator 73 ontslag Hoge Raad','site.rechtspraak.nl Hoge Raad 87 Fw proportionaliteit','site.rechtspraak.nl Hoge Raad 85 Fw cassatie'],'selected_full_decisions':['ECLI:NL:HR:'+k.replace('-',':') for k in keys],'method':'Official search results identify primary decisions; full official XML read separately, not snippets or PHR holdings. Local national corpus full texts compared.','local_corpus':'/Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr/','limitations':'Selective relevant research. No separately verified judgment found and used for the remaining technical committee/voting provisions. No exhaustive subsequent-case search.'}
(W/'sources/review-art-73-89-search-log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
# Reuse audited mechanical source checks, with this batch’s own substantive findings.
s=(W/'_review_60a_72_audit.py').read_text().replace('60a-72','73-89').replace('60a_72','73_89')
s=s.replace("['60a','60b','61','62','63','63a','63b','63c','63d','63e','64','65','66','67','68','68a','69','70','71','72']","['73','73a','74','75','75a','76','77','78','79','80','80a','81','82','83','84','85','86','87','88','89']")
s=s.replace("['2016-2997','2018-1799']",repr(keys))
notes={
'art-73':('1–2','Hoorplicht en concrete toets lijstschrapping toegevoegd met HR 2024; rekening aan opvolger, initiatiefnemers en 69-route aanvaard.',['art-65','art-69','art-85'],['ECLI:NL:HR:2024:1382']),
'art-73a':('1–3','Aanvaard: drie maanden, verlengbaarheid en kosteloze openbaarheid; a/c-rapportage versus vertrouwelijk b; persoonsgegevens en voorlopige verdenkingen correct.',['art-68','art-68a'],[]),
'art-74':('1–2','Aanvaard: facultatieve instelling, oneven aantal, belangrijke groepen en rechtbankvacature via dubbeltal; geen individueel zetelrecht.',['art-75','art-76','art-77','art-78','art-79'],[]),
'art-75':('1–3','Aanvaard: raadplegen na verificatie ook zonder voorlopige commissie, dadelijke benoeming bij wens vergadering, proces-verbaal en vacature door RC.',['art-74'],[]),
'art-75a':('1–2','Aanvaard: facultatief reglement bij instelling, passende bekendmaking en ontslag door bevoegde rechter; geen automatische personeelswissel of bevoegdheidswijziging.',['art-74','art-75','art-76','art-77','art-78','art-79'],[]),
'art-76':('ongesplitst','Aanvaard: tijdige toegang tot alle faillissementsinformatie en inlichtingen tegenover curator, geen publieke inzage door iedere schuldeiser; noodzakelijke gegevensverwerking.',['art-68a','art-73a'],[]),
'art-77':('ongesplitst','Aanvaard: curator organiseert, zit voor en voert pen; discretionair overleg heft verplichte adviesmomenten niet op.',['art-78','art-79'],[]),
'art-78':('1 inclusief volledige lijst; 2','Volledige verwijzingslijst en werkelijk in huidige bron opgenomen 73 lid 2 uitgewerkt. Procesrollen, verificatie-uitzondering, vereffening en uitdelingsmoment onderscheiden. Oproeping met bekwame termijn geen voorspelde weigering.',['art-37','art-39','art-40','art-58','art-72','art-73','art-79','art-100','art-101','art-175','art-177'],[]),
'art-79':('ongesplitst','Aanvaard: niet-bindend advies, onmiddellijke afwijkingsmelding, verklaring commissie en precies drie dagen opschorting; geen onbeperkt veto.',['art-72'],[]),
'art-80':('1–2','Aanvaard: RC voorzitter, curator aanwezig of vervanger met goedvinden, onderscheiden van vormkeuze.',['art-80a'],[]),
'art-80a':('ongesplitst','Aanvaard: RC kiest fysieke, schriftelijke of elektronische vorm; geen wijziging stemgewicht, vertegenwoordiging of oproepregels.',['art-81','art-82','art-83','art-84'],[]),
'art-81':('1–2','Aanvaard: volstrekte stemmenmeerderheid aanwezigen, elke 45 euro plus restantstem; 100 euro geeft 3 stemmen; latere splitsing schept geen extra stemrecht, bijzondere meerderheid voorbehouden.',['art-82','art-83'],[]),
'art-82':('ongesplitst','Aanvaard: erkend/voorwaardelijk/toonder, niet louter ingediend; betwiste aanspraak niet door stemtoelating definitief; houderschap en gewicht gescheiden.',['art-81','art-83'],[]),
'art-83':('1–2','Aanvaard: persoon/schriftelijk gemachtigde/advocaat; vervolgopepen naar gemachtigde tenzij schriftelijk gewijzigd; erkenning en gewicht niet door volmacht hersteld.',['art-81','art-82'],[]),
'art-84':('1–2','Stemgerechtigde geadresseerden en uur toegevoegd; beide verzoekdrempels behouden, precies een vijfde voldoende, schriftelijk minimaal tien dagen en agenda.',['art-80a','art-82','art-83'],[]),
'art-85':('ongesplitst','Vage rechtsmiddelreserve geconcretiseerd: cassatie bij ontslagcurator versus bewaring/schorsing geheel buiten beheer/vereffening, met HR-bronnen; geen uniforme termijn verzonnen.',['art-67','art-73','art-87','art-88'],['ECLI:NL:HR:2024:1382','ECLI:NL:HR:2021:102']),
'art-86':('ongesplitst','Op de minuut en categorietoets toegelicht; geen omzeiling vrijheidswaarborgen. Uitzondering 106b lid6 en checklist aanvaard.',['art-13','art-85','art-106b'],['ECLI:NL:HR:2021:102']),
'art-87':('1–4','Bewaringsplaatsen/toezicht en initiatiefregels verduidelijkt. Schorsing, stilstaande termijn, herbeoordeling en ontbrekende grond toegevoegd; HR 2026 contactverbod afgewogen tegen eigenlijke dictum, geen inherente extra beperking.',['art-88','art-105','art-105a'],['ECLI:NL:HR:2021:102','ECLI:NL:HR:2026:400']),
'art-88':('1–2','Zekerheidsdoel behouden; ontslag en schorsing gescheiden, verzoek tijdens schorsing en gebruiksrestrictie bij wilsafhankelijke informatie toegevoegd. Geen algemeen zwijgrecht of documentimmuniteit afgeleid.',['art-87','art-105'],['ECLI:NL:HR:2021:102','ECLI:NL:HR:2014:161']),
'art-89':('vervallen slot','Aanvaard: geen voortlevende grond of termijnverlenging; historische vermelding vraagt toenmalig recht.',['art-87','art-88'],[])
}
s=s[:s.index('notes={')]+'notes='+repr(notes)+'\n'+s[s.index('assert list(notes)==ids'):]
s=s.replace('Two selected full HR decisions independently fetched','Four selected full HR decisions independently fetched')
(W/'_review_73_89_audit.py').write_text(s)
