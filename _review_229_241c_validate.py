from pathlib import Path
import json,subprocess,sys,hashlib,shutil
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir']);P='review-art-229-241c';S=W/'sources';B=W/'batches/art-229-241c';T=O/'batches/art-229-241c'
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
results={}
for label,path in [('bounded',B),('whole_book',W)]:
 q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/validate.py',str(path)],capture_output=True,text=True);results[label]=json.loads(q.stdout)
assert results['bounded']['ok'] and results['bounded']['units']==20 and results['bounded']['verbatim_ratio']==1.0
assert results['whole_book']['verbatim_ratio']==1.0
assert len(results['whole_book']['errors'])==1 and '179' in results['whole_book']['errors'][0]
for root in [W,O]:save(root/'sources'/(P+'-post-commit-validation.json'),results)
for root in [B,T]:save(root/'sources'/(P+'-post-commit-validation.json'),results)
for root in [W,O]:
 p=root/'review-result.json';j=json.loads(p.read_text());j['validation_result']=results['whole_book'];j['bounded_validation']=results['bounded'];save(p,j);save(root/'sources'/(P+'-result.json'),j)
 p=root/'status.json';j=json.loads(p.read_text());j['bounded_review_art_229_241c']['bounded_validation']=results['bounded'];j['bounded_review_art_229_241c']['whole_book_validation']=results['whole_book'];save(p,j)
for root in [B,T]:shutil.copyfile(W/'review-result.json',root/'sources'/(P+'-result.json'))
p=W/'source-manifest.json';j=json.loads(p.read_text());j['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()]
for root in [W,O]:save(root/'source-manifest.json',j)
shutil.copyfile(W/'_review_229_241c_validate.py',O/'_review_229_241c_validate.py')
for root in [W,O]:
 paths=['sources/'+P+'-post-commit-validation.json','review-result.json','sources/'+P+'-result.json','status.json','source-manifest.json','_review_229_241c_validate.py','batches/art-229-241c/sources/'+P+'-post-commit-validation.json','batches/art-229-241c/sources/'+P+'-result.json']
 subprocess.run(['git','-C',str(root),'add','--',*paths],check=True);subprocess.run(['git','-C',str(root),'commit','-m','Leg geslaagde batchvalidatie en resterende boekgrens vast'],check=True,capture_output=True)
 print(str(root),subprocess.check_output(['git','-C',str(root),'rev-parse','--short','HEAD'],text=True).strip())
q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/validate.py',str(B)],capture_output=True,text=True);assert q.returncode==0,q.stdout;print(q.stdout)
