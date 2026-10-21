from pathlib import Path
import json,sys,re,hashlib,datetime,subprocess,xml.etree.ElementTree as E,shutil,collections,html
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-270-281h'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W))
ids=['art-'+x for x in '270 271 272 273 274 275 276 277 278 279 280 281 281a 281b 281c 281d 281e 281f 281g 281h'.split()]
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
pre={'complete':True,'decisive_date':m['decisive_date'],'review_date_local':'2026-10-21','official_url':m['source_url'],'verified_at':records[0]['access_timestamp_utc'],'version_evidence':{'selected_toestand':'2026-09-01_0','effective_from':'2026-09-01','current_route_redirect':records[0]['final_url'],'explicit_validity':records[0]['validity_statements'],'changes_since_intake':[],'next_dated_change':min(d for d in dates if d>'2026-10-21'),'xml_sha256':sha(S/(P+'-selected.xml')),'wti_sha256':sha(S/(P+'-wti.xml')),'future_dates_excluded':[d for d in dates if d>'2026-10-21']},'historical_versions_checked':[],'annexes_checked':[{'status':'verified_absence','evidence_path':'sources/'+P+'-selected.xml','method':'All official XML tags and independent HTML TOC enumerated; no operative annex. All non-article opening/closing text and source annotations accounted for by _coverage.py.'}],'unresolved_blockers':[],'parser_evidence':'sources/'+P+'-parser-check.json'}
for name in ['version-register.xml','review-art-212z-213a-historical-2025.xml']:
 old=E.parse(S/name).getroot();ls=[a.get('label') for a in old.iter('artikel')];assert len(ls)==len(set(ls));pre['historical_versions_checked'].append({'path':'sources/'+name,'sha256':sha(S/name),'effective_from':old.get('inwerkingtreding'),'assigned_present_ids':['art-'+a.removeprefix('Artikel ') for a in ls if 'art-'+a.removeprefix('Artikel ') in ids],'disposition':'Excluded historical toestand; current labels drawn only from 2026-09-01 XML. Repealed 270 preserved.'})
save(S/(P+'-preflight-result.json'),pre)
j=json.loads((W/'preflight-result.json').read_text());j['bounded_review_art_270_281h']=pre;save(W/'preflight-result.json',j)
comparisons=[]
for name,ecli,localname in [('hr-2003','ECLI:NL:HR:2003:AI0369','ecli-nl-hr-2003-ai0369.md'),('rbdha-2024','ECLI:NL:RBDHA:2024:18898',None)]:
 raw=S/(P+'-'+name+'.xml');rt=E.parse(raw).getroot();u=rt.find('{*}uitspraak');assert u is not None
 text=''.join(u.itertext());(S/(P+'-'+name+'.txt')).write_text(text)
 rec={'ecli':ecli,'sha256':sha(raw),'full_text_read':True,'full_text_chars':len(text)}
 if localname:
  src=Path('/Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr')/localname;dest=S/(P+'-'+name+'-local.md');shutil.copyfile(src,dest)
  missing=[norm(''.join(e.itertext()))[:120] for e in u.findall('.//{*}para') if norm(''.join(e.itertext())) not in norm(dest.read_text())];assert not missing
  rec.update(local_corpus_path=str(src),local_snapshot=str(dest.relative_to(W)),local_sha256=sha(dest),unmatched_paragraph_prefixes=missing)
 else:
  old=S/'author-art-254-269b-rbdha-2024.xml';assert raw.read_bytes()==old.read_bytes();rec['identical_to_previous_read_snapshot']=True
 comparisons.append(rec)
save(S/(P+'-case-comparison.json'),comparisons)
external=json.loads((S/(P+'-external-fetch.json')).read_text());assert all(x['accepted'] for x in external)
assert 'Afdeling 3.5.6. Beleggerscompensatiestelsel en depositogarantiestelsel' in (S/(P+'-wft.html')).read_text()
notes=[
'Vervallen nummerplaats expliciet behouden. Geen huidige bevoegdheid ontleend; overgangsnoot onderscheiden van geldende norm.',
'Beide leden: openbaar schriftelijk RC-rapport, spreekrecht bewindvoerders/iedere schuldeiser,152(2)schuldenaar en later onmiddellijk vastgestelde zittingsdag;269b en281e(5)vergeleken.',
'Alle zes leden en vier verplichte gronden gecontroleerd. Eerste grond exact gemaakt, vierde als alternatieve kostendekking verduidelijkt met3.9Rb. Zelfstandige toets/motivering HR3.3.2 onderscheiden van vrijheid/cassatietoets3.9.3. Facultatieve gronden, faillissementskeuze, kracht van gewijsde, publicatie, DNB en154–156/160 gelezen.',
'Gebondenheid alle onder surseance vallende schuldeisers, ook tegen/afwezig;232/257 afbakening en274titel onderscheiden;160 derdenrechten.',
'Combinatie onherroepelijke homologatie/PV269, onbetwist door schuldenaar en tot akkoord toegetreden borgen gecontroleerd. Termijnvoorbeeld beperkt tot opeisbare prestatie.',
'Alleen wettelijke termijnvoortduring bij aangeboden, nog niet uiteindelijk beslist akkoord;254andere beëindiging/276succes en272/277mislukking vergeleken.',
'Einde bij kracht van gewijsde, geen constitutieve publicatie of wachten volledige uitvoering. Artikel216 en275 gelezen.',
'Facultatief faillissement, vooraf DNB-horen bijzondere moedermaatschappij, einde zonder faillissement na ongebruikte269a-termijn/weigering verbetering en216publicatie gecontroleerd.',
'Drie leden en acht dagen vanuit269a-verloop, verzoek hof, directe dag/uur en Staatscourant/ieder schuldeiser. Foutieve verwijzing282voor ondertekening gecorrigeerd naar283(1);282algemene beperking apart verklaard.',
'Cassatiegerechtigden afhankelijk van handhaving/vernietiging, optreden in hoger beroep vereist voor schuldeiser. Acht dagen na hofuitspraak verduidelijkt; vier dagen exploot en283(3)Hoge Raad-advocaat toegevoegd.',
'Drie leden,165/166volledig gelezen: wanprestatie jegens vorderende schuldeiser, schuldenaarbewijslast, maximaal maand uitstel, procesroute, verplicht faillissement en DNB-waarborg.',
'Beide leden: uitsluitend faillissement krachtens272/277/280 sluit nieuw akkoord uit; internationale47(1)/5(3)verwijzing functioneel afgebakend, geen algehele buitenlandse gelijkstelling. Checklist gecontroleerd.',
'Beide leden: >10000rechtstreeks, >5000tot en met10000toestemming, per aard groepen/globale aantallen en bedragen; beide grensgevallen/214vergeleken.',
'Twee leden: aangetoond >5000, verzoek bewindvoerders/facultatieve rechtbank,281c–f en verplichte koppeling d/e. Geen automatische toepassing vanuit281a.',
'Limitatieve215(2)/256(2)/264(2)oproepingen, Staatscourant of aangewezen nieuwsbladen, verplichte uiterste datum/inhoud. Geen eigen website als vervanging afgeleid.',
'Soort en bedrag als onderscheiden routes, plafond450en beneden-grens strikt, lijst259geen kwijtschelding, verplichte koppeling281egelezen.',
'Alle vijf leden: >=9en belangrijkste groepen, exclusief218/268stemrecht, >kwart blokkade/3kwart instemming,2derde eerste quorum en tweede zonder quorum.269(1)eerste zin beperking expliciet gemaakt;154beroepskring onderscheiden van271ruimer spreekrecht.',
'Voorzienbaar meerdere uitkeringen, rechter bij homologatie, eerste uitgifte toonderpapier en uitsluitend aanbieding later;281bvoorvoorwaarden, geen zelfstandige nieuwe uitkeringshoogte/vervaldag of verliesherstel bedacht.',
'Afdeling11Aen212a(a)/212bgelezen. Alle vijf vervangingen exact217/228(2)/234(1)/235(2)/241a. Geen blanketvrijstelling financiële betalingen; systeemvoorwaarden/tijd/onbekendheid behouden.',
'Exacte twee categorieën1:1Wft/verklaring3:110en overeenkomstige3.5.6. Titel afdeling toegevoegd na verse officiële Wft-check. Geen volledige Wftanalyse of dekking voor elke financiële onderneming afgeleid.'
]
rows=[]
for i,n in zip(ids,notes):
 after=hashlib.sha256(cs[i].encode()).hexdigest();rows.append({'id':i,'official_path':by[i]['official_path'],'finding':n,'result':'corrected' if before[i]!=after else 'accepted_without_change','before_sha256':before[i],'after_sha256':after,'statutory_sha256':hashlib.sha256(by[i]['text'].encode()).hexdigest()})
assert len(rows)==len(notes)==20
paras=[p for i in ids for p in cs[i].split('\n\n') if len(p)>200];assert len(paras)==len(set(paras));assert all(len(cs[i])>=700 or i=='art-270' for i in ids)
limitations=['Only these twenty units substantively reviewed; whole book remains incomplete.','Selective verification of two existing judicial authorities, no exhaustive subsequent-treatment research.','External transitional statutes in editorial source notes not independently analysed for historical proceedings.','Article281h does not analyse every imported Wft provision. No external professional approval.']
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[x['id'] for x in rows if x['result']=='corrected'],'checked_at_utc':now,'whole_book_complete':False,'limitations':limitations}
for dest in [W/'review-result.json',S/(P+'-result.json')]:save(dest,result)
checks={'ok':True,'reviewed_ids':ids,'unassigned_commentaries_unchanged':True,'duplicate_long_paragraphs':0,'commentary_chars':{i:len(cs[i]) for i in ids},'source_agreement':1.0,'whole_book_complete':False}
for dest in [W/'review-checks.json',S/(P+'-checks.json')]:save(dest,checks)
log={'checked_at_utc':now,'scope':'Verification of authorities already cited in assigned articles; two complete judgments read, fresh full XML preserved, HR compared paragraph-wise with national corpus.','queries':['Existing citations in commentary/part-29.md: ECLI:NL:HR:2003:AI0369 and ECLI:NL:RBDHA:2024:18898','Local national corpus exact ECLI lookup hr/ecli-nl-hr-2003-ai0369.md','Official data.rechtspraak.nl full-content endpoints for both ECLIs'],'not_used':'Earlier author RBAMS2021:3197 fetch was an HTML shell and is not cited or treated as verified law.','current_law_comparison':'HR2003 homologation principles272(2)(3)compared with current272. Earlier270references not used as current law. RBDHA2024 substantive272grounds checked. No party allegations in section2 treated as holdings.','no_additional_case_claim':'No separate sufficiently relevant verified case added to technical/repealed units. Not an exhaustive negative search.','limitations':limitations}
save(S/(P+'-search-log.json'),log)
j=json.loads((S/'verification.json').read_text());j['bounded_review_art_270_281h']={'records':records+cases+external,'preflight':'sources/'+P+'-preflight-result.json'};save(S/'verification.json',j)
j=json.loads((W/'status.json').read_text());j['bounded_review_art_270_281h']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/'+P+'-result.json'};j['stage']='authoring_incomplete';save(W/'status.json',j)
print(json.dumps({'reviewed':20,'changed':result['changed_units'],'all_639_texts_exact':True}))
