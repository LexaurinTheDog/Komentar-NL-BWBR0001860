from pathlib import Path
import json,hashlib,sys,subprocess,re,collections,datetime,xml.etree.ElementTree as E,html,shutil
W=Path(__file__).resolve().parent;S=W/'sources';prefix='review-art-212z-213a'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ids=['art-212'+s for s in ['z','aa','bb','cc','dd','ee','ff','gg','hh','ii','jj','kk','ll','mm','nn','nna','oo','pp']]+['art-213','art-213a']
us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W));before=json.loads((S/(prefix+'-before-hashes.json')).read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat();m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir'])
assert all(before[k]==hashlib.sha256(v.encode()).hexdigest() for k,v in cs.items() if k not in ids)
fetch=json.loads((S/(prefix+'-fetch.json')).read_text());assert all(r['accepted'] and r['http_status']==200 and sha(W/r['raw_path'])==r['sha256'] for r in fetch)
r=E.parse(S/(prefix+'-selected.xml')).getroot();assert sha(S/(prefix+'-selected.xml'))==sha(S/'official-2026-09-01.xml')
expected=['art-'+a.get('label').removeprefix('Artikel ') for a in r.iter('artikel')]
toc=['art-'+html.unescape(x).removeprefix('Artikel ') for x in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',(S/(prefix+'-current.html')).read_text())]
assert expected==toc==[u['id'] for u in us] and len(set(expected))==639
norm=lambda s:re.sub(r'\s+','',s)
def flat(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+flat(c)+' '+(c.tail or '') for c in e)
arts={a.get('label'):a for a in r.iter('artikel')}
for a in r.iter('artikel'):assert norm(flat(a))==norm(by['art-'+a.get('label').removeprefix('Artikel ')]['text'])
assert not [e for e in r.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
wt=E.parse(S/(prefix+'-wti.xml')).getroot();dates=sorted({e.get('waarde') for e in wt.findall('./wijzigingen/regeling/datum') if e.get('waarde')})
assert max(d for d in dates if d<='2026-10-21')=='2026-09-01'
assert not [d for d in dates if '2026-10-01'<d<='2026-10-21']
hist=json.loads((S/(prefix+'-historical-2025-fetch.json')).read_text())[0];assert hist['accepted'] and sha(W/hist['raw_path'])==hist['sha256']
old=E.parse(W/hist['raw_path']).getroot();oldn=next(a for a in old.iter('artikel') if a.get('label')=='Artikel 212nna');assert oldn.get('status')=='goed' and '3A.1.5' in flat(oldn)
assert arts['Artikel 212nna'].get('inwerking')=='2026-03-25'
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
names=['units.jsonl','meta.json','coverage-evidence.json','completeness-report.json'];hashes={n:sha(W/n) for n in names}
for script in ['_parse.py','_coverage.py']:
 p=subprocess.run([sys.executable,str(W/script)],capture_output=True,text=True);assert p.returncode==0,p.stderr
assert hashes=={n:sha(W/n) for n in names}
parser={'ok':True,'source_sha256':sha(S/(prefix+'-selected.xml')),'expected_ids':expected,'parsed_ids':[u['id'] for u in us],'html_toc_ids':toc,'missing':[],'duplicate_ids':[],'parser_reproduced_unchanged':hashes,'annex_disposition':comp['annexes'],'non_article_disposition':comp['non_article_text']}
save(S/(prefix+'-parser-check.json'),parser)
pre={'complete':True,'decisive_date':m['decisive_date'],'review_date_local':'2026-10-21','official_url':m['source_url'],'verified_at':now,'version_evidence':{'records':'sources/'+prefix+'-fetch.json','effective_from':'2026-09-01','current_route':'Geldend van 01-09-2026 t/m heden; displayed consultation date 20-10-2026, distinct from actual capture time','source_sha256':sha(S/(prefix+'-selected.xml')),'changes_since_intake':[],'future_dates_excluded':[d for d in dates if d>'2026-10-21']},'historical_versions_checked':[hist,{'path':'sources/version-register.xml','sha256':sha(S/'version-register.xml'),'disposition':'Historical 2002 state excluded, not concatenated.'},{'ids':['art-212hgd*','art-212hgd'],'disposition':'Distinct simultaneously operative XML paths; not historical duplicates.'}],'annexes_checked':comp['annexes'],'opening_and_closing_checked':comp['non_article_text'],'coverage_evidence':'sources/'+prefix+'-parser-check.json','unresolved_blockers':[]}
save(S/(prefix+'-preflight-result.json'),pre);p=W/'preflight-result.json';j=json.loads(p.read_text());j['bounded_review_art_212z_213a']=pre;save(p,j)
notes=[
('ongenummerd; bronnoot','Lex rei sitae voor contractuele liquidatiegevolgen en kwalificatie roerend/onroerend; geen eigen opzeggingsrecht.',['212t','212aa']),
('ongenummerd','Gezag over register, rechten van bank en verschil met contract-/beschikkingsvraag gecontroleerd.',['212t','212z','212cc']),
('ongenummerd','Gereglementeerde markt als kwalificatie, rechten en verplichtingen, voorbehoud212hh.',['212t','212hh']),
('ongenummerd','Na opening, onder bezwarende titel, objectcategorieën, plaats/registergezag; geldigheid niet gegarandeerd.',['212t','212aa']),
('ongenummerd','Aanhangig geding, betrokken goed en verlies beheer/beschikking; procesrecht niet gehele materiële vraag.',['212t']),
('aanhef;a;b;bronnoot','Cumulatief tegenbewijs door begunstigde; concreet onaantastbaarheidsonderzoek, geen algemene immuniteit.',['212t']),
('ongenummerd;bronnoot','Onjuiste actuele wettelijke verwijzing naar212a,m blootgelegd: m is rekening, l verrekening; verwijzing naar212w naast212x gecorrigeerd.',['212a','212t','212w','212x']),
('ongenummerd;bronnoot','Gelijke hoeveelheid activa van dezelfde soort, lidstaatrecht en voorbehoud212hh.',['212t','212hh']),
('ongenummerd;bronnoot','Uitoefenen rechten, registratievoorwaarde, rekening/depotlocatie; bewaarketen en toepassingsgrenzen.',['212t','212bb','212gg']),
('leden1–3;bronnoot','Omvang buitenlandse bevoegdheid versus Nederlandse uitoefening; dwang en rechtspraak uitgesloten; beide bijstandswegen.',['212jj']),
('leden1–2;bronnoot','Gewaarmerkt bewijs, Nederlandse vertaling op verlangen van ieder betrokken persoon; geen verzonnen beëdigingseis.',['212ii']),
('ongenummerd','Verzoek buitenlandse curator, Haagse griffier, register19; publiciteit geen nieuwe opening.',['19','212ii','212jj']),
('drie volzinnen','Derde-landbank met bijkantoor; griffier→DNB→autoriteiten, ook beëindiging; geen automatische boedelconsolidatie.',['212mm']),
('leden1–2','Rechtbank/instanties versus DNB/autoriteiten; inspanning curator naar vergunninghoudende lidstaten, geen resultaatsgarantie.',[]),
('ongenummerd','Verbod in openbare73a-verslagen op informatie reddingsderden; eerdere pogingen en indirecte herkenbaarheid; geen algemene geheimhoudingsregel.',['73a']),
('vervallen;historische ongenummerde tekst','Historische functie specifiek toegevoegd; DNB-bevoegdheid en c–g, uitzonderingen212k/r onderscheiden van huidig212pp.',['212k','212r','212pp']),
('leden1–3','Twee categorieën met verschillende uitzonderingen en toezichthoudervervanging; vergunningintrekking indien nog aanwezig.',['212ha','212hb','212hi','212k','212n','212ra','212rf']),
('ongenummerd','Entiteitscategorieën c–f, Nederlandse zetel, eigen uitzonderingen, geen algemene toezichtuitsluiting.',['212hb','212k','212ra','212re','212oo']),
('aanhef;a–r;structurele bronnoot','Alle18 definities gelezen; anomalie a met twee benamingen/drie verwijzingen nu expliciet; geen stilzwijgend herstel; Solvabiliteitkwalificatie en verzekeringsvordering begrensd.',[]),
('leden1–3;3a–b','Amsterdam, uitsluiting vergunninghoudende andere lidstaat en afzonderlijke bijkantoorscenario’s; lidstaat omvat EER.',['2','213'])]
rows=[]
for i,(parts,note,refs) in zip(ids,notes):
 assert all('art-'+x in by for x in refs)
 rows.append({'id':i,'official_path':by[i]['official_path'],'source_parts_reviewed':parts,'notes_reviewed':by[i]['notes'],'finding':note,'internal_cross_references_checked':['art-'+x for x in refs],'result':'corrected' if before[i]!=hashlib.sha256(cs[i].encode()).hexdigest() else 'accepted_without_change','before_sha256':before[i],'after_sha256':hashlib.sha256(cs[i].encode()).hexdigest(),'statutory_sha256':hashlib.sha256(by[i]['text'].encode()).hexdigest()})
assert len(rows)==20
paras=[p for i in ids for p in cs[i].split('\n\n') if len(p)>200];assert len(set(paras))==len(paras)
counts=collections.Counter(re.findall(r'^=== (\S+)', '\n'.join(p.read_text() for p in (W/'commentary').glob('*.md')),re.M));assert all(counts[i]==1 and len(cs[i])>=400 and not re.search('TODO|FIXME',cs[i]) for i in ids)
for script,suffix in [('build_repo.py','build.txt'),('validate.py','validation.txt')]:
 q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/'+script,str(W)],capture_output=True,text=True);(S/(prefix+'-'+suffix)).write_text(q.stdout+q.stderr)
 if script=='validate.py':validation=json.loads(q.stdout)
assert validation['verbatim_ratio']==1.0
save(S/(prefix+'-validation.json'),validation)
missing=sum(not cs.get(u['id']) for u in us)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[x['id'] for x in rows if x['result']=='corrected'],'review_date_local':'2026-10-21','checked_at_utc':now,'whole_book_complete':False,'validation_result':validation,'limitations':['Exact assigned batch only; project-internal second reading, no external professional approval.','Selective case research only. LBI full-text HTTP202 empty PDF rejected; no holding attributed.','Textual anomalies in212ff and213 definition references are disclosed, not silently repaired. EU qualification criteria not independently certified in full.',f'{missing} out-of-scope commentaries remain missing; full build/validator cannot pass.']}
checks={'ok':True,'reviewed_ids':ids,'completed_units':20,'unassigned_commentaries_unchanged':True,'commentary_chars':{i:len(cs[i]) for i in ids},'duplicate_long_paragraphs':0,'delimiter_counts':{i:counts[i] for i in ids},'source_agreement':1.0,'whole_book_complete':False,'validation_result':validation}
for p,j in [(W/'review-result.json',result),(S/(prefix+'-result.json'),result),(W/'review-checks.json',checks),(S/(prefix+'-checks.json'),checks)]:save(p,j)
p=S/'verification.json';j=json.loads(p.read_text());j['bounded_review_art_212z_213a']={'records':fetch,'historical':hist,'preflight':'sources/'+prefix+'-preflight-result.json','rejected_case_capture':'sources/'+prefix+'-case-fetch.json'};save(p,j)
p=W/'status.json';j=json.loads(p.read_text());j['bounded_review_art_212z_213a']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/'+prefix+'-result.json'};j['updated_at_utc']=now;save(p,j)
print(json.dumps({'reviewed':20,'corrected':result['changed_units'],'verbatim_ratio':1.0,'missing_elsewhere':missing}))
