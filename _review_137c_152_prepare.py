from pathlib import Path
import json,datetime,hashlib
W=Path(__file__).resolve().parent
ids=['art-'+n for n in ['137c','137d','137e','137f','137g']+[str(i) for i in range(138,153)]]
data=[
('1–3','Tegeldemaking, 175 lid2 huisraad, 176 cumulatieve grens en toestemming, 177 diensten; lijstinhoud, volledige reservering geschil en kosten; na-uitdeling194 versus137g.', ['175','176','177','122','194','137g'],[]),
('1–5','Goedkeuring, tien dagen, verslag, kosteloze inzage iedereen, Staatscourant, alle bekende crediteuren met beperking concurrenten; omslag182 verduidelijkt.', ['182','137e','137f'],[]),
('1–4','Elke crediteur, gemotiveerd griffiebezwaar, ontvangst/bijvoeging, beperkte concurrente uitsluitingsgrond; openbare behandeling185 en cassatie187 verduidelijkt.', ['137d','185','187','137f'],[]),
('1–2','Eigen insolventiemoment, geen uitkering voor onherroepelijk verzet; functies188/189/190/192/193 afzonderlijk uitgelegd en samenloop192 begrensd.', ['137d','188','189','190','192','193','137g'],[]),
('1–3','Concrete opkomende baten met concurrente ruimte; alle vergadergegevens,80a/108, onmiddellijke mededeling/publicatie en afdelingen5/6/7; overgangsnotitie behouden.', ['80a','108'],[]),
('ongesplitst','Aanbodbevoegdheid en beide wederzijdse BW-routeblokkades met afzonderlijke beëindigingsvoorwaarden; gezamenlijke schuldeisers is geen onbeperkte schuldreikwijdte.', ['139','128','157'],['ECLI:NL:HR:2024:210']),
('1–2','Acht dagen vóór verificatie, iedereen kosteloos, na verificatie direct met voorbehoud141; gelijktijdige toezending curator/ieder voorlopig commissielid.', ['141'],[]),
('ongesplitst','Afzonderlijke schriftelijke adviezen ter vergadering of spoedig daarna; geen gelijkstelling advies en homologatie, financieringsvoorbeeld.', ['153'],[]),
('1°–2°','Nieuwe commissie staande vergadering met andere personen plus meerderheid advieswens; late neerlegging plus meerderheid uitstel; uiterlijk drie weken.', ['142','144'],[]),
('ongesplitst','Onverwijld schriftelijk aan afwezige erkende/voorwaardelijk toegelaten crediteuren, summiere inhoud; 83 lid2 vertegenwoordiging gecontroleerd.', ['141','83'],[]),
('1–2','Voorrang ook betwist, afstand vóór aanvang ten behoeve boedel, blijvend concurrent ondanks verwerping;163 bescherming en153 controle juist afgebakend.', ['163','153'],[]),
('ongesplitst','Toelichten/verdedigen en wijzigen tijdens raadpleging, vastgelegde stemming zelfde voorstel; advies140, waarborg153 en verbod158 onderscheiden.', ['140','153','158'],[]),
('ongesplitst','Dubbele meerderheid, personen verschenen versus bedrag totale toegelaten concurrente schuld inclusief afwezigen; primaire rechtbankuitleg toegevoegd.', ['81','143','146'],['ECLI:NL:RBGEL:2015:5785']),
('a–b','Verzoek schuldenaar/curator, gemotiveerde discretionaire beschikking, driekwart personen en causaal onredelijke tegenstem cumulatief; afwezigheid niet gelijkgesteld.', ['145'],['ECLI:NL:RBGEL:2015:5785']),
('ongesplitst','Latere aantal/bedragwijziging verandert aanneming/vaststelling/verwerping niet; oorspronkelijke vastleggingsfout149 en oneerlijke totstandkoming153 onderscheiden.', ['149','153'],[]),
('1–2','Volledige inhoud, namen individuele stemmen uitslag gebeurtenissen, twee ondertekeningen, iedereen acht dagen gratis inzage;149/154 verschillende rechten.', ['149','154'],[]),
('ongesplitst','Alleen voorstemmers/gefailleerde acht dagen na vergadering rechtbank, stukken zelf onterechte verwerping; ook gestelde interpretatiefout volgens rechtbank mogelijk, geen herstemming.', ['147','150','145'],['ECLI:NL:RBGEL:2015:5785']),
('1–3','Aangenomen/vastgesteld RC vóór sluiting;149 rechtbankbeschikking met schriftelijk curatorbericht;8–14 dagen juiste startpunten, geen homologatie vooraf.', ['149','151','152'],[]),
('ongesplitst','Schuldeisers schriftelijk aan RC gedurende tussenperiode, concrete redenen weigering;153 eigen toets en152 zitting, geen veto of rechtsmiddelvervanging.', ['153','152'],[]),
('1–2','Openbare zitting rapport RC schriftelijk, elke crediteur pro/con persoonlijk/gemachtigd/advocaat en gefailleerde belangenverdediging; stellingen geen vastgestelde feiten.', ['153','154'],[])]
notes={k:(p,t,['art-'+r for r in refs],cases) for k,(p,t,refs,cases) in zip(ids,data)}
s=(W/'_review_121_137b_audit.py').read_text().replace('121-137b','137c-152').replace('121_137b','137c_152')
a=s.index("ids=['art-");b=s.index('\nrecords=[]',a);s=s[:a]+'ids='+repr(ids)+s[b:]
a=s.index('notes={');b=s.index('\nassert list(notes)==ids',a);s=s[:a]+'notes='+repr(notes)+s[b:]
s=s.replace('One full HR decision (2014:3464) freshly fetched, read and compared with national corpus. Older procedural rules explicitly excluded; selective research, no exhaustive subsequent-treatment check.','Two full decisions read: HR 2024:210 and RBGEL 2015:5785; HR compared to local corpus. Selective research; no exhaustive later-treatment review.').replace('actual HR holdings','actual judicial holdings')
(W/'_review_137c_152_audit.py').write_text(s)
log={'searched_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'queries':['site.rechtspraak.nl faillissementsakkoord artikel 146 145 faillissementswet drie vierde','local HR corpus: 146 Fw|art.145 Fw|artikel146'],'full_decisions_read':['ECLI:NL:HR:2024:210','ECLI:NL:RBGEL:2015:5785'],'local_corpus_read':['ecli-nl-hr-2024-210.md','ecli-nl-hr-2019-425.md'],'not_used':['HR2019:425 false keyword hit: criminal seizure, no Fw authority','PHR2023:554 search result is advisory opinion, not used as holding'],'limits':'Selective research. No verified relevant case added for each technical provision; no exhaustive subsequent-treatment review.'}
(W/'sources/review-art-137c-152-search-log.json').write_text(json.dumps(log,indent=2)+'\n')
