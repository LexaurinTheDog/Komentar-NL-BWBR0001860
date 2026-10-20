from pathlib import Path
import sys,json,hashlib,re,datetime,xml.etree.ElementTree as E,html,subprocess,shutil,collections
W=Path(__file__).resolve().parent;sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_commentary,load_units
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ids=['art-212'+x for x in ['hg','hga','hgb','hgc','hgd*','hgd','hi','hj','hk','hl','hm','hn','ho','hp','hq','hr','i','j','k','l']]
c=load_commentary(str(W));units=load_units(str(W));by={u['id']:u for u in units};now=datetime.datetime.now(datetime.timezone.utc).isoformat();m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir'])
before=json.loads((W/'sources/review-art-212hg-212l-before-hashes.json').read_text())
assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
records=json.loads((W/'sources/review-art-212hg-212l-fetch.json').read_text());assert all(r['accepted'] and r['http_status']==200 and sha(W/r['raw_path'])==r['sha256'] for r in records)
raw=W/'sources/review-art-212hg-212l-selected.xml';root=E.parse(raw).getroot();assert sha(raw)==sha(W/'sources/official-2026-09-01.xml')
expected=['art-'+a.get('label').removeprefix('Artikel ') for a in root.iter('artikel')]
h=(W/'sources/review-art-212hg-212l-current.html').read_text();hi=['art-'+html.unescape(t).removeprefix('Artikel ') for t in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',h)]
assert expected==hi==[u['id'] for u in units] and len(expected)==len(set(expected))==639
assert 'Geldend van 01-09-2026 t/m heden.' in h
norm=lambda s:re.sub(r'\s+','',s)
def flatten(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+flatten(x)+' '+(x.tail or '') for x in e)
for a in root.iter('artikel'):assert norm(flatten(a))==norm(by['art-'+a.get('label').removeprefix('Artikel ')]['text'])
assert not [e for e in root.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
wt=E.parse(W/'sources/review-art-212hg-212l-wti.xml').getroot();dates=sorted({x.get('waarde') for x in wt.findall('./wijzigingen/regeling/datum') if x.get('waarde')})
assert max(d for d in dates if d<='2026-10-21')=='2026-09-01';assert not [d for d in dates if '2026-10-01'<d<='2026-10-21']
historical=json.loads((W/'sources/review-art-212hg-212l-historical.json').read_text());assert historical['accepted'] and sha(W/historical['raw_path'])==historical['sha256'];hr=E.parse(W/historical['raw_path']).getroot();assert hr.get('inwerkingtreding')=='2018-01-01'
old={a.get('label'):a for a in hr.iter('artikel')}
for k in ids[7:16]:assert old['Artikel '+k.removeprefix('art-')].find('lid') is not None or old['Artikel '+k.removeprefix('art-')].find('al') is not None;assert by[k]['text'].strip()=='Vervallen'
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
# Reproduce parser and separate completeness check, requiring byte-identical existing canonical products.
names=['units.jsonl','meta.json','coverage-evidence.json','completeness-report.json'];hashes={n:sha(W/n) for n in names}
for script in ['_parse.py','_coverage.py']:
 p=subprocess.run([sys.executable,str(W/script)],capture_output=True,text=True);assert p.returncode==0,p.stderr
assert hashes=={n:sha(W/n) for n in names}
save(W/'sources/review-art-212hg-212l-parser-check.json',{'ok':True,'reproduced_scripts':['_parse.py','_coverage.py'],'unchanged_hashes':hashes,'official_xml_sha256':sha(raw),'expected_ids':expected,'parsed_ids':[u['id'] for u in units],'missing':[],'duplicates':[]})
pre={'complete':True,'decisive_date':m['decisive_date'],'official_url':m['source_url'],'verified_at':now,'version_evidence':{'fresh_http_records':'sources/review-art-212hg-212l-fetch.json','effective_from':'2026-09-01','current_route_validity':'Geldend van 01-09-2026 t/m heden; official cached response consulted 20-10-2026; fetched 20 October UTC / 21 October Prague','changes_since_intake':[],'next_wti_date_excluded':min(d for d in dates if d>'2026-10-21')},'historical_versions_checked':[historical,{'path':'sources/version-register.xml','effective_from':E.parse(W/'sources/version-register.xml').getroot().get('inwerkingtreding'),'disposition':'Historical, excluded from current units.'},{'ids':['art-212hgd*','art-212hgd'],'disposition':'Distinct simultaneously effective XML article paths Artikel212hgd_1 and Artikel212hgd_2, not historical duplicates.'}],'annexes_checked':comp['annexes'],'opening_and_closing_text_checked':comp['non_article_text'],'coverage':{'official_count':639,'parsed_count':639,'missing':[],'duplicate_ids':[],'parser_reproduction':'sources/review-art-212hg-212l-parser-check.json'},'unresolved_blockers':[]}
save(W/'sources/review-art-212hg-212l-preflight-result.json',pre)
p=W/'preflight-result.json';z=json.loads(p.read_text());z['bounded_review_art_212hg_212l']=pre;save(p,z)
notes=[
('ongesplitst','Bijzondere summiere rechterlijke toets, niet automatisch DNB-verzoek; Europese onderdelen niet uit geheugen ingevuld.',['212hf','212ha']),
('1–2','Overgang geheel/deel bancaire verbintenissen; instemming derde wel nodig, anderen niet; machtiging versus wijziging.',['212hgb','212hgc']),
('1a–d;2–5','Geografisch en materieel bereik, iedere beschermde categorie, cliëntbeperking derivatenvermogen, uitsluiting schadevergoeding facultatief, hoor-/adviesroute, duur en verlenging uitgewerkt.',['176','212hga','212hgc']),
('1–3 en bronnoot','Staatscourant blijft vereist, andere bekendmaking geen vrijstelling daarvan; tweede dag, buitenlandse dienstenroutes; verzekeraars-overgang begrensd.',['212hga','212hgb']),
('1–2 en nummeringsnoot','Alle publicatiegegevens, aantallen dagbladen, taal, bijzondere EU/buitenlandse aanvullingen en onmiddellijke publicatie onderscheiden; DNB draagt voor maar benoemt niet.',['212hgd']),
('1–2','Verschillende geadresseerden: verkrijger onder lid1, bank/groep onder lid2; noodzakelijke faciliteiten en geen algemene gegevensvrijbrief.',['212hgd*']),
('1–2 en bronnoot','Limitatieve beschikkingen uitvoerbaar bij voorraad, artikel10 uitgesloten; geen fictief totaalverbod rechtsmiddelen.',['10','212hb','212hga','212hgb']),
]
for k in ids[7:16]:notes.append(('vervallen en bronnoot','Individuele historische inhoud gelezen in officiële toestand2018; huidige vervallen status gecontroleerd; XIVlid4 betreft oudere verzekeraars, geen algemene voortzetting bankregel.',[]))
notes += [
('ongesplitst en checklist','Vrijstelling uitsluitend DNB-verzoek bankfaillissement; geen algemene materiële of vertegenwoordigingsvrijstelling; checklist passend.',['5','212hgd*','212hgd']),
('a–b','Afschrift aan bank versus inhoud aan buitenlandse autoriteiten; verschillende vestigings-/dienstenroutes en verzoekstadium.',['212n']),
('ongesplitst','Vergunning bij faillietverklaring; ontwerp versus definitieve intrekking getoetst tegen daadwerkelijk gelezen Wft1:104lid5; geen vrije keuze of automatische intrekking.',[]),
('ongesplitst','Gelijktijdige aangewezen maatregel en eigen aangifte, verval van rechtswege; geen herleving of uitbreiding tot elk verzoek; XMLwijzigingsdatum21december2021 bevestigd.',[])]
assert len(notes)==20
rows=[]
for k,(paras,note,refs) in zip(ids,notes):
 for ref in refs:assert 'art-'+ref in by
 assert c[k] and len(c[k])>=(120 if by[k]['text'].strip()=='Vervallen' else 400)
 rows.append({'id':k,'official_path':by[k]['official_path'],'source_paragraphs_reviewed':paras,'source_notes_reviewed':by[k].get('notes',[]),'assessment':note,'internal_cross_references_checked':['art-'+r for r in refs],'case_authorities_checked':[],'result':'corrected_or_extended' if hashlib.sha256(c[k].encode()).hexdigest()!=before[k] else 'accepted_without_change','commentary_before_sha256':before[k],'commentary_after_sha256':hashlib.sha256(c[k].encode()).hexdigest(),'statutory_text_sha256':hashlib.sha256(by[k]['text'].encode()).hexdigest()})
paragraphs=collections.defaultdict(list)
for k in ids:
 for para in c[k].split('\n\n'):
  if len(para)>200:paragraphs[para].append(k)
assert not [v for v in paragraphs.values() if len(v)>1]
validation=json.loads((W/'sources/review-art-212hg-212l-validation.txt').read_text());assert validation['verbatim_ratio']==1.0
save(W/'sources/review-art-212hg-212l-validation.json',validation)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'limitations':['Only these twenty units independently reviewed in this process; no whole-book approval or external lawyer approval.','No sufficiently relevant verified full-text case found in selective official-web and local HR corpus searches; no judgment or holding attributed. No exhaustive case-law or subsequent-treatment claim.','SRM, EU financial-collateral and securities-law instruments not separately certified in full; their statutory references preserved without invented contents. Wft1:104lid5 checked against saved official full HTML.','339 missing commentaries elsewhere prevent a successful whole-book build and strict validation; batch has all twenty substantive comments and statutory agreement is 100%.'],'whole_book_complete':False,'review_date_local':'2026-10-21','checked_at_utc':now,'changed_units':[r['id'] for r in rows if r['result']=='corrected_or_extended'],'validation_result':validation}
checks={'ok':True,'reviewed_ids':ids,'reviewed_count':20,'commentary_chars':{k:len(c[k]) for k in ids},'unassigned_commentaries_unchanged':True,'expected_official_count':639,'parsed_count':639,'statutory_verbatim_ratio':1.0,'exact_repeated_long_paragraphs':[],'whole_book_complete':False,'strict_validation':validation}
for name,obj in [('review-result.json',result),('sources/review-art-212hg-212l-result.json',result),('review-checks.json',checks),('sources/review-art-212hg-212l-checks.json',checks)]:save(W/name,obj)
save(W/'sources/review-art-212hg-212l-search-log.json',{'searched_at_utc':now,'queries':['site:rechtspraak.nl "212hgb"','site:rechtspraak.nl "212hg" "faillissement"'],'web_result':'No sufficiently relevant official full judgment located; nonofficial commentary search hits not used as judicial authority.','local_search':'rg -l -i 212hgb|212hg|212hgd /Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr --glob *.md','local_matches':[],'author_search_evidence_for_212j_212l':'sources/author-art-212j-212l-search-log.json','limitation':'Selective search; no exhaustive negative assertion.'})
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_212hg_212l']={'records':records,'historical':historical,'preflight':'sources/review-art-212hg-212l-preflight-result.json','existing_transition_evidence':'sources/review-art-207-212hf-transitional-fetch.json','external_wft_evidence':'sources/author-art-212j-212l-wft.html'};save(p,v)
p=W/'status.json';v=json.loads(p.read_text());v['bounded_review_art_212hg_212l']={'complete':True,'reviewed_ids':ids,'units_reviewed':20,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/review-art-212hg-212l-result.json'};v['completed_units']=len(c);v['updated_at_utc']=now;save(p,v)
print(json.dumps({'reviewed':20,'corrected':len(result['changed_units']),'unchanged':20-len(result['changed_units']),'source_agreement':1.0}))
