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
        if e.get('status')=='vervallen':assert t=='Vervallen'
        assert t
        units.append({'id':'art-'+nr,'label':label,'title':'','chapter':len(chapters),'structure':structure,'text':t,'notes':notes,'official_path':e.get('bwb-ng-variabel-deel'),'official_status':e.get('status'),'effective_from':e.get('inwerking'),'xml_id':e.get('id')})
        return
    for c in e:
        if c.tag not in SKIP:walk(c,structure)
walk(R.find('.//wettekst'),[])
assert len(units)==639 and len({u['id'] for u in units})==639
(W/'units.jsonl').write_text(''.join(json.dumps(u,ensure_ascii=False)+'\n' for u in units))
canonical=['# Faillissementswet — BWB-toestand 2026-09-01','## Aanhef',render(R.find('.//aanhef'))]
for u in units:canonical +=['## '+u['label'],u['text']]+['Redactionele aantekening: '+n for n in u['notes']]
canonical+=['## Slotformulier en ondertekening',render(R.find('.//wetsluiting'))]
(W/'sources/canonical.md').write_text('\n\n'.join(canonical)+'\n')
meta={'cc':'nl','lang':'nl','repo':'Komentar-NL-BWBR0001860','repo_dir':'/Volumes/LaCie/open-commentary/nl/Komentar-NL-BWBR0001860','title':'Commentaar op de Faillissementswet','source_path':str(W/'sources/canonical.md'),'source_url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01','decisive_date':'2026-10-19','version_effective_from':'2026-09-01','intro_file':'00-inleiding.md','intro_desc':'Stelsel, methode en bronverantwoording','labels':{'text':'Wettekst','chapter':'Hoofdstuk','notes':'Redactionele aantekening'},'chapters':chapters}
(W/'meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(f'{len(units)} units; {len(chapters)} chapters')
