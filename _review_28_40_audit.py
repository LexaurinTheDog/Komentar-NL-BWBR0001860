"""Reproduce integrity checks for the manually reviewed, exact art-28–40 batch.
The assessments record a manual second reading; assertions are not legal certification.
"""
from pathlib import Path
import json,re,hashlib,datetime,xml.etree.ElementTree as E,sys
W=Path(__file__).resolve().parent
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_commentary
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ids=['art-'+i for i in ['28','29','30','31','32','33','33a','34','35','35a','35b','36','36a','37','37a','37b','38','38a','39','40']]
records=json.loads((W/'sources/review-art-28-40-fetch.json').read_text())
for rec in records:
 assert rec['accepted'] and rec['http_status']==200,rec
 assert sha(W/rec['raw_path'])==rec['sha256']
 if rec['raw_path'].endswith('.xml'):
  root=E.parse(W/rec['raw_path']).getroot()
  assert root.tag.split('}')[-1] in {'toestand','wetstechnische-informatie','open-rechtspraak'}
  if 'hr-' in rec['raw_path']:assert root.find('{*}uitspraak') is not None
raw=W/'sources/review-art-28-40-selected.xml';root=E.parse(raw).getroot()
assert root.get('bwb-id')=='BWBR0001860' and root.get('inwerkingtreding')=='2026-09-01'
assert sha(raw)==sha(W/'sources/official-2026-09-01.xml')
h=(W/'sources/review-art-28-40-current.html').read_text()
assert 'Geraadpleegd op 20-10-2026.' in h and 'Geldend van 01-09-2026 t/m heden.' in h
wt=E.parse(W/'sources/review-art-28-40-wti.xml').getroot()
dates=sorted({e.get('waarde') for e in wt.findall('./wijzigingen/regeling/datum') if e.get('waarde')})
assert max(d for d in dates if d<='2026-10-19')=='2026-09-01'
assert not [d for d in dates if '2026-10-01'<d<='2026-10-20']
assert min(d for d in dates if d>'2026-10-20')=='2027-11-15'
historical=E.parse(W/'sources/version-register.xml').getroot();assert historical.get('inwerkingtreding')=='2002-01-01'
expected=['art-'+a.get('label').removeprefix('Artikel ') for a in root.findall('.//artikel')]
# Second official enumeration is HTML TOC text, not the parser or its identifiers.
import html
html_ids=['art-'+html.unescape(re.sub('<[^>]+>','',t)).strip().removeprefix('Artikel ') for t in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',h)]
units=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()];by={u['id']:u for u in units}
assert expected==html_ids==[u['id'] for u in units] and len(expected)==len(set(expected))==639
assert not [e for e in root.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
assert not re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>[^<]*(?:Bijlage|Annex)',h)
def tokens(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+tokens(c)+' '+(c.tail or '') for c in e)
norm=lambda s:re.sub(r'\s+','',s)
for a in root.findall('.//artikel'):
 key='art-'+a.get('label').removeprefix('Artikel ')
 assert norm(tokens(a))==norm(by[key]['text']),key
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
assert len(comp['repealed_slots'])==57 and comp['editorial_notes']==481
parser_before=json.loads((W/'sources/review-art-28-40-parser-before.json').read_text())
assert all(sha(W/p)==v for p,v in parser_before.items())
casecomp=json.loads((W/'sources/review-art-28-40-case-comparison.json').read_text())
for rec in casecomp:
 assert rec['normalized_corpus_body_is_official_suffix']
 assert sha(W/rec['official_raw_path'])==rec['official_sha256'] and sha(W/rec['local_snapshot_path'])==rec['local_sha256']
 u=E.parse(W/rec['official_raw_path']).getroot().find('{*}uitspraak')
 local=(W/rec['local_snapshot_path']).read_text().split('## Uitspraak\n\n',1)[1]
 assert norm(''.join(u.itertext())).endswith(norm(local))
notes={
'art-28':('1–4','Oproepingstermijn, uitzondering artikel 30, beperking tot proceskosten bij onmiddellijke instemming en precieze rechtskracht bij niet-verschijning verduidelijkt. Geen automatische toewijzing of executierecht afgeleid.',['art-25','art-29','art-30','art-33'],[]),
'art-29':('ongesplitst','Schorsing beperkt tot verifieerbare faillissementsvorderingen; zelfstandige boedelvorderingen onderscheiden. Artikel 30 en noodzaak van betwisting vóór voortzetting toegevoegd. Gemengde eisen per onderdeel beoordelen.',['art-26','art-27','art-28','art-30'],[]),
'art-30':('1–2','Ongewijzigd aanvaard. Stukken voor beslissing vóór faillietverklaring, uitsluiting 25 lid 2 en 27–29, hervatting bij dezelfde rechter na diens beslissing en geen zelfstandige executievoorrang correct.',['art-25','art-27','art-28','art-29','art-33'],[]),
'art-31':('ongesplitst','Ongewijzigd aanvaard. Specifieke voortgezette procedure, voorafgaande proceshandeling, bewuste benadeling en kennis wederpartij vereisen bewijs; geen louter objectief nadelige proceskeuze. Vergelijking met 42 is onderscheid, geen gelijkstelling van bewijsmaatstaven.',['art-29','art-42'],[]),
'art-32':('ongesplitst','Ongewijzigd aanvaard. Overeenkomstige toepassing beperkt tot rechtsvordering over concreet goed/recht met verlies beheer en beschikking door erkende procedure. EU-artikel 19 en nationaal registerartikel onderscheiden; geen groepsbrede schorsing afgeleid.',['art-5','art-19','art-27','art-28','art-29','art-30','art-31'],[]),
'art-33':('1–4','Onherroepelijkheid als moment voor ontslag uit bestaande gijzeling expliciet toegevoegd. Verval/doorhaling/herleving met exploot en veertiendagentermijn gescheiden. Lijfsdwanguitzondering niet als vrijstelling van collectief geldverhaal voorgesteld; 57 en 34 afgebakend.',['art-14','art-34','art-57','art-87'],[]),
'art-33a':('Vervallen','Ongewijzigd aanvaard. Actueel vervallen slot behouden; geen historische inhoud als huidig recht ingevuld. Historisch dossier vergt afzonderlijke datumcontrole.',['art-33','art-34'],[]),
'art-34':('ongesplitst','Ongewijzigd aanvaard. Verkoopdag al vóór faillissement bepaald, keuze curator, machtiging rechter-commissaris en verkoop voor boedelrekening correct cumulatief behandeld. Geen eigen executiebevoegdheid beslaglegger.',['art-33'],[]),
'art-35':('1–3','Dagwerking en afzonderlijke onvoltooide levering tegenover levering bij voorbaat uitgewerkt. Alle voorwaarden vruchten/beplantingen benoemd. Publicatiekennis leidt niet tot automatische bescherming vóór publicatie. Externe BW-verwijzingen als verwijzing behouden.',['art-14','art-23'],[]),
'art-35a':('ongesplitst','Ongewijzigd aanvaard. Alleen het in 6:252 BW bedoelde beding en ontbreken inschrijving op faillissementsdag; verkoop volgens 101/176. Geen bevoegdheid tot algemene lastenverwijdering gesuggereerd.',['art-101','art-176'],[]),
'art-35b':('ongesplitst','Ongewijzigd aanvaard. Gift, opschortende voorwaarde/tijdsbepaling en onvervuld/niet-verschenen op faillissementsdag onderscheiden. Geen recht tegen boedel; geen algemene pauliana of uitsluiting van elke betwiste schuld.',['art-42','art-45'],[]),
'art-36':('1–2','Ongewijzigd aanvaard. Reikwijdte artikel 26, aflopen tijdens faillissement of zes maanden daarna, doorloop tot zes maanden na einde en van rechtswege aanvangende vervaltermijnen correct. Geen herstel reeds voltooide verjaring of vervanging indieningsdeadline.',['art-26'],[]),
'art-36a':('ongesplitst','Inhoudelijke uitleg ongewijzigd aanvaard: alleen twee genoemde BW-termijnen, nog lopend bij faillietverklaring, redelijkerwijs noodzakelijke verlenging en nieuwe redelijke termijn wederpartij. Aan hoofdstukeinde concrete controlelijst toegevoegd voor procesroute, beslag, levering en termijnen.',['art-27','art-28','art-29','art-30','art-33','art-35','art-36'],[]),
'art-37':('1–3','Materieel aangescherpt: verlies nakomingsrecht volgens HR 2016:2729 beperkt tot nog niet geleverde tegenprestatie. Aanwezige betalingsbate en onvoltooide contractprestatie onderscheiden. Niet-gestanddoening is geen actieve beëindigingsbevoegdheid; 2014:1681 en 2018:424 volledig gecontroleerd. Schriftelijke termijn, zekerheid, 68 lid 3 en persoonlijke prestatie behouden.',['art-37a','art-68'],['ECLI:NL:HR:2013:BY6108','ECLI:NL:HR:2014:1681','ECLI:NL:HR:2016:2729','ECLI:NL:HR:2018:424']),
'art-37a':('ongesplitst','Latere beperking van de ruim geformuleerde uitspraak uit 2013 toegevoegd met 2018:424. Reeds besloten rechtspositie en ongeoorloofde uitbreiding aanspraken onderscheiden; geen automatische verificatie door oude contractdatum. Beide wettelijke categorieën en boedelschulden afgebakend.',['art-37'],['ECLI:NL:HR:2013:BY6108','ECLI:NL:HR:2018:424']),
'art-37b':('1–3','Ongewijzigd aanvaard. Vier benoemde voorzieningen en noodzakelijkheid, oude geldachterstand, oude tekortkoming en insolventie-/beslagclausule met goedvinden curator onderscheiden. Geen kosteloze nieuwe levering of algemene uitsluiting van iedere andere beëindigingsgrond geclaimd.',[],[]),
'art-38':('ongesplitst, beide zinnen','Ontbrekende cumulatieve voorwaarde dat het geval van artikel 37 zich voordoet toegevoegd. Automatische ontbinding onderscheiden van termijnstelling; niet elke termijnkoop beurswaar. Schade van wederpartij en boedel afzonderlijk, met volledig vooruitbetaalde prijs als afbakeningsvoorbeeld.',['art-37'],[]),
'art-38a':('1–3','Ontbindingsverklaring tegenover automatische ontbinding verduidelijkt, reikwijdte beperkt tot failliete huurkoper. Verschuldigd bedrag verkoper helder geformuleerd; teruggave, afrekening en rang onderscheiden zonder bedrag als vaststaand aan te nemen.',['art-37','art-38'],[]),
'art-39':('1–2','Driemaandstermijn geen minimum; vooruitbetaling, eindtijdstip, pacht en 68 lid 3 behouden. HR 2018:2067 vult onderscheid oude herstelclaim/actieve schending door curator aan. Boedelschuld en afzonderlijke persoonlijke aansprakelijkheid niet gelijkgesteld.',['art-68'],['ECLI:NL:HR:2013:BY6108','ECLI:NL:HR:2018:2067']),
'art-40':('1–3','Zes weken geen minimum, geen automatische beëindiging. Loon/premies vanaf faillissementsdag en agentuur onderscheiden. Ontbrekende machtiging 68/72 en eigen beroepstermijn 67 lid 2 uitgeschreven en van zes weken gescheiden. HR BY6108 slechts voor boedelschuld, niet modern arbeidsprocesrecht gebruikt.',['art-5','art-13a','art-67','art-68','art-72'],['ECLI:NL:HR:2013:BY6108'])}
assert list(notes)==ids
before=json.loads((W/'sources/review-art-28-40-before-hashes.json').read_text());new=load_commentary(str(W))
assert set(before)==set(new) and len(new)==297
assert all(hashlib.sha256(t.encode()).hexdigest()==before[key] for key,t in new.items() if key not in ids)
rows=[]
for key in ids:
 for ref in notes[key][2]:assert ref in by
 rows.append({'id':key,'official_path':by[key]['official_path'],'source_paragraphs_reviewed':notes[key][0],'source_notes_reviewed':by[key]['notes'],'source_effective_from':by[key]['effective_from'],'statutory_text_sha256':hashlib.sha256(by[key]['text'].encode()).hexdigest(),'commentary_before_sha256':before[key],'commentary_after_sha256':hashlib.sha256(new[key].encode()).hexdigest(),'result':'corrected_or_extended' if hashlib.sha256(new[key].encode()).hexdigest()!=before[key] else 'accepted_without_change','assessment':notes[key][1],'internal_cross_references_checked':notes[key][2],'case_authorities_checked':notes[key][3],'unresolved_blockers':[]})
checks={'checked_at_utc':now,'source_records':'sources/review-art-28-40-fetch.json','official_source_sha256':sha(raw),'decisive_date':'2026-10-19','selected_version':'2026-09-01_0','current_validity_statements':['Geraadpleegd op 20-10-2026.','Geldend van 01-09-2026 t/m heden.'],'latest_effective_change':'2026-09-01','next_dated_change_excluded':'2027-11-15','changes_since_intake':[],'historical_version_excluded':{'path':'sources/version-register.xml','effective_from':'2002-01-01','sha256':sha(W/'sources/version-register.xml')},'expected_official_count':639,'parsed_count':639,'fresh_official_html_toc_count':len(html_ids),'whole_source_token_agreement':True,'annex_disposition':comp['annexes'],'opening_closing_text_checks':comp['non_article_text'],'editorial_notes_preserved':481,'source_coverage_report':'completeness-report.json','parser_idempotent_verified':True,'unassigned_commentaries_unchanged':True,'case_comparison':'sources/review-art-28-40-case-comparison.json','reviewed_ids':ids,'reviewed_count':20,'commentaries_changed':sum(r['result']!='accepted_without_change' for r in rows),'unresolved_blockers':[],'ok':True}
save(W/'review-checks.json',checks)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'max_units':20,'checked_at_utc':now,'decisive_date':'2026-10-19','official_url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01','whole_book_complete':False,'unresolved_blockers':[],'findings':rows,'limitations':['Only the exact assigned 20 units were substantively reviewed in this process. Earlier 40 distinct unit reviews are preserved, not repeated or claimed as this process work.','342 unwritten commentaries remain outside this assignment; the full-book shared builder and validator cannot pass.','Case research is selective: four additional full HR decisions and BY6108 reread in official XML and the local national corpus. No exhaustive subsequent-case search or case-by-case absence claim.','Cross-referenced external Rv, BW and EU regimes have not been independently certified in full. The current Faillissementswet wording and its external references were checked; no Czech law is addressed.','Historical source and external transitional annotations are preserved; no comprehensive treatment of all legacy proceedings under other acts.','Fresh-process second reading, not external professional approval. No minimum-length or script result is a substitute for substantive review.'],'technical_evidence':'review-checks.json','commentary_before_snapshot':'sources/review-art-28-40-commentary-before.txt','previous_batch_result':'sources/review-art-15-27-result.json','changed_units':[r['id'] for r in rows if r['result']!='accepted_without_change'],'accepted_without_change':[r['id'] for r in rows if r['result']=='accepted_without_change']}
p=W/'review-result.json'
if p.exists():
 prior=json.loads(p.read_text())
 if prior.get('findings')==rows and 'validation' in prior:result['validation']=prior['validation']
save(p,result)
# Supplement prior preflight without erasing its previous source or review stages.
p=W/'preflight-result.json';pre=json.loads(p.read_text());pre['bounded_review_art_28_40_recheck']={'complete':True,'verified_at':now,'source_records':checks['source_records'],'decisive_date':'2026-10-19','selected_version':'2026-09-01_0','latest_effective_change':'2026-09-01','next_dated_change_excluded':'2027-11-15','historical_version_excluded':checks['historical_version_excluded'],'annexes_checked':checks['annex_disposition'],'opening_closing_text_checked':checks['opening_closing_text_checks'],'fresh_html_ids_agree':True,'parser_idempotent':True,'statutory_wording_changes':0,'unresolved_blockers':[]};save(p,pre)
save(W/'sources/review-art-28-40-preflight-result.json',{'complete':True,'decisive_date':'2026-10-19','official_url':result['official_url'],'verified_at':now,'version_evidence':{'selected_toestand':'2026-09-01_0','explicit_validity':checks['current_validity_statements'],'latest_effective_change':'2026-09-01','next_dated_change_excluded':'2027-11-15','changes_since_intake':[],'source_records':checks['source_records']},'historical_versions_checked':[checks['historical_version_excluded'],{'path':str(raw.relative_to(W)),'effective_from':'2026-09-01','sha256':sha(raw),'disposition':'Only selected current toestand parsed, 639 unique identifiers and paths.'}],'annexes_checked':checks['annex_disposition'],'opening_and_closing_text_checked':checks['opening_closing_text_checks'],'parser_idempotent':True,'coverage_complete':True,'unresolved_blockers':[],'limitations':['Source preflight only; substantive second reading exactly 20 assigned places.']})
print(json.dumps({'scope_complete':True,'reviewed':20,'changed_or_extended':checks['commentaries_changed'],'unassigned_unchanged':True,'statutory_token_agreement':True,'whole_book_complete':False}))
