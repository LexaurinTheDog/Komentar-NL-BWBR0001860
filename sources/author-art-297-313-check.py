from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E,re,ast,shutil,sys,datetime
W=Path.cwd();S=W/'sources';B=W/'batches/art-297-313';O=Path('/Volumes/LaCie/open-commentary/nl/Komentar-NL-BWBR0001860');B.mkdir(parents=True,exist_ok=True)
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
raw=S/'author-art-297-313-selected.xml';r=E.parse(raw).getroot();assert r.tag=='toestand' and r.get('inwerkingtreding')=='2026-09-01'
a=[a for a in r.findall('.//artikel') if re.fullmatch(r'(?:29[7-9][ab]?|30[0-9]a?|31[0-3])',a.findtext('kop/nr','').strip())]
expected=['art-'+a.findtext('kop/nr').strip() for a in a];assert len(expected)==20 and len(set(expected))==20
units=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()];selected=[u for u in units if u['id'] in expected];assert [u['id'] for u in selected]==expected
# Reuse only pure renderer definitions from parser without executing its writes.
tree=ast.parse((W/'_parse.py').read_text());ns={'re':re,'SKIP':{'meta-data','kop'},'BLOCK':{'al','lid','lijst','li','lidnr','li.nr','wij','considerans.al','afkondiging','slotformulering','gegeven','ondertekening','uitgifte','dagtekening'}}
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['text','render']:exec(compile(ast.Module(body=[node],type_ignores=[]),'parser-render','exec'),ns)
assert all(ns['render'](a)==u['text'] for a,u in zip(a,selected))
assert not [n for n in r.iter() if 'bijlage' in n.tag.lower()]
cov={'official_source':{'url':json.loads((S/'author-art-297-313-fetch.json').read_text())[1]['url'],'local_raw_evidence_path':'sources/'+raw.name,'sha256':sha(raw)},'expected_ids':expected,'parsed_ids':[u['id'] for u in selected],'annex_disposition':[{'status':'verified_absence','evidence_path':'sources/'+raw.name,'method':'All selected XML element names checked; no bijlage element. Unnumbered opening/closing material retained in existing canonical source.'}],'missing':[],'duplicates':[],'all_texts_exact':True,'scope':'Assigned articles only; full title evidence remains coverage-evidence.json'}
dump(S/'author-art-297-313-coverage.json',cov)
records=json.loads((S/'author-art-297-313-fetch.json').read_text());prior=json.loads((S/'review-art-282-296-fetch.json').read_text());assert all(records[i]['sha256']==prior[i]['sha256'] for i in range(3))
hist=[]
for p in [S/'version-register.xml',S/'review-art-212z-213a-historical-2025.xml']:
 root=E.parse(p).getroot();hist.append({'path':str(p.relative_to(W)),'sha256':sha(p),'effective_from':root.get('inwerkingtreding'),'assigned_present_ids':['art-'+x.findtext('kop/nr').strip() for x in root.findall('.//artikel') if 'art-'+x.findtext('kop/nr','').strip() in expected],'disposition':'Historical text excluded, never concatenated with selected text.'})
pre={'complete':True,'decisive_date':'2026-10-19','batch_authoring_date':'2026-10-21','official_url':records[0]['final_url'],'verified_at':records[0]['access_timestamp_utc'],'version_evidence':{'current_validity':records[0]['validity_statements'],'fresh_fetch':'sources/author-art-297-313-fetch.json','comparison':'Current HTML, selected XML and WTI hashes identical to preceding verified preflight; version-evidence.json latest effective change 2026-09-01, next dated change 2027-11-15. No change since intake.','selected_xml_sha256':sha(raw)},'historical_versions_checked':hist,'annexes_checked':cov['annex_disposition'],'unresolved_blockers':[],'assigned_ids':expected,'all_statutory_texts_exact':True,'limitations':['Article 309a retains reference to repealed 309; preserved and expressly discussed. No reconstructed historical rule.']}
dump(S/'author-art-297-313-preflight-result.json',pre)
v=json.loads((S/'verification.json').read_text());v['bounded_author_art_297_313']={'records':records,'preflight':'sources/author-art-297-313-preflight-result.json'};dump(S/'verification.json',v)
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
c=load_commentary(str(W));assert all(c[x] for x in expected);assert len(set(c[x] for x in expected))==20
# Durable self-contained bounded build, preserving the full title's metadata.
m=json.loads((W/'meta.json').read_text());m['repo_dir']=str(O/'batches/art-297-313');m['chapters']=[x for x in m['chapters'] if x['n']==39];dump(B/'meta.json',m)
(B/'units.jsonl').write_text(''.join(json.dumps(u,ensure_ascii=False)+'\n' for u in selected));(B/'commentary').mkdir(exist_ok=True);shutil.copy2(W/'commentary/part-39.md',B/'commentary/part-39.md')
for n in ['00-inleiding.md','LICENSE']:shutil.copy2(W/n,B/n)
(B/'README.md').write_text('# Faillissementswet — artikelen 297–313\n\nBegrensde auteursbatch: twintig officiële artikelposities, inclusief vervallen artikelen 298 en 309. Wettekst geldend vanaf 1 september 2026, actuele route en XML opnieuw gecontroleerd op 21 oktober 2026. Bron: https://wetten.overheid.nl/BWBR0001860/2026-09-01. Alleen deze batch is hier technisch voltooid; geen voltooiingsverklaring voor het hele boek.\n\nOorspronkelijk Nederlands commentaar © 2026 Vojtěch Říha, Apache-2.0; officiële wettekst en officiële uitspraken zijn afzonderlijk als bronnen opgenomen en worden niet als oorspronkelijk commentaar geclaimd. Mechanische extractie, onafhankelijke XML-identificatie en letterlijke vergelijking. Selectief onderzochte rechtspraak: HR 2020:322 en Hof Amsterdam 2016:4304, volledige officiële teksten gelezen. Geen uitputtend jurisprudentieonderzoek of externe professionele goedkeuring. Concept in afwachting van onafhankelijke inhoudelijke tweede lezing.\n\n[Broncontrole](sources/author-art-297-313-preflight-result.json), [dekking](coverage-evidence.json), [HR-zaaknotitie](sources/author-art-297-313-case-hr.md), [hofzaaknotitie](sources/author-art-297-313-case-ghams.md).\n')
(B/'sources').mkdir(exist_ok=True)
for p in S.glob('author-art-297-313-*'):
 if p.suffix not in ['.py']:shutil.copy2(p,B/'sources'/p.name)
dump(B/'coverage-evidence.json',cov)
local=Path('/Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr/ecli-nl-hr-2020-322.md');t=local.read_text();assert '2020:322' in t;shutil.copy2(local,S/'author-art-297-313-hr-2020-322-local.md')
# Actual local full-text read plus independent official judgment read in authoring process.
print(t)
dump(S/'author-art-297-313-search-log.json',{'queries':['site.rechtspraak.nl "307" "schuldsaneringsregeling" "Hoge Raad"','site.rechtspraak.nl "305" "schuldsaneringsregeling" "ontruiming"'],'local_corpus':str(local.parent),'local_snapshot':'sources/author-art-297-313-hr-2020-322-local.md','verified_full_judgments':['ECLI:NL:HR:2020:322','ECLI:NL:GHAMS:2016:4304'],'method':'Official full XML, rendered complete text read; local HR version compared. No Firecrawl needed for structured API.','limits':'Selective research; no separately verified case for other technical units; search hits and PHR conclusions not treated as holdings.'})
dump(S/'author-art-297-313-checks.json',{'assigned_ids':expected,'completed_units':20,'text_agreement':1.0,'lengths':{x:len(c[x]) for x in expected},'duplicate_commentaries':False,'unresolved_blockers':[],'independent_review':False})
