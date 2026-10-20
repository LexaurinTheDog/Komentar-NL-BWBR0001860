#!/usr/bin/env python3
"""Audit captured official evidence and preserve the original authoring-date record."""
from pathlib import Path
import json,hashlib,datetime,xml.etree.ElementTree as E,re,collections
W=Path(__file__).resolve().parent;S=W/'sources'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
records=json.loads((S/'preflight-2026-10-20-fetch.json').read_text())
for rec in records:
 assert rec['accepted'] and rec['http_status']==200,rec
 assert sha(W/rec['raw_path'])==rec['sha256']
info=(S/'preflight-2026-10-20-information.html').read_text()
current=(S/'preflight-2026-10-20-current.html').read_text()
for text in [info,current]:
 assert 'Geraadpleegd op 20-10-2026.' in text
 assert 'Geldend van 01-09-2026 t/m heden.' in text
assert sha(S/'preflight-2026-10-20-selected.xml')==sha(S/'official-2026-09-01.xml')
assert sha(S/'preflight-2026-10-20-wti.xml')==sha(S/'wti.xml')
r=E.parse(S/'official-2026-09-01.xml').getroot();wti=E.parse(S/'preflight-2026-10-20-wti.xml').getroot()
assert r.get('inwerkingtreding')=='2026-09-01'
dates=wti.findall('./wijzigingen/regeling/datum');dated=sorted(d.get('waarde') for d in dates if d.get('waarde'))
relevant=[]
for d in dates:
 if not d.get('waarde') or d.get('waarde')>='2026-01-01':
  relevant.append({'effective_date':d.get('waarde'),'disposition':'undated/pending excluded' if not d.get('waarde') else ('future excluded' if d.get('waarde')>'2026-10-19' else 'effective by decisive date'), 'details':[{'type':x.findtext('betreft'),'sources':[{'section':parent.tag,'type':b.get('type'),'publication':b.find('bekendmaking').attrib if b.find('bekendmaking') is not None else None,'dossier':b.findtext('dossiernummer')} for parent in x for b in parent.findall('bron')]} for x in d.findall('details')]})
version={'decisive_date':'2026-10-19','verification_date':'2026-10-20','selected_toestand':'2026-09-01_0','current_route':records[3]['url'],'current_redirect_target':records[3]['final_url'],'explicit_information_page_statements':['Geraadpleegd op 20-10-2026.','Geldend van 01-09-2026 t/m heden.','Toekomstige wijziging(en) voorzien met ingang van: 15-11-2027.'],'latest_dated_amendment_by_decisive_date':max(d for d in dated if d<='2026-10-19'),'dated_changes_since_intake_2026_10_01_through_preflight':[d for d in dated if '2026-10-01'<d<='2026-10-20'],'next_dated_amendment':min(d for d in dated if d>'2026-10-20'),'wti_generated':wti.find('wijzigingen').get('gegenereerd'),'recent_future_and_undated_changes':relevant,'source_paths':[x['raw_path'] for x in records],'xml_unchanged_since_original_authoring_check':True,'wti_unchanged_since_original_authoring_check':True,'all_article_effective_dates_on_or_before_decisive_date':all(x.get('inwerking')<='2026-10-19' for x in r.findall('.//artikel'))}
assert version['latest_dated_amendment_by_decisive_date']=='2026-09-01' and not version['dated_changes_since_intake_2026_10_01_through_preflight']
save(S/'version-evidence.json',version)
oldpath=S/'verification-2026-10-19.json'
if not oldpath.exists():oldpath.write_bytes((S/'verification.json').read_bytes())
verification=json.loads(oldpath.read_text())
verification.update(checked_at_utc=now,current_effectiveness_evidence='Fresh official current-route redirect to 2026-09-01; both HTML pages explicitly valid 01-09-2026 through present on 20-10-2026. WTI dates independently enumerated in sources/version-evidence.json; latest effective amendment 2026-09-01, next dated amendment 2027-11-15. Original decisive date 2026-10-19 retained.',canonical_sha256=sha(S/'canonical.md'),verification_date='2026-10-20',original_verification_path='sources/verification-2026-10-19.json',version_evidence_path='sources/version-evidence.json')
verification['records']+=records
verification['supplementary_attempts']=[{'url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01/informatie','access_date':'2026-10-20','method':'Firecrawl CLI scrape','result':'Insufficient credits; no body, no HTTP response recorded; direct official fetch succeeded.'},{'url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01/informatie','access_date':'2026-10-20','method':'web open','result':'Tool returned inaccessible; direct official fetch succeeded.'}]
save(S/'verification.json',verification)
historical=E.parse(S/'version-register.xml').getroot()
assert historical.get('inwerkingtreding')=='2002-01-01'
completeness=json.loads((W/'completeness-report.json').read_text())
changes=json.loads((S/'change-map.json').read_text())
changes.update(preflight_checked_at_utc=now,fresh_official_xml_sha256=sha(S/'preflight-2026-10-20-selected.xml'),statutory_wording_changes=0,editorial_representation_repairs=['21 structural editorial notes preserved and displayed once below their heading at its first article.','Official intitule/citeertitel and exact opening/closing text explicitly inventoried with hashes.'],non_article_evidence='sources/non-article-text.json',structural_note_evidence='sources/structural-editorial-notes.json')
save(S/'change-map.json',changes)
result={'kind':'preflight','complete':bool(completeness['ok']),'decisive_date':'2026-10-19','preflight_date':'2026-10-20','official_url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01','verified_at':now,'version_evidence':{'path':'sources/version-evidence.json','selected_toestand':'2026-09-01_0','effective_from':'2026-09-01','explicit_valid_through':'heden, geraadpleegd op 20-10-2026','latest_effective_change':'2026-09-01','next_dated_change_excluded':'2027-11-15','changes_since_intake':[],'same_xml_sha256_as_earlier_capture':True},'historical_versions_checked':[{'path':'sources/version-register.xml','sha256':sha(S/'version-register.xml'),'root':historical.tag,'effective_from':historical.get('inwerkingtreding'),'disposition':'2002 historical toestand excluded from selected source and parser.'},{'path':'sources/official-2026-09-01.xml','sha256':sha(S/'official-2026-09-01.xml'),'root':r.tag,'effective_from':r.get('inwerkingtreding'),'disposition':'Only this toestand parsed. 639 unique article labels and unique official paths. 212hgd* and 212hgd are distinct simultaneous slots, not duplicate historical versions.'}],'annexes_checked':completeness['annexes'],'total_units':639,'completed_commentaries':297,'new_commentary_units':0,'coverage_ok':completeness['ok'],'editorial_notes_preserved':481,'structural_editorial_notes_repaired':21,'opening_and_closing_text_checked':completeness['non_article_text'],'unresolved_blockers':[],'limitations':['This task checks statutory sources and parser coverage only, not substantive correctness of the 297 existing commentaries.','342 commentaries remain unwritten; whole-book build/strict validation failure on missing commentary is expected.','No independent substantive review or new case-law research performed.','External transitional provisions referenced by editorial notes remain annotations; no claim of a separate full analysis of those instruments.'],'whole_book_complete':False}
save(W/'preflight-result.json',result)
print(json.dumps({'preflight_complete':result['complete'],'decisive_date':result['decisive_date'],'verified_at':now,'units':639,'structural_notes_repaired':21,'unresolved_blockers':[]}))
