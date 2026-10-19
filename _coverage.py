#!/usr/bin/env python3
"""Independent coverage inventory: XML labels/paths vs parsed kop identifiers."""
from pathlib import Path
import xml.etree.ElementTree as E,json,re,hashlib,collections
W=Path(__file__).resolve().parent
raw=W/'sources/official-2026-09-01.xml';r=E.parse(raw).getroot()
# Independent traversal: article @label, not parser output or kop/nr.
a=[x for x in r.iter() if x.tag=='artikel']
expected=[]
for x in a:
    m=re.fullmatch(r'Artikel (\d+[a-z]*[0-9]*\*?)',x.attrib['label']);assert m,x.attrib
    expected.append('art-'+m[1])
u=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()]
parsed=[x['id'] for x in u]
ann=[x for x in r.iter() if 'bijlage' in x.tag.lower() or 'annex' in x.tag.lower()]
assert not ann
h=hashlib.sha256(raw.read_bytes()).hexdigest()
evidence={'official_source':{'url':'https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/2026-09-01_0/xml/BWBR0001860_2026-09-01_0.xml','local_raw_evidence_path':'sources/official-2026-09-01.xml','sha256':h},'expected_ids':expected,'parsed_ids':parsed,'annex_disposition':[{'status':'verified_absence','method':'Full XML element enumeration: no bijlage or annex elements; all direct wettekst children inventoried.','direct_wettekst_children':[{'tag':x.tag,'official_path':x.get('bwb-ng-variabel-deel'),'articles':len(x.findall('.//artikel'))} for x in r.findall('.//wettekst/*')]}]}
(W/'coverage-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
# Token stream fidelity to raw XML excludes only metadata/kop; no legal tokens discarded.
def tokens(e):
 if e.tag in {'meta-data','kop'}:return ''
 s=e.text or ''
 for c in e:s+=' '+tokens(c)+' '+(c.tail or '')
 return s
norm=lambda s:re.sub(r'\s+','',s)
bad=[]
for x,y in zip(a,u):
 if norm(tokens(x))!=norm(y['text']):bad.append(y['id'])
rep={'source_sha256':h,'expected_count':len(expected),'parsed_count':len(parsed),'missing':sorted(set(expected)-set(parsed)),'extra':sorted(set(parsed)-set(expected)),'duplicates':[k for k,v in collections.Counter(parsed).items() if v>1],'order_equal':expected==parsed,'raw_xml_token_mismatch':bad,'repealed_slots':[{'id':'art-'+x.get('label').split()[-1],'effective_from':x.get('inwerking'),'text':'Vervallen'} for x in a if x.get('status')=='vervallen'],'structural_headings':[{'tag':x.tag,'path':x.get('bwb-ng-variabel-deel')} for x in r.iter() if x.tag in {'titeldeel','afdeling','paragraaf'}],'non_article_text':{'aanhef':'preserved in sources/canonical.md, constitutional promulgation and consideration, discussed in introduction','wetsluiting':'preserved in sources/canonical.md, promulgation/signature, no separate operative numbered rule'},'editorial_notes':sum(len(x.get('notes',[])) for x in u),'footnote_elements':len(r.findall('.//noot')),'annexes':evidence['annex_disposition']}
rep['ok']=not(rep['missing'] or rep['extra'] or rep['duplicates'] or bad) and rep['order_equal']
(W/'completeness-report.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in rep.items() if k in ['ok','expected_count','parsed_count','missing','extra','duplicates','raw_xml_token_mismatch']}))
