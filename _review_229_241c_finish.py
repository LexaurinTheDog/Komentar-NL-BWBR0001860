from pathlib import Path
import sys,json,shutil,re,hashlib,subprocess,xml.etree.ElementTree as E
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-229-241c'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools');from build_repo import load_units,load_commentary,quote
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);r=json.loads((W/'review-result.json').read_text());ids=r['reviewed_ids'];cs=load_commentary(str(W));us=load_units(str(W))
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
review='''\n\n## Afgebakende tweede lezing — artikelen 229–241c

Op 21 oktober 2026 zijn exact twintig artikelen beoordeeld: 229, 230, 231, 231a, 232, 233, 234, 235, 236, 236a, 237, 237a, 237b, 238, 239, 240, 241, 241a, 241b en 241c. [Bevindingen en exacte reviewed_ids](sources/review-art-229-241c-result.json). Zes commentaren zijn verbeterd: bij 230 de zesmaandenverlenging en vervaltermijnen via artikel 36; bij 234 de waardering volgens 261–262; bij 238 het onderscheid tussen schade bij wettelijke opzegging en contractuele ontbinding en de mogelijke grens van redelijkheid en billijkheid; bij 239 de concreet verwezen opzegtermijnen; bij 240 gedeeltelijke bevrijding in plaats van verwarrende verrekeningsterminologie; bij 241b de voorwaardelijke bewaarroute van Rv 490b lid 2. De laatste correctie herstelt de te ruime indruk dat iedere ontvangst onvoorwaardelijk tot volledige storting verplicht. Alle veertien overige commentaren zijn aanvaard. Niet-toegewezen commentaren zijn hashgelijk gebleven.

De [verse broncaptures](sources/review-art-229-241c-fetch.json) bewaren URL, UTC-ophaaltijd, HTTP 200, SHA-256 en formaatcontrole. De [preflight](sources/review-art-229-241c-preflight-result.json) behoudt de auteurspeildatum 19 oktober 2026. De actuele officiële route vermeldt gelding van 1 september 2026 tot heden; de raadpleegdatum en UTC-ophaaltijd zijn apart gehouden. Het wijzigingsregister toont geen ingegane wijziging sinds intake; toekomstige en ongedateerde wijzigingen zijn uitgesloten. De historische toestanden van 2002 en 2025 zijn afzonderlijk op unieke labels en hun uitsluiting uit de huidige extractie gecontroleerd.

De [parsercontrole](sources/review-art-229-241c-parser-check.json) vindt 639 unieke officiële artikelplaatsen en volledige tekstovereenkomst. Parser en onafhankelijke dekkingscontrole zijn opnieuw uitgevoerd met identieke producthashes. Geen ontbrekende of dubbele identificaties of onverklaarde juridische tekst; geen operationele bijlagen in de volledige XML. Aanhef, slot, vervallen plaatsen en structurele bronnotities blijven verantwoord. De brongebonden term ‘curator’ in 241a lid 3 is zichtbaar behouden en niet stilzwijgend gerepareerd.

Beide geciteerde Hoge Raad-uitspraken zijn volledig gelezen en opnieuw officieel opgehaald: ECLI:NL:HR:2023:1135 en ECLI:NL:HR:2005:AT2650. De XML is bytegelijk aan de eerdere capture; lokale nationale corpusversies zijn tevens bewaard en vergeleken. [Vergelijking](sources/review-art-229-241c-case-comparison.json), [selectief onderzoekslog](sources/review-art-229-241c-search-log.json). De eigen oordelen van de Hoge Raad zijn onderscheiden van partijstellingen en de weergegeven lagere uitspraak. Het arrest van 2023 verklaart niet alle concernverrekening definitief geldig. De huuruitspraak van 2005 wordt gebruikt voor het onderscheid in beëindigingsgronden, zonder algemene aanspraak op resterende huurtermijnen. Actuele BW 6:136, BW 7:672 en Rv 490b zijn rechtstreeks gelezen; [capturegegevens](sources/review-art-229-241c-external-fetch.json). Geen uitputtend onderzoek naar alle latere rechtspraak, geen nieuwe autoriteit voor technische bepalingen zonder voldoende geverifieerde relevantie.

De volledige boekbouw en strikte validatie zijn uitgevoerd. De wettekstovereenkomst is 100%; 179 ontbrekende commentaren buiten deze batch verhinderen voltooiing van het boek. Het afzonderlijke checkpoint is met de ongewijzigde gedeelde bouwer samengesteld en apart gevalideerd. Lengte-, herhalings- en linkcontroles zijn technische controles en bewijzen geen juridische kwaliteit. Deze projectinterne tweede lezing geldt uitsluitend voor de genoemde twintig artikelen, zonder externe professionele goedkeuring. De afzonderlijke overgangswetten in bronnotities zijn niet integraal beoordeeld voor historische procedures.
'''
p=W/'REVIEW.md';assert '## Afgebakende tweede lezing — artikelen 229–241c' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing 229–241c: [bevindingen](sources/'+P+'-result.json), [preflight](sources/'+P+'-preflight-result.json), [selectief onderzoek](sources/'+P+'-search-log.json).\n')
parts=['# Artikelen 229–241c — beoordeeld checkpoint','Twintig toegewezen artikelen uit een onvoltooid commentaar. Wettekst 1 september 2026; tweede lezing 21 oktober 2026. Zes toelichtingen gecorrigeerd of aangevuld, veertien aanvaard. [Exacte beoordeling](sources/'+P+'-result.json). Commentaar © 2026 Vojtěch Říha; Apache-2.0. Concept; geen externe professionele goedkeuring.']
for u in us:
 if u['id'] in ids:parts+=['### '+u['label'],'**Wettekst:**',quote(u['text'])]+['*Redactionele bronnotitie:* '+n for n in u['notes']]+[cs[u['id']]]
(O/'31-art-229-241c-checkpoint.md').write_text('\n\n'.join(parts)+'\n')
p=O/'INDEX.md';p.write_text(p.read_text().replace('Auteurscheckpoint: artikelen 229–241c','Beoordeeld checkpoint: artikelen 229–241c'))
# A separately identified bounded build, never substituted for full-book units or metadata.
B=W/'batches/art-229-241c';T=O/'batches/art-229-241c';(B/'commentary').mkdir(parents=True,exist_ok=True);(T/'sources').mkdir(parents=True,exist_ok=True);(B/'sources').mkdir(exist_ok=True)
bm={**m,'repo':m['repo']+'-batch-art-229-241c','repo_dir':str(T),'title':'Faillissementswet — beoordeeld checkpoint artikelen 229–241c','chapters':[c for c in m['chapters'] if c['n'] in {u['chapter'] for u in us if u['id'] in ids}]}
save(B/'meta.json',bm);(B/'units.jsonl').write_text(''.join(json.dumps(u,ensure_ascii=False)+'\n' for u in us if u['id'] in ids));shutil.copyfile(W/'commentary/part-26.md',B/'commentary/part-26.md')
(B/'README.md').write_text('''# Faillissementswet — artikelen 229–241c

Dit afzonderlijke checkpoint bevat uitsluitend twintig bepalingen: 229–231, 231a, 232–236, 236a, 237, 237a, 237b, 238–241, 241a, 241b en 241c. Het volledige boek blijft onvoltooid. De officiële wettekst geldt vanaf 1 september 2026, beoordeeld naar de auteurspeildatum 19 oktober 2026 en opnieuw officieel geverifieerd op 21 oktober 2026 lokale tijd. [Officiële bron](https://wetten.overheid.nl/BWBR0001860/2026-09-01); [preflight](sources/review-art-229-241c-preflight-result.json); [captures met HTTP, tijd en hashes](sources/review-art-229-241c-fetch.json).

De wettekst is mechanisch uit officiële XML overgenomen. Elke toegewezen bepaling heeft een specifieke toelichting en een fictief voorbeeld. Selectief jurisprudentieonderzoek omvat de volledig gelezen Hoge Raad-uitspraken van 25 augustus 2023 en 13 mei 2005; zie de [onderzoeksverantwoording](sources/review-art-229-241c-search-log.json). Geen uitputtende rechtspraakinventarisatie. De tweede lezing heeft alle twintig artikelen behandeld en zes toelichtingen verbeterd; [exacte bevindingen](sources/review-art-229-241c-result.json).

Oorspronkelijk commentaar © 2026 Vojtěch Říha; Apache-2.0, zie LICENSE. Officiële wettekst en uitspraken zijn afzonderlijk herkenbaar en worden niet als oorspronkelijk commentaar geclaimd. Geen commerciële annotaties overgenomen. Concept voor verdere juridische controle; geen externe professionele goedkeuring. Technische validatie bewijst op zichzelf geen juridische kwaliteit.
''')
(B/'00-inleiding.md').write_text('''# Inleiding

Deze batch behandelt uitsluitend de gevolgen van surseance in artikelen 229–241c: gemeenschapsvermogen, executie en procedures, de betrokken schulden, evenredige betaling en verrekening, wederkerige contracten, huur en arbeid, bevrijdende betaling, medeschuldenaren en afkoeling. Artikelen buiten dit bereik zijn niet opnieuw inhoudelijk beoordeeld. Alle leden en bronnoten zijn tegen de officiële geselecteerde versie gelezen. REVEW-evidence en de bronkaarten leggen de grenzen van het selectieve onderzoek vast. De toepasselijke overgangsregelingen bij historische procedures vergen afzonderlijke beoordeling.\n'''.replace('REVEW-evidence','De beoordeling'))
(B/'REVIEW.md').write_text('# Tweede lezing artikelen 229–241c\n'+review)
raw=E.parse(S/(P+'-selected.xml')).getroot();labels=['art-'+a.get('label').removeprefix('Artikel ') for a in raw.iter('artikel')];lo=labels.index('art-229');hi=labels.index('art-241c')+1;exp=labels[lo:hi];assert exp==ids
save(B/'coverage-evidence.json',{'official_source':{'url':m['source_url'],'local_raw_evidence_path':'sources/'+P+'-selected.xml','sha256':hashlib.sha256((S/(P+'-selected.xml')).read_bytes()).hexdigest()},'expected_ids':exp,'parsed_ids':[u['id'] for u in us if u['id'] in ids],'method':'Independently enumerate official XML labels in contiguous229–241c range; outside-range articles remain in whole-book units, not this bounded build.','annex_disposition':'Full official XML has no operative annex elements; opening/closing preserved in whole-book canonical source.'})
q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/build_repo.py',str(B)],capture_output=True,text=True);assert q.returncode==0,q.stderr;(S/(P+'-bounded-build.txt')).write_text(q.stdout+q.stderr)
for target in [B,T]:
 for p in S.glob(P+'-*'):shutil.copyfile(p,target/'sources'/p.name)
 for p in S.glob('author-art-229-241c-case-*.md'):shutil.copyfile(p,target/'sources'/p.name)
 for suffix in ['hr-2023.xml','hr-2005.xml','fetch.json']:shutil.copyfile(S/('author-art-229-241c-'+suffix),target/'sources'/('author-art-229-241c-'+suffix))
shutil.copyfile(B/'REVIEW.md',T/'REVIEW.md');shutil.copyfile(B/'coverage-evidence.json',T/'coverage-evidence.json')
for n in ['REVIEW.md','SOURCES.md','preflight-result.json','status.json','review-result.json','review-checks.json']:shutil.copyfile(W/n,O/n)
for p in S.glob(P+'-*'):shutil.copyfile(p,O/'sources'/p.name)
shutil.copyfile(S/'verification.json',O/'sources/verification.json')
for p in W.glob('_review_229_241c_*.py'):shutil.copyfile(p,O/p.name)
checked=0;broken=[]
for p in [O/'31-art-229-241c-checkpoint.md',T/'REVIEW.md',T/'README.md']+list(T.glob('*wet*.md')):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(https?://|mailto:|#)',link):continue
  checked+=1
  if not (p.parent/link.split('#')[0]).exists():broken.append([str(p),link])
assert not broken,broken
j=json.loads((W/'review-checks.json').read_text());j.update(local_links_checked=checked,broken_local_links=broken)
for p in [W/'review-checks.json',S/(P+'-checks.json'),O/'review-checks.json',O/'sources'/(P+'-checks.json'),T/'sources'/(P+'-checks.json'),B/'sources'/(P+'-checks.json')]:save(p,j)
j=json.loads((W/'source-manifest.json').read_text());j['files']=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d in ['sources','cases'] for p in sorted((W/d).rglob('*')) if p.is_file()];j['scope']='Preserved evidence through bounded review229–241c; whole book incomplete.'
for p in [W/'source-manifest.json',O/'source-manifest.json']:save(p,j)
print(json.dumps({'reviewed':20,'corrected':6,'links_checked':checked,'whole_book_complete':False}))
