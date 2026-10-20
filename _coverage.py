#!/usr/bin/env python3
"""Independent official XML/HTML inventory; no identifiers derived from parser output."""
from pathlib import Path
import xml.etree.ElementTree as E,json,re,hashlib,collections,html
W=Path(__file__).resolve().parent
raw=W/'sources/official-2026-09-01.xml';r=E.parse(raw).getroot()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
norm=lambda s:re.sub(r'\s+','',s)
a=[x for x in r.iter() if x.tag=='artikel'];expected=[]
for x in a:
 m=re.fullmatch(r'Artikel (\d+[a-z]*[0-9]*\*?)',x.attrib['label']);assert m,x.attrib
 expected.append('art-'+m[1])
u=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()];parsed=[x['id'] for x in u]
by_id={x['id']:x for x in u}
# HTML TOC supplies a second official structural enumeration, independent of both scripts.
hp=W/'sources/preflight-2026-10-20-current.html';hs=hp.read_text()
html_ids=['art-'+html.unescape(re.sub('<[^>]+>','',t)).strip().removeprefix('Artikel ') for t in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',hs)]
ann=[x for x in r.iter() if 'bijlage' in x.tag.lower() or 'annex' in x.tag.lower()]
html_annex_anchors=re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>([^<]*(?:Bijlage|Annex)[^<]*)</a>',hs)
assert not ann and not html_annex_anchors
annexes=[{'status':'verified_absence','method':'Full XML tag enumeration and official HTML TOC: no annex elements or annex entries. References to annexes in other instruments and case-file attachments are not annexes of this Act.','xml_annex_elements':0,'html_annex_toc_entries':0,'html_evidence_path':str(hp.relative_to(W)),'html_sha256':sha(hp),'direct_wettekst_children':[{'tag':x.tag,'official_path':x.get('bwb-ng-variabel-deel'),'articles':len(x.findall('.//artikel'))} for x in r.findall('.//wettekst/*')]}]
evidence={'official_source':{'url':'https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/2026-09-01_0/xml/BWBR0001860_2026-09-01_0.xml','local_raw_evidence_path':'sources/official-2026-09-01.xml','sha256':sha(raw)},'expected_ids':expected,'parsed_ids':parsed,'independent_method':'All official XML artikel @label attributes; second check against official HTML TOC anchor text. Neither inventory uses units.jsonl or parser identifiers.','html_expected_ids':html_ids,'html_evidence_path':str(hp.relative_to(W)),'html_sha256':sha(hp),'annex_disposition':annexes}
(W/'coverage-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
# Independent text flattening: metadata/headings excluded; every other legal token retained.
def tokens(e):
 if e.tag in {'meta-data','kop'}:return ''
 return (e.text or '')+''.join(' '+tokens(c)+' '+(c.tail or '') for c in e)
bad=[key for node,key in zip(a,expected) if key not in by_id or norm(tokens(node))!=norm(by_id[key]['text'])]
non_articles=json.loads((W/'sources/non-article-text.json').read_text())
canonical=(W/'sources/canonical.md').read_text()
boundary_checks=[]
for tag in ['intitule','citeertitel','aanhef','wetsluiting']:
 node=r.find('.//'+tag);n=next(x for x in non_articles if x['tag']==tag)
 boundary_checks.append({'tag':tag,'official_path':node.get('bwb-ng-variabel-deel'),'text_sha256':hashlib.sha256(n['text'].encode()).hexdigest(),'raw_tokens_equal':norm(tokens(node))==norm(n['text']),'canonical_contains':n['text'] in canonical,'disposition':n['disposition']})
# Account for every editorial note, including all structural notes omitted in the earlier export.
parents={c:p for p in r.iter() for c in p};note_checks=[]
structural=json.loads((W/'sources/structural-editorial-notes.json').read_text())
for note in r.findall('.//opmerkingen-inhoud'):
 node=parents[note]
 while node.tag not in {'artikel','titeldeel','afdeling','paragraaf','aanhef','wetsluiting','wetgeving'}:node=parents[node]
 if node.tag=='artikel':
  key='art-'+node.get('label').split()[-1];matched=any(norm(tokens(note))==norm(n) for n in by_id[key]['notes'])
 else:
  candidates=[n for n in structural if n['official_path']==node.get('bwb-ng-variabel-deel') and norm(n['text'])==norm(tokens(note))]
  matched=bool(candidates) and all(any(norm(n['text']) in norm(b) for b in by_id[n['display_at']]['notes']) for n in candidates)
 note_checks.append({'official_path':node.get('bwb-ng-variabel-deel'),'parent_tag':node.tag,'preserved':matched})
# No free-standing operative leaf text may escape the article/boundary inventory.
allowed={'intitule','citeertitel','aanhef','wetsluiting','artikel','kop','meta-data'}
unaccounted=[]
for node in r.iter():
 if not (node.text or '').strip():continue
 chain=[];p=node
 while p in parents:chain.append(p.tag);p=parents[p]
 if not any(t in allowed for t in chain):unaccounted.append({'tag':node.tag,'text':node.text})
rep={'source_sha256':sha(raw),'expected_count':len(expected),'parsed_count':len(parsed),'missing':sorted(set(expected)-set(parsed)),'extra':sorted(set(parsed)-set(expected)),'duplicates':[k for k,v in collections.Counter(parsed).items() if v>1],'official_identifier_duplicates':[k for k,v in collections.Counter(expected).items() if v>1],'official_path_duplicates':[k for k,v in collections.Counter(x.get('bwb-ng-variabel-deel') for x in a).items() if v>1],'order_equal':expected==parsed,'html_toc_count':len(html_ids),'html_toc_order_equal':html_ids==expected,'raw_xml_token_mismatch':bad,'repealed_slots':[{'id':'art-'+x.get('label').split()[-1],'effective_from':x.get('inwerking'),'text':'Vervallen'} for x in a if x.get('status')=='vervallen'],'structural_headings':[{'tag':x.tag,'path':x.get('bwb-ng-variabel-deel'),'heading':' '.join(''.join(x.find('kop').itertext()).split())} for x in r.iter() if x.tag in {'titeldeel','afdeling','paragraaf'}],'non_article_text':boundary_checks,'unaccounted_legal_text_nodes':unaccounted,'editorial_notes':len(note_checks),'structural_editorial_notes':len(structural),'editorial_note_disposition':note_checks,'footnote_elements':len(r.findall('.//noot')),'annexes':annexes,'numbering_disposition':[{'ids':['art-212hgd*','art-212hgd'],'reason':'Distinct current official labels and XML paths Artikel212hgd_1 / Artikel212hgd_2. Both preserved; not a historical duplicate.'},{'absent_numeric_range':'363–368','reason':'No article elements or HTML TOC entries in the selected official version; no invented repealed slots. Article 362 and articles 369–387 preserved.'}],'limitations':['Completeness proves coverage of this official toestand, not accuracy or completeness of legal commentary.','Editorial references to external transitional provisions remain source annotations; their full substantive assessment is outside this preflight.']}
rep['ok']=not any([rep['missing'],rep['extra'],rep['duplicates'],rep['official_identifier_duplicates'],rep['official_path_duplicates'],bad,unaccounted]) and rep['order_equal'] and rep['html_toc_order_equal'] and all(x['raw_tokens_equal'] and x['canonical_contains'] for x in boundary_checks) and all(x['preserved'] for x in note_checks)
(W/'completeness-report.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in rep.items() if k in ['ok','expected_count','parsed_count','missing','extra','duplicates','raw_xml_token_mismatch','html_toc_count','html_toc_order_equal','editorial_notes','structural_editorial_notes','unaccounted_legal_text_nodes']}))
assert rep['ok']
