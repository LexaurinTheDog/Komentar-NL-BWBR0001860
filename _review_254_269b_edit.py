from pathlib import Path
import sys,json,hashlib
W=Path(__file__).resolve().parent
sys.path.insert(0,'/Volumes/LaCie/open-commentary/_tools')
from build_repo import load_commentary
cs=load_commentary(str(W));P='review-art-254-269b';S=W/'sources'
(S/(P+'-before-hashes.json')).write_text(json.dumps({i:hashlib.sha256(t.encode()).hexdigest() for i,t in cs.items()},indent=2)+'\n')
p=W/'commentary/part-28.md';t=p.read_text();(S/(P+'-commentary-before.txt')).write_text(t)
changes=[
('Het moment van indiening van het akkoord beïnvloedt daarmee daadwerkelijk het procesverloop.','Ook bij deze route worden de rechter-commissaris en bewindvoerders gehoord; lid 3 laat die stap niet vervallen. Het moment van indiening van het akkoord beïnvloedt daarmee daadwerkelijk het procesverloop.'),
('Van artikel 136 worden uitsluitend de eerste twee leden over hoofdelijke schuldenaren en hun onderlinge aanspraken overgenomen.','Bij toondervorderingen kan de naam «toonder» worden gebruikt; elke aldus opgenomen vordering geldt als die van een afzonderlijke schuldeiser. Dat is ook voor de personenmeerderheid relevant. Van artikel 136 worden uitsluitend de eerste twee leden over hoofdelijke schuldenaren en hun onderlinge aanspraken overgenomen. De oorspronkelijke schuldeiser kan voor het nog verschuldigde geheel opkomen totdat hij volledig is voldaan. Voor toelating van de regresgerechtigde medeschuldenaar gelden de alternatieven van lid 2: de schuldeiser komt niet zelf op of kan dat niet, de toelating geldt voor het geval van diens volledige voldoening, of zij beïnvloedt de uitkeringspercentages voor concurrente schuldeisers om een andere reden niet nadelig.'),
('Na de reguliere indieningsdag maar uiterlijk twee dagen vóór de vergadering ingediende vorderingen kunnen op een ter vergadering gedaan verzoek nog op de lijst komen als bewindvoerders noch een aanwezige schuldeiser bezwaar maken.','Na de reguliere indieningsdag maar uiterlijk twee dagen vóór de vergadering ingediende vorderingen worden op een ter vergadering gedaan verzoek nog op de lijst geplaatst als bewindvoerders noch een aanwezige schuldeiser bezwaar maken. In dat geval bestaat dus geen vrije weigeringsbevoegdheid. Een bezwaar sluit toelating niet definitief uit: dan beslist de rechter-commissaris volgens lid 5.'),
('HR 8 december 2017, ECLI:NL:HR:2017:3110, rov. 3.6.2 en 3.8.3, maakt daarnaast duidelijk dat een gestelde onjuiste toepassing van de regels over het proces-verbaal niet zonder meer een doorbrekingsgrond voor het rechtsmiddelenverbod oplevert.','In HR 8 december 2017, ECLI:NL:HR:2017:3110, geeft rov. 3.6.2 de klacht van de verzoeker weer dat uit het proces-verbaal de individuele stemmen niet bleken; dit is geen eigen vaststelling van de Hoge Raad dat het proces-verbaal gebrekkig was. Het eigen oordeel in rov. 3.8.3 luidt dat onjuiste toepassing van een regel geen doorbrekingsgrond voor het rechtsmiddelenverbod is. De in rov. 3.7.1 omschreven andere doorbrekingsgronden moeten daarvan worden onderscheiden.')]
for a,b in changes:
 assert t.count(a)==1,a;t=t.replace(a,b)
p.write_text(t)
print('Four assigned commentaries corrected.')
