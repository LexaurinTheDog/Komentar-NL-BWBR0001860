from pathlib import Path
import json,sys,shutil,subprocess,re,hashlib
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-254-269b';sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_units,load_commentary
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);r=json.loads((W/'review-result.json').read_text());ids=r['reviewed_ids'];us=load_units(str(W));cs=load_commentary(str(W));B=W/'batches/art-254-269b';T=O/'batches/art-254-269b'
review='''

## Afgebakende tweede lezing — artikelen 254–269b

Op 21 oktober 2026 lokale tijd zijn exact twintig artikelen tegen de officiële bron beoordeeld: 254–257, 257a, 258–268, 268a, 269, 269a en 269b. [Exacte identifiers en bevinding per artikel](sources/review-art-254-269b-result.json). Vier toelichtingen zijn verbeterd: de hoorplicht in 255 lid 3; toondervorderingen en de onderscheiden voorwaarden voor regres in 260/134/136; verplichte plaatsing zonder bezwaar en de rechterlijke beslisroute bij bezwaar in 265; en het onderscheid tussen de klacht van de verzoeker en het eigen oordeel van de Hoge Raad bij 269. Zestien toelichtingen zijn zonder wijziging aanvaard. Alle niet-toegewezen toelichtingen zijn hashgelijk gebleven.

De [nieuwe bronopnamen](sources/review-art-254-269b-fetch.json) bewaren URL, UTC-ophaaltijd, HTTP200, SHA-256 en formaatcontrole. De [preflight](sources/review-art-254-269b-preflight-result.json) behoudt de oorspronkelijke auteurspeildatum 19 oktober 2026. De actuele officiële route verwijst naar 1 september 2026 en vermeldt gelding tot heden. De lokale reviewdatum, UTC-ophaaltijd en officiële raadpleegdatum zijn afzonderlijk vastgelegd. Het volledige wijzigingsregister bevat geen ingegane wijziging sinds de intake; toekomstige toestanden zijn uitgesloten. De historische bronnen van 2002 en 2025 zijn op unieke artikelplaatsen gecontroleerd en niet in de huidige tekst gemengd.

De [parsercontrole](sources/review-art-254-269b-parser-check.json) vergelijkt 639 officiële XML-labels onafhankelijk met de verse HTML-inhoudsopgave en de JSONL-extractie. Geen ontbrekende of dubbele identifiers, alle wettelijke teksten exact gelijk, geen onverklaarde juridische tekst. De volledige XML en inhoudsopgave bevatten geen operationele bijlagen. Aanhef, slot, structurele bronnotities en vervallen plaatsen zijn behouden; deze twintig artikelen bevatten geen vervallen slot. Parser en afzonderlijke volledigheidscontrole zijn opnieuw uitgevoerd met ongewijzigde producthashes. Technische dekking en minimumlengte bewijzen geen juridische kwaliteit.

De volledige uitspraken ECLI:NL:HR:2017:3110 en ECLI:NL:RBDHA:2024:18898 zijn opnieuw officieel opgehaald en gelezen. [Capturevergelijking en nationale corpusversie](sources/review-art-254-269b-case-comparison.json), [onderzoekslog](sources/review-art-254-269b-search-log.json), [Hoge Raad-kaart](sources/review-art-254-269b-case-2017.md), [rechtbankkaart](sources/review-art-254-269b-case-2024.md). Het arrest van 2017 ondersteunt het rechtsmiddelenverbod voor beslissingen onder 267/268a en de beperkte doorbrekingsgronden. De oude verwijzing naar het inmiddels vervallen artikel 270 wordt niet als huidige rechtsmiddelenroute gebruikt. Rov. 3.6 geeft klachten weer; 3.7 en 3.8 bevatten de eigen toets. Rov. 3.10 beoordeelt de verbeteringsgronden van 269a niet inhoudelijk. De rechtbankbeschikking ondersteunt onder 257 het onderscheid tussen gedekte en concurrente delen; haar waardering en oordeel over begunstiging blijven zaakgebonden. De in onderdeel 2 geciteerde akkoordtekst en het bewindvoerdersverslag zijn geen zelfstandige rechterlijke rechtsregels.

Dit is selectieve controle van bestaande rechtspraakverwerking, geen uitputtend nieuw rechtspraakonderzoek of volledige controle van latere rechtspraak. Externe overgangswetten in bronnotities zijn niet zelfstandig inhoudelijk beoordeeld voor historische procedures. Het afgebakende checkpoint is opnieuw gebouwd en strikt gevalideerd met de ongewijzigde gedeelde scripts. De boekbrede bouw en validatie zijn afzonderlijk vastgelegd; ontbrekende toelichtingen buiten deze batch blijven bestaan. [Validatie](sources/review-art-254-269b-validation.json). Geen voltooid boek en geen externe professionele goedkeuring.
'''
p=W/'REVIEW.md';assert '## Afgebakende tweede lezing — artikelen 254–269b' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing 254–269b: [bevindingen](sources/'+P+'-result.json), [broncontrole](sources/'+P+'-preflight-result.json), [parsercontrole](sources/'+P+'-parser-check.json), [rechtspraakcontrole](sources/'+P+'-search-log.json).\n')
intro='''# Faillissementswet — beoordeeld checkpoint artikelen 254–269b

Dit checkpoint bevat uitsluitend de twintig artikelen 254–269b, inclusief 257a, 268a, 269a en 269b. Wettekst geldend vanaf 1 september 2026, naar de oorspronkelijke auteurspeildatum 19 oktober 2026; tweede lezing en nieuwe officiële broncontrole op 21 oktober 2026 lokale tijd. [Officiële bron](https://wetten.overheid.nl/BWBR0001860/2026-09-01). Vier toelichtingen verbeterd, zestien aanvaard. Het hele boek blijft onvoltooid.

Oorspronkelijk commentaar © 2026 Vojtěch Říha; Apache-2.0. Officiële wettekst en rechterlijke uitspraken zijn afzonderlijk bronmateriaal. Concept, geen externe professionele goedkeuring. Selectieve verwerking van een volledige Hoge Raad-uitspraak en een rechtbankbeschikking; geen uitputtend rechtspraakonderzoek.

[Bevindingen](sources/review-art-254-269b-result.json) · [Broncontrole](sources/review-art-254-269b-preflight-result.json) · [Dekking](sources/review-art-254-269b-parser-check.json) · [Rechtspraakonderzoek](sources/review-art-254-269b-search-log.json) · [Tweede lezing](REVIEW.md).
'''
(B/'README.md').write_text(intro);(B/m['intro_file']).write_text(intro);shutil.copyfile(W/'commentary/part-28.md',B/'commentary/part-28.md')
check=json.loads((S/(P+'-parser-check.json')).read_text());ex=check['expected_ids'];ex=ex[ex.index('art-254'):ex.index('art-269b')+1];assert ex==ids
coverage={'official_source':{'url':'https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0001860/2026-09-01_0/xml/BWBR0001860_2026-09-01_0.xml','local_raw_evidence_path':'sources/'+P+'-selected.xml','sha256':sha(S/(P+'-selected.xml'))},'expected_ids':ex,'parsed_ids':[u['id'] for u in us if u['id'] in ids],'annex_disposition':check['annex_disposition'],'scope':'Independently enumerated official contiguous range 254–269b; full 639-ID inventory in parser-check.json.'};save(B/'coverage-evidence.json',coverage)
bm=json.loads((B/'meta.json').read_text());bm['title']='Faillissementswet — beoordeeld checkpoint artikelen 254–269b';save(B/'meta.json',bm)
for year in ['2017','2024']:
 p=S/('author-art-254-269b-case-'+year+'.md');t=p.read_text().replace('author-art-254-269b','review-art-254-269b');t+='\nTweede lezing op 21 oktober 2026: volledige officiële uitspraak opnieuw opgehaald en gelezen; dictum, eigen overwegingen en weergegeven partijstellingen onderscheiden. Huidige nationale bepalingen vergeleken; beperkingen hierboven blijven gelden.\n';(S/(P+'-case-'+year+'.md')).write_text(t)
q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/build_repo.py',str(W)],capture_output=True,text=True);(S/(P+'-build.txt')).write_text(q.stdout+q.stderr)
q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/build_repo.py',str(B)],capture_output=True,text=True);assert q.returncode==0,q.stderr;(S/(P+'-bounded-build.txt')).write_text(q.stdout+q.stderr)
for c in bm['chapters']:shutil.copyfile(T/f"{c['n']:02d}-{c['slug']}.md",O/f"{c['n']:02d}-art-254-269b-checkpoint-{c['n']}.md")
for root in [O,B,T]:
 (root/'sources').mkdir(exist_ok=True)
 for p in S.glob(P+'-*'):shutil.copyfile(p,root/'sources'/p.name)
 for name in ['SOURCES.md','REVIEW.md']:shutil.copyfile(W/name,root/name)
for name in ['review-result.json','review-checks.json','preflight-result.json','status.json']:shutil.copyfile(W/name,O/name)
shutil.copyfile(S/'verification.json',O/'sources/verification.json')
for p in W.glob('_review_254_269b_*.py'):shutil.copyfile(p,O/p.name)
print(json.dumps({'reviewed':20,'corrected':4,'whole_book_complete':False}))
