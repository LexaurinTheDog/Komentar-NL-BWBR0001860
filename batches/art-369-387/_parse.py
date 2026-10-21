from pathlib import Path
import ast,json,xml.etree.ElementTree as E
W=Path(__file__).resolve().parent
ns={};exec('import re',ns)
for n in ast.parse((W.parent.parent/'_parse.py').read_text()).body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'SKIP','BLOCK'} for t in n.targets):exec(compile(ast.Module(body=[n],type_ignores=[]),'<renderer>','exec'),ns)
 if isinstance(n,ast.FunctionDef) and n.name in {'text','render'}:exec(compile(ast.Module(body=[n],type_ignores=[]),'<renderer>','exec'),ns)
us=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()]
r=E.parse(W/'sources/author-art-369-387-selected.xml').getroot()
lookup={'art-'+a.findtext('kop/nr','').strip():a for a in r.iter('artikel')}
for u in us:u['text']=ns['render'](lookup[u['id']])
(W/'units.jsonl').write_text(''.join(json.dumps(u,ensure_ascii=False)+'\n' for u in us))
