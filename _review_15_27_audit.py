"""Integrity evidence for the bounded manual second reading of art-15 through art-27.
Manual legal assessments are recorded below; script success is not legal approval.
"""
from pathlib import Path
import json,re,hashlib,datetime,xml.etree.ElementTree as E,sys,collections
W=Path(__file__).resolve().parent
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_commentary
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ids=['art-'+i for i in ['15','15a','15b','15c','15d','16','17','18','19','19a','19b','20','21','22','22a','23','24','25','26','27']]
records=json.loads((W/'sources/review-art-15-27-fetch.json').read_text())
for r in records:
 assert r['accepted'] and r['http_status']==200,r
 assert sha(W/r['raw_path'])==r['sha256'],r
 if 'hr-' in r['raw_path']:assert E.parse(W/r['raw_path']).getroot().find('{*}uitspraak') is not None
raw=W/'sources/review-art-15-27-selected.xml';root=E.parse(raw).getroot()
assert root.tag=='toestand' and root.get('bwb-id')=='BWBR0001860' and root.get('inwerkingtreding')=='2026-09-01'
assert sha(raw)==sha(W/'sources/official-2026-09-01.xml')
h=(W/'sources/review-art-15-27-current.html').read_text()
assert 'Geldend van 01-09-2026 t/m heden.' in h and 'Geraadpleegd op 20-10-2026.' in h
wt=E.parse(W/'sources/review-art-15-27-wti.xml').getroot()
dates=sorted({e.get('waarde') for e in wt.findall('./wijzigingen/regeling/datum') if e.get('waarde')})
assert max(d for d in dates if d<='2026-10-19')=='2026-09-01'
assert not [d for d in dates if '2026-10-01'<d<='2026-10-20']
assert min(d for d in dates if d>'2026-10-20')=='2027-11-15'
historical=E.parse(W/'sources/version-register.xml').getroot();assert historical.get('inwerkingtreding')=='2002-01-01'
expected=['art-'+a.get('label').removeprefix('Artikel ') for a in root.findall('.//artikel')]
units=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()];by={u['id']:u for u in units}
assert expected==[u['id'] for u in units] and len(expected)==len(set(expected))==639
assert not [e for e in root.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
def tokens(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+tokens(c)+' '+(c.tail or '') for c in e)
norm=lambda s:re.sub(r'\s+','',s)
for a in root.findall('.//artikel'):
 key='art-'+a.get('label').removeprefix('Artikel ')
 assert norm(tokens(a))==norm(by[key]['text']),key
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
parser_before=json.loads((W/'sources/review-art-15-27-parser-before.json').read_text())
assert all(sha(W/p)==v for p,v in parser_before.items())
case_comparison=json.loads((W/'sources/review-art-15-27-case-comparison.json').read_text())
for r in case_comparison:
 assert r['normalized_comparison_equal'] and sha(W/r['official_raw_path'])==r['official_sha256'] and sha(W/r['local_snapshot_path'])==r['local_sha256']
# A metadata-only HTTP-200 reply was rejected, not cited.
rejected=json.loads((W/'sources/review-art-15-27-first-fetch.json').read_text())
assert any('2015-1401' in r['raw_path'] and not r['accepted'] and r['full_uitspraak_chars']==0 for r in rejected)
notes={
'art-15':('1–3','Materieel herstel: kennisgeving artikel 15 onderscheiden van openbare aankondiging bij de beschermingsgrens van artikel 13. Wachtvoorwaarde niet op cassatie geplakt; overeenkomstige salaris- en zienswijzeregel artikel 71 lid 3 toegevoegd.',['art-13','art-71'],[]),
'art-15a':('ongesplitst','Ongewijzigd aanvaard. Omgekeerde procesgang (eerst afwijzing, dan faillietverklaring in beroep/cassatie), oorspronkelijke griffie als ontvanger en ontbreken van nieuw rechtsmiddel correct onderscheiden.',['art-14','art-15'],[]),
'art-15b':('1–6, lid 3 a–c','Beide toegangsroutes en beide afsnijmomenten uitgewerkt. Alle drie uitsluitingen afzonderlijk genoemd; afwijking van partner-medewerking artikel 284 lid 3 en bevoegdheid partner via 6 lid 2 verduidelijkt. Definitieve toepassing, aankondiging en verval geplande vergadering behouden.',['art-3','art-6','art-15c','art-15d','art-108','art-137a','art-284','art-293','art-340'],[]),
'art-15c':('1–5','Exacte indienings-, behandel- en uitspraakankers uitgeschreven: acht dagen na uitspraak, twintig dagen na indiening, acht dagen na zitting en cassatie acht dagen na uitspraak. Alleen de in lid 5 omschreven aanhangige procesfasen als blokkade aangeduid; geen algemeen vereffeningsverbod afgeleid.',['art-13','art-15b'],[]),
'art-15d':('1 a–c, 2','Ongewijzigd aanvaard. Handelingen, boedelschuldkarakter en indiening onderscheiden; ingediende vordering niet als erkend voorgesteld. Voor 43/45 blijft oorspronkelijke faillissementsdatum bepalend.',['art-43','art-45'],[]),
'art-16':('1–4','Kostenlast schuldenaar en bijzondere voorrang expliciet gemaakt. Overeenkomstige efficiëntie- en zienswijzeregel 71 lid 3 en taak griffier bij staatsdeel publicatiekosten toegevoegd. Kostenvaststelling en opheffing blijven onderscheiden voor rechtsmiddelen.',['art-17','art-18','art-71'],[]),
'art-17':('ongesplitst','Ongewijzigd aanvaard. Vrijstelling beperkt tot griffiekosten na bevel artikel 16; geen staatsgarantie voor salaris of uitwissing van andere schulden gesuggereerd. Kosteloze behandeling onderscheiden van opheffing.',['art-16'],[]),
'art-18':('ongesplitst, beide zinnen','Ongewijzigd aanvaard. Publicatie en rechtsmiddelen tegen opheffing onderscheiden van onaanvechtbare kostenvaststelling. Driejaarstermijn alleen bij aanvraag, niet bij eigen aangifte; voldoende baten voor kosten blijven te bewijzen.',['art-9','art-12','art-14','art-16'],[]),
'art-19':('1 onderdelen 1°–8°, 2–4','Registratie per faillissement met dagtekening en alle acht categorieën expliciet gemaakt, inclusief bijzondere opheffingen 15b/16 en aanwijzing bij of krachtens AMvB. Registreren, doorgeven en registerhouden gescheiden; kosteloze inzage voor ieder correct.',['art-5','art-14','art-15b','art-16','art-19a'],[]),
'art-19a':('ongesplitst','Ongewijzigd aanvaard. Minister of aangewezen ander orgaan als registerhouder; aanlevertaak griffie en oorspronkelijke rechterlijke beslissing correct onderscheiden.',['art-19'],[]),
'art-19b':('ongesplitst','Ongewijzigd aanvaard. Griffier Den Haag registreert de specifieke buitenlandse procedure van 14 lid 4; registratie niet als zelfstandige Nederlandse faillietverklaring behandeld.',['art-14'],[]),
'art-20':('ongesplitst','Ongewijzigd aanvaard. Aanwezig vermogen en verkrijging tijdens faillissement, eigendomsvraag en uitzonderingen onderscheiden; verkrijging van erfenis niet louter wegens later moment uitgesloten.',['art-21','art-22a','art-23'],[]),
'art-21':('1°–7°','Ontbrekende auteursrechtuitzondering, onderhoud krachtens wettelijke plicht en reikwijdte inkomenscategorieën toegevoegd. Vruchtgenot, specifieke consignatie en fiscale kwalificatie per onderdeel onderscheiden; externe verwijzingen niet als zelfstandig integraal onderzochte regimes gepresenteerd.',['art-20','art-60a'],[]),
'art-22':('ongesplitst','Ongewijzigd aanvaard. Gelijkstelling partner alleen voor voorafgaand artikel, onder voorwaarde enige gemeenschap; geen eigen faillissement of beslag op alle privégoederen afgeleid.',['art-21'],[]),
'art-22a':('1 a–c, 2–5','Voorwaarden afkoop en begunstigingswijziging afzonderlijk uitgewerkt, maximumbedrag en schriftelijke overdrachtstoestemming toegevoegd. Latere onherroepelijkheid, vasthouden, uitzondering bij vaststaande niet-wijziging en toegang via 69 uitgewerkt. Bewijslast verzekeraarskennis en verhaal op begunstigde onderscheiden. Volledig gelezen HR 2017:2564 ondersteunt begrensde verzorgingsuitleg.',['art-20','art-69'],['ECLI:NL:HR:2017:2564']),
'art-23':('ongesplitst','Ongewijzigd aanvaard. Dagwerking omvat gehele faillissementsdag; geen algemene handelingsonbekwaamheid aangenomen. Levering en eventuele derdenbescherming blijven afzonderlijke vragen.',['art-20','art-35'],[]),
'art-24':('ongesplitst','Ontstaan niet beperkt tot vrijwillig aangaan; factuurdatum en opeisbaarheid onderscheiden van ontstaan. Baatbegrenzing en ontbreken van herstel beschikkingsmacht toegevoegd. Boedelschuld uit curatorhandelen onderscheiden met opnieuw gelezen BY6108.',['art-23'],['ECLI:NL:HR:2013:BY6108']),
'art-25':('1–2','Procespositie aan beide zijden expliciet; verificatieroute beperkt tot verifieerbare vorderingen zodat zelfstandige boedelvordering niet ten onrechte uitgesloten wordt. Geen-rechtskrachtregel tegenover boedel en bijzondere lopende-procesregels behouden.',['art-23','art-26','art-27','art-28','art-29','art-30'],[]),
'art-26':('ongesplitst','Te brede openingszin beperkt tot vorderingen op schuldenaar die ter verificatie worden ingediend; zelfstandige boedelvorderingen uitdrukkelijk onderscheiden. Opnieuw gelezen HR BY6108 ondersteunt afbakening, niet een algemene voorrang voor later ontstane schuld.',['art-25','art-29','art-110'],['ECLI:NL:HR:2013:BY6108']),
'art-27':('1–3','Rechterlijke oproepingstermijn en uitzondering artikel 30 toegevoegd. Stilzwijgen curator geeft recht ontslag te vragen, geen automatische toewijzing. HR BA5197 volledig gelezen: belangenafweging en goede procesorde, cassatie-incident onderscheiden van definitieve beoordeling hofklacht.',['art-29','art-30'],['ECLI:NL:HR:2007:BA5197'])
}
before_hash=json.loads((W/'sources/review-art-15-27-before-hashes.json').read_text())
parts=re.split(r'(?m)^=== (\S+)\s*\n',(W/'sources/review-art-15-27-commentary-before.txt').read_text());old={parts[i]:parts[i+1].strip() for i in range(1,len(parts),2)}
new=load_commentary(str(W));assert list(old)==list(notes)==ids
outside=[i for i,t in new.items() if i not in ids and hashlib.sha256(t.encode()).hexdigest()!=before_hash[i]];assert not outside
rows=[]
for key in ids:
 assert hashlib.sha256(old[key].encode()).hexdigest()==before_hash[key]
 for ref in notes[key][2]:assert ref in by
 rows.append({'id':key,'official_path':by[key]['official_path'],'source_paragraphs_reviewed':notes[key][0],'source_notes_reviewed':by[key]['notes'],'source_effective_from':by[key]['effective_from'],'statutory_text_sha256':hashlib.sha256(by[key]['text'].encode()).hexdigest(),'commentary_before_sha256':before_hash[key],'commentary_after_sha256':hashlib.sha256(new[key].encode()).hexdigest(),'result':'corrected' if new[key]!=old[key] else 'accepted_without_change','assessment':notes[key][1],'internal_cross_references_checked':notes[key][2],'case_authorities_checked':notes[key][3],'unresolved_blockers':[]})
checks={'checked_at_utc':now,'source_records':'sources/review-art-15-27-fetch.json','official_source_sha256':sha(raw),'selected_version':'2026-09-01_0','decisive_date':'2026-10-19','current_validity_statements':['Geraadpleegd op 20-10-2026.','Geldend van 01-09-2026 t/m heden.'],'latest_effective_change':'2026-09-01','next_dated_change_excluded':'2027-11-15','changes_since_intake':[],'historical_version_excluded':{'path':'sources/version-register.xml','effective_from':'2002-01-01','sha256':sha(W/'sources/version-register.xml')},'expected_official_count':639,'parsed_count':639,'whole_source_token_agreement':True,'annex_disposition':comp['annexes'],'opening_closing_text_checks':comp['non_article_text'],'source_coverage_report':'completeness-report.json','parser_idempotent_verified':True,'unassigned_commentaries_unchanged':True,'case_comparison':'sources/review-art-15-27-case-comparison.json','rejected_metadata_only_case':'sources/review-art-15-27-first-fetch.json','reviewed_ids':ids,'reviewed_count':20,'commentaries_changed':sum(r['result']=='corrected' for r in rows),'unresolved_blockers':[],'ok':True}
save(W/'review-checks.json',checks)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'max_units':20,'checked_at_utc':now,'decisive_date':'2026-10-19','official_url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01','whole_book_complete':False,'unresolved_blockers':[],'findings':rows,'limitations':['Exactly these 20 assigned units were substantively reviewed in this process. Earlier review of 20 different units is preserved separately, not repeated or claimed as work of this process.','342 unwritten commentaries and their expected full-book build/validator failure remain outside this bounded task.','Selective case research only: two additional full HR judgments and the existing BY6108 decision reread. No exhaustive later-case search or assertion that every technical unit lacks relevant authority.','Cross-referenced external Rv, BW, fiscal and EU rules are not independently reconstructed; official cross-references and source transitional notes are retained without certification of all external regimes.','Fresh-process second reading, not external professional approval. Minimum length and script success do not certify legal quality.'],'technical_evidence':'review-checks.json','commentary_before_snapshot':'sources/review-art-15-27-commentary-before.txt','previous_batch_result':'sources/review-art-1-14b-result.json','changed_units':[r['id'] for r in rows if r['result']=='corrected'],'accepted_without_change':[r['id'] for r in rows if r['result']=='accepted_without_change']}
p=W/'review-result.json'
if p.exists():
 prior=json.loads(p.read_text())
 if prior.get('findings')==rows and 'validation' in prior:result['validation']=prior['validation']
save(p,result)
print(json.dumps({'scope_complete':True,'reviewed':20,'changed':checks['commentaries_changed'],'unassigned_unchanged':True,'statutory_token_agreement':True,'whole_book_complete':False}))
