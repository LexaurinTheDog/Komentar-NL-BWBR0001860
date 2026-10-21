from pathlib import Path
import urllib.request,datetime,hashlib,json,xml.etree.ElementTree as E,re,concurrent.futures
W=Path.cwd(); S=W/'sources'
items=[('current.html','https://wetten.overheid.nl/BWBR0001860'),('selected.xml','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/2026-09-01_0/xml/BWBR0001860_2026-09-01_0.xml'),('wti.xml','https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/BWBR0001860.WTI'),('hr-2020-322.xml','https://data.rechtspraak.nl/uitspraken/content?id=ECLI:NL:HR:2020:322'),('ghams-2016-4304.xml','https://data.rechtspraak.nl/uitspraken/content?id=ECLI:NL:GHAMS:2016:4304')]
def fetch(x):
 name,url=x;p=S/('author-art-297-313-'+name);stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=90) as r:b=r.read();status=r.status;final=r.url
 p.write_bytes(b);d=dict(url=url,access_timestamp_utc=stamp,http_status=status,final_url=final,raw_path=str(p.relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
 if name.endswith('.xml'):
  root=E.fromstring(b);d['xml_root']=root.tag
  if 'hr-' in name or 'ghams-' in name:
   body=root.find('{http://www.rechtspraak.nl/schema/rechtspraak-1.0}uitspraak');assert body is not None
   p.with_suffix('.txt').write_text('\n'.join(''.join(n.itertext()) for n in body),encoding='utf-8')
 else:d['validity_statements']=re.findall(r'Geldend van[^<]+',b.decode())
 d['accepted']=True;return d
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: records=list(ex.map(fetch,items))
(S/'author-art-297-313-fetch.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(records,indent=2,ensure_ascii=False))
