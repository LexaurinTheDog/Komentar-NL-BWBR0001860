"""Fresh source snapshots for the bounded independent review; no previous capture replaced."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,urllib.error,datetime,hashlib,json,xml.etree.ElementTree as E
W=Path(__file__).resolve().parent
S=W/'sources'
targets=[('bw7.html','https://wetten.overheid.nl/BWBR0005290',None),('eu.html','https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:02015R0848-20251106',None)]
def fetch(t):
 name,url,root=t;p=S/('review-art-241d-253-'+name)
 rec={'url':url,'access_timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_path':str(p.relative_to(W)),'accepted':False}
 try:
  try:r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'OpenCommentary-review/1.0'}),timeout=30)
  except urllib.error.HTTPError as err:r=err
  b=r.read();p.write_bytes(b);h=p.with_suffix(p.suffix+'.headers');h.write_text('HTTP status: '+str(r.status)+'\n'+str(r.headers))
  rec.update(http_status=r.status,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),headers_path=str(h.relative_to(W)))
  if root:
   x=E.fromstring(b);rec.update(xml_root=x.tag,xml_attributes=x.attrib)
   rec['accepted']=r.status==200 and x.tag.split('}')[-1]==root.split('}')[-1]
   if name=='selected.xml':rec['accepted'] &= x.get('bwb-id')=='BWBR0001860' and x.get('inwerkingtreding')=='2026-09-01'
   if name.startswith('hr-'):
    u=x.find('{*}uitspraak');rec['full_uitspraak_chars']=len(''.join(u.itertext())) if u is not None else 0
    rec['accepted'] &= u is not None and rec['full_uitspraak_chars']>300
    if u is None:rec['finding']='Metadata-only response rejected: no full uitspraak.'
  else:
   s=b.decode('utf8');rec['validity_statements']=__import__('re').findall(r'(?:Geldend van|Geraadpleegd op)[^<\n]+',s)
   rec['accepted']=r.status==200 and (('Burgerlijk Wetboek Boek 7' in s and 't/m heden' in s) if name=='bw7.html' else ('Artikel 51' in s and 'Omzetting' in s and len(s)>10000))
 except Exception as err:rec['error']=str(err)
 return rec
with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,targets))
p=S/'review-art-241d-253-external-fetch.json';p.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
for r in records:print({k:v for k,v in r.items() if k!='xml_attributes'})
