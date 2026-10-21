from pathlib import Path
import json,subprocess,sys,shutil,re,hashlib
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-270-281h';O=Path(json.loads((W/'meta.json').read_text())['repo_dir']);B=W/'batches/art-270-281h';T=Path(json.loads((B/'meta.json').read_text())['repo_dir'])
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def commit(root,names,msg):
 names=[n for n in names if (root/n).exists()]
 subprocess.run(['git','-C',str(root),'add','--',*names],check=True)
 if subprocess.run(['git','-C',str(root),'diff','--cached','--quiet']).returncode:subprocess.run(['git','-C',str(root),'commit','-m',msg],check=True,capture_output=True)
def names(root):
 ns=['REVIEW.md','SOURCES.md','review-result.json','review-checks.json','preflight-result.json','status.json','source-manifest.json','sources/verification.json']
 ns += [str(p.relative_to(root)) for p in (root/'sources').glob(P+'-*')]
 ns += [p.name for p in root.glob('_review_270_281h_*.py')]
 if root==W:ns += ['commentary/part-29.md','batches/art-270-281h']
 else:ns += ['checkpoints/art-270-281h']+[p.name for p in O.glob('*art-270-281h-checkpoint*.md')]
 return ns
shutil.copyfile(Path(__file__),O/Path(__file__).name)
commit(O,names(O),'Beoordeel artikelen 270–281h en corrigeer vijf toelichtingen')
validation={}
for key,path in [('bounded',B),('whole_book',W)]:
 q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/validate.py',str(path)],capture_output=True,text=True);validation[key]=json.loads(q.stdout)
assert validation['bounded']['ok'] and validation['bounded']['units']==20 and validation['bounded']['verbatim_ratio']==1.0,validation
assert validation['whole_book']['verbatim_ratio']==1.0,validation
save(S/(P+'-validation.json'),validation)
r=json.loads((W/'review-result.json').read_text());r['validation_result']=validation
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,r)
j=json.loads((W/'status.json').read_text());j['bounded_review_art_270_281h']['validation_result']=validation;j['stage']='authoring_incomplete';save(W/'status.json',j)
checked=0
for p in [B/'README.md',B/'REVIEW.md',B/'SOURCES.md',T/'README.md',T/'REVIEW.md',T/'SOURCES.md',T/'sources'/(P+'-case-2003.md'),T/'sources'/(P+'-case-2024.md')]+list(T.glob('*wet*.md'))+list(O.glob('*art-270-281h-checkpoint*.md')):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',link):continue
  target=p.parent/link.split('#')[0]
  if not target.exists() and link=='sources/'+P+'-validation.json':assert (S/(P+'-validation.json')).exists()
  else:assert target.exists(),(p,link)
  checked+=1
j=json.loads((W/'review-checks.json').read_text());j.update(local_links_checked=checked,broken_local_links=[])
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,j)
for root in [O,B,T]:
 for p in S.glob(P+'-*'):shutil.copyfile(p,root/'sources'/p.name)
for name in ['review-result.json','review-checks.json','status.json']:shutil.copyfile(W/name,O/name)
j=json.loads((W/'source-manifest.json').read_text());j['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':sha(p)} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];j['scope']='Preserved sources through bounded second pass 270–281h; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:save(p,j)
# Store a batch source manifest as well, using paths local to that checkpoint.
for root in [B,T]:save(root/'source-manifest.json',{'scope':'Bounded reviewed checkpoint 270–281h','files':[{'path':str(p.relative_to(root)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted((root/'sources').glob('*')) if p.is_file()]})
commit(O,names(O),'Leg strikte validatie en bronmanifest van review 270–281h vast')
commit(W,names(W),'Tweede lezing van twintig artikelen 270–281h')
# Validate committed checkpoint again; keep this comparison read-only.
for key,path in [('bounded',B),('whole_book',W)]:
 q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/validate.py',str(path)],capture_output=True,text=True);assert json.loads(q.stdout)==validation[key]
print(json.dumps({'reviewed':20,'corrected':r['changed_units'],'validation':validation,'links_checked':checked,'work_commit':subprocess.check_output(['git','-C',str(W),'rev-parse','--short','HEAD'],text=True).strip(),'output_commit':subprocess.check_output(['git','-C',str(O),'rev-parse','--short','HEAD'],text=True).strip()},ensure_ascii=False))
