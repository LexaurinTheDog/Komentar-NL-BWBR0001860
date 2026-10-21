from pathlib import Path
p=Path('_review_254_269b_audit.py').read_text();p=p[:p.index('pre=json.loads')];p=p.replace('254-269b','270-281h').replace("'254 255 256 257 257a 258 259 260 261 262 263 264 265 266 267 268 268a 269 269a 269b'","'270 271 272 273 274 275 276 277 278 279 280 281 281a 281b 281c 281d 281e 281f 281g 281h'")
Path('_review_270_281h_audit.py').write_text(p)
