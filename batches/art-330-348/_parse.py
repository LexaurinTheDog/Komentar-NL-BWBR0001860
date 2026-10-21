#!/usr/bin/env python3
"""Reproducible bounded extraction, selected official toestand only."""
from pathlib import Path
import xml.etree.ElementTree as E,re,json,hashlib
W=Path(__file__).resolve().parent
P=W/'sources/author-art-330-348-selected.xml';r=E.parse(P).getroot()
assert r.tag=='toestand' and r.get('bwb-id')=='BWBR0001860' and r.get('inwerkingtreding')=='2026-09-01'
IDS=['art-'+str(n) for n in range(330,349)];IDS.insert(4,'art-333a')
SKIP={'meta-data','kop'}
BLOCK={'al','lid','lijst','li','lidnr','li.nr','wij','considerans.al','afkondiging','slotformulering','gegeven','ondertekening','uitgifte','dagtekening'}
def text(e):
 if e.tag in SKIP:return ''
 out=e.text or ''
 for c in e:
  s=text(c)
  out+=('\n\n'+s+'\n\n') if c.tag in BLOCK else s
  out+=c.tail or ''
 return out

def render(e):
 s=re.sub(r'[ \t\r\f\v]+',' ',text(e));s=re.sub(r' *\n *','\n',s);s=re.sub(r'\n{3,}','\n\n',s).strip()
 return re.sub(r'(^|\n\n)(\d+|[a-z]+[.)]|[–−-])\n\n',r'\1\2 ',s)
units=[];expected=[]
for a in r.iter('artikel'):
 nr=a.findtext('kop/nr','').strip();uid='art-'+nr
 if uid not in IDS:continue
 expected.append(uid);chapter=44 if nr in {'347','348'} else 43
 units.append(dict(id=uid,label='Artikel '+nr,title='',chapter=chapter,structure=['Titel III Schuldsaneringsregeling natuurlijke personen','Zevende afdeling De vereffening van de boedel' if chapter==44 else 'Zesde afdeling Het akkoord'],text=render(a),notes=[render(n) for n in a.findall('./meta-data/brondata/opmerkingen-inhoud')],official_path=a.get('bwb-ng-variabel-deel'),official_status=a.get('status'),effective_from=a.get('inwerking'),xml_id=a.get('id')))
assert expected==IDS and len({u['id'] for u in units})==20
(W/'units.jsonl').write_text(''.join(json.dumps(u,ensure_ascii=False)+'\n' for u in units))
print(json.dumps({'units':len(units),'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'expected_ids':expected,'annexes':len(list(r.iter('bijlage')))}))
