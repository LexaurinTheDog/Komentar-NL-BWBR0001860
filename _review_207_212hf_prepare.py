from pathlib import Path
import json
W=Path(__file__).resolve().parent
ids=['art-'+str(n) for n in range(207,213)]+['art-212'+s for s in ['a','b','c','d','e','f','g','h','ha','hb','hc','hd','he','hf']]
data=[
('ongesplitst','Alle erkende crediteuren; bewijs bij verzoek, niet alleen akkoordnakoming; RBROT2020:1792 rov4.1 gelezen en toegevoegd.',['206','209'],['ECLI:NL:RBROT:2020:1792']),
('ongesplitst','Staatscourant versus aanvraagbeslissing; historische dagbladplicht in Almelo1999 niet actueel overgenomen.',['209','210','212'],['ECLI:NL:RBALM:1999:AA3942']),
('1–2','Erkende crediteur, gemotiveerd bezwaarschrift, ontvangstbewijs, twee maanden en uitsluitend207-grond; geen algemene heropening.',['207','208'],[]),
('ongesplitst','Wachten termijn ook zonder verzet; conclusie OM versus eigen rechterlijke beoordeling; Almelo positief praktijkgeval zonder bewijsvermoeden.',['207','209','211'],['ECLI:NL:RBALM:1999:AA3942']),
('ongesplitst','Expliciet hogerberoep- en cassatieverbod alleen voor deze beslissing; geen onbewezen doorbrekingsleer ingevoegd.',['210'],[]),
('ongesplitst','Openbare toewijzing en centraal register bevestigd tegen19/19a; geen foutieve terugkeer naar oude lokale registratie; checklist specifiek.',['19','19a','207','208'],[]),
('a–p; a1/2,b1–3,j1/2','Alle rollen en opdrachten onderscheiden; b3eigen minimum/exclusies; werkdag dag/nacht; bereik11AA; overgangIII2025/363 geverifieerd.',['212b','212d'],[]),
('1–6','Minuutwerking; afkoelingbevoegdheden/goederen; lid3niet-tegenwerpelijkheid, werkdag en exploitantkennis bij onherroepelijkheid; lid4alleen1/3; interoperabiliteit en overgang.',['23','24','35','53','54','63a','212a'],[]),
('1–3','Onverwijlde griffier/DNB/autoriteitenketen; gegevensregels derde land; geen automatische verschuiving werking; overgang geverifieerd.',['212a','212b','212d'],[]),
('1–8;1a/b,2a/b','Verschillende uitsluitingslijsten1/2 en clearing/uitvoering niet gelijkgesteld; systeemovereenkomst3; voorschriften4; exploitant5; letterlijke publicatieverwijzing6; aanmelding7; instelling8; overgang.',['212a'],[]),
('ongesplitst','Systeemgebonden conflictenregel, niet alle schulden of goederen; buitenlandse uitkomst niet uit Fw alleen afgeleid.',['212a','212b'],[]),
('vervallen','Actuele lege plaats; eigen2002effectenzekerheden-conflictenregel alleen historisch toegevoegd; checklist behouden.',['212a','212e'],[]),
('1a–u; f1/2;2a/b','Alle categorieën en instrumentverwijzingen onderscheiden; deposito-overeenkomst; gegarandeerd versus in aanmerking komend; lid1bereik11AB versus lid2dezeafdeling; brontypografie bewaard.',['212h'],[]),
('1–3;3a/b','Amsterdam, verbod elders vergunde lidstaatbank; onvergunde lidstaat en derdeland bijkantoor; EER niet vergeten.',['2','212g'],[]),
('1–4;4a/b','DNB/SRB-oordeel versus DNB-verzoek; uitsluiting anderen; eigen aangifte en onverwijlde meldingen; zeven dagen vanaf DAGTEKENING, alternatieve DNB-mededeling niet cumulatief.',['1','212g','212h','212hg'],[]),
('ongesplitst','Nederlandse zetel, ontbrekende genoemde vergunning, gezamenlijke schuldeisers en bijzondere voorziening; geen automatische faillietgrond; uitvoerbaarheid212hi gecontroleerd.',['212ha','212hi'],[]),
('vervallen','Geen actuele aanvraaggrond; XIVlid4van2018/489daadwerkelijk gelezen: verzekeraars overgang, herleeft bankplaats niet.',[],[]),
('ongesplitst','Afschrift bank versus inhoud autoriteiten; diensten vanuit vestigingen andere lidstaat precies overgenomen; aanvraag versus publicatie.',['212ha','212hf','212hgd*'],[]),
('ongesplitst','Meeste spoed, besloten behandeling en subsidiair burgerlijk proces; afstemming/wachtvoorwaarde blijft; openbare uitspraak elders gecontroleerd.',['212ha','212hf','212hgd*'],[]),
('1–2','Hoorgelegenheid en redelijkheidstoets voor DNB-oordeel a/b, geen automatische toets c of ieder Europees oordeel; relatie summier212hg.',['212ha','212hg'],[])
]
notes={k:(p,t,['art-'+r for r in refs],cases) for k,(p,t,refs,cases) in zip(ids,data)}
s=(W/'_review_187_206_audit.py').read_text().replace('187-206','207-212hf').replace('187_206','207_212hf')
a=s.index('ids=');b=s.index('\nrecords=[]',a);s=s[:a]+'ids='+repr(ids)+s[b:]
s=s.replace("['fetch','cases-fetch']","['fetch','cases-fetch','transitional-fetch']")
a=s.index('notes={');b=s.index('\nassert list(notes)==ids',a);s=s[:a]+'notes='+repr(notes)+s[b:]
s=s.replace('Full HR2014:1630 and HR2016:759 read and compared to national corpus. HR2016:202 read but rejected as substantive authority: article81 rejection without own explanation, not an adoption of the PHR inadmissibility conclusion. Relevant Fw provisions196/197/203 retain their operative wording. The old EU regulation1346/2000 discussed in 2014 is not presented as current EU law. Selective research; no exhaustive later-treatment check.','Full RBROT2020:1792 and RBALM1999:AA3942 read. Historical article208 required additional newspaper publication, current article208 does not. National local corpus contains only higher courts and no lower-court matching decision was found. Selective research, no exhaustive later-treatment check.')
(W/'_review_207_212hf_audit.py').write_text(s)
# Case cards preserve own holdings rather than parties allegations.
(W/'cases/RBROT-2020-1792-rehabilitatie.md').write_text('''# Rechtbank Rotterdam 21 februari 2020 — bewijs bij rehabilitatie

ECLI:NL:RBROT:2020:1792. Het officiële stuk vermeldt als insolventienummer uitsluitend [nummer]; geen kenmerk aangevuld. Ondersteunt art-207.

[Officiële uitspraak](https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:RBROT:2020:1792) · [volledige XML](../sources/review-art-207-212hf-case-rbrot-2020-1792.xml) · [leesversie](../sources/review-art-207-212hf-case-rbrot-2020-1792.txt) · [HTTP en hashes](../sources/review-art-207-212hf-cases-fetch.json).

Rov. 3.1 beschrijft het verzoekersstandpunt; rov. 4.1 bevat het oordeel. Een gehomologeerd en uitgevoerd akkoord plus de concrete curatorverklaring bewezen niet dat iedere erkende schuldeiser naar genoegen was voldaan. Nominaal volledige betaling was volgens de rechtbank evenmin vereist. Zij noemt individuele verklaringen als voorbeeld van bewijs, geen exclusief wettelijk model. Dictum: niet-ontvankelijk. De huidige artikel207-tekst behoudt deze bewijsvoorwaarde; geen algemene certificering van de BW-gevolgen van een akkoord. Eerste aanleg en concrete bewijswaardering; selectief onderzoek, latere behandeling niet uitputtend gecontroleerd. In het lokale corpus van hogere rechters is geen duplicaat gevonden.
''')
(W/'cases/RBALM-1999-AA3942-rehabilitatie.md').write_text('''# Rechtbank Almelo 15 december 1999 — verleende rehabilitatie

ECLI:NL:RBALM:1999:AA3942; rekestnummer 33051 FT RK 99.342 (metadata: 33051 FT RK 99-342). Ondersteunt art-208 en art-210.

[Officiële uitspraak](https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:RBALM:1999:AA3942) · [volledige XML](../sources/review-art-207-212hf-case-rbalm-1999-aa3942.xml) · [leesversie](../sources/review-art-207-212hf-case-rbalm-1999-aa3942.txt) · [HTTP en hashes](../sources/review-art-207-212hf-cases-fetch.json).

De uitspraak heeft geen genummerde rechtsoverwegingen. De alinea na de conclusie van het OM bevat het eigen oordeel dat aan de vereisten is voldaan. De volgende alinea vermeldt volledige voldoening van erkende en geverifieerde vorderingen; de daaropvolgende vermeldt publicaties van 26 augustus 1999, een verstreken verzetstermijn en geen bezwaar. Dictum: rehabilitatie verleend, openbaar uitgesproken. Dit is een positief procedurevoorbeeld, geen oordeel dat uitsluitend volledige betaling mogelijk is. Dagbladpublicatie was onderdeel van de oude artikel208-tekst, bevestigd in de officiële historische toestand2002; de huidige tekst noemt alleen de Staatscourant. De toenmalige Rv-verwijzing en procureursrol zijn niet als actueel overgenomen. Geen bewijs dat het OM-oordeel de rechter bond. Eerste aanleg, historische context, selectieve dekking. Lokale hogere-rechtencorpus bevat geen duplicaat.
''')
(W/'sources/review-art-207-212hf-search-log.json').write_text(json.dumps({'queries':['site.rechtspraak.nl rehabilitatie "207" "Faillissementswet"','site.rechtspraak.nl "212b" faillissement','site.rechtspraak.nl "212hf"'],'official_full_decisions_read':['ECLI:NL:RBROT:2020:1792','ECLI:NL:RBALM:1999:AA3942'],'local_corpus_searched':'/Volumes/LaCie/law-intake/eu/nl/rechtspraak: cbb, crvb, hr, phr, rvs and their _raw snapshots; no lower court collection; exact ECLI text and filename search found no matching snapshot.','limitations':'Selective search, no sufficiently relevant full verified judgment used for other assigned units. No exhaustive negative claim about existence or later treatment.'},indent=2)+'\n')
