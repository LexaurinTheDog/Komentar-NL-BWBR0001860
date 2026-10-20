from pathlib import Path
import json,re,xml.etree.ElementTree as E,hashlib
W=Path(__file__).resolve().parent
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
ids=['art-'+str(n) for n in range(187,207)]
data=[
('1–4','Acht dagen vanaf gegeven beschikking; zitting binnen twintig dagen; curator/iedere schuldeiser versus schuldenaar; openbare deelname en twee routes tot verbindendheid.',['183','185','189','192'],[]),
('1–3','Cumulatie levering en koopprijs; alle hypotheken tegenover alleen niet-tegenwerpelijke beperkte rechten; verklaring op verzoek, inschrijving bij of na levering; Rv578-schepenverwijzing niet inhoudelijk uitgebreid.',[],[]),
('1–2','Voorwaardelijke toelating en betwiste voorrang gescheiden; bij rang alleen meerdere boven concurrent percentage reserveren; geen fictieve volledige blokkade.',['181','192'],[]),
('ongesplitst','Correctie uitsluitend reeds ontvangen percentage over hetzelfde batig gerangschikte bedrag; numeriek voorbeeld6000 minus600 niet minus1000.',['179','180'],[]),
('vervallen','Lege plaats en overgangsnotitie2018 behouden; geen huidige bevoegdheid afgeleid.',['189','190','192'],[]),
('ongesplitst','Letterlijke betaalmomenten, samenhang187lid4/189; niet-beschikte uitdelingen binnen maand versus gereserveerde; geen inhoudelijke nieuwe verificatie.',['183','187','189'],[]),
('1–3','Volledige betaling of verbindende slotlijst; publicatie14; maand verantwoordingsplicht onderscheiden van afgifte boeken; persoonlijke aanspraak TEGEN schuldenaar gecorrigeerd.',['14','193','194'],[]),
('ongesplitst','Terugvallende reserveringen en onbekende baten; rechtbankbevel versus RC-goedkeuring; vroegere lijsten als basis, geen universele heropening.',['180','189','193'],[]),
('ongesplitst','Terugkeer individuele executie bij verbindende slotlijst voor onvoldaan deel, geen automatische kwijtschelding of titelgarantie.',['196','197'],[]),
('ongesplitst','121lid4-erkenning en ondertekend verificatiePV, geen voorlopige lijst; HR7593.4.4–7 twintigjaar vanaf dag na ondertekening; titel niet onverjaarbaar.',['121','197'],['ECLI:NL:HR:2016:759']),
('ongesplitst','126-betwisting bewaart uitzondering tegen persoonlijke titelwerking, ook partieel; gronden en expliciete afbakening126lid2 vereist; niet vernietiging erkende boedelclaim.',['126','196'],['ECLI:NL:HR:2016:759']),
('vervallen','Historische2002nalatenschapsaanvraag onderscheiden van huidig vervallen slot; resterende verwijzing5 vult leeg materieel artikel niet aan.',['5'],[]),
('vervallen','Historische2002bevoegde rechtbank en erfgenamenoproeping afzonderlijk verantwoord; geen huidige oproepingsregel.',[],[]),
('vervallen','Historische2002vermogensafscheiding uitgelegd met tijdsgrens; geen actuele erfgenamenaansprakelijkheid afgeleid.',[],[]),
('vervallen','Historische2002aanvraagtermijnen nalatenschap versus actuele lege plaats; geen huidige termijn naverdeling.',[],[]),
('vervallen','Historische2002uitsluiting akkoord/achtsteafdeling met zuivere-aanvaardingsuitzondering; geen actuele uitzondering195–197.',[],[]),
('ongesplitst','Na faillissement afzonderlijk ontvangen buitenlandse opbrengst; voorrangsuitzondering dubbel getoetst volgens HR16303.3.4/3.4, niet enkel nationale naam of buitenlands label.',['20'],['ECLI:NL:HR:2014:1630']),
('1–2','Overdrager vergoedt werkelijk verhaal bij doelgerichte cessie; vermoeden weerlegbaar bij kennis aanvraag, niet pas uitspraak.',['203'],[]),
('1–2','Overdracht schuld OF vordering, causaliteit en Fw-verboden buitenlandse verrekening; vermoeden204lid2;54alle drie leden onderscheiden.',['54','204'],[]),
('ongesplitst','Alleen einde161/193, verzoek schuldenaar/erfgenamen rechtbank;5advocaat en207bewijs; source typo behouden, geen schuldkwijtschelding.',['5','161','193','207','208','209','210','211','212'],[])
]
notes={k:(p,t,['art-'+r for r in refs],cases) for k,(p,t,refs,cases) in zip(ids,data)}
s=(W/'_review_172_186_audit.py').read_text().replace('172-186','187-206').replace('172_186','187_206')
a=s.index("ids=['art-");b=s.index('\nrecords=[]',a);s=s[:a]+'ids='+repr(ids)+s[b:]
a=s.index('notes={');b=s.index('\nassert list(notes)==ids',a);s=s[:a]+'notes='+repr(notes)+s[b:]
s=s.replace('Full HR2017:2808 read and compared to preserved national corpus; the relevant articles67/184 remain operative. Selective research; no exhaustive later-treatment check.','Full HR2014:1630 and HR2016:759 read and compared to national corpus. HR2016:202 read but rejected as substantive authority: article81 rejection without own explanation, not an adoption of the PHR inadmissibility conclusion. Relevant Fw provisions196/197/203 retain their operative wording. The old EU regulation1346/2000 discussed in 2014 is not presented as current EU law. Selective research; no exhaustive later-treatment check.')
s=s.replace("assert 'Geraadpleegd op 20-10-2026.' in h", "assert 'Geraadpleegd op 20-10-2026.' in h")
(W/'_review_187_206_audit.py').write_text(s)
# Brief original case cards; full primary texts and corpus snapshots are linked.
(W/'cases/HR-2014-1630-buitenlands-verhaal.md').write_text('''# Hoge Raad 11 juli 2014 — buitenlandse voorrang

ECLI:NL:HR:2014:1630; zaak 13/03015; ondersteunt art-203.

[Officieel](https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:HR:2014:1630) · [XML](../sources/review-art-187-206-case-hr-2014-1630.xml) · [leesversie](../sources/review-art-187-206-case-hr-2014-1630.txt) · [corpus](../sources/review-art-187-206-hr-2014-1630-local.md) · [opvraging en hashes](../sources/review-art-187-206-cases-fetch.json).

Rov. 3.3.4 verlangt buitenlandse voorrang én inhoudelijke of functionele gelijkwaardigheid met Nederlandse voorrang. Rov. 3.4 past dit toe: de gestelde New Yorkse beslagpositie volstond niet. Het beroep wordt verworpen. Rov. 3.2 beschrijft daarentegen het hof; rov. 3.3.1 de cassatieklachten. De oude Europese verordening in de voorgeschiedenis wordt hier niet als actueel recht gebruikt. Geen algemene afwijzing van buitenlandse zekerheden; selectief onderzoek, geen volledige controle van latere rechtspraak.
''')
(W/'cases/HR-2016-759-verificatietitel.md').write_text('''# Hoge Raad 29 april 2016 — verificatietitel

ECLI:NL:HR:2016:759; zaak 15/00217; ondersteunt art-196 en art-197.

[Officieel](https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:HR:2016:759) · [XML](../sources/review-art-187-206-case-hr-2016-759.xml) · [leesversie](../sources/review-art-187-206-case-hr-2016-759.txt) · [corpus](../sources/review-art-187-206-hr-2016-759-local.md) · [opvraging en hashes](../sources/review-art-187-206-cases-fetch.json).

Rov. 3.4.1–3.4.3 verklaren de bescherming door persoonlijke betwisting. Rov. 3.4.4–3.4.7 behandelen executieverjaring; rov. 3.4.6 onderscheidt artikel 36 Fw. Het beroep wordt verworpen. De onverjaarbaarheid die de kantonrechter aannam (3.2.2) is geen oordeel van de Hoge Raad. Voorlopige erkenning en authentieke schikkingsakten vallen niet zonder meer onder deze beslissing. Selectief onderzoek; geen volledige controle van latere rechtspraak of afzonderlijke certificering van alle externe BW-bepalingen.
''')
save(W/'sources/review-art-187-206-search-log.json',{'queries':['site.rechtspraak.nl "203" "Faillissementswet" "Hoge Raad"','site.rechtspraak.nl "192" "187" "uitdelingslijst" cassatie','"artikel 192" "cassatie" "uitkering" curator','site.rechtspraak.nl "187" "192" "onherroepelijk"','site.rechtspraak.nl "196" "197" "Hoge Raad" betwist'],'full_decisions_read':['ECLI:NL:HR:2014:1630','ECLI:NL:HR:2016:759','ECLI:NL:HR:2016:202'],'used_decisions':['ECLI:NL:HR:2014:1630','ECLI:NL:HR:2016:759'],'not_used':{'ECLI:NL:HR:2016:202':'Actual decision rejects appeal under art81; no reasoned holding on procedural standing. PHR inadmissibility recommendation is not the court decision.','PHR:2022:540 and PHR:2022:37':'Search leads only, not cited as judicial holdings.'},'local_corpus':'Read preserved snapshots sources/review-art-187-206-hr-*-local.md alongside full official XML.','limitations':'Selective search; no exhaustive later-treatment review. No additional sufficiently relevant verified judgment used for the remaining technical or repealed places.'})
# Every official judicial paragraph compared against the full local corpus rendition.
comparisons=[]
norm=lambda s:re.sub(r'\s+','',s)
for k in ['2014-1630','2016-759','2016-202']:
 p=W/f'sources/review-art-187-206-case-hr-{k}.xml';local=W/f'sources/review-art-187-206-hr-{k}-local.md';root=E.parse(p).getroot();paras=root.findall('.//{*}uitspraak//{*}para');miss=[norm(''.join(e.itertext()))[:130] for e in paras if norm(''.join(e.itertext())) not in norm(local.read_text())]
 # Front matter is retained only in XML; court reasoning is in both renderings.
 comparisons.append({'ecli':'ECLI:NL:HR:'+k.replace('-',':'),'official_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'corpus_sha256':hashlib.sha256(local.read_bytes()).hexdigest(),'paragraphs':len(paras),'not_matched':miss})
save(W/'sources/review-art-187-206-case-comparison.json',comparisons)
