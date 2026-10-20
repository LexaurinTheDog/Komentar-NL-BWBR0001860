"""Reproduce source/integrity checks for the explicitly scoped second reading.
The per-unit assessments below record a manual source-to-commentary reading;
the mechanical checks do not themselves establish the legal conclusions.
"""
from pathlib import Path
import json,re,hashlib,datetime,xml.etree.ElementTree as E,collections,sys
W=Path(__file__).resolve().parent
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_commentary
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ids=['art-'+x for x in ['1','2','3','3a','3b','3d','4','5','5a','6','7','8','9','10','11','12','13','13a','14','14b']]
records=json.loads((W/'sources/review-art-1-14b-fetch.json').read_text())
for rec in records:
 assert rec['accepted'] and rec['http_status']==200,rec
 assert sha(W/rec['raw_path'])==rec['sha256']
r=E.parse(W/'sources/review-art-1-14b-selected.xml').getroot()
assert r.tag=='toestand' and r.get('bwb-id')=='BWBR0001860' and r.get('inwerkingtreding')=='2026-09-01'
assert sha(W/'sources/review-art-1-14b-selected.xml')==sha(W/'sources/official-2026-09-01.xml')
h=(W/'sources/review-art-1-14b-current.html').read_text()
assert 'Geldend van 01-09-2026 t/m heden.' in h and 'Geraadpleegd op 20-10-2026.' in h
expected=['art-'+x.get('label').removeprefix('Artikel ') for x in r.findall('.//artikel')]
assert len(expected)==639 and len(set(expected))==639
parsed=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()];by={u['id']:u for u in parsed}
assert expected==[u['id'] for u in parsed]
assert not [x for x in r.iter() if 'bijlage' in x.tag.lower() or 'annex' in x.tag.lower()]
historical=E.parse(W/'sources/version-register.xml').getroot()
assert historical.get('inwerkingtreding')=='2002-01-01'
wti=E.parse(W/'sources/review-art-1-14b-wti.xml').getroot()
assert wti.tag=='wetstechnische-informatie'
dates=sorted({x.get('waarde') for x in wti.findall('./wijzigingen/regeling/datum') if x.get('waarde')})
assert max(d for d in dates if d<='2026-10-19')=='2026-09-01'
assert not [d for d in dates if '2026-10-01'<d<='2026-10-20']
assert min(d for d in dates if d>'2026-10-20')=='2027-11-15'
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok']
assert comp['html_toc_order_equal'] and not comp['unaccounted_legal_text_nodes']
# Independent flattening of statutory nodes, without reusing _parse.py.
def legal_tokens(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+legal_tokens(c)+' '+(c.tail or '') for c in e)
norm=lambda s:re.sub(r'\s+','',s)
for node in r.findall('.//artikel'):
 key='art-'+node.get('label').removeprefix('Artikel ')
 assert norm(legal_tokens(node))==norm(by[key]['text']),key
# Full local/official case comparison, excluding the omitted local party caption.
case=E.parse(W/'sources/review-art-1-14b-hr-2018-1100.xml').getroot()
assert case.find('{*}uitspraak').get('id')=='ECLI:NL:HR:2018:1100:DOC'
body=''.join(case.find('{*}uitspraak').itertext());body=body[body.index('1Het geding in feitelijke instanties'):]
local=(W/'sources/review-art-1-14b-hr-2018-1100-local.md').read_text().split('## Uitspraak\n\n',1)[1]
assert norm(local)==norm(body)
assert sha(W/'sources/review-art-1-14b-hr-2018-774.xml')==sha(W/'sources/case-2018-774.xml')
notes={
'art-1':('1–2','Steunvordering hoeft niet opeisbaar of in omvang vastgesteld te zijn; voorwaardelijke schenking verduidelijkt. Verwijzingsopdracht van HR onderscheiden van een definitieve faillietverklaring.',['art-6'],['ECLI:NL:HR:2018:774']),
'art-2':('1–5','Laatste woonplaats, firma-kantoor, cumulatieve voorwaarden van lid 4 en beperking van lid 5 expliciet gemaakt. Internationale rechtsmacht blijft afzonderlijk.',['art-4','art-5'],[]),
'art-3':('1–2','Geen inhoudelijke wijziging nodig: natuurlijke persoon, ontbreken saneringsverzoek, verzending plus veertien dagen en schorsing correct. Voorbeeld claimt geen toelating.',['art-3a','art-3b','art-284'],[]),
'art-3a':('1–3','Verschil tussen kracht van gewijsde in lid 2 en uitspraak tot definitieve toepassing in lid 3 verduidelijkt; geen extra onherroepelijkheidseis voor verval toegevoegd.',['art-1','art-6'],[]),
'art-3b':('ongesplitst','Geen wijziging nodig: daadwerkelijk lopende regeling sluit 3/3a uit; een beëindigde regeling is niet gelijkgesteld en geen zelfstandige faillissementsgrond verzonnen.',['art-3','art-3a'],[]),
'art-3d':('1–2','Geen wijziging nodig: eigen aangifte en schuldeisersverzoek, prioriteit deskundigenverzoek, schorsing tot beslissing en bij toewijzing gedurende afkoelingsperiode afzonderlijk behandeld.',['art-3a','art-371','art-376'],[]),
'art-4':('1–5','Griffie-indiening, horen OM en voorbehoud van 15b toegevoegd. Partneruitzondering, vennotengegevens, rechtsmachtinformatie en uitvoerbaarheid blijven onderscheiden.',['art-13','art-15b','art-284'],[]),
'art-5':('1–3','Eigen aangifte onderscheiden van verzoeken met advocaatplicht. Europese opsomming en de al in artikel 67 lid 2 verifieerbare bijzondere werknemersberoepstermijn verduidelijkt.',['art-4','art-5a','art-67'],[]),
'art-5a':('1–5','Beroep beperkt tot beslissing krachtens de aangewezen Europese artikelplaats; lid 3 regelt indiening en geen tweede termijn. Procespartijen en griffiebericht uitgewerkt, geen fusie van boedels gesuggereerd.',['art-2','art-5'],[]),
'art-6':('1–4','Bij buitenlandse hoofdprocedure ook de schriftelijke zienswijzegelegenheid binnen rechterlijke termijn en de afzonderlijke verschijningsbevoegdheid van de partner beschreven. Summiere toets blijft onderscheiden van automatisme.',['art-1','art-5'],['ECLI:NL:HR:2018:774']),
'art-7':('1–2','Geen wijziging nodig: discretionair verlof op verzoek, facultatieve zekerheid, aangewezen notaris en uitsluiting/beschrijving van artikel-21-zaken correct; voorbeeld schept geen eigen beslagrecht.',['art-21'],[]),
'art-8':('1–6','Oproepings- en behandelingsleden explicieter verwerkt. Wettelijk aanvangspunt niet als absolute uitsluiting van kennisgevingsfouten behandeld; verwijzing naar de bij artikel 12 besproken rechtspraak.',['art-4','art-12'],[]),
'art-9':('1–3','Aangever/aanvrager, griffies en wettelijke termijnankering uitgewerkt; derdenverzet verwezen naar 11 lid 2. Betaling als relevante herbeoordelingsomstandigheid, geen automatische toewijzing.',['art-4','art-5','art-6','art-8','art-10','art-11'],[]),
'art-10':('1–5','Onduidelijk curatorloos-afwikkelingsvoorbeeld vervangen door toets aan actuele betalingstoestand; indiening, oproeping en advocaatplicht expliciet, geen schorsende werking aan verzet toegekend.',['art-4','art-5','art-13','art-15'],[]),
'art-11':('1–4','Beroepsgerechtigden bij vernietiging en verwijzing van lid 3 uitgeschreven; andere crediteuren niet automatisch cassatie- of beroepsgerechtigd verklaard.',['art-4','art-5','art-6','art-9','art-10','art-12'],[]),
'art-12':('1–3','Termijnankering na de dag van uitspraak toegevoegd. HR 2018:1100 volledig gelezen: relatieve einduitspraak, beperkte rechterlijke-foutuitzondering en daadwerkelijke niet-ontvankelijkheid verantwoord.',['art-10'],['ECLI:NL:HR:2018:1100']),
'art-13':('1–2','Materiële correctie: geen openbare aankondiging als grens; verwijzing naar kennisgeving artikel 15. Verbod op akkoordraadpleging onderscheiden van vereffening met toestemming.',['art-4','art-13a','art-14','art-15'],[]),
'art-13a':('ongesplitst','Ook overeengekomen regels expliciet opgenomen; vernietiging zelf als wettelijk aanvangsmoment, zonder nieuwe termijnduur of automatische ongeldigheid te poneren.',['art-13'],[]),
'art-14':('1–5, 5a–b','Meervoudige benoeming, inhoud publicatie, Nederlandse vestiging, vier toegelaten talen en afzonderlijke onderdelen van de aanstellingscriteria uitgewerkt. Minuutregistratie wijzigt dagwerking artikel 23 niet.',['art-5','art-23'],[]),
'art-14b':('ongesplitst','Geen wijziging nodig: afzonderlijk en gezamenlijk optreden correct onderscheiden van een uitbreiding van de wettelijke bevoegdheden; voorbeeld blijft binnen toezichtstaak.',[],[])
}
oldparts=re.split(r'(?m)^=== (\S+)\s*\n',(W/'sources/review-art-1-14b-commentary-before.txt').read_text())
old={oldparts[i]:oldparts[i+1].strip() for i in range(1,len(oldparts),2)}
new=load_commentary(str(W));before_hash=json.loads((W/'sources/review-art-1-14b-before-hashes.json').read_text())
assert list(old)==ids and list(notes)==ids and len(ids)==20
rows=[]
for key in ids:
 assert hashlib.sha256(old[key].encode()).hexdigest()==before_hash[key]
 assert new.get(key) and key in by
 for ref in notes[key][2]:assert ref in by
 rows.append({'id':key,'official_path':by[key]['official_path'],'source_paragraphs_reviewed':notes[key][0],'source_notes_reviewed':by[key]['notes'],'source_effective_from':by[key]['effective_from'],'statutory_text_sha256':hashlib.sha256(by[key]['text'].encode()).hexdigest(),'commentary_before_sha256':before_hash[key],'commentary_after_sha256':hashlib.sha256(new[key].encode()).hexdigest(),'result':'corrected' if new[key]!=old[key] else 'accepted_without_change','assessment':notes[key][1],'internal_cross_references_checked':notes[key][2],'case_authorities_checked':notes[key][3],'unresolved_blockers':[]})
checks={'checked_at_utc':now,'source_records':'sources/review-art-1-14b-fetch.json','official_source_sha256':sha(W/'sources/review-art-1-14b-selected.xml'),'selected_version':'2026-09-01_0','decisive_date':'2026-10-19','current_validity_statements':['Geraadpleegd op 20-10-2026.','Geldend van 01-09-2026 t/m heden.'],'latest_effective_change':'2026-09-01','next_dated_change_excluded':'2027-11-15','changes_since_intake':[],'historical_version_excluded':{'path':'sources/version-register.xml','effective_from':historical.get('inwerkingtreding'),'sha256':sha(W/'sources/version-register.xml')},'expected_official_count':len(expected),'parsed_count':len(parsed),'whole_source_token_agreement':True,'annex_disposition':comp['annexes'],'opening_closing_text_checks':comp['non_article_text'],'source_coverage_report':'completeness-report.json','parser_idempotent_verified':True,'local_case_2018_1100_core_equal':True,'reviewed_ids':ids,'reviewed_count':20,'commentaries_changed':sum(row['result']=='corrected' for row in rows),'unresolved_blockers':[],'ok':True}
save(W/'review-checks.json',checks)
# Preserve prior report on reruns only through git; this script is the bounded review record.
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'max_units':20,'checked_at_utc':now,'decisive_date':'2026-10-19','official_url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01','whole_book_complete':False,'unresolved_blockers':[],'findings':rows,'limitations':['Only the exact 20 assigned article places were substantively reviewed; no conclusion about the other 619 places.','The 342 unwritten commentaries remain out of scope; shared full-book build and validator are expected to fail for that reason.','Case-law research is selective: the 2018:774 judgment was reread and 2018:1100 was newly read in full against official XML and the national corpus. No exhaustive later-case search.','External Rv, BW and EU provisions are only referred to within the scope expressly stated by the reviewed Faillissementswet text; this review does not certify their complete independent treatment.','Official editorial references to external transitional acts are preserved but no general review of legacy proceedings under those acts is claimed.','This is a fresh-process substantive second reading, not external professional approval.'],'technical_evidence':'review-checks.json','commentary_before_snapshot':'sources/review-art-1-14b-commentary-before.txt','changed_units':[row['id'] for row in rows if row['result']=='corrected'],'accepted_without_change':[row['id'] for row in rows if row['result']=='accepted_without_change']}
# Retain validation results already recorded if rerunning integrity checks without prose changes.
p=W/'review-result.json'
if p.exists():
 prior=json.loads(p.read_text())
 if prior.get('findings')==rows and 'validation' in prior:result['validation']=prior['validation']
save(p,result)
print(json.dumps({'reviewed':20,'changed':checks['commentaries_changed'],'accepted_unchanged':20-checks['commentaries_changed'],'scope_complete':True,'whole_book_complete':False,'source_checks_ok':True}))
