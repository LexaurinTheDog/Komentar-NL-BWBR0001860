from pathlib import Path
import json,datetime,shutil
W=Path(__file__).resolve().parent
ids=['art-'+n for n in ['106a','106b','106c','106d','106e','107','108','109','110','110a','111','112','113','114','115','116','117','118','119','120']]
a=[
('1a–e,2–4','Afzonderlijke gronden, rechterlijke onherroepelijkheid, ernstige tekortkoming, twee eerdere betrokkenheden en uitzonderingen natuurlijke personen; grond c feitelijk geïllustreerd, grond d niet door zaak bewezen.',['42','47','106b'],['ECLI:NL:RBOVE:2020:1557']),
('1–6','Duur vanaf kracht van gewijsde, nietige benoeming versus beletsel, registratie, dwangsom en geen uitvoerbaarheid verbod; afzonderlijke kostenveroordeling onderscheiden.',['86','106c'],['ECLI:NL:RBOVE:2020:1557']),
('1–6','Uittreksel, zienswijze, enige-bestuurderuitzondering, bezoldiging, voorlopige schorsing op verzoek/vordering, maximumduur en registerinschrijving.',['106b'],[]),
('1–2','Feitelijk beleidsbepaler vereist rol als ware bestuurder; one-tier gelijkstellingen niet vanzelf zelfstandige verbodsgrond.',['106a','106b','106c'],[]),
('ongesplitst','Europese rechtsvormen en statutaire zetel Nederland; personele reikwijdte en overeenkomstige voorwaarden, geen automatische schadeaansprakelijkheid.',['106a','106b','106c','106d'],[]),
('1–2','Schuldeisersafschrift en publieke afschriftenkring onderscheiden, kopiekosten tegenover gratis inzage; checklist gelezen.',['73a','97','68a'],[]),
('ongesplitst','Na onherroepelijkheid zo nodig één of meer vergaderingen; RC bepaalt vorm en planning, samenhang deadline.',['80a','127'],[]),
('1–2','Onmiddellijke kennisgeving beschikking tegenover zo spoedig mogelijke deadlinewaarschuwing; bekende schuldeisers, schriftelijkheid.',['108','110','127'],[]),
('1–3','Aard, bedrag, bewijs en rang; ontvangbewijs geen erkenning; collectieve overeenkomst doelgroep, elektronische route, facultatief vervalbeding en verwijzingen 128/133/136 aangevuld.',['111','128','133','136'],[]),
('ongesplitst','Herstel onvolledig Europees standaardformulier; geen zelfbedachte automatische verlenging van indieningsdag.',['5'],[]),
('ongesplitst','Actieve toets, overleg bij bezwaar, ontbrekende documenten en oorspronkelijke bewijzen; ontvangst versus erkenning.',['110','112'],[]),
('ongesplitst','Twee voorlopige lijsten, motivering, gedeeltelijke betwisting, herziening en definitieve vastlegging onderscheiden.',['119','113','114'],[]),
('ongesplitst','Omschrijving en rang/zekerheden, alleen rang of retentie betwist laat schuld voorlopig erkend; voorbeeld voorwaardelijk gehouden.',[],[]),
('1–2','Zevendaagse kosteloze inzage voor iedereen en kosteloze neerlegging onderscheiden van afschriftkosten.',['112','119','127','68a','107'],[]),
('ongesplitst','Bericht alle bekende crediteuren, nadere oproeping en ontwerp-akkoord; geen aanneming of homologatie door vermelding.',['83'],[]),
('ongesplitst','Deelnamevorm RC, vragen via RC en proces-verbaal; informatie geen aansprakelijkheidsoordeel.',['117','105'],[]),
('1–2','Personele verwijzing art106 eerste/tweede lid, curatoroproeping vereist, overeenkomstige toepassing VOF/CV.',['116','106'],[]),
('vervallen','Expliciete vervallen plaats behouden; geen historische inhoud als actuele verplichting.',['116','117'],[]),
('1–3','Lijstinformatie, rechten daarop voorkomende schuldeisers, wijzigbaar curatorstandpunt, eed onbetwiste schuld, rechthebbenden na overlijden en nadere vergadering.',['121','122'],[]),
('1–3','Eed in persoon/bijzondere volmacht, latere dag, griffierbericht afwezige, verklaring of PV; samenhang voorwaardelijke toelating.',['119','121'],[])]
notes={k:(p,t,['art-'+r for r in refs],cases) for k,(p,t,refs,cases) in zip(ids,a)}
s=(W/'_review_90_106_audit.py').read_text().replace('90-106','106a-120').replace('90_106','106a_120')
start=s.index("ids=['art-");end=s.index('\nrecords=[]',start);s=s[:start]+'ids='+repr(ids)+s[end:]
start=s.index('comparisons=[]');end=s.index('notes={',start);s=s[:start]+s[end:]
start=s.index('notes={');end=s.index('\nassert list(notes)==ids',start);s=s[:start]+'notes='+repr(notes)+s[end:]
s=s.replace("'case_comparison':'sources/review-art-106a-120-case-comparison.json'","'case_source':'sources/review-art-106a-120-cases-fetch.json'")
s=s.replace('Two selected full HR decisions independently fetched and compared with national corpus; no exhaustive case-law search or separate case for every technical article.','One selected full district-court decision independently fetched and read; local HR 2021:112 consulted as context but not cited as authority. No exhaustive search or separately verified decision for each technical unit.')
(W/'_review_106a_120_audit.py').write_text(s)
(W/'sources/review-art-106a-120-search-log.json').write_text(json.dumps({'searched_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'queries':['site.rechtspraak.nl "106a" "bestuursverbod" "ernstige"','site.rechtspraak.nl "Faillissementswet" "110" "verificatie" Hoge Raad'],'selected_full_decisions':['ECLI:NL:RBOVE:2020:1557'],'method':'Official search discovery followed by full primary XML read, including parties positions, judicial reasoning and disposition.','local_corpus_consulted':'/Volumes/LaCie/law-intake/eu/nl/rechtspraak/hr/ecli-nl-hr-2021-112.md','local_context_disposition':'Read as research context on verification and composition; no proposition or citation added from this decision, whose main scope is penal monetary claims. Local corpus has HR/PHR and administrative decisions; district-court source fetched directly.','limitations':'Selective research; no exhaustive subsequent treatment check. No separately verified case used for technical verification units.'},ensure_ascii=False,indent=2)+'\n')
