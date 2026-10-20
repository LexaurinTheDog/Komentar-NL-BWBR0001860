from pathlib import Path
import json,sys,shutil,re,subprocess,hashlib
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-215-228';O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_units,load_commentary,quote
r=json.loads((W/'review-result.json').read_text());ids=r['reviewed_ids'];us=load_units(str(W));cs=load_commentary(str(W))
review='''\n\n## Afgebakende tweede lezing — artikelen 215–228

Op 21 oktober 2026 zijn exact twintig toegewezen bepalingen gelezen: 215, 215a, 215b, 216, 217, 218, 219, 220, 221, 222, 222a, 222b, 223, 223a, 223b, 224, 225, 226, 227 en 228. [Bevindingen per artikel en exacte reviewed_ids](sources/review-art-215-228-result.json). Vier commentaren zijn aangevuld: bij 215 de internationale kennisgeving en typering van de procedure via artikel 6; bij 215a het efficiënte looncriterium en het horen van de bewindvoerder via 250(3); bij 223b de beëdiging en uitzonderingen van Rv 177; bij 224 de rechterlijk aangewezen zelfstandige werkkring via 70(2). De overige zestien zijn aanvaard. Alle niet-toegewezen commentaren zijn hashgelijk gebleven.

De [nieuwe officiële captures](sources/review-art-215-228-fetch.json) bewaren URL, UTC-ophaaltijd, HTTP-status, SHA-256 en formaatcontrole. De actuele officiële route vermeldt gelding vanaf 1 september 2026 tot heden. De [preflight](sources/review-art-215-228-preflight-result.json) behoudt 19 oktober 2026 als auteurspeildatum, controleert wijzigingen sinds intake en sluit toekomstige en ongedateerde wijzigingen uit. Historische toestanden van 2002 en 2025 blijven afzonderlijk. De [parsercontrole](sources/review-art-215-228-parser-check.json) vindt 639 unieke officiële artikelen, geen ontbrekende of dubbele identificaties en volledige tekstovereenkomst; parser en dekking zijn opnieuw uitgevoerd met identieke producthashes. De volledige XML bevat geen operationele bijlagen. Aanhef en slot zijn afzonderlijk bewaard.

Beide aangehaalde Hoge Raad-uitspraken zijn volledig gelezen en opnieuw officieel opgehaald: ECLI:NL:HR:2017:1280 en ECLI:NL:HR:2010:BN6123. De nieuwe XML is bytegelijk aan de auteurscaptures; [vergelijking](sources/review-art-215-228-case-comparison.json). De eigen oordelen zijn onderscheiden van de partijstellingen en samenvattingen van het hof. De latere WHOA-uitzonderingen zijn bij het gebruik van de oudere uitleg van 215 behouden. Bij 228 zijn stilzwijgende toestemming, enkele voortzetting, concrete groepsboedelbinding en informatieplicht afzonderlijk gecontroleerd. Zie [selectief onderzoekslog](sources/review-art-215-228-search-log.json) en de bronkaarten. Geen uitputtend jurisprudentieonderzoek of externe professionele goedkeuring wordt geclaimd. De actuele officiële tekst van Rv 177 is daarnaast rechtstreeks gelezen; [capturegegevens](sources/review-art-215-228-rv-fetch.json).

De volledige bouw en strikte validatie zijn uitgevoerd; 100% wettekstovereenkomst, maar ontbrekende commentaren buiten deze batch verhinderen voltooiing van het boek. Het afzonderlijke twintig-artikelencheckpoint is opnieuw gebouwd en strikt gevalideerd. Lengte-, herhalings- en linkcontroles zijn technische controles en bewijzen op zichzelf geen juridische kwaliteit. Deze beoordeling geldt uitsluitend voor de twintig genoemde artikelen.
'''
p=W/'REVIEW.md';assert '## Afgebakende tweede lezing — artikelen 215–228' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing 215–228: [resultaat](sources/'+P+'-result.json), [preflight](sources/'+P+'-preflight-result.json), [selectief onderzoekslog](sources/'+P+'-search-log.json).\n')
parts=['# Artikelen 215–228 — beoordeeld checkpoint','Twintig toegewezen artikelen uit een onvoltooid commentaar. Wettekst 1 september 2026; projectinterne tweede lezing 21 oktober 2026. Vier toelichtingen aangevuld, zestien aanvaard. [Beoordeling](sources/'+P+'-result.json). Commentaar © 2026 Vojtěch Říha; Apache-2.0. Concept; geen externe professionele goedkeuring.']
for u in us:
 if u['id'] in ids:
  parts+=['### '+u['label'],'**Wettekst:**',quote(u['text'])];parts+=['*Redactionele bronnotitie:* '+n for n in u['notes']];parts+=[cs[u['id']]]
(O/'30-art-215-228-checkpoint.md').write_text('\n\n'.join(parts)+'\n')
p=O/'INDEX.md';p.write_text(p.read_text().replace('Auteurscheckpoint: artikelen 215–228','Beoordeeld checkpoint: artikelen 215–228'))
# Rebuild the existing explicitly bounded manuscript using the shared builder.
B=W/'batches/art-215-228';T=O/'batches/art-215-228';shutil.copyfile(W/'commentary/part-25.md',B/'commentary/part-25.md')
p=B/'README.md';s=p.read_text().replace('Een onafhankelijke tweede lezing van deze auteursbatch is nog niet uitgevoerd.','Een projectinterne tweede lezing van alle twintig artikelen is op 21 oktober 2026 uitgevoerd; vier commentaren zijn aangevuld. Zie REVIEW.md en de exacte reviewed_ids in sources/review-art-215-228-result.json.');p.write_text(s)
(B/'REVIEW.md').write_text('# Tweede lezing artikelen 215–228\n'+review)
q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/build_repo.py',str(B)],capture_output=True,text=True);assert q.returncode==0,q.stderr;(S/(P+'-bounded-build.txt')).write_text(q.stdout+q.stderr)
for n in ['REVIEW.md','SOURCES.md','preflight-result.json','status.json','review-result.json','review-checks.json']:shutil.copyfile(W/n,O/n)
for target in [O,T]:
 for p in S.glob(P+'-*'):shutil.copyfile(p,target/'sources'/p.name)
 for n in ['verification.json']:shutil.copyfile(S/n,target/'sources'/n)
for n in ['REVIEW.md']:shutil.copyfile(B/n,T/n)
for p in W.glob('_review_215_228_*.py'):shutil.copyfile(p,O/p.name)
# Only new checkpoint/evidence links; pre-existing unrelated content stays outside this review.
checked=0;broken=[]
for p in [O/'30-art-215-228-checkpoint.md',T/'REVIEW.md',T/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',link):continue
  checked+=1
  if not (p.parent/link.split('#')[0]).exists():broken.append([str(p),link])
assert not broken,broken
j=json.loads((W/'review-checks.json').read_text());j.update(local_links_checked=checked,broken_local_links=broken)
for p in [W/'review-checks.json',S/(P+'-checks.json'),O/'review-checks.json',O/'sources'/(P+'-checks.json'),T/'sources'/(P+'-checks.json')]:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
j=json.loads((W/'source-manifest.json').read_text());j['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];j['scope']='Preserved evidence through bounded review215–228; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reviewed':20,'corrected':4,'links_checked':checked,'whole_book_complete':False}))
