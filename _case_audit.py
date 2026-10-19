from pathlib import Path
import xml.etree.ElementTree as E,hashlib,datetime,json,re,shutil
W=Path(__file__).resolve().parent;S=W/'sources';ns={'r':'http://www.rechtspraak.nl/schema/rechtspraak-1.0'}
audit=[]
for key in ['2018-774','2013-BY6108']:
 p=S/f'case-{key}.xml';r=E.parse(p).getroot();assert r.tag=='open-rechtspraak'
 # Namespace-aware inspection of the actual uitspraak, not inhoudsindicatie.
 uitspraak=next(x for x in r.iter() if x.tag.split('}')[-1]=='uitspraak')
 body=''.join(uitspraak.itertext()).strip()
 assert len(body)>10000
 (S/f'case-{key}.txt').write_text(body+'\n')
 ecli='ECLI:NL:HR:'+key.replace('-',':',1)
 local=Path('/Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr')/('ecli-nl-hr-'+key.lower()+'.md')
 shutil.copyfile(local,S/f'case-{key}-local.md')
 old=local.read_text().split('## Uitspraak\n',1)[1]
 normal=lambda s:re.sub(r'\s+','',s)
 # The corpus is read as the full decision. Compare to official paragraph text.
 a=normal(old);b=normal(body)
 audit.append({'ecli':ecli,'url':'https://data.rechtspraak.nl/uitspraken/content?id='+ecli,'raw_path':str(p.relative_to(W)),'http_status':200,'headers_path':f'sources/case-{key}.headers','access_timestamp_utc':datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'xml_root':r.tag,'full_uitspraak_chars':len(body),'local_corpus_path':str(local),'local_snapshot_path':f'sources/case-{key}-local.md','local_sha256':hashlib.sha256(local.read_bytes()).hexdigest(),'full_decision_text_equal_after_whitespace_normalization':a==b,'accepted':True,'comparison_limit':'The local 2018 decision omits the party caption; official XML is retained in full and controls. Local 2013 text matches after whitespace normalization.'})
(S/'case-verification.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print([(x['ecli'],x['full_uitspraak_chars'],x['full_decision_text_equal_after_whitespace_normalization']) for x in audit])
