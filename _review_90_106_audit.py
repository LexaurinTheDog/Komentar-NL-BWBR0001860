from pathlib import Path
import json,re,hashlib,datetime,xml.etree.ElementTree as E,sys,html
W=Path(__file__).resolve().parent
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_commentary
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ids=['art-90', 'art-91', 'art-92', 'art-93', 'art-93a', 'art-94', 'art-95', 'art-96', 'art-97', 'art-98', 'art-99', 'art-100', 'art-101', 'art-102', 'art-103', 'art-104', 'art-105', 'art-105a', 'art-105b', 'art-106']
records=[]
for n in ['fetch','cases-fetch']:records+=json.loads((W/f'sources/review-art-90-106-{n}.json').read_text())
for r in records:assert r['accepted'] and r['http_status']==200 and sha(W/r['raw_path'])==r['sha256']
raw=W/'sources/review-art-90-106-selected.xml';root=E.parse(raw).getroot()
assert root.get('inwerkingtreding')=='2026-09-01' and sha(raw)==sha(W/'sources/official-2026-09-01.xml')
h=(W/'sources/review-art-90-106-current.html').read_text()
assert 'Geraadpleegd op 20-10-2026.' in h and 'Geldend van 01-09-2026 t/m heden.' in h
wt=E.parse(W/'sources/review-art-90-106-wti.xml').getroot()
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
for k in ['2026-400', '2014-161']:
 p=W/f'sources/review-art-90-106-hr-{k}.xml';lp=W/f'sources/review-art-90-106-hr-{k}-local.md'
 body=''.join(E.parse(p).getroot().find('{*}uitspraak').itertext());local=lp.read_text().split('## Uitspraak\n',1)[1]
 assert norm(body).endswith(norm(local)),k
 comparisons.append({'ecli':'ECLI:NL:HR:'+k.replace('-',':'),'official_raw_path':str(p.relative_to(W)),'official_sha256':sha(p),'local_snapshot_path':str(lp.relative_to(W)),'local_sha256':sha(lp),'normalized_corpus_body_is_official_suffix':True})
save(W/'sources/review-art-90-106-case-comparison.json',comparisons)
notes={'art-90': ('1–2', 'Overbrenging op last RC en uitvoering OM onderscheiden van ontslag bewaring.', ['art-87', 'art-88'], []), 'art-91': ('ongesplitst', 'Toestemming RC voor verlaten woonplaats; niet alleen landsgrens of curatorinstemming.', ['art-106'], []), 'art-92': ('ongesplitst', 'Onmiddellijk veiligstellen, ontvangbewijs en facultatieve consignatie; digitale bewaring onderscheiden van publicatie.', ['art-94', 'art-105a', 'art-105b', 'art-68a'], []), 'art-93': ('1–2', 'Noodzaak bij curator of RC, notaris en proces-verbaal; uitzonderingen precies afgebakend.', ['art-7', 'art-21', 'art-92'], []), 'art-93a': ('ongesplitst', 'Redelijke taaknoodzaak en machtigingsbevoegdheid onderscheiden; toegang beslist niet over eigendom. Externe Awbi-procedure niet volledig uiteengezet.', [], []), 'art-94': ('1–3', 'Spoed, onderhandse beschrijving en curatorwaardering onder RC-goedkeuring; aanwezigheid voorlopige commissie.', ['art-96'], []), 'art-95': ('ongesplitst', 'Aangehechte staat beschermde goederen tegenover opname artikel 92; geen eigendomsbeslissing.', ['art-21', 'art-92', 'art-94', 'art-96'], []), 'art-96': ('ongesplitst', 'Direct na inventaris, aard en bedragen baten/schulden en crediteuren; geen definitieve verificatie.', ['art-97', 'art-68a'], []), 'art-97': ('1–2', 'Bevoegde griffie, gewaarmerkte kopieën, kosteloze inzage voor iedereen en neerlegging; afschriftkosten apart.', ['art-107'], []), 'art-98': ('ongesplitst', 'Machtiging zonder commissie; met commissie advies en afwijkingsprocedure; latere voortzetting apart.', ['art-39', 'art-40', 'art-78', 'art-79', 'art-173a'], []), 'art-99': ('1–2', 'Postlast en kennisgeving, directe terhandstelling niet-boedelpost, einde beide bevoegdheden; formele verklaringen via curator.', ['art-14', 'art-15', 'art-68a'], []), 'art-100': ('ongesplitst', 'Facultatieve uitkering, omstandigheden, vaststelling RC en verplicht commissieadvies.', ['art-21', 'art-78'], []), 'art-101': ('1–2', 'Openbare/onderhandse verkoop, cumulatieve 2000-eurogrens volgens inventaris en bijzondere baten; commissieadvies.', ['art-78', 'art-176'], []), 'art-102': ('1–2', 'Onmiddellijke bewaring tenzij andere wijze RC; overliquiditeit belegd op boedelnaam met goedkeuring.', ['art-103'], []), 'art-103': ('ongesplitst', 'Derdenbewaring volgens RC en belegde gelden; voor gezien getekende stukken, geen zelfstandig uitdelingsrecht.', ['art-102'], []), 'art-104': ('ongesplitst', 'Advies bestaande commissie en RC-goedkeuring cumulatief; inhoud finale kwijting en verhaalafweging.', ['art-72'], []), 'art-105': ('1, 2a–b, 3', 'Gevraagde en spontane informatie onderscheiden; buitenlands melden en meewerken; partners enkel gemeenschap; beperkte betekenis oudere HR-dwangwaarborg.', ['art-105a'], ['ECLI:NL:HR:2014:161']), 'art-105a': ('1–3', 'Algemene medewerking, onmiddellijke volledige ongeschonden administratie en leesmiddelen; partnerbeperking en grenzen contactdwang.', ['art-105b'], ['ECLI:NL:HR:2026:400']), 'art-105b': ('1–3', 'Beroepsmatige derden op verzoek, leesmiddelen, retentierecht doorbroken en strijdige bedingen nietig; bestaande gegevens versus nieuw werk.', ['art-60'], []), 'art-106': ('1, 2a–b, 3', 'Huidige/voormalige bestuurders en commissarissen, driejaarstermijn, feitelijke beleidsbepalers, indirect bestuur, VOF/CV; geen zelfstandige aansprakelijkheid.', ['art-87', 'art-88', 'art-89', 'art-90', 'art-91', 'art-92', 'art-105', 'art-105a'], [])}
assert list(notes)==ids
c=load_commentary(str(W));before=json.loads((W/'sources/review-art-90-106-before-hashes.json').read_text())
assert len(c)==len(before)==297
assert all(hashlib.sha256(v.encode()).hexdigest()==before[k] for k,v in c.items() if k not in ids)
rows=[]
for k in ids:
 for ref in notes[k][2]:assert ref in by
 rows.append({'id':k,'official_path':by[k]['official_path'],'source_paragraphs_reviewed':notes[k][0],'source_notes_reviewed':by[k]['notes'],'statutory_text_sha256':hashlib.sha256(by[k]['text'].encode()).hexdigest(),'commentary_before_sha256':before[k],'commentary_after_sha256':hashlib.sha256(c[k].encode()).hexdigest(),'result':'corrected_or_extended' if hashlib.sha256(c[k].encode()).hexdigest()!=before[k] else 'accepted_without_change','assessment':notes[k][1],'internal_cross_references_checked':notes[k][2],'case_authorities_checked':notes[k][3]})
pre={'complete':True,'decisive_date':'2026-10-19','official_url':'https://wetten.overheid.nl/BWBR0001860/2026-09-01','verified_at':now,'version_evidence':{'fresh_records':'sources/review-art-90-106-fetch.json','selected_toestand':'2026-09-01_0','current_validity':'Geldend van 01-09-2026 t/m heden; geraadpleegd op 20-10-2026','latest_effective_change':'2026-09-01','changes_since_intake':[],'next_dated_change_excluded':'2027-11-15'},'historical_versions_checked':[{'path':'sources/version-register.xml','sha256':sha(W/'sources/version-register.xml'),'effective_from':'2002-01-01','disposition':'Historical version excluded, no historical concatenation.'},{'path':str(raw.relative_to(W)),'sha256':sha(raw),'effective_from':'2026-09-01','disposition':'639 unique simultaneous current slots; 212hgd* and 212hgd distinct.'}],'annexes_checked':comp['annexes'],'opening_and_closing_text_checked':comp['non_article_text'],'coverage_complete':True,'unresolved_blockers':[]}
save(W/'sources/review-art-90-106-preflight-result.json',pre)
p=W/'preflight-result.json';v=json.loads(p.read_text());v['bounded_review_art_90_106_recheck']=pre;save(p,v)
checks={'ok':True,'reviewed_ids':ids,'reviewed_count':20,'unassigned_commentaries_unchanged':True,'expected_official_count':639,'parsed_count':639,'independent_html_toc_count':639,'statutory_verbatim_ratio':1.0,'source_records':'sources/review-art-90-106-fetch.json','case_comparison':'sources/review-art-90-106-case-comparison.json','commentaries_changed':sum(r['result']=='corrected_or_extended' for r in rows)}
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'limitations':['Exactly these 20 places substantively reviewed; earlier review evidence preserved, not claimed as work of this process.','342 missing commentaries elsewhere remain; whole-book completion and successful full build are not claimed.','Two selected full HR decisions independently fetched and compared with national corpus; no exhaustive case-law search or separate case for every technical article.','External Rv, BW, Invorderingswet, EU and transitional instruments are not separately certified in full; statutory references retained and explanations limited to verified Fw or actual HR holdings.','Fresh second reading inside project; no external professional approval.'],'checked_at_utc':now,'whole_book_complete':False,'technical_evidence':'review-checks.json','changed_units':[r['id'] for r in rows if r['result']=='corrected_or_extended']}
for n,v in [('review-result.json',result),('review-checks.json',checks),('sources/review-art-90-106-result.json',result),('sources/review-art-90-106-checks.json',checks)]:save(W/n,v)
print(json.dumps(checks))
