from pathlib import Path
import sys,json,hashlib,re,datetime,xml.etree.ElementTree as E,html,subprocess,collections
W=Path(__file__).resolve().parent;sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary
ids=['art-212'+x for x in ['m','ma','n','o','p','q','r','ra','rb','rc','rd','re','rf','s','t','u','v','w','x','ij']];prefix='review-art-212m-212ij'
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W));before=json.loads((W/f'sources/{prefix}-before-hashes.json').read_text());m=json.loads((W/'meta.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in cs.items() if k not in ids)
records=json.loads((W/f'sources/{prefix}-fetch.json').read_text());assert all(r['accepted'] and r['http_status']==200 and sha(W/r['raw_path'])==r['sha256'] for r in records)
raw=W/f'sources/{prefix}-selected.xml';root=E.parse(raw).getroot();assert sha(raw)==sha(W/'sources/official-2026-09-01.xml')
expected=['art-'+a.get('label').removeprefix('Artikel ') for a in root.iter('artikel')]
h=(W/f'sources/{prefix}-current.html').read_text();hi=['art-'+html.unescape(t).removeprefix('Artikel ') for t in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',h)]
assert expected==hi==[u['id'] for u in us] and len(expected)==len(set(expected))==639
norm=lambda s:re.sub(r'\s+','',s)
def flatten(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+flatten(x)+' '+(x.tail or '') for x in e)
for a in root.iter('artikel'):assert norm(flatten(a))==norm(by['art-'+a.get('label').removeprefix('Artikel ')]['text'])
assert not [e for e in root.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
wt=E.parse(W/f'sources/{prefix}-wti.xml').getroot();dates=sorted({x.get('waarde') for x in wt.findall('./wijzigingen/regeling/datum') if x.get('waarde')})
assert max(d for d in dates if d<='2026-10-21')=='2026-09-01';assert not [d for d in dates if '2026-10-01'<d<='2026-10-21']
historical=json.loads((W/'sources/review-art-212hg-212l-historical.json').read_text());assert historical['accepted'] and sha(W/historical['raw_path'])==historical['sha256'];hr=E.parse(W/historical['raw_path']).getroot();old={a.get('label'):a for a in hr.iter('artikel')};assert old['Artikel 212m'].find('lid') is not None and old['Artikel 212ma'].find('al') is not None
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
names=['units.jsonl','meta.json','coverage-evidence.json','completeness-report.json'];hashes={n:sha(W/n) for n in names}
for script in ['_parse.py','_coverage.py']:
 p=subprocess.run([sys.executable,str(W/script)],capture_output=True,text=True);assert p.returncode==0,p.stderr
assert hashes=={n:sha(W/n) for n in names}
save(W/f'sources/{prefix}-parser-check.json',{'ok':True,'unchanged_hashes':hashes,'official_xml_sha256':sha(raw),'expected_ids':expected,'parsed_ids':[u['id'] for u in us],'missing':[],'duplicates':[],'scripts':['_parse.py','_coverage.py']})
pre={'complete':True,'decisive_date':m['decisive_date'],'review_date_local':'2026-10-21','official_url':m['source_url'],'verified_at':now,'version_evidence':{'fresh_http_records':f'sources/{prefix}-fetch.json','effective_from':'2026-09-01','current_route_validity':'Geldend van 01-09-2026 t/m heden; cached official consultation date 20-10-2026; actual fetch timestamp separately recorded','changes_since_intake':[],'future_wti_dates_excluded':[d for d in dates if d>'2026-10-21']},'historical_versions_checked':[historical,{'path':'sources/version-register.xml','disposition':'Historical 2002 record excluded from selected current text.'},{'ids':['art-212hgd*','art-212hgd'],'disposition':'Distinct simultaneous current XML paths, not historical duplicates.'}],'annexes_checked':comp['annexes'],'opening_and_closing_text_checked':comp['non_article_text'],'coverage':{'official_count':639,'parsed_count':639,'missing':[],'duplicate_ids':[],'parser_reproduction':f'sources/{prefix}-parser-check.json'},'unresolved_blockers':[]}
save(W/f'sources/{prefix}-preflight-result.json',pre)
p=W/'preflight-result.json';v=json.loads(p.read_text());v['bounded_review_art_212m_212ij']=pre;save(p,v)
notes=[
('vervallen; historische leden1–4 en3a–g; bronnoot','Historische overgang noodregeling/faillissement concreet uitgelegd; foutieve suggestie algemeen bankovergangsrecht hersteld.',['212ma','43','45','362']),
('vervallen; historische ongenummerde tekst; bronnoot','Historische vangnetkoppeling onderscheiden van212m; XIVlid4 betreft oudere verzekeraarsfaillissementen.',['212m']),
('ongenummerd','Onverwijlde DNB-informatie aan alle andere lidstaten; vonnis en concrete gevolgen; eigen taak naast publicatie en individuele informatie.',['212c','212o','212p']),
('1–4 en bronnoot','Verplichte EU- en buitenlandse publicatie versus facultatieve registerinschrijving; kosten alleen lid3; buitenlandse rechtskeuzeartikelen slechts ter vergelijking; overgang genuanceerd.',['14','212t','212p']),
('1–3 en bronnoot','Onmiddellijke schriftelijke kennisgeving, indieningsbericht inclusief zekerheid en periodieke voortgang; onhandige wettelijke verwijzing109lid1 uitgelegd met127leden1–3.',['109','108','127','212o','212q']),
('1–3','Nederlands formulier met alle EU-opschriften; taal indiening verbonden aan woonlidstaat; vertaalverzoek geen zelfgemaakte termijnverlenging.',['212p']),
('ongenummerd','Afwijking52lid2, bank geen natuurlijk persoon; bewijs daadwerkelijke onbekendheid bij betaler; geen algemene respijttermijn.',['52']),
('1a–b;2','Depositorang a voor b en gelijk binnen categorie; fonds en derde-landbijkantoren; datum25maart2026 tegen XMLmetadata gecontroleerd.',[]),
('1–3','Kwalificerende instrumenten tussen concurrent en achtergesteld; gelijkheid en uitgiftetijdstip entiteitsstatus; EUcriteria niet uit geheugen ingevuld.',['212rf']),
('1–2 en bronnoot','Automatische indiening nafaillissementsrente en promemorieverificatie onderscheiden van materiële renteaanspraak; IIIStb2022/105 exact toegepast.',['110','128','212rd']),
('1;2a–c en bronnoot','Toestemming op curatorverzoek; cumulatieve waarschijnlijkheid/rentebeperking/geen nadeel; discretionair; overgang2022/105 concreet.',['212rc']),
('ongenummerd en bronnoot','Derdenrecht blijft gelijk; geen nieuwe garantie of boedelrang; overgangStb2022/22leden1en3 met uitgiftecategorieën gecorrigeerd.',[]),
('1a–c;2–4','Eigenvermogensrang, verlies erkenning, verwijzingsachterstelling en gedeeltelijke erkenning afzonderlijk; externe kwalificaties niet gecertificeerd.',[]),
('1–2','Automatische erkenning andere herkomstlidstaat; werkingstijdstip daar, geen uitgestelde Nederlandse publicatievoorwaarde.',['212t','212u']),
('ongenummerd en bronnoot','Lexconcursus voor procedure/gevolgen, geen universele contractrechtskeuze; wettelijke uitzonderingen afzonderlijk onderzocht.',['212u','212ij']),
('1;2a–d;3;4a–c','Goederenrechtelijke typen, tegenwerpelijk registerverkrijgingsrecht, variabele goederen en eigen lokalisatieregels; peiltijd en benadelingsactie.',['212x']),
('1–3','Bank als koper versus verkoper; eigendomsvoorbehoud versus bescherming verkrijging; andere vereisten blijven, lokalisatie via212u.',['212u','212x']),
('ongenummerd','Verrekeningsrecht volgens recht op vordering VAN bank; wederkerigheid, geen scheppen recht of immuniteit benadeling.',['212x']),
('ongenummerd en bronnoot','Nietigheid/vernietiging/niettegenwerpelijkheid ondanks bescherming; geen zelfstandige complete paulianaregel.',['212u','212v','212w']),
('ongenummerd en bronnoot; checklist','Arbeid en andere arbeidsrechtsverhoudingen uitsluitend recht toepasselijke lidstaat; geen automatische uitbreiding tot elke rangvraag; checklist relevant.',['212t'])]
assert len(notes)==len(ids)==20
rows=[]
for k,(paras,note,refs) in zip(ids,notes):
 assert len(cs[k])>=(120 if by[k]['text'].strip()=='Vervallen' else 400)
 for ref in refs:assert 'art-'+ref in by
 rows.append({'id':k,'official_path':by[k]['official_path'],'source_paragraphs_reviewed':paras,'source_notes_reviewed':by[k].get('notes',[]),'assessment':note,'internal_cross_references_checked':['art-'+r for r in refs],'case_authorities_checked':[],'result':'corrected' if hashlib.sha256(cs[k].encode()).hexdigest()!=before[k] else 'accepted_without_change','commentary_before_sha256':before[k],'commentary_after_sha256':hashlib.sha256(cs[k].encode()).hexdigest(),'statutory_text_sha256':hashlib.sha256(by[k]['text'].encode()).hexdigest()})
# Verify dated assertions against current official article metadata.
arts={a.get('label'):a for a in root.iter('artikel')}
assert arts['Artikel 212ra'].get('inwerking')=='2026-03-25';assert arts['Artikel 212re'].get('inwerking')=='2022-07-08'
paragraphs=collections.defaultdict(list)
for k in ids:
 for para in cs[k].split('\n\n'):
  if len(para)>200:paragraphs[para].append(k)
assert not [v for v in paragraphs.values() if len(v)>1]
r=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/build_repo.py',str(W)],capture_output=True,text=True);(W/f'sources/{prefix}-build.txt').write_text(r.stdout+r.stderr)
r=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/validate.py',str(W)],capture_output=True,text=True);(W/f'sources/{prefix}-validation.txt').write_text(r.stdout+r.stderr);validation=json.loads(r.stdout);assert validation['verbatim_ratio']==1.0;save(W/f'sources/{prefix}-validation.json',validation)
missing=sum(not cs.get(u['id']) for u in us)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'limitations':['Only these twenty units checked; no whole-book approval or external professional approval.','Selective official web and local HR corpus search found no sufficiently relevant verified full-text judgment; no holding attributed. No exhaustive case-law coverage.','Referenced European instrument qualification criteria not independently certified in full; commentary does not invent their contents.',f'{missing} missing commentaries outside this batch prevent successful whole-book build and strict validation.'],'whole_book_complete':False,'review_date_local':'2026-10-21','checked_at_utc':now,'changed_units':[r['id'] for r in rows if r['result']=='corrected'],'validation_result':validation}
checks={'ok':True,'reviewed_ids':ids,'reviewed_count':20,'commentary_chars':{k:len(cs[k]) for k in ids},'unassigned_commentaries_unchanged':True,'expected_official_count':639,'parsed_count':639,'statutory_verbatim_ratio':1.0,'exact_repeated_long_paragraphs':[],'whole_book_complete':False,'strict_validation':validation}
for name,obj in [('review-result.json',result),(f'sources/{prefix}-result.json',result),('review-checks.json',checks),(f'sources/{prefix}-checks.json',checks)]:save(W/name,obj)
save(W/f'sources/{prefix}-search-log.json',{'searched_at_utc':now,'queries':['site:rechtspraak.nl "212rc"','site:rechtspraak.nl "212ra"','site:rechtspraak.nl "212u" bank'],'web_result':'No search results; no judgment attributed.','local_search':'rg -l -i 212ra|212rb|212rc|212rd|212rf|212u|212w /Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr --glob *.md','local_matches':[],'limitation':'Selective only; no exhaustive negative claim.'})
p=W/'sources/verification.json';v=json.loads(p.read_text());v['bounded_review_art_212m_212ij']={'records':records,'preflight':f'sources/{prefix}-preflight-result.json','historical':historical,'transition_evidence':f'sources/{prefix}-transition-fetch.json','transition_2018_489':'sources/review-art-207-212hf-stb-2018-489.xml'};save(p,v)
p=W/'status.json';v=json.loads(p.read_text());v['bounded_review_art_212m_212ij']={'complete':True,'reviewed_ids':ids,'units_reviewed':20,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':f'sources/{prefix}-result.json'};v['completed_units']=len(cs);v['updated_at_utc']=now;save(p,v)
print(json.dumps({'reviewed':20,'corrected':len(result['changed_units']),'source_agreement':1.0,'missing_elsewhere':missing}))
