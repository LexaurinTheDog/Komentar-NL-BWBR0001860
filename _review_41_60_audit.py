"""Integrity evidence for exact art-41–60 manual review; not legal certification."""
from pathlib import Path
import json,re,hashlib,datetime,xml.etree.ElementTree as E,sys,html
W=Path(__file__).resolve().parent;sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_commentary
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ids=['art-'+s for s in ['41','42','42a','43','45','47','48','49','50','51','52','53','54','55','56','57','58','59','59a','60']]
records=[]
for filename in ['fetch','cases-fetch','latest-case-fetch','external-fetch']:
 records+=json.loads((W/f'sources/review-art-41-60-{filename}.json').read_text())
for r in records:
 assert r['accepted'] and r['http_status']==200 and sha(W/r['raw_path'])==r['sha256'],r
 if r['raw_path'].endswith('.xml'):
  x=E.parse(W/r['raw_path']).getroot();assert x.tag in {'toestand','wetstechnische-informatie','open-rechtspraak'}
  if 'hr-' in r['raw_path']:assert x.find('{*}uitspraak') is not None
raw=W/'sources/review-art-41-60-selected.xml';root=E.parse(raw).getroot()
assert root.get('bwb-id')=='BWBR0001860' and root.get('inwerkingtreding')=='2026-09-01'
assert sha(raw)==sha(W/'sources/official-2026-09-01.xml')
h=(W/'sources/review-art-41-60-current.html').read_text()
assert 'Geraadpleegd op 20-10-2026.' in h and 'Geldend van 01-09-2026 t/m heden.' in h
wt=E.parse(W/'sources/review-art-41-60-wti.xml').getroot()
dates=sorted({x.get('waarde') for x in wt.findall('./wijzigingen/regeling/datum') if x.get('waarde')})
assert max(d for d in dates if d<='2026-10-19')=='2026-09-01'
assert not [d for d in dates if '2026-10-01'<d<='2026-10-20']
assert min(d for d in dates if d>'2026-10-20')=='2027-11-15'
historical=E.parse(W/'sources/version-register.xml').getroot();assert historical.get('inwerkingtreding')=='2002-01-01'
expected=['art-'+a.get('label').removeprefix('Artikel ') for a in root.findall('.//artikel')]
html_ids=['art-'+html.unescape(re.sub('<[^>]+>','',t)).strip().removeprefix('Artikel ') for t in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',h)]
units=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()];by={x['id']:x for x in units}
assert expected==html_ids==[x['id'] for x in units] and len(expected)==len(set(expected))==639
assert not [e for e in root.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
assert not re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>[^<]*(?:Bijlage|Annex)',h)
def tokens(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+tokens(c)+' '+(c.tail or '') for c in e)
norm=lambda s:re.sub(r'\s+','',s)
for a in root.findall('.//artikel'):
 key='art-'+a.get('label').removeprefix('Artikel ');assert norm(tokens(a))==norm(by[key]['text']),key
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
assert len(comp['repealed_slots'])==57 and comp['editorial_notes']==481
assert all(sha(W/p)==v for p,v in json.loads((W/'sources/review-art-41-60-parser-before.json').read_text()).items())
casecomp=json.loads((W/'sources/review-art-41-60-case-comparison.json').read_text())
assert len(casecomp)==5
for r in casecomp:
 assert r['normalized_corpus_body_is_official_suffix'] and sha(W/r['official_raw_path'])==r['official_sha256'] and sha(W/r['local_snapshot_path'])==r['local_sha256']
 body=''.join(E.parse(W/r['official_raw_path']).getroot().find('{*}uitspraak').itertext())
 local=(W/r['local_snapshot_path']).read_text().split('## Uitspraak\n',1)[1]
 assert norm(body).endswith(norm(local))
external=[('BWBR0003045','Geldend van 01-07-2026 t/m heden.','Artikel138_Lid10'),('BWBR0005291','Geldend van 01-07-2025 t/m heden.','Artikel184_Lid1')]
for bid,validity,anchor in external:
 t=(W/f'sources/review-art-41-60-{bid}.html').read_text();assert validity in t and 'Geraadpleegd op 20-10-2026.' in t and anchor in t
notes={
'art-41':('1–2','Ongewijzigd aanvaard. Nieuwe erfenis binnen 20, uitsluitend beneficiaire aanvaarding en afzonderlijke machtiging voor verwerping onderscheiden; geen overname van onbeperkte nalatenschapsschuld verondersteld.',['art-20'],[]),
'art-42':('1–3','Uitgebreid met actuele HR-uitleg van wetenschap, werkelijk samenhangende transacties, toets van benadeling en verschil tussen bewijsjaar en vernietigingsbevoegdheid. Uitsluiting 3:50 lid 2, machtiging bij procederen en restitutie onderscheiden.',['art-43','art-45','art-47','art-51','art-68'],['ECLI:NL:HR:2025:975']),
'art-42a':('1 a 1°–2°, b; 2','Ontbrekende noodzaakroutes stemming en homologatie en cumulatieve belangencriteria uitgewerkt. Precieze geïmporteerde leden en zinnen, procedurekeuze, rechtsmacht en bijzonder verzet verduidelijkt; geen algemene immuniteit of import van alle deskundigenbevoegdheden.',['art-42','art-369','art-370','art-371','art-384'],[]),
'art-43':('1 onderdelen 1°–6° inclusief a–d; 2–6','Alle categorieën en onderscheiden kapitaal-/verwantschapsverbindingen beschreven, aparte terugkijktermijn voormalig functionaris uitgelegd. Lid 6 is financieringsvoorziening bij lege boedel, geen extra aansprakelijkheidsvermoeden; beperkte externe verwijzing officieel geverifieerd.',['art-42'],[]),
'art-45':('ongesplitst','Ongewijzigd aanvaard. Vermoeden alleen wetenschap schuldenaar bij benadelende handeling om niet binnen jaar; bescherming 42 lid 3 en oorspronkelijke datum bij 15d lid 2 correct onderscheiden.',['art-42','art-15d'],[]),
'art-47':('ongesplitst, beide alternatieven en schorsingsuitzondering','Ongewijzigd aanvaard. Aanvraagkennis niet gelijk aan algemene financiële zorg; doelgericht overleg niet ieder betalingsoverleg; schorsing 3d/376 en opeisbaarheid correct.',['art-3d','art-42','art-376'],[]),
'art-48':('1–2','Voorbeeld gecorrigeerd: uitgiftekennis van daadwerkelijke aanvraag in plaats van alleen naderend faillissement. Tijdstip uitgifte, begunstigde versus houder en alternatief begunstigingsoverleg expliciet gemaakt.',['art-47'],[]),
'art-49':('1–2','Voorbeeld verbeterd: schulderkenning kan grondslag ingediende vordering zijn; zekerheid alleen schept die schuld niet. Exclusieve curatoractie en defensief verificatieverweer schuldeiser behouden.',['art-42','art-48','art-50'],[]),
'art-50':('ongesplitst','Materieel timingherstel: einde faillissement bij in kracht van gewijsde gegane homologatie volgens 161, niet enkel uitspraak. Boedelafstand en vereffenaarsbevoegdheid blijven aparte uitzondering.',['art-49','art-161'],[]),
'art-51':('1–3','Ongewijzigd aanvaard. Teruggave, derden anders dan om niet, derden om niet met bewijs niet-gebaat en beperkte restitutie boedel versus concurrent restant afzonderlijk juist uitgelegd. Bestaande praktische controlelijst behouden.',['art-37','art-42','art-50'],[]),
'art-52':('1–3','Ongewijzigd aanvaard. Alleen voldoening oude verbintenis; bewijsrisico vóór en na aankondiging, tegenbewijs werkelijke kennis en bevrijding voor werkelijke boedelbaat correct. Geen bescherming afgeleid enkel uit afschrijving.',['art-14'],[]),
'art-53':('1–3','Materiële nuance toegevoegd: wederkerigheid regelend, oud bewezen kruisverrekenbeding mogelijk; tijdsgrens dwingend. Nominaal versus waardering en uitgesloten processueel beroep 6:136 onderscheiden. HR-verwijzing bewijst geen feitelijk bestaan contract.',['art-54','art-55','art-130','art-131'],['ECLI:NL:HR:2019:1789']),
'art-54':('1–3 a–b','Goede-trouwmaatstaf omvat weten én behoren te weten; reddingsbereidheid alleen onvoldoende. Eigen-schuldpandrecht versus oorspronkelijk stil verpande vordering, concernbetaling en nieuwste afwijzing uitgaande-betalingenuitzondering uitgewerkt. Latere WHOA-regel niet op feiten 2020 geplakt; lid 3 heft lid 2 niet op.',['art-53','art-370','art-371'],['ECLI:NL:HR:2018:2189','ECLI:NL:HR:2023:1135','ECLI:NL:HR:2026:390']),
'art-55':('ongesplitst','Ongewijzigd aanvaard. Verkrijging én goede trouw op faillissementsmoment door verrekenaar te bewijzen; later bezit alleen onvoldoende; algemene grenzen blijven.',['art-53','art-54'],[]),
'art-56':('ongesplitst','Ontbrekend materieel effect ingevuld: toerekening gemeenschapsschuld op aandeel gefailleerde, doorbreking externe uitsluiting onvervulde voorwaarde en waardering 130/131. Officiële 3:184 leden 1–2 gelezen; geen vrijstaande boedelschuld gecreëerd.',['art-130','art-131'],[]),
'art-57':('1–4','Ongewijzigd aanvaard. Separatistische bevoegdheid, vervallen beperkte rechten met vergoeding, beslagleggersrechten en hoger bevoorrechten plus specifieke rangregeling onderscheiden. Termijnstelling en afkoelingsperiode als begrenzingen aanwezig.',['art-58','art-59','art-63a'],[]),
'art-58':('1–2','Verkoop versus alleen aankondiging, aanvrager verlenging, rechtsmiddeluitsluiting 67, machtiging bij lossing 68 en kostenverschil via 182 toegevoegd. Behoud opbrengstrecht geen garantie gelijke netto-uitkering.',['art-57','art-67','art-68','art-101','art-176','art-182'],[]),
'art-59':('ongesplitst','Ongewijzigd aanvaard. Concurrente tekortdeelname ook beperkt gerechtigde; feitelijke netto-ontvangsten en geen dubbele voldoening correct, taxatie geen definitief tekort.',['art-57'],[]),
'art-59a':('1–7','Alle zeven leden uitgewerkt: registervoorwaarde, specifieke voorrechten, slechts 57 leden 2/3 geïmporteerd, verzoek verlenging, procesficties, vast te stellen kostendeel, lossing en teruggebrachte tekortregel. Geen ongecontroleerde reconstructie van heel luchtvaart-/verdragsrecht.',['art-57','art-58','art-59','art-67'],[]),
'art-60':('1–4','Machtigingsvereiste 68, aanvrager verlenging en uitsluiting beroep 67, schorsing door afkoeling 63a en precieze sanctie registergoed uitgewerkt. Termijnrichting tegenover 58 en niet-tijdige verkoop onderscheiden; praktische hoofdstukcontrolelijst toegevoegd.',['art-58','art-63a','art-67','art-68','art-101','art-176'],[])
}
assert list(notes)==ids
before=json.loads((W/'sources/review-art-41-60-before-hashes.json').read_text());new=load_commentary(str(W))
assert set(before)==set(new) and len(new)==297
assert all(hashlib.sha256(t.encode()).hexdigest()==before[key] for key,t in new.items() if key not in ids)
rows=[]
for key in ids:
 for ref in notes[key][2]:assert ref in by
 rows.append({'id':key,'official_path':by[key]['official_path'],'source_paragraphs_reviewed':notes[key][0],'source_notes_reviewed':by[key]['notes'],'source_effective_from':by[key]['effective_from'],'statutory_text_sha256':hashlib.sha256(by[key]['text'].encode()).hexdigest(),'commentary_before_sha256':before[key],'commentary_after_sha256':hashlib.sha256(new[key].encode()).hexdigest(),'result':'corrected_or_extended' if hashlib.sha256(new[key].encode()).hexdigest()!=before[key] else 'accepted_without_change','assessment':notes[key][1],'internal_cross_references_checked':notes[key][2],'case_authorities_checked':notes[key][3],'unresolved_blockers':[]})
checks={'checked_at_utc':now,'source_records':[f'sources/review-art-41-60-{n}.json' for n in ['fetch','cases-fetch','latest-case-fetch','external-fetch']],'official_source_sha256':sha(raw),'decisive_date':'2026-10-19','selected_version':'2026-09-01_0','current_validity_statements':['Geraadpleegd op 20-10-2026.','Geldend van 01-09-2026 t/m heden.'],'latest_effective_change':'2026-09-01','next_dated_change_excluded':'2027-11-15','changes_since_intake':[],'historical_version_excluded':{'path':'sources/version-register.xml','effective_from':'2002-01-01','sha256':sha(W/'sources/version-register.xml')},'expected_official_count':639,'parsed_count':639,'fresh_official_html_toc_count':639,'whole_source_token_agreement':True,'annex_disposition':comp['annexes'],'opening_closing_text_checks':comp['non_article_text'],'editorial_notes_preserved':481,'source_coverage_report':'completeness-report.json','parser_idempotent_verified':True,'unassigned_commentaries_unchanged':True,'case_comparison':'sources/review-art-41-60-case-comparison.json','reviewed_ids':ids,'reviewed_count':20,'commentaries_changed':sum(r['result']!='accepted_without_change' for r in rows),'unresolved_blockers':[],'ok':True}
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'max_units':20,'checked_at_utc':now,'decisive_date':'2026-10-19','official_url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01','whole_book_complete':False,'unresolved_blockers':[],'findings':rows,'limitations':['Exactly the assigned 20 units were substantively reviewed in this process. Earlier 60 distinct unit reviews are preserved, not repeated or claimed as work of this process.','342 missing commentaries remain outside this bounded task; the complete-book builder and validator cannot pass.','Five selected full HR judgments were read and matched with the local national corpus. No exhaustive subsequent-case research or separately verified case for each technical unit.','External law independently checked only for limited BW references 2:138 lid 10 and 3:184. Other external Rv, BW, aviation, EU and transitional regimes are not certified in full; the verified current Faillissementswet references are retained.','Fresh-process second reading, not external professional approval. Minimum length, source match and script success do not prove legal quality.'],'technical_evidence':'review-checks.json','commentary_before_snapshot':'sources/review-art-41-60-commentary-before.txt','previous_batch_result':'sources/review-art-28-40-result.json','changed_units':[r['id'] for r in rows if r['result']!='accepted_without_change'],'accepted_without_change':[r['id'] for r in rows if r['result']=='accepted_without_change']}
p=W/'review-result.json'
if p.exists():
 old=json.loads(p.read_text())
 if old.get('findings')==rows and 'validation' in old:result['validation']=old['validation']
for name,value in [('review-checks.json',checks),('review-result.json',result),('sources/review-art-41-60-checks.json',checks),('sources/review-art-41-60-result.json',result)]:save(W/name,value)
pre={'complete':True,'decisive_date':'2026-10-19','official_url':result['official_url'],'verified_at':now,'version_evidence':{'selected_toestand':'2026-09-01_0','explicit_validity':checks['current_validity_statements'],'latest_effective_change':'2026-09-01','next_dated_change_excluded':'2027-11-15','changes_since_intake':[],'source_records':checks['source_records']},'historical_versions_checked':[checks['historical_version_excluded'],{'path':str(raw.relative_to(W)),'effective_from':'2026-09-01','sha256':sha(raw),'disposition':'Only this toestand parsed; 639 unique current article identifiers and official paths. 212hgd* and 212hgd retained as distinct simultaneous slots.'}],'annexes_checked':checks['annex_disposition'],'opening_and_closing_text_checked':checks['opening_closing_text_checks'],'parser_idempotent':True,'coverage_complete':True,'unresolved_blockers':[],'limitations':['Source preflight is complete; substantive review is restricted to the 20 assigned places.']}
save(W/'sources/review-art-41-60-preflight-result.json',pre)
p=W/'preflight-result.json';v=json.loads(p.read_text());v['bounded_review_art_41_60_recheck']=pre;save(p,v)
print(json.dumps({'scope_complete':True,'reviewed':20,'changed':checks['commentaries_changed'],'unassigned_unchanged':True,'statutory_token_agreement':True,'whole_book_complete':False}))
