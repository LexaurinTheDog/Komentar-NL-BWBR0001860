#!/usr/bin/env python3
"""Fetch fresh official evidence without overwriting earlier captures."""
from pathlib import Path
import urllib.request,urllib.error,datetime,json,hashlib,xml.etree.ElementTree as E
from concurrent.futures import ThreadPoolExecutor
W=Path(__file__).resolve().parent
S=W/'sources'; date=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
targets=[
('selected.xml','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/2026-09-01_0/xml/BWBR0001860_2026-09-01_0.xml','toestand'),
('wti.xml','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/BWBR0001860.WTI','wetstechnische-informatie'),
('information.html','https://wetten.overheid.nl/BWBR0001860/2026-09-01/informatie',None),
('current.html','https://wetten.overheid.nl/BWBR0001860',None)]
def fetch(t):
 name,url,root=t; p=S/('preflight-'+date+'-'+name)
 rec={'url':url,'access_timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_path':str(p.relative_to(W)),'accepted':False}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'OpenCommentary-source-verification/1.0','Accept':'application/xml,text/html;q=0.9,*/*;q=0.5'})
  try:response=urllib.request.urlopen(req,timeout=45)
  except urllib.error.HTTPError as err:response=err
  data=response.read();p.write_bytes(data)
  hp=p.with_suffix(p.suffix+'.headers');hp.write_text('HTTP status: '+str(response.status)+'\n'+str(response.headers))
  rec.update(http_status=response.status,final_url=response.url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),headers_path=str(hp.relative_to(W)))
  if root:
   try:
    x=E.fromstring(data);rec.update(xml_root=x.tag,xml_attributes=x.attrib)
    rec['accepted']=response.status==200 and x.tag==root and x.get('bwb-id')=='BWBR0001860'
   except E.ParseError as err:rec['format_error']=str(err)
  else:
   s=data.decode('utf-8',errors='replace');rec['accepted']=response.status==200 and 'Faillissementswet' in s and 'Geldend' in s and 'captcha' not in s.lower()
 except Exception as err:rec.update(http_status=None,raw_path=None,error=repr(err))
 return rec
with ThreadPoolExecutor(max_workers=4) as pool: records=list(pool.map(fetch,targets))
p=S/('preflight-'+date+'-fetch.json');p.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
for r in records:print({k:v for k,v in r.items() if k not in ('xml_attributes',)})
