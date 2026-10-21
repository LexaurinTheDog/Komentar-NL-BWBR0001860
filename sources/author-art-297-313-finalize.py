from pathlib import Path
import sys,json,shutil,re,datetime
W=Path.cwd();O=Path('/Volumes/LaCie/open-commentary/nl/Komentar-NL-BWBR0001860');B=W/'batches/art-297-313';sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
m=json.loads((W/'meta.json').read_text());c=load_commentary(str(W));units=load_units(str(W));ch=next(x for x in m['chapters'] if x['n']==39)
parts=[f"# {m['labels']['chapter']} 39 — {ch['title']}\n"];last=None
for u in [x for x in units if x['chapter']==39]:
 st=u.get('structure') or []
 if st!=last:
  common=0
  if last:
   while common<min(len(st),len(last)) and st[common]==last[common]:common+=1
  for s in st[common:]:parts.append(f'#### {s}\n')
  last=st
 parts.extend([f"### {u['label']}\n",f"**{m['labels']['text']}:**\n",quote(u['text'])+'\n'])
 for note in u.get('notes',[]):parts.append(f"*{m['labels']['notes']}:* {note.strip()}\n")
 parts.append(c[u['id']].strip()+'\n')
(O/'39-wet-39.md').write_text('\n'.join(parts))
for p in (W/'sources').glob('author-art-297-313-*'):
 if p.suffix!='.py':
  shutil.copy2(p,B/'sources'/p.name);shutil.copy2(p,O/'sources'/p.name)
shutil.copy2(B/'coverage-evidence.json',O/'batches/art-297-313/coverage-evidence.json')
shutil.copytree(B/'sources',O/'batches/art-297-313/sources',dirs_exist_ok=True)
# Verify relative prose links, including full chapter's existing sources.
problems=[]
for p in [O/'39-wet-39.md',O/'batches/art-297-313/README.md',O/'batches/art-297-313/39-wet-39.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' not in target and not (p.parent/target.split('#')[0]).exists():problems.append({'file':str(p),'target':target})
assert not problems,problems
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
res={'kind':'bounded_author','assigned_ids':json.loads((B/'coverage-evidence.json').read_text())['expected_ids'],'total_units':20,'completed_units':20,'stage':'drafted_technical_validation_pending','source_checks':'sources/author-art-297-313-preflight-result.json','case_law_sources':['ECLI:NL:HR:2020:322','ECLI:NL:GHAMS:2016:4304'],'full_book_build':'Blocked by 79 unassigned missing commentaries beginning art-314; no unrelated prose filled. Full chapter 39 rendered from existing plus assigned commentary using shared builder format.','bounded_build':'20 units, one chapter, build_repo.py succeeded','relative_links_ok':True,'limitations':['Selective case-law coverage.','Independent second pass remains outstanding.','Article 309a statutory cross-reference to repealed article 309 expressly flagged.'],'updated_at_utc':now}
(W/'sources/author-art-297-313-result.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');(B/'status.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
s=json.loads((W/'status.json').read_text());s['updated_at_utc']=now;s['bounded_author_art_297_313']=res;s['stage']='authoring_incomplete';s['completed_units']=sum(bool(c.get(u['id'])) for u in units);s['total_units']=len(units);(W/'status.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(res,ensure_ascii=False))
