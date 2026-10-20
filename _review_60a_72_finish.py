from pathlib import Path
import json,re,collections,hashlib,shutil,sys,datetime
W=Path(__file__).resolve().parent;O=Path('/Volumes/LaCie/open-commentary/nl/Komentar-NL-BWBR0001860')
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_commentary
c=load_commentary(str(W));ids=json.loads((W/'review-result.json').read_text())['reviewed_ids']
found=[]
for p in (W/'commentary').glob('*.md'):found+=re.findall(r'^=== (\S+)',p.read_text(),re.M)
assert len(found)==len(set(found))==297
paras=collections.defaultdict(list)
for k,t in c.items():
 for p in re.split(r'\n\s*\n',t):
  if len(p)>150:paras[p].append(k)
repeated=[v for v in paras.values() if len(v)>1];assert not repeated
broken=[];count=0
for p in O.glob('*.md'):
 for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?://|#|mailto:)',url):continue
  target=url.split('#')[0];count+=1
  if not (p.parent/target).exists():broken.append({'file':p.name,'target':target})
assert not broken,broken
checks=json.loads((W/'review-checks.json').read_text());checks.update(parser_idempotent=True,duplicate_commentary_ids=0,repeated_paragraphs=0,broken_output_local_links=broken,output_local_links_checked=count,assigned_commentary_count=20,assigned_nonempty=True,assigned_min_chars=min(len(c[k]) for k in ids),whole_book_complete=False)
for n in ['review-checks.json','sources/review-art-60a-72-checks.json']:(W/n).write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
for n in ['_review_60a_72_audit.py','_review_60a_72_fetch.py','_review_60a_72_cases_fetch.py','_review_60a_72_finish.py','validation.json','review-checks.json']:
 shutil.copyfile(W/n,O/n)
shutil.copyfile(W/'sources/review-art-60a-72-checks.json',O/'sources/review-art-60a-72-checks.json')
manifest=json.loads((W/'source-manifest.json').read_text())
manifest['files']=[]
for d in ['sources','cases']:
 for p in sorted((W/d).rglob('*')):
  if p.is_file():manifest['files'].append({'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for base in [W,O]:(base/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks))
