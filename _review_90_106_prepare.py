from pathlib import Path
import json,shutil
W=Path(__file__).resolve().parent
ids=['art-'+n for n in ['90','91','92','93','93a','94','95','96','97','98','99','100','101','102','103','104','105','105a','105b','106']]
assess=[
('1–2','Overbrenging op last RC en uitvoering OM onderscheiden van ontslag bewaring.',['87','88']),
('ongesplitst','Toestemming RC voor verlaten woonplaats; niet alleen landsgrens of curatorinstemming.',['106']),
('ongesplitst','Onmiddellijk veiligstellen, ontvangbewijs en facultatieve consignatie; digitale bewaring onderscheiden van publicatie.',['94','105a','105b','68a']),
('1–2','Noodzaak bij curator of RC, notaris en proces-verbaal; uitzonderingen precies afgebakend.',['7','21','92']),
('ongesplitst','Redelijke taaknoodzaak en machtigingsbevoegdheid onderscheiden; toegang beslist niet over eigendom. Externe Awbi-procedure niet volledig uiteengezet.',[]),
('1–3','Spoed, onderhandse beschrijving en curatorwaardering onder RC-goedkeuring; aanwezigheid voorlopige commissie.',['96']),
('ongesplitst','Aangehechte staat beschermde goederen tegenover opname artikel 92; geen eigendomsbeslissing.',['21','92','94','96']),
('ongesplitst','Direct na inventaris, aard en bedragen baten/schulden en crediteuren; geen definitieve verificatie.',['97','68a']),
('1–2','Bevoegde griffie, gewaarmerkte kopieën, kosteloze inzage voor iedereen en neerlegging; afschriftkosten apart.',['107']),
('ongesplitst','Machtiging zonder commissie; met commissie advies en afwijkingsprocedure; latere voortzetting apart.',['39','40','78','79','173a']),
('1–2','Postlast en kennisgeving, directe terhandstelling niet-boedelpost, einde beide bevoegdheden; formele verklaringen via curator.',['14','15','68a']),
('ongesplitst','Facultatieve uitkering, omstandigheden, vaststelling RC en verplicht commissieadvies.',['21','78']),
('1–2','Openbare/onderhandse verkoop, cumulatieve 2000-eurogrens volgens inventaris en bijzondere baten; commissieadvies.',['78','176']),
('1–2','Onmiddellijke bewaring tenzij andere wijze RC; overliquiditeit belegd op boedelnaam met goedkeuring.',['103']),
('ongesplitst','Derdenbewaring volgens RC en belegde gelden; voor gezien getekende stukken, geen zelfstandig uitdelingsrecht.',['102']),
('ongesplitst','Advies bestaande commissie en RC-goedkeuring cumulatief; inhoud finale kwijting en verhaalafweging.',['72']),
('1, 2a–b, 3','Gevraagde en spontane informatie onderscheiden; buitenlands melden en meewerken; partners enkel gemeenschap; beperkte betekenis oudere HR-dwangwaarborg.',['105a']),
('1–3','Algemene medewerking, onmiddellijke volledige ongeschonden administratie en leesmiddelen; partnerbeperking en grenzen contactdwang.',['105b']),
('1–3','Beroepsmatige derden op verzoek, leesmiddelen, retentierecht doorbroken en strijdige bedingen nietig; bestaande gegevens versus nieuw werk.',['60']),
('1, 2a–b, 3','Huidige/voormalige bestuurders en commissarissen, driejaarstermijn, feitelijke beleidsbepalers, indirect bestuur, VOF/CV; geen zelfstandige aansprakelijkheid.',['87','88','89','90','91','92','105','105a'])]
notes={k:(paragraph,txt,['art-'+x for x in refs],['ECLI:NL:HR:2014:161'] if k=='art-105' else ['ECLI:NL:HR:2026:400'] if k=='art-105a' else []) for k,(paragraph,txt,refs) in zip(ids,assess)}
s=(W/'_review_73_89_audit.py').read_text().replace('73-89','90-106').replace('73_89','90_106')
a=s.index("ids=['art-'+n");b=s.index('\nrecords=[]',a);s=s[:a]+'ids='+repr(ids)+s[b:]
s=s.replace("['2024-1382', '2021-102', '2026-400', '2014-161']","['2026-400', '2014-161']")
a=s.index('notes={');b=s.index('\nassert list(notes)==ids',a);s=s[:a]+'notes='+repr(notes)+s[b:]
s=s.replace('Four selected full HR decisions independently fetched','Two selected full HR decisions independently fetched')
(W/'_review_90_106_audit.py').write_text(s)
for k in ['2026-400','2014-161']:
 for suffix in ['.txt','-local.md']:
  shutil.copyfile(W/f'sources/review-art-73-89-hr-{k}{suffix}',W/f'sources/review-art-90-106-hr-{k}{suffix}')
(W/'sources/review-art-90-106-search-log.json').write_text(json.dumps({'method':'Focused re-examination of two primary HR decisions identified by previous research; full text read, fresh official XML fetched and national corpus snapshots compared. No new exhaustive database search.','selected':['ECLI:NL:HR:2014:161','ECLI:NL:HR:2026:400'],'scope':'Information and cooperation duties; no separate case cited for technical inventory and custody units.','search_evidence':'review-art-73-89-search-log.json'},indent=2)+'\n')
