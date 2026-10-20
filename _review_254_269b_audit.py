from pathlib import Path
import json,sys,re,hashlib,datetime,subprocess,xml.etree.ElementTree as E,shutil,collections,html
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-254-269b'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W))
ids=['art-'+x for x in '254 255 256 257 257a 258 259 260 261 262 263 264 265 266 267 268 268a 269 269a 269b'.split()]
now=datetime.datetime.now(datetime.timezone.utc).isoformat();before=json.loads((S/(P+'-before-hashes.json')).read_text())
assert set(before)==set(cs) and all(before[k]==hashlib.sha256(v.encode()).hexdigest() for k,v in cs.items() if k not in ids)
records=json.loads((S/(P+'-fetch.json')).read_text());cases=json.loads((S/(P+'-case-fetch.json')).read_text())
assert all(x['accepted'] and sha(W/x['raw_path'])==x['sha256'] for x in records+cases)
r=E.parse(S/(P+'-selected.xml')).getroot();expected=['art-'+a.get('label').removeprefix('Artikel ') for a in r.iter('artikel')];parsed=[u['id'] for u in us]
assert expected==parsed and len(expected)==len(set(expected))==639
assert ids==expected[expected.index(ids[0]):expected.index(ids[-1])+1]
assert sha(S/(P+'-selected.xml'))==sha(S/'official-2026-09-01.xml')
def flat(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+flat(c)+' '+(c.tail or '') for c in e)
norm=lambda s:re.sub(r'\s+','',s)
for a in r.iter('artikel'):assert norm(flat(a))==norm(by['art-'+a.get('label').removeprefix('Artikel ')]['text'])
assert not [e for e in r.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
ht=(S/(P+'-current.html')).read_text();htmlids=['art-'+html.unescape(t).strip().removeprefix('Artikel ') for t in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',ht)]
assert htmlids==expected
assert not re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>([^<]*(?:Bijlage|Annex)[^<]*)</a>',ht)
wt=E.parse(S/(P+'-wti.xml')).getroot();dates=sorted({e.get('waarde') for e in wt.findall('./wijzigingen/regeling/datum') if e.get('waarde')})
assert max(d for d in dates if d<='2026-10-21')=='2026-09-01';assert not [d for d in dates if '2026-10-01'<d<='2026-10-21']
names=['units.jsonl','meta.json','coverage-evidence.json','completeness-report.json'];hashes={n:sha(W/n) for n in names}
for script in ['_parse.py','_coverage.py']:
 q=subprocess.run([sys.executable,str(W/script)],capture_output=True,text=True);assert q.returncode==0,q.stderr
assert hashes=={n:sha(W/n) for n in names}
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
save(S/(P+'-parser-check.json'),{'ok':True,'expected_ids':expected,'parsed_ids':parsed,'fresh_html_ids':htmlids,'missing':[],'duplicates':[],'all_official_article_texts_equal':True,'annex_disposition':comp['annexes'],'opening_closing':comp['non_article_text'],'reproduced_hashes':hashes,'official_xml_sha256':sha(S/(P+'-selected.xml'))})
pre=json.loads((S/'author-art-254-269b-preflight-result.json').read_text());pre.update(verified_at=now,review_date_local='2026-10-21',parser_evidence='sources/'+P+'-parser-check.json')
pre['version_evidence'].update(fresh_records='sources/'+P+'-fetch.json',future_dates_excluded=[d for d in dates if d>'2026-10-21'],fresh_wti_matches_previous=sha(S/(P+'-wti.xml'))==sha(S/'author-art-254-269b-wti.xml'))
assert pre['version_evidence']['fresh_wti_matches_previous']
for h in pre['historical_versions_checked']:
 assert sha(W/h['path'])==h['sha256'];old=E.parse(W/h['path']).getroot();labels=[a.get('label') for a in old.iter('artikel')];assert len(labels)==len(set(labels));h['assigned_present_ids']=['art-'+a.removeprefix('Artikel ') for a in labels if 'art-'+a.removeprefix('Artikel ') in ids]
pre['limitations']=['Separate external transitional statutes cited in editorial notes were not independently analysed for historical proceedings.','The substantive second pass covers exactly the twenty assigned units; no whole-book review claimed.']
save(S/(P+'-preflight-result.json'),pre)
p=W/'preflight-result.json';j=json.loads(p.read_text());j['bounded_review_art_254_269b']=pre;save(p,j)
comparisons=[]
for name,ecli in [('hr-2017','ECLI:NL:HR:2017:3110'),('rbdha-2024','ECLI:NL:RBDHA:2024:18898')]:
 a=S/(P+'-'+name+'.xml');b=S/('author-art-254-269b-'+name+'.xml');rt=E.parse(a).getroot();u=rt.find('{*}uitspraak');assert u is not None;assert a.read_bytes()==b.read_bytes()
 rec={'ecli':ecli,'official_sha256':sha(a),'full_text_chars':len(''.join(u.itertext())),'same_as_author_capture':True,'full_text_read':True}
 if name=='hr-2017':
  local=Path('/Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr/ecli-nl-hr-2017-3110.md');dest=S/(P+'-hr-2017-local.md');shutil.copyfile(local,dest);paras=u.findall('.//{*}para');rec.update(local_corpus_path=str(local),local_snapshot=str(dest.relative_to(W)),local_sha256=sha(dest),official_paragraphs=len(paras),unmatched_paragraph_prefixes=[norm(''.join(e.itertext()))[:100] for e in paras if norm(''.join(e.itertext())) not in norm(dest.read_text())])
 comparisons.append(rec)
save(S/(P+'-case-comparison.json'),comparisons)
log=json.loads((S/'author-art-254-269b-search-log.json').read_text());log['second_pass']={'checked_at':now,'scope':'Existing selective research independently reviewed. Two complete official judgments freshly fetched and read; HR local corpus compared. No exhaustive additional judicial research claimed.','holdings':'HR2017:3.4.2–3.5 article282 bar for267/268a;3.6 complaints only;3.7.1 grounds for exceptional review;3.7.2 eight-day deadline;3.8 own disposition;3.10 no distinct complaints against improvement refusal. RBDHA2024:3.16 secured/unsecured split, loss of security on submission, case-specific market valuation;3.17 no unfair preference in these facts. Quoted composition and administrator report in section2 are not judicial holdings.','current_law_comparison':'Current267/268a/269/269a/282 checked. Repealed270 reference in older HR2017 deadline reasoning not presented as a current route. Current257(2) checked against judgment.','limitations':'Selective sources; no exhaustive later-treatment audit. No separately verified relevant judgment added to technical provisions.'};save(S/(P+'-search-log.json'),log)
notes=[
'Verval gekoppeld aan volgorde kracht van gewijsde beëindiging/homologatie; stemming of uitspraakdatum vervangt dat criterium niet. Geen automatische omzetting faillissementsakkoord.',
'Alle drie leden: gelijktijdige indiening en facultatieve route, afzonderlijke data met veertiendagengrens, latere route na onherroepelijke definitieve verlening. Horen RC/bewindvoerders in lid3 expliciet aangevuld.',
'Alle vier leden: dadelijke Staatscourantpublicatie beschikking/neerlegging en beperkte216uitzondering, alle bekende schuldeisers met257(2)waarschuwing, verschijningsvormen en kostenvoorschot gecontroleerd.',
'Alle drie leden: aard/bedrag/bewijs, wettelijke werking en verlies vier rechten, herstel vóór begin stemming voor zover teruggenomen, ontvangbewijs. RBDHA2024 volledige tekst en specifiek3.16–3.17 gelezen; geen universele waarderingsregel.',
'Verwijzing110a en55/5(3)gecontroleerd: onvolledig standaardformulier aanvullen, functionele rol bewindvoerder, geen erkenning of automatische termijnverlenging.',
'Vergelijking administratie/opgaven, overleg bij toelatingsbezwaar, ontbrekende stukken en raadpleging oorspronkelijke administratie/bewijs gecontroleerd. Voorbeeld creditnota relevant; geen automatisch primaat schuldenaarboekhouding.',
'Naam/woonplaats/bedrag/omschrijving en geheel/gedeeltelijke erkenning/betwisting, actualisering266 en gewaarmerkte bijlage269 gecontroleerd. Geen materiële erkenning door enkele plaatsing.',
'Rentegrens en alle geïmporteerde bepalingen129/133–135/136(1–2)gelezen. Toondervordering per schuldeiser en de alternatieve voorwaarden regresopneming verduidelijkt; vervallen135 levert geen extra norm.',
'Beide leden, aanvangswaarde versus volle voorwaardelijke toelating bij waarderingsonenigheid gecontroleerd. Bestaansbetwisting onderscheiden; ontbindend via260/129.',
'Alle drie leden: onzeker tijdstip/periodiek, verval binnen jaar, waarde na eerste jaar bij later verval, uitsluitend opgesomde factoren. Geen willekeurige insolventiekorting of opname elke toekomstige relatie.',
'Beide leden: afschrift lijst, griffie, zeven voorafgaande dagen, ieder kosteloze inzage en kosteloze neerlegging. Geen automatische kosteloze toezendingsplicht afgeleid.',
'Beide leden: alleen RCbeslissing ambtshalve/bewindvoerdersverzoek en overeenkomstige256communicatie/verschijning/voorschot. Aangepaste inzageplanning263 onderscheiden van enkele onderlinge afspraak.',
'Alle vijf leden en144gelezen: schriftelijke verslagen, toelichten/wijzigen, laat-maar-tweedagentijdige aanmelding met verzoek, latere uitsluiting, causale buitenlandse verhindering, RCbeslissing na raadpleging. Verplichte plaatsing zonder bezwaar en beslisroute bij bezwaar verduidelijkt.',
'Alle drie leden: herziening eigen erkenning/betwisting bewindvoerders, zelfstandige betwisting schuldenaar/verschenen schuldeiser, lijstactualisering. Stemrechtbeslissing267 onderscheiden van vaststelling schuld.',
'Procesrechtelijke stemtoelating/bedrag en verbinding259/266/268 gecontroleerd; volledige HR2017:3.4.2–3.5/3.7.1/3.8.3gelezen; geen gewoon rechtsmiddel of definitief betalingsvonnis afgeleid.',
'Beide leden, dubbele meerderheid en verschillende noemers gecontroleerd: gewone verschenen personenmeerderheid, ten minste helft totale erkende/toegelaten bedragen, dwangsomuitzondering, latere wijzigingen147. Rekenvoorbeeld correct.',
'Cumulatieve drie-vierdedrempel en concreet onredelijk tegenstemmen, omstandigheden/liquidatiebetaling, verzoek en gemotiveerde RCbeschikking gecontroleerd. HR2017rechtsmiddelenbeperking en partijstellingen onderscheiden; vaststelling geen homologatie.',
'Beide leden: volledige PVinhoud, lijst gewaarmerkt door RC/griffier, acht dagen ieder kosteloze inzage. Expliciet verduidelijkt dat HR2017:3.6.2een klacht weergeeft en3.8.3het eigen oordeel bevat; geen vastgesteld PVgebrek.',
'Toezending na verworpenverklaring, beperkte verzoekersgroep, acht dagen na vergadering, uit stukken zelf blijkende fout en269bgecontroleerd. HR2017:3.10geen inhoudelijke uitspraak over afwijzingsgronden.',
'Alle vier leden: RCvóór sluiting, rechtbank bij269aen schriftelijke kennisgeving, acht/veertien dagen met twee aanknopingsmomenten, schriftelijke bezwaren RC,271eigen uitstelroute. Praktische checklist en voorbeeld beoordeeld.'
]
rows=[]
for i,n in zip(ids,notes):
 after=hashlib.sha256(cs[i].encode()).hexdigest();rows.append({'id':i,'official_path':by[i]['official_path'],'finding':n,'result':'corrected' if before[i]!=after else 'accepted_without_change','before_sha256':before[i],'after_sha256':after,'statutory_sha256':hashlib.sha256(by[i]['text'].encode()).hexdigest()})
assert len(rows)==20 and len(notes)==20
paras=[p for i in ids for p in cs[i].split('\n\n') if len(p)>200];assert len(paras)==len(set(paras));assert all(len(cs[i])>=700 for i in ids)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[r['id'] for r in rows if r['result']=='corrected'],'checked_at_utc':now,'whole_book_complete':False,'limitations':['Only twenty assigned units reviewed; no external professional approval.','Existing selective judicial research verified; no exhaustive case-law or later-treatment research claimed.','Whole-book authoring remains incomplete.','Separate external transitional statutes in editorial notes not independently analysed for historical proceedings.']}
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,result)
checks={'ok':True,'reviewed_ids':ids,'unassigned_commentaries_unchanged':True,'duplicate_long_paragraphs':0,'commentary_chars':{i:len(cs[i]) for i in ids},'source_agreement':1.0,'whole_book_complete':False}
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,checks)
p=S/'verification.json';j=json.loads(p.read_text());j['bounded_review_art_254_269b']={'records':records+cases,'preflight':'sources/'+P+'-preflight-result.json'};save(p,j)
p=W/'status.json';j=json.loads(p.read_text());j['bounded_review_art_254_269b']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/'+P+'-result.json'};save(p,j)
print(json.dumps({'reviewed':20,'changed':result['changed_units'],'all_639_texts_exact':True}))
