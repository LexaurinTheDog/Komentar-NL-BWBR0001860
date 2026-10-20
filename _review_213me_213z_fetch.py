from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'_review_213aq_213md_fetch.py').read_text().replace('review-art-213aq-213md','review-art-213me-213z')
exec(compile(s,__file__,'exec'))
