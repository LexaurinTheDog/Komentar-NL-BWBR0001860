from pathlib import Path
import urllib.request,datetime,hashlib,json,xml.etree.ElementTree as ET
W=Path(__file__).resolve().parent
items=[('current','https://wetten.overheid.nl/BWBR0001860/','html'),('selected','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/2026-09-01_0/xml/BWBR0001860_2026-09-01_0.xml','xml'),('wti','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/BWBR0001860.WTI','xml'),('paget','https://eur-lex.europa.eu/legal-content/NL/TXT/HTML/?uri=CELEX:62020CJ0724','html')]
records=[]
for name,url,ext in items:
 r={'url':url,'access_timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  res=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60);raw=res.read();p=W/f'author-art-213me-213z-{name}.{ext}';p.write_bytes(raw)
  r.update(http_status=res.status,final_url=res.url,raw_path=str(p.relative_to(W.parent)),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw));(W/f'author-art-213me-213z-{name}.headers').write_text(str(res.headers))
  if ext=='xml':r['xml_root']=ET.fromstring(raw).tag
  else:r['html_validated']=b'<html' in raw.lower()
 except Exception as e:r['error']=str(e)
 records.append(r)
(W/'author-art-213me-213z-fetch.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
