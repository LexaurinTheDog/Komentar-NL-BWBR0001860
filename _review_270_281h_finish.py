from pathlib import Path
import json,sys,shutil,subprocess,re,hashlib
W=Path(__file__).resolve().parent;S=W/'sources';P='review-art-270-281h';B=W/'batches/art-270-281h';m=json.loads((W/'meta.json').read_text());O=Path(m['repo_dir']);bm=json.loads((B/'meta.json').read_text());T=Path(bm['repo_dir'])
save=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'review-result.json').read_text());ids=r['reviewed_ids']
review='''

## Afgebakende tweede lezing — artikelen 270–281h

Op 21 oktober 2026 lokale tijd zijn precies twintig eenheden inhoudelijk aan de officiële tekst getoetst: artikelen 270–281 en 281a–281h. [Bevinding per artikel en exacte identifiers](sources/review-art-270-281h-result.json). Vijf toelichtingen zijn gecorrigeerd of verduidelijkt: 272 (de boedelbatentoets, alternatieve kostenwaarborg en precieze strekking van de aangehaalde rechtspraak), 278 (advocaatsondertekening volgens 283 in plaats van 282), 279 (acht dagen na hofuitspraak, cassatieadvocaat), 281e (beperking van de verwijzing naar 269 en onderscheid tussen beroep en spreekrecht), 281h (geverifieerd opschrift Wft-afdeling). Vijftien zijn zonder wijziging aanvaard. De overige toelichtingen zijn hashgelijk gebleven. Artikel 270 blijft als vervallen nummerplaats bewaard.

[Verse bronopnamen](sources/review-art-270-281h-fetch.json) bevatten werkelijke URL, UTC-tijd, HTTP-status, SHA-256 en formaatcontrole. De actuele route verwijst naar 1 september 2026 en vermeldt gelding tot heden. De oorspronkelijke auteurspeildatum blijft 19 oktober 2026. Het wijzigingsregister toont geen ingegane wijziging sinds de intake. Toekomstige wijzigingen en historische toestanden zijn uitgesloten. De historische bronnen van 2002 en 2025 zijn afzonderlijk op artikelplaatsen gecontroleerd. [Preflight](sources/review-art-270-281h-preflight-result.json).

De [parsercontrole](sources/review-art-270-281h-parser-check.json) vergelijkt onafhankelijk alle 639 officiële XML-labels, de HTML-inhoudsopgave en JSONL. Alle wettelijke teksten komen overeen; geen ontbrekende of dubbele identifiers. Het volledige officiële XML bevat geen operationele bijlagen. Aanhef, slottekst, vervallen plaatsen en bronnotities zijn verantwoord. Parser en volledigheidscontrole zijn herhaald met ongewijzigde producthashes. Deze technische bevinding bewijst geen juridische kwaliteit.

Beide bestaande autoriteiten zijn opnieuw volledig opgehaald en gelezen: [HR 26 augustus 2003, R03/049HR, ECLI:NL:HR:2003:AI0369](sources/review-art-270-281h-case-2003.md) en [Rb. Den Haag 13 november 2024, C/09/24/20 S, ECLI:NL:RBDHA:2024:18898](sources/review-art-270-281h-case-2024.md). HR rov. 3.3.2 ondersteunt zelfstandige toetsing en motivering; 3.9.3 betreft de beoordelingsvrijheid en cassatietoets. De Haagse rov. 3.2–3.3 onderscheidt de wettelijke surseancetoets van de WHOA; rov. 3.9 past de kostenwaarborg toe op concrete beschikbare middelen. De partijstellingen en het geciteerde bewindvoerdersadvies in onderdeel 2 zijn geen eigen rechterlijke rechtsregels. De HR-tekst is per alinea vergeleken met het lokale nationale corpus. [Vergelijking](sources/review-art-270-281h-case-comparison.json), [onderzoekslog](sources/review-art-270-281h-search-log.json). De eerdere HTML-applicatieschil bij een andere uitspraak is verworpen. Geen uitputtend nieuw rechtspraakonderzoek of controle van alle latere behandeling geclaimd.

De [Wft-bron](sources/review-art-270-281h-external-fetch.json) bevestigt het opschrift van afdeling 3.5.6 in de versie vanaf 29 september 2026. Artikel 281h blijft een bespreking van de schakelbepaling, geen volledige analyse van dat externe stelsel. Externe overgangswetten uit redactionele noten zijn niet zelfstandig beoordeeld voor historische procedures.

De batch is opnieuw gebouwd en strikt gevalideerd; [resultaten](sources/review-art-270-281h-validation.json) onderscheiden het checkpoint van de nog onvoltooide volledige manuscriptbouw. Dit oordeel betreft uitsluitend twintig artikelen, zonder externe professionele goedkeuring.
'''
p=W/'REVIEW.md';assert '## Afgebakende tweede lezing — artikelen 270–281h' not in p.read_text();p.write_text(p.read_text().rstrip()+review+'\n')
p=W/'SOURCES.md';p.write_text(p.read_text().rstrip()+'\n\nTweede lezing 270–281h: [bevindingen](sources/'+P+'-result.json), [preflight](sources/'+P+'-preflight-result.json), [rechtspraak](sources/'+P+'-search-log.json).\n')
card2003='''# HR 26 augustus 2003 — ECLI:NL:HR:2003:AI0369

Zaak R03/049HR, UPC-homologatie; ondersteund artikel: 272. [Officiële volledige XML](review-art-270-281h-hr-2003.xml), [leestekst](review-art-270-281h-hr-2003.txt), [nationaal corpus](review-art-270-281h-hr-2003-local.md). [Officiële vindplaats](https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:HR:2003:AI0369).

Rov. 3.3.2: homologatie is een op spoedige beslissing gerichte procedure met zelfstandige rechterlijke goedkeuring of weigering; gewone stelplicht en bewijslast gelden niet als in een contradictoire procedure. De motivering moet controle van de ingrijpende beslissing mogelijk maken. Rov. 3.9.3: de feitenrechter heeft ruime vrijheid bij goedkeuren/weigeren; het middel toonde niet dat het hof de mogelijkheid van andere of ambtshalve gronden had miskend. Het beroep is verworpen.

Bezwaren tegen lening, zekerheden en aandeelhoudersbegunstiging zijn zaakgebonden; weergegeven cassatieklachten zijn geen vaststellingen. Rov. 3.3.2 draagt de motiveringsregel; 3.9.3 gaat over beoordelingsvrijheid, niet een tweede algemene motiveringsregel. Huidig 272(2)(3) is vergeleken met de aangehaalde toets. Het arrest wordt niet gebruikt voor de huidige zittingsbepaling van het vervallen 270, noch voor bewijslast bij latere ontbinding onder 280/165. Geen audit van alle latere rechtspraak. Volledige uitspraak in deze tweede lezing gelezen, geen externe professionele goedkeuring.
'''
card2024='''# Rb. Den Haag 13 november 2024 — ECLI:NL:RBDHA:2024:18898

Insolventienummer C/09/24/20 S; ondersteund artikel: 272. [Officiële volledige XML](review-art-270-281h-rbdha-2024.xml), [leestekst](review-art-270-281h-rbdha-2024.txt). [Officiële vindplaats](https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:RBDHA:2024:18898).

Rov. 3.1–3.3: de gekozen surseanceprocedure brengt de toets van artikel 272 mee; WHOA-vereisten worden niet enkel wegens een mogelijke andere procedurekeuze ingevoerd. Rov. 3.9: op basis van de verklaring over beschikbare salarismiddelen doet de vierde verplichte weigeringsgrond zich hier niet voor. Rov. 3.20 en dictum: akkoord gehomologeerd, salaris en kosten vastgesteld.

De beschikking ontslaat niet van verplichte toetsing en maakt een algemene belofte om ooit te betalen niet voldoende zekerheid. De lezing van de grammaticaal ongelukkige kostenbepaling wordt gekoppeld aan het daadwerkelijke doel en deze concrete toepassing. Onderdeel 2 citeert partijstellingen, akkoord en bewindvoerdersadvies; dat materiaal wordt niet zelfstandig als rechterlijk oordeel behandeld. De waarderings- en begunstigingsbeslissingen elders in de beschikking zijn feitelijk gebonden. Huidig artikel 272 gecontroleerd; geen volledige latere-rechtspraakaudit. Volledige tekst gelezen en identiek aan eerdere officiële opname; selectieve dekking.
'''
(S/(P+'-case-2003.md')).write_text(card2003);(S/(P+'-case-2024.md')).write_text(card2024)
shutil.copyfile(W/'commentary/part-29.md',B/'commentary/part-29.md')
intro='''# Faillissementswet — beoordeeld checkpoint artikelen 270–281h

Precies twintig artikelen, inclusief het vervallen artikel 270. Wettekst vanaf 1 september 2026, auteurspeildatum 19 oktober 2026; tweede lezing op 21 oktober 2026 lokale tijd. [Officiële bron](https://wetten.overheid.nl/BWBR0001860/2026-09-01). Vijf toelichtingen verbeterd, vijftien aanvaard. Het volledige boek blijft onvoltooid.

Origineel commentaar © 2026 Vojtěch Říha, Apache-2.0. Officiële tekst en uitspraken zijn afzonderlijk bronmateriaal. Concept, geen externe professionele goedkeuring of individueel juridisch advies. Selectieve verificatie van twee volledige uitspraken; geen uitputtende rechtspraakdekking. Externe overgangswetten niet zelfstandig beoordeeld voor historische zaken; geen volledige analyse van de Wft-afdeling.

[Review](REVIEW.md) · [Bronnen](SOURCES.md) · [Dekking](coverage-evidence.json) · [Bevindingen](sources/review-art-270-281h-result.json).
'''
(B/'README.md').write_text(intro);(B/m['intro_file']).write_text(intro)
check=json.loads((S/(P+'-parser-check.json')).read_text());ex=check['expected_ids'];ex=ex[ex.index('art-270'):ex.index('art-281h')+1];assert ex==ids
save(B/'coverage-evidence.json',{'official_source':{'url':m['source_url'],'local_raw_evidence_path':'sources/'+P+'-selected.xml','sha256':sha(S/(P+'-selected.xml'))},'expected_ids':ex,'parsed_ids':[json.loads(l)['id'] for l in (B/'units.jsonl').read_text().splitlines()],'annex_disposition':'Verified absence: all XML tags and independent official HTML TOC checked, no operative annex. Full 639-unit inventory in parser-check.json. Repealed article270 retained.','scope':'Official contiguous range 270–281h; expected IDs independently obtained from official XML.'})
bm['title']='Faillissementswet — beoordeeld checkpoint artikelen 270–281h';save(B/'meta.json',bm)
for key,path in [('whole_book',W),('bounded',B)]:
 q=subprocess.run([sys.executable,'/Volumes/LaCie/open-commentary/_tools/build_repo.py',str(path)],capture_output=True,text=True);(S/(P+'-'+key+'-build.txt')).write_text(q.stdout+q.stderr)
 if key=='bounded':assert q.returncode==0,q.stderr
for c in bm['chapters']:
 shutil.copyfile(T/f"{c['n']:02d}-{c['slug']}.md",O/f"{c['n']:02d}-art-270-281h-checkpoint-{c['n']}.md")
for root in [O,B,T]:
 (root/'sources').mkdir(exist_ok=True)
 for p in S.glob(P+'-*'):shutil.copyfile(p,root/'sources'/p.name)
for name in ['REVIEW.md','SOURCES.md','review-result.json','review-checks.json','preflight-result.json','status.json']:shutil.copyfile(W/name,O/name)
for root in [B,T]:
 (root/'REVIEW.md').write_text('# Tweede lezing van twintig artikelen\n'+review)
 (root/'SOURCES.md').write_text('# Bronnen\n\n[Officiële tekst](https://wetten.overheid.nl/BWBR0001860/2026-09-01), [bronopnamen](sources/'+P+'-fetch.json), [preflight](sources/'+P+'-preflight-result.json), [parser](sources/'+P+'-parser-check.json), [rechtspraakonderzoek](sources/'+P+'-search-log.json), [Hoge Raad](sources/'+P+'-case-2003.md), [rechtbank](sources/'+P+'-case-2024.md).\n')
shutil.copyfile(S/'verification.json',O/'sources/verification.json')
for p in W.glob('_review_270_281h_*.py'):shutil.copyfile(p,O/p.name)
print('Built bounded checkpoint; whole-book build separately recorded.')
