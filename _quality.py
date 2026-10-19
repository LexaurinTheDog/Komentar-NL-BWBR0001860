#!/usr/bin/env python3
from pathlib import Path
import json,re,collections,datetime,sys,urllib.parse
W=Path(__file__).resolve().parent;sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);u=load_units(str(W));c=load_commentary(str(W))
# Create a real report path before testing links to this report.
for target in [W/'quality-report.json',O/'quality-report.json']:
 if not target.exists():target.write_text('{}\n')
ids=[]
for p in sorted((W/'commentary').glob('*.md')):ids+=re.findall(r'^=== (\S+)\s*$',p.read_text(),re.M)
paragraphs=collections.defaultdict(list)
sentences=collections.defaultdict(list)
for key,body in c.items():
 for par in re.split(r'\n\s*\n',body):
  norm=re.sub(r'\s+',' ',par.strip())
  if len(norm)>=160:paragraphs[norm].append(key)
 for s in re.split(r'(?<=[.!?])\s+',body):
  norm=re.sub(r'\s+',' ',s.strip())
  if len(norm)>=180:sentences[norm].append(key)
broken=[];checked=0
for p in O.rglob('*.md'):
 if '.git' in p.parts:continue
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  target=target.strip().split(' "')[0].strip('<>')
  if urllib.parse.urlsplit(target).scheme or target.startswith('#'):continue
  path=urllib.parse.unquote(target.split('#',1)[0]);checked+=1
  if path and not (p.parent/path).exists():broken.append({'file':str(p.relative_to(O)),'target':target})
missing=[x['id'] for x in u if not c.get(x['id'])]
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'total_statutory_units':len(u),'commented_units':len(c),'missing_commentary_ids':missing,'duplicate_commentary_ids':[x for x,n in collections.Counter(ids).items() if n>1],'unmatched_commentary_ids':sorted(set(c)-{x['id'] for x in u}),'commentary_characters':sum(map(len,c.values())),'short_authored_commentaries':[x['id'] for x in u if x['id'] in c and len(c[x['id']])<(120 if len(x['text'])<160 else 400)],'exact_repeated_paragraphs':[{'text':p,'units':keys} for p,keys in paragraphs.items() if len(set(keys))>1],'long_repeated_sentences':[{'text':p,'units':keys} for p,keys in sentences.items() if len(set(keys))>2],'local_output_links_checked':checked,'broken_local_output_links':broken,'limitations':['No automatic metric certifies legal quality or a complete semantic cross-reference review.','Minimum length is a format check only.','No independent second-pass review has occurred.','No claim of exhaustive case-law research.'],'complete_manuscript':not missing}
for p in [W/'quality-report.json',O/'quality-report.json']:p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['total_statutory_units','commented_units','commentary_characters','duplicate_commentary_ids','unmatched_commentary_ids','short_authored_commentaries','local_output_links_checked','broken_local_output_links','complete_manuscript']},ensure_ascii=False))
print('Repeated paragraphs:',len(report['exact_repeated_paragraphs']),'Repeated long sentences:',len(report['long_repeated_sentences']))
