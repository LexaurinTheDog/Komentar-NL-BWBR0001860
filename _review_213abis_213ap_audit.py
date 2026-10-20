from pathlib import Path
import json,hashlib,sys,re,datetime,subprocess,xml.etree.ElementTree as E,html,shutil,urllib.request
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-213abis-213ap'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W));ids=['art-'+i for i in '213abis 213ab 213ac 213ad 213ad1 213ae 213af 213ag 213aga 213agb 213agc 213ah 213ai 213aj 213ak 213al 213am 213an 213ao 213ap'.split()];now=datetime.datetime.now(datetime.timezone.utc).isoformat();before=json.loads((S/(P+'-before-hashes.json')).read_text())
assert all(before[k]==hashlib.sha256(v.encode()).hexdigest() for k,v in cs.items() if k not in ids)
records=json.loads((S/(P+'-fetch.json')).read_text());assert all(r['accepted'] and sha(W/r['raw_path'])==r['sha256'] for r in records)
r=E.parse(S/(P+'-selected.xml')).getroot();expected=['art-'+a.get('label').removeprefix('Artikel ') for a in r.iter('artikel')]
toc=['art-'+html.unescape(x).removeprefix('Artikel ') for x in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',(S/(P+'-current.html')).read_text())]
assert expected==toc==[u['id'] for u in us] and len(set(expected))==639
assert sha(S/(P+'-selected.xml'))==sha(S/'official-2026-09-01.xml')
def flat(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+flat(c)+' '+(c.tail or '') for c in e)
norm=lambda s:re.sub(r'\s+','',s)
for a in r.iter('artikel'):assert norm(flat(a))==norm(by['art-'+a.get('label').removeprefix('Artikel ')]['text'])
assert not [e for e in r.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
wt=E.parse(S/(P+'-wti.xml')).getroot();dates=sorted({e.get('waarde') for e in wt.findall('./wijzigingen/regeling/datum') if e.get('waarde')});assert max(d for d in dates if d<='2026-10-21')=='2026-09-01'
assert not [d for d in dates if '2026-10-01'<d<='2026-10-21']
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
names=['units.jsonl','meta.json','coverage-evidence.json','completeness-report.json'];hashes={n:sha(W/n) for n in names}
for script in ['_parse.py','_coverage.py']:
 q=subprocess.run([sys.executable,str(W/script)],capture_output=True,text=True);assert q.returncode==0,q.stderr
assert hashes=={n:sha(W/n) for n in names}
save(S/(P+'-parser-check.json'),{'ok':True,'official_source':{'url':records[1]['url'],'local_raw_evidence_path':records[1]['raw_path'],'sha256':records[1]['sha256']},'expected_ids':expected,'parsed_ids':[u['id'] for u in us],'html_toc_ids':toc,'missing':[],'duplicates':[],'annex_disposition':comp['annexes'],'opening_closing':comp['non_article_text'],'reproduced_hashes':hashes})
pre={'complete':True,'decisive_date':m['decisive_date'],'review_date_local':'2026-10-21','official_url':m['source_url'],'verified_at':now,'version_evidence':{'fetch_records':'sources/'+P+'-fetch.json','effective_from':'2026-09-01','current_route':'Geldend van 01-09-2026 t/m heden; displayed consultation date 20-10-2026 distinct from UTC capture','changes_since_intake':[],'future_dates_excluded':[d for d in dates if d>'2026-10-21']},'historical_versions_checked':[{'path':'sources/version-register.xml','sha256':sha(S/'version-register.xml'),'disposition':'Historical 2002 state excluded; no concatenated historical articles.'},{'path':'sources/review-art-212z-213a-historical-2025.xml','sha256':sha(S/'review-art-212z-213a-historical-2025.xml'),'disposition':'Separately preserved earlier toestand; no historical units substituted for selected current slots.'},{'path':'sources/author-art-213abis-213ap-stb-2023-306.xml','sha256':sha(S/'author-art-213abis-213ap-stb-2023-306.xml'),'disposition':'Article III C-E read: 213ad repealed, 213aga 3-5 added, 213agb 6 repealed.'},{'path':'sources/review-art-207-212hf-stb-2018-489.xml','sha256':sha(S/'review-art-207-212hf-stb-2018-489.xml'),'disposition':'Article XIV(4) read: previous Act remains applicable to pre-commencement insurance bankruptcies.'},{'path':'sources/review-art-207-212hf-stb-2016-290.xml','sha256':sha(S/'review-art-207-212hf-stb-2016-290.xml'),'disposition':'CIX transitional note at 213ae checked; no universal historical procedural rule inferred.'}],'annexes_checked':comp['annexes'],'opening_and_closing_checked':comp['non_article_text'],'parser_evidence':'sources/'+P+'-parser-check.json','unresolved_blockers':[]}
save(S/(P+'-preflight-result.json'),pre)
p=W/'preflight-result.json';j=json.loads(p.read_text());j['bounded_review_art_213abis_213ap']=pre;save(p,j)
# Re-capture the full court text, never treat an application shell as a judgment.
url='https://data.rechtspraak.nl/uitspraken/content?id=ECLI:NL:RBAMS:2022:7475';req=urllib.request.Request(url,headers={'User-Agent':'OpenCommentary-review/1.0'});at=datetime.datetime.now(datetime.timezone.utc).isoformat()
with urllib.request.urlopen(req,timeout=30) as response:
 b=response.read();status=response.status;headers=str(response.headers)
p=S/(P+'-rbams-2022-7475.xml');p.write_bytes(b);p.with_suffix('.xml.headers').write_text('HTTP '+str(status)+'\n'+headers);court=E.fromstring(b);judgment=court.find('{*}uitspraak');assert status==200 and judgment is not None
text=''.join(judgment.itertext());assert len(text)>10000 and '85%' in text
(S/(P+'-rbams-2022-7475.txt')).write_text(text)
save(S/(P+'-case-check.json'),{'url':url,'access_timestamp_utc':at,'http_status':status,'sha256':sha(p),'path':str(p.relative_to(W)),'full_judgment_chars':len(text),'reviewed_parts':'Full judgment 1.1–6.2 read; holdings 5.2–5.6 distinguished from DNB 3.1 and RC 4.1; no reliance on absent appendix 8 contents.','supported_units':['art-213aga','art-213agb'],'limits':'2022 decision predates 2024 additions to 213aga. Does not decide extension or create an 85% threshold.'})
findings=[
'Alle vier leden: Wft 3A:85(1)a-b tegen vers gevangen Wft gelezen; c geen faillissementsvoorwaarde. Vergunninghistorie, aanvraag door anderen, eigen aangifte en advies onderscheiden.',
'Collectief belang en bijzondere voorziening, ontbreken DNB-vergunning en onverminderd artikel1(1); territoriale grens213a en eerdere vergunning213abis gecontroleerd.',
'Expliciet vervallen sinds2019; bronnoot en XIV(4) controleren toepasselijkheid oud recht, zonder vroegere inhoud te reconstrueren.',
'Expliciet vervallen sinds2024; wijzigingswet III C geverifieerd; 213ad1 blijft afzonderlijke eenheid.',
'Beide leden gelezen: rechter/deskundige, zakelijke gegevens, houder en rechterlijke termijn; geen schuldeisersinzage of automatische sanctie verzonnen.',
'DNB-verzoek en eigen aangifte, spoed, beslotenheid en burgerlijke rechtspleging; publicatie213ag onderscheiden. CIX-bronnoot gecontroleerd.',
'Beide leden: gelegenheid gehoord te worden en beperkte redelijkheidstoets; geen universele toepassing op latere curatorbesluiten.',
'Alle drie leden: summierlijk blijken, benoeming/voordracht en alle publicatiekanalen/gegevens. Onderwerp van beschikking expliciet toegevoegd bij aanvullende publicatiegegevens.',
'Alle vijf leden: twee aanvraagmomenten, toestemming derde, besloten spoedzitting/horen DNB, duur/verlenging en advies176. Case1.1–1.2/4.1 getoetst; temporele grens2024 correct.',
'Alle vijf leden: wijziging bij overgang, uitsluiting schadevergoeding, levensverzekeringgrens, horen DNB en duur. Ook gelijktijdige machtiging expliciet gemaakt. Case5.2–5.6 volledig gecontroleerd; geen85%-drempel.',
'Alle drie leden: publicatie Staatscourant/3 dagbladen, tweede dag, DNB-informatie; fictief kalendervoorbeeld juist.',
'Uitvoerbaar bij voorraad; onderscheid rechtsmiddel, duur, transactievoorwaarden en publicatie juist.',
'Vervallen2019; geen actuele bevoegdheid gereconstrueerd; verwijzing213ah en overgangsrecht juist.',
'Vervallen2019; onderscheiden van parseromissie; oude faillissementsdatum blijft bepalend.',
'Vervallen2019; geen actuele aanvullende overdrachtsvoorwaarde; huidige machtigingen correct genoemd.',
'Vervallen2019; oude polisbrief schept geen actuele aanspraak; overgangsrecht afgebakend.',
'Vervallen2019; geen terugwerkende ongeldigverklaring oude handelingen verondersteld; XIV(4) correct.',
'Vervallen2019; geen actuele publicatievrijstelling; historische toepasselijkheid openlijk apart gehouden.',
'Vervallen2019; expliciet behouden slot; historische uitspraak vereist destijds geldende tekst.',
'Vervallen2019; geen actuele sluitregel. Praktische controle sluit aan bij213aga/b/gc; geen onjuist paragraafeinde geclaimd.'
]
rows=[]
for i,note in zip(ids,findings):
 after=hashlib.sha256(cs[i].encode()).hexdigest();rows.append({'id':i,'official_path':by[i]['official_path'],'effective_from':by[i]['effective_from'],'source_notes_checked':by[i]['notes'],'finding':note,'result':'corrected' if before[i]!=after else 'accepted_without_change','before_sha256':before[i],'after_sha256':after,'statutory_sha256':hashlib.sha256(by[i]['text'].encode()).hexdigest()})
assert len(rows)==20 and len(set(ids))==20
paras=[p for i in ids for p in cs[i].split('\n\n') if len(p)>200];assert len(set(paras))==len(paras)
assert all(len(cs[i])>=(120 if by[i]['text']=='Vervallen' else 700) and not re.search('TODO|FIXME',cs[i]) for i in ids)
for script,suffix in [('build_repo.py','build.txt'),('validate.py','validation.txt')]:
 q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/'+script,str(W)],capture_output=True,text=True);(S/(P+'-'+suffix)).write_text(q.stdout+q.stderr)
 if script=='validate.py':validation=json.loads(q.stdout)
assert validation['verbatim_ratio']==1.0
save(S/(P+'-validation.json'),validation)
missing=sum(not cs.get(u['id']) for u in us)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[r['id'] for r in rows if r['result']=='corrected'],'checked_at_utc':now,'review_date_local':'2026-10-21','whole_book_complete':False,'validation_result':validation,'limitations':['Exact assigned twenty units only; project-internal second reading, no external professional approval.','Selective case-law coverage. Full judgment read; unpublished appendix8 not relied upon. No new exhaustive research claimed.','Repealed slots reviewed as current status and transitional law; former substantive text not reconstructed.',f'{missing} out-of-scope commentaries missing; strict full-book validation remains unsuccessful.']}
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,result)
checks={'ok':True,'reviewed_ids':ids,'unassigned_commentaries_unchanged':True,'duplicate_long_paragraphs':0,'commentary_chars':{i:len(cs[i]) for i in ids},'source_agreement':1.0,'whole_book_complete':False}
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,checks)
p=S/'verification.json';j=json.loads(p.read_text());j['bounded_review_art_213abis_213ap']={'records':records,'preflight':'sources/'+P+'-preflight-result.json','case_verification':'sources/'+P+'-case-check.json'};save(p,j)
p=W/'status.json';j=json.loads(p.read_text());j['bounded_review_art_213abis_213ap']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':2,'whole_book_complete':False,'evidence':'sources/'+P+'-result.json'};save(p,j)
print(json.dumps({'reviewed':20,'changed':result['changed_units'],'missing_elsewhere':missing,'verbatim_ratio':1.0}))
