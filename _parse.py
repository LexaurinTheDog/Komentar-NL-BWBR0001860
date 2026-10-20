#!/usr/bin/env python3
"""Reproducible BWB XML extraction. Only the selected toestand is parsed."""
from pathlib import Path
import xml.etree.ElementTree as ET
import re,json,hashlib,collections
W=Path(__file__).resolve().parent
RAW=W/'sources/official-2026-09-01.xml'
R=ET.parse(RAW).getroot()
assert R.tag=='toestand' and R.get('bwb-id')=='BWBR0001860'
assert R.get('inwerkingtreding')=='2026-09-01'
SKIP={'meta-data','kop'}
BLOCK={'al','lid','lijst','li','lidnr','li.nr','wij','considerans.al','afkondiging','slotformulering','gegeven','ondertekening','uitgifte','dagtekening'}
def text(e):
    if e.tag in SKIP:return ''
    out=e.text or ''
    for c in e:
        s=text(c)
        if c.tag in BLOCK:out+='\n\n'+s+'\n\n'
        else:out+=s
        out+=c.tail or ''
    return out

def render(e):
    s=text(e)
    s=re.sub(r'[ \t\r\f\v]+',' ',s)
    s=re.sub(r' *\n *','\n',s)
    s=re.sub(r'\n{3,}','\n\n',s).strip()
    # Keep paragraph and letter labels attached to their following paragraph.
    s=re.sub(r'(^|\n\n)(\d+|[a-z]+[.)]|[–−-])\n\n',r'\1\2 ',s)
    return s

def heading(e):
    k=e.find('kop')
    return re.sub(r'\s+',' ',''.join(k.itertext())).strip() if k is not None else e.get('label','')

# Structural editorial notes belong to their official heading, not to its wording.
# Attach them once to the first article below that heading for shared-builder display.
structural_notes=[]
for node in R.iter():
    if node.tag not in {'titeldeel','afdeling','paragraaf'}: continue
    descendants=node.findall('.//artikel')
    for note in node.findall('./meta-data/brondata/opmerkingen-inhoud'):
        structural_notes.append({'official_path':node.get('bwb-ng-variabel-deel'),
            'heading':heading(node), 'text':render(note),
            'display_at':'art-'+descendants[0].findtext('kop/nr').strip() if descendants else None})
assert all(n['display_at'] for n in structural_notes), 'Unattached structural editorial note'
(W/'sources/structural-editorial-notes.json').write_text(json.dumps(structural_notes,ensure_ascii=False,indent=2)+'\n')
non_articles=[]
for tag in ['intitule','citeertitel','aanhef','wetsluiting']:
    nodes=R.findall('.//'+tag);assert len(nodes)==1, tag
    node=nodes[0]
    non_articles.append({'tag':tag,'official_path':node.get('bwb-ng-variabel-deel'),
        'text':render(node),'text_sha256':hashlib.sha256(render(node).encode()).hexdigest(),
        'disposition':'Preserved in canonical source; unnumbered title/promulgation material, not an article slot.'})
(W/'sources/non-article-text.json').write_text(json.dumps(non_articles,ensure_ascii=False,indent=2)+'\n')
units=[];chapters=[];group=None;count=0

def walk(e,structure):
    global group,count
    if e.tag in ('titeldeel','afdeling','paragraaf'):
        structure=structure+[heading(e)]
    if e.tag=='artikel':
        label=e.get('label');nr=e.findtext('kop/nr').strip();assert label=='Artikel '+nr
        g=tuple(structure[:2] if structure and structure[0].startswith('Titel') else structure[:1])
        if group!=g or count>=25:
            n=len(chapters)+1
            chapters.append({'n':n,'slug':f'wet-{n:02d}','title':' / '.join(g) or 'Slotbepalingen'})
            group=g;count=0
        count+=1
        t=render(e)
        notes=[render(x) for x in e.findall('./meta-data/brondata/opmerkingen-inhoud') if render(x)]
        notes += ['Bij '+n['heading']+': '+n['text'] for n in structural_notes if n['display_at']=='art-'+nr]
        if e.get('status')=='vervallen':assert t=='Vervallen'
        assert t
        units.append({'id':'art-'+nr,'label':label,'title':'','chapter':len(chapters),'structure':structure,'text':t,'notes':notes,'official_path':e.get('bwb-ng-variabel-deel'),'official_status':e.get('status'),'effective_from':e.get('inwerking'),'xml_id':e.get('id')})
        return
    for c in e:
        if c.tag not in SKIP:walk(c,structure)
walk(R.find('.//wettekst'),[])
assert len(units)==639 and len({u['id'] for u in units})==639
(W/'units.jsonl').write_text(''.join(json.dumps(u,ensure_ascii=False)+'\n' for u in units))
canonical=['# Faillissementswet — BWB-toestand 2026-09-01']
for n in non_articles[:3]: canonical += ['## '+n['tag'],n['text']]
for u in units:canonical +=['## '+u['label'],u['text']]+['Redactionele aantekening: '+n for n in u['notes']]
canonical+=['## Slotformulier en ondertekening',render(R.find('.//wetsluiting'))]
(W/'sources/canonical.md').write_text('\n\n'.join(canonical)+'\n')
meta={'cc':'nl','lang':'nl','repo':'Komentar-NL-BWBR0001860','repo_dir':'/Volumes/LaCie/open-commentary/nl/Komentar-NL-BWBR0001860','title':'Commentaar op de Faillissementswet','source_path':str(W/'sources/canonical.md'),'source_url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01','decisive_date':'2026-10-19','version_effective_from':'2026-09-01','source_verification_date':'2026-10-20','source_verification_evidence':'sources/verification.json','non_article_text_path':'sources/non-article-text.json','structural_editorial_notes_path':'sources/structural-editorial-notes.json','intro_file':'00-inleiding.md','intro_desc':'Stelsel, methode en bronverantwoording','labels':{'text':'Wettekst','chapter':'Hoofdstuk','notes':'Redactionele aantekening'},'chapters':chapters}
(W/'meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(f'{len(units)} units; {len(chapters)} chapters')
