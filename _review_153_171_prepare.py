from pathlib import Path
import json,xml.etree.ElementTree as E,shutil
W=Path(__file__).resolve().parent
ids=['art-'+str(i) for i in range(153,172)];ids.insert(ids.index('art-162'),'art-161a')
data=[
('1–3','Drie verplichte weigeringen afzonderlijk; overige ambtshalve gronden en motivering, vergelijking realiseerbare baten en financieringsvoorbeeld.',['153','384']),
('ongesplitst','Acht dagen, gerechtigden per uitkomst/stem, ontdekking na homologatie als bijzondere grond voor voorstemmer; bronnotitie bewaard.',['148','153','155']),
('1–2','Verzoek hof, advocaat5, twintig dagen behandeling versus acht instellen, kennisgeving; openbare zitting en uitzondering RC expliciet gemaakt; overgangsnotitie2016.',['5','152','153','154']),
('ongesplitst','Cassatieverwijzing acht dagen en snelle behandeling geëxpliciteerd, rechtsvragen versus feiten en toepasselijke vertegenwoordiging.',['154','155','161']),
('ongesplitst','Binding ook niet-opgekomen concurrenten; gecorrigeerd met verificatiegrens en natuurlijke verbintenis uit HR2024:210; lopende rente uitgesloten.',['128','160','161a']),
('ongesplitst','Geen nieuw aanbod na verwerping/weigering binnen zelfde faillissement, onderscheiden wijzigingen, uitslagherstel en rechtsmiddel.',['144','149','170']),
('ongesplitst','Cumulatieve titelstukken, erkende en niet persoonlijk betwiste claim, akkoordborg versus oorspronkelijke borg, opeisbaarheid.',['126','160','165']),
('ongesplitst','Behoud derdenrechten en zekerheden, geen dubbele ontvangst, materieel recht versus executoriale titel.',['159']),
('ongesplitst','Einde bij onherroepelijkheid, Staatscourant declaratoire publicatie, resterende afwikkelingsplichten.',['162','163','164','165','167']),
('ongesplitst','Verifieerbaar, werkelijke127-termijn en redelijke onmogelijkheid, herleving168, onderscheid uitgesloten rente; overgangsnotitie2018.',['127','128','157','168']),
('1–2','Rekening aan schuldenaar ten overstaan RC; afzonderlijke afgifte tegen kwijting behoudens akkoord, grens163.',['163']),
('1–3','Storting of zekerheid, bewaring zolang beide ontbreken, maand en betaling beschikbare baten, begroting bedrag en individuele delen; zekerheid verhindert onbeperkte bewaring.',['164']),
('ongesplitst','Voorwaardelijk erkende voorrang alleen zekerheid; bij ontbreken reservering relevante bedrag en geen onvoorwaardelijke betaling.',['163']),
('1–3','Elke benadeelde akkoordcrediteur, schuldenaar bewijst voldoening, discretionair ambtshalve hersteluitstel maximaal maand.',['166','167']),
('ongesplitst','Verwezen procedure4,6–9,12 en advocaat5, geen buitengerechtelijke ontbinding/heropening door aanmaning.',['4','5','6','7','8','9','12','165']),
('1–3','Gelijktijdig heropeningsbevel, RC/curator en commissie indien eerder, voorkeur geen recht, publicatie14lid3; overgangsnotitie2018.',['14','168','169','170','171']),
('1–3','Exacte verwijzingsomvang incl13lid1 maar niet13lid2; verificatiecontinuïteit en161a-herleving; oude crediteuren betwisten nu ingediende claims; overgangsnotitie2018.',['13','15','16','17','18','161a']),
('ongesplitst','Binding tussen homologatie en heropening, niet gelijkgesteld met onherroepelijkheid, paulianavoorwaarden42ev en geen automatische vernietiging.',['42','161']),
('1–2','Geen nieuw akkoord en zonder verwijl vereffenen, geen vrijbrief verkoopwaarborgen over te slaan.',['158','171']),
('1–2','Inhaalverdeling oud/nieuw en deelbetalingen; concreet100/20-rekenvoorbeeld, gelijkelijk geen gelijk bedrag per persoon; checklist behouden.',['168','170'])]
notes={k:(p,t,['art-'+r for r in refs],['ECLI:NL:HR:2024:210'] if k in ['art-157','art-161a'] else []) for k,(p,t,refs) in zip(ids,data)}
s=(W/'_review_137c_152_audit.py').read_text().replace('137c-152','153-171').replace('137c_152','153_171')
a=s.index("ids=['art-");b=s.index('\nrecords=[]',a);s=s[:a]+'ids='+repr(ids)+s[b:]
a=s.index('notes={');b=s.index('\nassert list(notes)==ids',a);s=s[:a]+'notes='+repr(notes)+s[b:]
s=s.replace('Two full decisions read: HR 2024:210 and RBGEL 2015:5785; HR compared to local corpus. Selective research; no exhaustive later-treatment review.','Full HR2024:210 read and compared to preserved national corpus. Selective research; no exhaustive later-treatment check.')
(W/'_review_153_171_audit.py').write_text(s)
x=E.parse(W/'sources/review-art-153-171-case-hr-2024-210.xml').getroot();(W/'sources/review-art-153-171-case-hr-2024-210.txt').write_text(''.join(x.find('{*}uitspraak').itertext()))
shutil.copyfile(W/'sources/review-art-137c-152-hr-2024-210-local.md',W/'sources/review-art-153-171-hr-2024-210-local.md')
log={'queries':['site.rechtspraak.nl 157 2024:210','site.rechtspraak.nl 165 akkoord Hoge Raad ontbinding'],'full_decisions_read':['ECLI:NL:HR:2024:210'],'local_corpus_read':'sources/review-art-153-171-hr-2024-210-local.md','not_used':'PHR advisory opinions and unrelated search hits excluded; no verified additional authority for technical units.','limitations':'Selective search; no exhaustive coverage or subsequent-treatment review.'}
(W/'sources/review-art-153-171-search-log.json').write_text(json.dumps(log,indent=2)+'\n')
