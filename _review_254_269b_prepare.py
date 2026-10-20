from pathlib import Path
p=Path('_review_241d_253_audit.py').read_text()
p=p[:p.index('comparisons=[]')]
p=p.replace('241d-253','254-269b').replace('241d_253','254_269b').replace("'241d 241e 242 243 244 245 246 247 247a 247b 247c 247d 248 249 249a 250 250a 251 252 253'","'254 255 256 257 257a 258 259 260 261 262 263 264 265 266 267 268 268a 269 269a 269b'")
p=p.replace(";external=json.loads((S/(P+'-external-fetch.json')).read_text())",'')
p=p.replace("assert external[0]['accepted'] and external[1]['http_status']==202 and not external[1]['accepted']\n",'')
Path('_review_254_269b_audit.py').write_text(p)
