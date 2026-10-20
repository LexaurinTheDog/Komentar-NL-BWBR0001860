from pathlib import Path
import json,hashlib,sys,re,datetime,subprocess,xml.etree.ElementTree as E,html,shutil,urllib.request
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-213aq-213md'
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary,quote
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);us=load_units(str(W));by={u['id']:u for u in us};cs=load_commentary(str(W));ids=['art-'+i for i in '213aq 213ar 213b 213c 213d 213e 213f 213g 213h 213i 213j 213k 213ka 213kaa 213l 213m 213ma 213mb 213mc 213md'.split()];now=datetime.datetime.now(datetime.timezone.utc).isoformat();before=json.loads((S/(P+'-before-hashes.json')).read_text())
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
pre=json.loads((S/'author-art-213aq-213md-preflight-result.json').read_text())
pre.update(verified_at=now,review_date_local='2026-10-21',parser_evidence='sources/'+P+'-parser-check.json')
pre['version_evidence'].update(records='sources/'+P+'-fetch.json',future_dates_excluded=[d for d in dates if d>'2026-10-21'],fresh_wti_matches_previous=sha(S/(P+'-wti.xml'))==sha(S/'author-art-213aq-213md-wti.xml'))
assert pre['version_evidence']['fresh_wti_matches_previous']
for h in pre['historical_versions_checked']:assert sha(W/h['path'])==h['sha256']
for k in ['transition_evidence','amendment_evidence']:assert sha(W/pre[k]['path'])==pre[k]['sha256']
save(S/(P+'-preflight-result.json'),pre)
p=W/'preflight-result.json';j=json.loads(p.read_text());j['bounded_review_art_213aq_213md']=pre;save(p,j)
save(S/(P+'-search-log.json'),{'searched_at':now,'web_queries':['site:uitspraken.rechtspraak.nl "213ma" "213mc"','site:uitspraken.rechtspraak.nl "213ka" verzekeraar'],'web_result':'No results returned.','local_search':'rg -l 213ma|213mc|213ka /Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr --glob *.md','local_result':'No matches; exit 1.','verified_full_text':[],'limits':'Selective search repeated during review; no sufficiently relevant verified judgment located. No case citations or holdings added.'})
findings=[
'Vervallen slot, bronnoot en overgangsrecht XIV(4) gelezen; geen actuele bevoegdheid of gereconstrueerde vroegere inhoud.',
'Alle vijf leden gelezen; cumulatieve financiële en afwikkelingsvoorwaarden, DNB-exclusiviteit, Amsterdam en hoorplicht onderscheiden. Rechtsmiddelen vervangen door bekendmaking bij verwijzing naar213ag; Wft3a:77 groepsdefinitie gecontroleerd.',
'Procesvrijstelling alleen DNB voor verzekeraar; moedermaatschappij en ontbrekende verwijzing in213ar(5) correct begrensd.',
'Afschrift voor verzekeraar onderscheiden van kennisgeving autoriteiten; onderdelen a/b, grensoverschrijdende diensten en solvabiliteitstoezichthouder gecontroleerd.',
'Intrekkingsplicht bij nog bestaande vergunning; geen verval van rechtswege of automatisch polis-einde. Gewijzigde2024-tekst gecontroleerd.',
'Vervallen per2024; geen actuele informatieplicht uit historisch draaiboek afgeleid. Wijzigingswet gelezen.',
'Vervallen2019 met expliciete overgangsnoot; historische beoordeling gescheiden van huidig slot.',
'Beide leden: griffier/DNB-keten, onverwijld, alle andere lidstaten en mogelijke gevolgen. Machtiging versus uitgevoerde overgang juist onderscheiden.',
'Vervallen2024 en wijzigingswet gecontroleerd; geen oude bekendmakingsplicht als actueel recht.',
'Beide leden: onmiddellijk schriftelijk, overgang versus machtiging; artikel109/127, indiening zekerheidscrediteuren en verzekeringseffecten besproken.',
'Alle drie leden: verzekering/andere vorderingen, woonplaats en indieningstaal onderscheiden. Verplicht Nederlands bericht en meertalig formulier verduidelijkt; geen facultatieve taalkeuze van curator.',
'Beide leden: regelmatige passende curatorinformatie en verzoekafhankelijke DNB-informatie onderscheiden van213g.',
'Alle vier leden: cumulatieve termijnpremie/risicovoorwaarden, RC-toestemming, uitsluiting37, spaarelement en beperkte boedelschulden per premiecomponent gecontroleerd.',
'Beide leden en drie cumulatieve voorwaarden: volledige premie, tijdelijke risicodekking, nog mogelijk voorval, drie maanden en groepstoestemming.',
'Alle vier leden: bereik lid1 aangescherpt tot na aanvang vervallende vorderingen; verificatiedatum lid2 en risicodatum lid3 onderscheiden. Geen ongelezen discontovoet verzonnen.',
'Alle vijf leden en onderdelen2a-h/3a-f: boedelkosten, zekerheden, persoonsuitkeringen, pensioen/loonperioden, onverschuldigde premie en aanvullende schade onderscheiden; restgroep en gelijke Europese voorrang gecontroleerd.',
'Alle zes leden: opeisbaarheid, categorieën a-d, strikte12500-grens, risicodatum, afkoop voor/na opening, verzoektermijn, indiening en hoogte/frequentie gecontroleerd.',
'Alle zes onderdelen: Zorginstituut/Waarborgfonds, aanvraaggebonden ontstaan en vereiste na-opening wilsuiting onderscheiden; geen ongefundeerde ruimere externe garantieregels.',
'Beide leden: prudente tegenfeitelijke raming, wijziging en toestemming-tenzij getoetst; grammatica gecorrigeerd zonder inhoudelijke wijziging.',
'Beide leden: uitvoering toestemming en continuering bestaande periodieke uitkeringen, zelfde bedrag en tijdig verzoek; geen automatische stop dag90. Checklist als thematische hulp, geen werkelijk afdelingsslot geclaimd.'
]
rows=[]
for i,note in zip(ids,findings):
 after=hashlib.sha256(cs[i].encode()).hexdigest();rows.append({'id':i,'official_path':by[i]['official_path'],'effective_from':by[i]['effective_from'],'source_notes_checked':by[i]['notes'],'finding':note,'result':'corrected' if before[i]!=after else 'accepted_without_change','before_sha256':before[i],'after_sha256':after,'statutory_sha256':hashlib.sha256(by[i]['text'].encode()).hexdigest()})
assert len(rows)==20
paras=[p for i in ids for p in cs[i].split('\n\n') if len(p)>200];assert len(paras)==len(set(paras))
assert all(len(cs[i])>=(120 if by[i]['text']=='Vervallen' else 700) and not re.search('TODO|FIXME',cs[i]) for i in ids)
for script,suffix in [('build_repo.py','build.txt'),('validate.py','validation.txt')]:
 q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/'+script,str(W)],capture_output=True,text=True);(S/(P+'-'+suffix)).write_text(q.stdout+q.stderr)
 if script=='validate.py':validation=json.loads(q.stdout)
assert validation['verbatim_ratio']==1.0
save(S/(P+'-validation.json'),validation)
missing=sum(not cs.get(u['id']) for u in us)
result={'kind':'bounded_independent_second_pass','complete':True,'units_reviewed':20,'reviewed_ids':ids,'unresolved_blockers':[],'findings':rows,'changed_units':[r['id'] for r in rows if r['result']=='corrected'],'checked_at_utc':now,'whole_book_complete':False,'validation_result':validation,'limitations':['Only the assigned twenty units reviewed; project-internal review, no external professional approval.','Selective unsuccessful judicial searches; no new verified judgment or claim of exhaustive case-law coverage.','Former repealed text not reconstructed; transitional applicability separately acknowledged.','External guarantee regimes not independently expounded; no unverified implementing valuation rule asserted.',f'{missing} unassigned commentaries absent; whole-book build and strict validation remain unsuccessful.']}
for p in [W/'review-result.json',S/(P+'-result.json')]:save(p,result)
checks={'ok':True,'reviewed_ids':ids,'unassigned_commentaries_unchanged':True,'duplicate_long_paragraphs':0,'commentary_chars':{i:len(cs[i]) for i in ids},'source_agreement':1.0,'whole_book_complete':False}
for p in [W/'review-checks.json',S/(P+'-checks.json')]:save(p,checks)
p=S/'verification.json';j=json.loads(p.read_text());j['bounded_review_art_213aq_213md']={'records':records,'preflight':'sources/'+P+'-preflight-result.json'};save(p,j)
p=W/'status.json';j=json.loads(p.read_text());j['bounded_review_art_213aq_213md']={'complete':True,'units_reviewed':20,'reviewed_ids':ids,'corrected':len(result['changed_units']),'whole_book_complete':False,'evidence':'sources/'+P+'-result.json'};save(p,j)
print(json.dumps({'reviewed':20,'changed':result['changed_units'],'missing_elsewhere':missing,'verbatim_ratio':1.0}))
