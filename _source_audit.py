from pathlib import Path
import json,hashlib,datetime,xml.etree.ElementTree as E,re,shutil
W=Path(__file__).resolve().parent;S=W/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(p):return datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()
records=[]
for file,url,hdr,accepted,why in [
('official-2026-09-01.xml','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/2026-09-01_0/xml/BWBR0001860_2026-09-01_0.xml','official-xml.headers',True,'toestand BWBR0001860 inwerkingtreding 2026-09-01; 639 articles'),
('wti.xml','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/BWBR0001860.WTI','wti.headers',True,'wetstechnische-informatie; generated 2026-10-07; dated and undated future changes inspected'),
('version-register.xml','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/BWBR0001860.xml','version-register.headers',False,'Valid XML but 2002-01-01 historical toestand, not a version register; excluded'),
('version-index.xml','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/metadata.xml','version-index.headers',False,'204 empty response; no version evidence')]:
 p=S/file;headers=(S/hdr).read_text();codes=re.findall(r'HTTP/\S+ (\d+)',headers)
 root=None
 if p.exists() and p.stat().st_size:
  try:root=E.parse(p).getroot().tag
  except E.ParseError:root='INVALID XML'
 records.append({'url':url,'access_timestamp_utc':stamp(p) if p.exists() else stamp(S/hdr),'http_status':int(codes[-1]) if codes else None,'raw_path':str(p.relative_to(W)) if p.exists() else None,'sha256':sha(p) if p.exists() else None,'bytes':p.stat().st_size if p.exists() else 0,'xml_root':root,'accepted':accepted,'finding':why,'headers_path':'sources/'+hdr})
for filename in ['official-current.json','official-information.json']:
 p=W/'.firecrawl'/filename;d=json.loads(p.read_text());shutil.copyfile(p,S/filename)
 (S/(filename+'.html')).write_text(d.get('html',''))
 records.append({'url':d['metadata']['sourceURL'],'access_timestamp_utc':stamp(p),'http_status':d['metadata']['statusCode'],'raw_path':'sources/'+filename,'sha256':sha(S/filename),'body_html_path':'sources/'+filename+'.html','body_html_sha256':sha(S/(filename+'.html')),'accepted':d['metadata']['statusCode']==200,'finding':'Information page explicitly: consulted 19-10-2026; valid 01-09-2026 through present; future 15-11-2027 and undated changes.' if 'information' in filename else '404 error document rejected; exact author-date route not used as current-text evidence.'})
records.append({'url':'https://wetten.overheid.nl/BWBR0001860/2026-10-19','access_timestamp_utc':stamp(S/'official-current.headers'),'http_status':None,'raw_path':None,'sha256':None,'accepted':False,'finding':'Direct curl failed HTTP/2 protocol error (exit 92), no response body.'})
records.append({'url':'https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/2026-10-19_0/xml/BWBR0001860_2026-10-19_0.xml','access_timestamp_utc':stamp(S/'author-date-xml.headers'),'http_status':301,'raw_path':None,'sha256':None,'accepted':False,'finding':'Redirect loop exit 47; no valid XML; no toestand with this exact start date used.'})
original=Path('/Volumes/LaCie/law-intake/eu/nl/bwb/bwb-bwbr0001860.md');shutil.copyfile(original,S/'intake-original.md')
# Both source representations are preserved. Compare legal wording without editorial prose.
intake=original.read_text();blocks=re.split(r'^#### Artikel ',intake,flags=re.M)[1:];old={}
for b in blocks:
 nr,body=b.split('\n',1);body=re.split(r'^### ',body,flags=re.M)[0];old['art-'+nr.strip()]=body.strip()
units=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()]
norm=lambda s:re.sub(r'\s+',' ',s).strip()
changes=[]
for u in units:
 b=old.get(u['id'],'');base=b.split('\n\n*')[0]
 equal=norm(u['text'])==norm(base)
 # Display transformations may include markup; retain explicit full-text pairs on mismatch.
 if not equal:changes.append({'id':u['id'],'intake_text':b,'verified_text':u['text'],'disposition':'requires representation comparison; do not assume legislative change'})
(S/'change-map.json').write_text(json.dumps({'intake_sha256':sha(original),'official_xml_sha256':sha(S/'official-2026-09-01.xml'),'intake_article_count':len(old),'verified_article_count':len(units),'missing_intake_ids':sorted(set(u['id'] for u in units)-set(old)),'absent_from_verified':sorted(set(old)-set(u['id'] for u in units)),'same_after_whitespace_normalization':len(units)-len(changes),'representation_differences':changes},ensure_ascii=False,indent=2)+'\n')
if (S/'case-verification.json').exists():records.extend(json.loads((S/'case-verification.json').read_text()))
(S/'verification.json').write_text(json.dumps({'decisive_date':'2026-10-19','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_version':'2026-09-01_0','current_effectiveness_evidence':'sources/official-information.json: explicit Geldend van 01-09-2026 t/m heden, Geraadpleegd op 19-10-2026; WTI inspected for date/undated changes. Retrieval timestamp alone not used.','future_changes_excluded':['15-11-2027 amendment to article 106a','undated amendments listed in WTI'], 'records':records,'original_intake_sha256':sha(original),'canonical_sha256':sha(S/'canonical.md')},ensure_ascii=False,indent=2)+'\n')
print('source audit records',len(records),'change representations',len(changes))

# A later verified preflight supplements (and must not be erased by) this original audit.
if (W/"_preflight_audit.py").exists() and (S/"preflight-2026-10-20-fetch.json").exists():
 import runpy
 runpy.run_path(str(W/"_preflight_audit.py"),run_name="__main__")
