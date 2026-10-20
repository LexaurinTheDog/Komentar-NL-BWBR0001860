from pathlib import Path
import json,re,hashlib,datetime,xml.etree.ElementTree as E,sys,html
W=Path(__file__).resolve().parent
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ids=['art-'+n for n in ['60a','60b','61','62','63','63a','63b','63c','63d','63e','64','65','66','67','68','68a','69','70','71','72']]
records=[]
for n in ['fetch','cases-fetch']:records+=json.loads((W/f'sources/review-art-60a-72-{n}.json').read_text())
for r in records:assert r['accepted'] and r['http_status']==200 and sha(W/r['raw_path'])==r['sha256']
raw=W/'sources/review-art-60a-72-selected.xml';root=E.parse(raw).getroot()
assert root.get('inwerkingtreding')=='2026-09-01' and sha(raw)==sha(W/'sources/official-2026-09-01.xml')
h=(W/'sources/review-art-60a-72-current.html').read_text()
assert 'Geraadpleegd op 20-10-2026.' in h and 'Geldend van 01-09-2026 t/m heden.' in h
wt=E.parse(W/'sources/review-art-60a-72-wti.xml').getroot()
dates=sorted({x.get('waarde') for x in wt.findall('./wijzigingen/regeling/datum') if x.get('waarde')})
assert max(d for d in dates if d<='2026-10-19')=='2026-09-01'
assert min(d for d in dates if d>'2026-10-20')=='2027-11-15'
assert not [d for d in dates if '2026-10-01'<d<='2026-10-20']
assert E.parse(W/'sources/version-register.xml').getroot().get('inwerkingtreding')=='2002-01-01'
expected=['art-'+a.get('label').removeprefix('Artikel ') for a in root.findall('.//artikel')]
htmlids=['art-'+html.unescape(re.sub('<[^>]+>','',t)).strip().removeprefix('Artikel ') for t in re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>(Artikel [^<]+)</a>',h)]
u=[json.loads(l) for l in (W/'units.jsonl').read_text().splitlines()];by={x['id']:x for x in u}
assert expected==htmlids==[x['id'] for x in u] and len(expected)==len(set(expected))==639
norm=lambda s:re.sub(r'\s+','',s)
def text(e):
 if e.tag in {'kop','meta-data'}:return ''
 return (e.text or '')+''.join(' '+text(c)+' '+(c.tail or '') for c in e)
for a in root.findall('.//artikel'):assert norm(text(a))==norm(by['art-'+a.get('label').removeprefix('Artikel ')]['text'])
assert not [e for e in root.iter() if 'bijlage' in e.tag.lower() or 'annex' in e.tag.lower()]
assert not re.findall(r'<a\b[^>]*\bid="TOC_[^"]+"[^>]*>[^<]*(?:Bijlage|Annex)',h)
comp=json.loads((W/'completeness-report.json').read_text());assert comp['ok'] and not comp['unaccounted_legal_text_nodes']
comparisons=[]
for k in ['2016-2997','2018-1799']:
 p=W/f'sources/review-art-60a-72-hr-{k}.xml';lp=W/f'sources/review-art-60a-72-hr-{k}-local.md'
 body=''.join(E.parse(p).getroot().find('{*}uitspraak').itertext());local=lp.read_text().split('## Uitspraak\n',1)[1]
 assert norm(body).endswith(norm(local)),k
 comparisons.append({'ecli':'ECLI:NL:HR:'+k.replace('-',':'),'official_raw_path':str(p.relative_to(W)),'official_sha256':sha(p),'local_snapshot_path':str(lp.relative_to(W)),'local_sha256':sha(lp),'normalized_corpus_body_is_official_suffix':True})
save(W/'sources/review-art-60a-72-case-comparison.json',comparisons)
notes={
'art-60a':('1–4','Machtiging 68 lid 3, aanmelding versus geverifieerde uitdeling, beide restantbestemmingen en doorlopende rekeningplicht verduidelijkt.',['art-20','art-68'],[]),
'art-60b':('1–2','Aanvaard: uitsluitend onbelast verhaalsgerechtigde die niet kan opkomen, opgehouden betaling, opdracht rechtbank en overeenkomstige toepassing. Geen automatische vermenging vermogens.',['art-60a'],[]),
'art-61':('ongesplitst','Aanvaard: eigendom en uitsluiting gemeenschap beide vereist; voorbeeld met bewezen privé-erfenis, samenhang 22 en 63. Bronnotitie overgangsrecht behouden zonder oud bewijsrecht te importeren.',['art-21','art-22','art-63'],[]),
'art-62':('vervallen slot','Aanvaard: expliciet vervallen; geen huidige bevoegdheid uit oude nummering afgeleid.',['art-61','art-63'],[]),
'art-63':('1–2','Aanvaard: gemeenschap, privéverhaal en artikel 21 afzonderlijk; wettig verbindende handelingen ongeacht partner, geen persoonlijk faillissement andere partner verondersteld.',['art-21'],[]),
'art-63a':('1–4','Schriftelijke afkondiging, verschillende initiatiefnemers, verhaal versus opeising, beide voorwaardensoorten en exacte richting termijnschorsing toegevoegd; twee plus twee maanden en geen automatisch gebruiksrecht behouden.',['art-58','art-63b','art-63c','art-63d'],[]),
'art-63b':('1–2','Aanvaard: mededeling, ontvangst en storting volledige bedrag onderscheiden; geen vrij besteedbare ontvangst of opheffing alle inningsgrenzen aangenomen. Externe verwijzing als verwijzing behouden.',['art-63a'],[]),
'art-63c':('1–2','Aanvaard: uitwinningsverbod met rechterlijke uitzondering tegenover niet-tegenwerpelijkheid later bodembeslag; eigenaar/pandhouder, voorafgaand exploot, plaats en eigendom expliciet.',['art-63a'],[]),
'art-63d':('ongesplitst','Aanvaard: alleen kwalificerend verpande goederen uitgezonderd; bank als wederpartij alleen onvoldoende. Geen nieuw pandrecht of volledige transactiegeldigheid afgeleid.',['art-63a','art-63e'],[]),
'art-63e':('1–2','Beperkte uitschakeling terugwerking versus uitgebreidere niet-tegenwerpelijkheid onderscheiden, volledige geïmporteerde artikelen en beide kenniscomponenten toegevoegd. Dag, tijdstip en bewijs wederpartij correct.',['art-14','art-23','art-24','art-35','art-53','art-54'],[]),
'art-64':('ongesplitst','Aanvaard: toezicht versus eigen curatortaak en afzonderlijke 69-/67-routes. Geen algemene rechterlijke overname beheer geponeerd.',['art-67','art-68','art-69'],[]),
'art-65':('ongesplitst','Aanvaard: verplichte raadpleging niet bindende toestemming; voorbeeld vervanging curator sluit aan bij 73. Geen automatische instemmingsplicht toegevoegd.',['art-73'],[]),
'art-66':('1–4','Doelmisbruik en bijzondere motiveringsplicht uit volledig HR-arrest toegevoegd. Partijstelling, lagere overweging en eigen HR-oordeel onderscheiden; terugwijzing geen definitieve vaststelling misbruik. Deskundige-uitbreiding en familieverschoning apart behouden.',['art-105','art-106'],['ECLI:NL:HR:2016:2997']),
'art-67':('1–3 inclusief uitzonderingslijst','Verkooptoestemming versus beschikking op 69-verzoek uit HR toegelicht; huidige verwijzing naar 68 lid 2 niet stilzwijgend naar lid 3 veranderd. Werknemersberoep en vernietigingsverklaring onderscheiden.',['art-19','art-68','art-69','art-72','art-176'],['ECLI:NL:HR:2018:1799']),
'art-68':('1; 2 a–c; 3; 4','Meldingsnoodzaak volgens curator OF rechter-commissaris, volledige machtigingslijst en vijfwerkdagenregel uitsluitend voor benoeming uitgewerkt. Geen automatische aangifte ieder gebrek.',['art-2','art-37','art-39','art-40','art-58','art-60','art-60a','art-73a','art-78'],[]),
'art-68a':('1; 2 a–o; 3 a–c','Actuele nieuwe tekst volledig gecontroleerd; verkoopinzage en afwikkeling, publicatie lijsten en beperkte overdracht gegevens onder f uitgewerkt. Geen algemene publieke of onbegrensde bewaarbevoegdheid.',['art-14','art-40','art-68','art-73a','art-76','art-77','art-92','art-94','art-96','art-97','art-98','art-99','art-101','art-106a','art-110','art-111','art-112','art-114','art-137','art-137c','art-137d','art-140','art-173a','art-180','art-183'],[]),
'art-69':('1–2','Concrete koper en transactie als toegestaan onderwerp met belangenafweging toegevoegd; bestaande toestemming ontneemt 69-route niet. Uitzondering melding/aangifte, drie dagen en eigen-claimgrens behouden.',['art-67','art-68','art-176'],['ECLI:NL:HR:2018:1799']),
'art-70':('1–2','Aanvaard: meerderheid of staking, zelfstandige werkkring alleen bij vonnis en binnen grenzen; informele afspraken niet gelijkgesteld.',['art-14b'],[]),
'art-71':('1–4','Aanvaard: rechtbank/homologatie, 15 lid 3, efficiënte behandeling, beide zienswijzetriggers en financieringsdelegatie afzonderlijk; geen vergoedingstarief verzonnen.',['art-15','art-68'],[]),
'art-72':('1–2','Geen algemene genezing andere bevoegdheidsgebreken en geen automatisch schadebedrag toegelicht. Machtiging ontbreekt versus informatie ontbreekt en beroep zelf duidelijk gescheiden.',['art-67','art-68','art-70','art-78','art-79'],[])
}
assert list(notes)==ids
c=load_commentary(str(W));before=json.loads((W/'sources/review-art-60a-72-before-hashes.json').read_text())
assert len(c)==len(before)==297
assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
rows=[]
for k in ids:
 for ref in notes[k][2]:assert ref in by
 rows.append({'id':k,'official_path':by[k]['official_path'],'source_paragraphs_reviewed':notes[k][0],'source_notes_reviewed':by[k]['notes'],'statutory_text_sha256':hashlib.sha256(by[k]['text'].encode()).hexdigest(),'commentary_before_sha256':before[k],'commentary_after_sha256':hashlib.sha256(c[k].encode()).hexdigest(),'result':'corrected_or_extended' if hashlib.sha256(c[k].encode()).hexdigest()!=before[k] else 'accepted_without_change','assessment':notes[k][1],'internal_cross_references_checked':notes[k][2],'case_authorities_checked':notes[k][3]})
pre={'complete':True,'decisive_date':'2026-10-19','official_url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01','verified_at':now,'version_evidence':{'fresh_records':'sources/review-art-60a-72-fetch.json','selected_toestand':'2026-09-01_0','current_validity':'Geldend van 01-09-2026 t/m heden; geraadpleegd op 20-10-2026','latest_effective_change':'2026-09-01','changes_since_intake':[],'next_dated_change_excluded':'2027-11-15'},'historical_versions_checked':[{'path':'sources/version-register.xml','sha256':sha(W/'sources/version-register.xml'),'effective_from':'2002-01-01','disposition':'Historical version excluded, no historical concatenation.'},{'path':str(raw.relative_to(W)),'sha256':sha(raw),'effective_from':'2026-09-01','disposition':'639 unique simultaneous current slots; 212hgd* and 212hgd distinct.'}],'annexes_checked':comp['annexes'],'opening_and_closing_text_checked':comp['non_article_text'],'coverage_complete':True,'unresolved_blockers':[]}
save(W/'sources/review-art-60a-72-preflight-result.json',pre)
p=W/'preflight-result.json';v=json.loads(p.read_text());v['bounded_review_art_60a_72_recheck']=pre;save(p,v)
checks={'ok':True,'reviewed_ids':ids,'reviewed_count':20,'unassigned_commentaries_unchanged':True,'expected_official_count':639,'parsed_count':639,'independent_html_toc_count':639,'statutory_verbatim_ratio':1.0,'source_records':'sources/review-art-60a-72-fetch.json','case_comparison':'sources/review-art-60a-72-case-comparison.json','commentaries_changed':sum(r['result']=='corrected_or_extended' for r in rows)}
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'limitations':['Exactly these 20 places substantively reviewed; earlier review evidence preserved, not claimed as work of this process.','342 missing commentaries elsewhere remain; whole-book completion and successful full build are not claimed.','Two selected full HR decisions independently fetched and compared with national corpus; no exhaustive case-law search or separate case for every technical article.','External Rv, BW, Invorderingswet, EU and transitional instruments are not separately certified in full; statutory references retained and explanations limited to verified Fw or actual HR holdings.','Fresh second reading inside project; no external professional approval.'],'checked_at_utc':now,'whole_book_complete':False,'technical_evidence':'review-checks.json','changed_units':[r['id'] for r in rows if r['result']=='corrected_or_extended']}
for n,v in [('review-result.json',result),('review-checks.json',checks),('sources/review-art-60a-72-result.json',result),('sources/review-art-60a-72-checks.json',checks)]:save(W/n,v)
print(json.dumps(checks))
