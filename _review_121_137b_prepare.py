from pathlib import Path
W=Path(__file__).resolve().parent
ids=['art-'+n for n in ['121','122','122a','123','124','125','126','127','128','129','130','131','132','133','134','135','136','137','137a','137b']]
data=[
('1–4','Onbetwist versus eedvoorwaarde; papier, ondertekening en kracht van gewijsde; bijzondere heropening begrensd, oudere vergaderingsregel uitgesloten.',['112','120','137','108'],True),
('1–4','Schikkingspoging, reeds aanhangig geschil, verwijzing zonder dagvaarding, advocaten en wederzijdse processancties; Rv-verwijzing en uitsluiting niet-betwistende crediteuren.',['29'],False),
('1–4','Curatorbetwisting versus medecrediteur, homologatie onherroepelijk, uitzondering reeds voor beslissing overgelegd, kostenpartij en twee hervattingsroutes; geen wijziging nodig.',[],False),
('ongesplitst','Geen zwaarder bewijs dan tegenover gefailleerde; bewijspositie onderscheiden van curatoronderzoek en eigen voorkeur voor documenten.',['111'],False),
('1–2','Onmiddellijke griffierkennisgeving aan afwezige, ontbreken niet in geding inroepbaar; geen algemene immuniteit voor alle oproepingsfouten.',['122'],False),
('ongesplitst','Discretionaire voorwaardelijke toelating en afzonderlijke rang, geen definitieve erkenning; uitsluiting hoger beroep en stemrecht expliciet toegevoegd.',['121','67','82'],False),
('1–2','Gehele/gedeeltelijke claim of rang, summiere gronden, grens bij gedeeltelijke betwisting; geen renvooi of blokkade; persoonlijke executiegevolgen en bijzondere toelatingsbeslissing toegevoegd.',['122','196','197'],True),
('1–4','Veertien dagen voor eerste vergadering, rechterlijke afwijking/aanpassing na belangenafweging, kennisgeving, sanctie en registratie; bronovergangsnotitie behouden.',['108','109','19','110a'],False),
('ongesplitst','Na faillissement lopende rente uitgesloten behalve pand/hypotheek, pro memorie, alleen batig gerangschikt; factuurdatum geen vervanging periode.',[],False),
('ongesplitst','Volledige verificatie ontbindende voorwaarde met latere werking voorwaarde; onderscheid opschortend.',['130'],False),
('1–2','Waarde faillissementsmoment of volle voorwaardelijke toelating bij geen overeenstemming; verwijzingen verrekening/gemeenschap afzonderlijk gecontroleerd.',['53','56'],False),
('1–3','Onzekere opeisbaarheid/periodiek, binnen versus later dan één jaar, exclusieve berekeningsfactoren en onderscheid uitdelingspercentage.',[],False),
('1–2','Vermoedelijk tekort aantonen, behoud voorrang; alle vier typen in lid1 benoemd en beperkte personele reikwijdte Rv-verwijzing lid2 verduidelijkt.',['59'],False),
('ongesplitst','Onbepaald/onzeker/niet in Nederlands geld/niet in geld, raming versus bestaan, voorwaarden en rente; geen ongefundeerde koersdatum.',['128'],False),
('ongesplitst','Toonder, afzonderlijke crediteur, identificatie tegen dubbel tellen, stem- en splitsingsregels afzonderlijk gecontroleerd.',['82','121','81'],False),
('vervallen','Expliciete vervallen nummerplaats, geen historische inhoud als actuele norm.',[],False),
('1–2a–c','Volledige nog verschuldigde claim per faillissementsmoment tot voldoening; regres naar interne verhouding, alternatieve toelatingsgronden en geen dubbele concurrentie.',[],False),
('1–2','Verslag en inlichtingen, neerlegging en inzage voor iedereen kosteloos; beperkte verbeteringsroute uit stukken zelf, onderscheiden bedrog/inhoud; checklist gelezen.',['68a','121'],False),
('1–3','Geen verwachte concurrente uitdeling, RC-beschikking, onmiddellijke berichten/Staatscourant; uitgesloten afdelingen en overeenkomstige 128–136 concreet, hoger beroep uitgesloten.',['16','137g','67'],False),
('1–4','Onderzoek preferentie/zekerheden; bericht en overleg, dan RC; exact 122 leden1–3; eigen bezwaren via curator en overeenkomstige126 verduidelijkt.',['122','126'],False)]
notes={k:(p,t,['art-'+x for x in refs],['ECLI:NL:HR:2014:3464'] if case else []) for k,(p,t,refs,case) in zip(ids,data)}
s=(W/'_review_106a_120_audit.py').read_text().replace('106a-120','121-137b').replace('106a_120','121_137b')
a=s.index("ids=['art-");b=s.index('\nrecords=[]',a);s=s[:a]+'ids='+repr(ids)+s[b:]
a=s.index('notes={');b=s.index('\nassert list(notes)==ids',a);s=s[:a]+'notes='+repr(notes)+s[b:]
s=s.replace('One selected full district-court decision independently fetched and read; local HR 2021:112 consulted as context but not cited as authority. No exhaustive search or separately verified decision for each technical unit.','One full HR decision (2014:3464) freshly fetched, read and compared with national corpus. Older procedural rules explicitly excluded; selective research, no exhaustive subsequent-treatment check.')
s=s.replace('actual HR holdings','actual HR holdings')
s=s.replace("'checked_at_utc':now", "'review_date_local':'2026-10-21','checked_at_utc':now")
s=s.replace("'current_validity':'Geldend van 01-09-2026 t/m heden; geraadpleegd op 20-10-2026'", "'current_validity':'Geldend van 01-09-2026 t/m heden; official response says geraadpleegd op 20-10-2026; fetched 20 October UTC / 21 October Europe/Prague','review_date_local':'2026-10-21'")
s=s.replace("assert not [d for d in dates if '2026-10-01'<d<='2026-10-20']", "assert not [d for d in dates if '2026-10-01'<d<='2026-10-21']")
(W/'_review_121_137b_audit.py').write_text(s)
