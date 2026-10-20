from pathlib import Path
import json,subprocess,sys,shutil,hashlib,re
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-254-269b';O=Path(json.loads((W/'meta.json').read_text())['repo_dir']);B=W/'batches/art-254-269b';T=O/'batches/art-254-269b'
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def commit_output(msg):
 names=['REVIEW.md','SOURCES.md','review-result.json','review-checks.json','preflight-result.json','status.json','source-manifest.json','sources/verification.json','batches/art-254-269b']
 names += [str(p.relative_to(O)) for p in O.glob('*art-254-269b-checkpoint*.md')]
 names += [str(p.relative_to(O)) for p in (O/'sources').glob(P+'-*')]
 names += [p.name for p in O.glob('_review_254_269b_*.py')]
 names=[n for n in names if (O/n).exists()]
 subprocess.run(['git','-C',str(O),'add','--',*names],check=True)
 q=subprocess.run(['git','-C',str(O),'diff','--cached','--quiet'])
 if q.returncode:subprocess.run(['git','-C',str(O),'commit','-m',msg],check=True,capture_output=True)
def validate():
 out={}
 for key,path in [('bounded',B),('whole_book',W)]:
  q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/validate.py',str(path)],capture_output=True,text=True);out[key]=json.loads(q.stdout)
 return out
# First durable commit of the review itself, then strict validation of committed output.
commit_output('Beoordeel en corrigeer artikelen 254–269b')
v=validate();assert v['bounded']['ok'] and v['bounded']['units']==20 and v['bounded']['verbatim_ratio']==1.0,v
assert v['whole_book']['verbatim_ratio']==1.0 and len(v['whole_book']['errors'])==1 and 'krátký/chybějící' in v['whole_book']['errors'][0],v
save(S/(P+'-validation.json'),v)
r=json.loads((W/'review-result.json').read_text());r['validation_result']=v
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,r)
j=json.loads((W/'status.json').read_text());j['bounded_review_art_254_269b']['validation_result']=v;j['stage']='authoring_incomplete';save(W/'status.json',j)
checked=0
for p in [B/'README.md',B/'REVIEW.md',B/'SOURCES.md',T/'README.md',T/'REVIEW.md',T/'SOURCES.md',T/'sources'/(P+'-case-2017.md'),T/'sources'/(P+'-case-2024.md')]+list(T.glob('*wet*.md'))+list(O.glob('*art-254-269b-checkpoint*.md')):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',link):continue
  # Validation result is copied below; otherwise all target files must already exist.
  if link=='sources/'+P+'-validation.json':assert (S/(P+'-validation.json')).exists()
  else:assert (p.parent/link.split('#')[0]).exists(),(p,link)
  checked+=1
j=json.loads((W/'review-checks.json').read_text());j.update(local_links_checked=checked,broken_local_links=[])
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,j)
for root in [O,B,T]:
 for p in S.glob(P+'-*'):shutil.copyfile(p,root/'sources'/p.name)
for n in ['review-result.json','review-checks.json','status.json']:shutil.copyfile(W/n,O/n)
# Include the validation helper itself as reproducible checkpoint tooling.
shutil.copyfile(Path(__file__),O/Path(__file__).name)
j=json.loads((W/'source-manifest.json').read_text());j['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':sha(p)} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];j['scope']='Preserved sources through bounded second pass 254–269b; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:save(p,j)
commit_output('Leg strikte validatie van reviewcheckpoint 254–269b vast')
final=validate();assert final==v,(final,v)
# Commit only files touched by this worker; orchestration and other workers remain untouched.
names=['commentary/part-28.md','REVIEW.md','SOURCES.md','review-result.json','review-checks.json','status.json','preflight-result.json','source-manifest.json','sources/verification.json','batches/art-254-269b']
names += [str(p.relative_to(W)) for p in S.glob(P+'-*')]+[p.name for p in W.glob('_review_254_269b_*.py')]
subprocess.run(['git','-C',str(W),'add','--',*names],check=True)
subprocess.run(['git','-C',str(W),'commit','-m','Tweede lezing van twintig artikelen 254–269b'],check=True,capture_output=True)
print(json.dumps({'reviewed':20,'corrected':len(r['changed_units']),'validation':final,'links_checked':checked,'work_commit':subprocess.check_output(['git','-C',str(W),'rev-parse','--short','HEAD'],text=True).strip(),'output_commit':subprocess.check_output(['git','-C',str(O),'rev-parse','--short','HEAD'],text=True).strip()},ensure_ascii=False))
