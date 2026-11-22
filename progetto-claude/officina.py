# officina.py foglio.png out_dir nomi(comma) [altezza_guardia] [righe]
# Toglie il verde, trova le pose (componenti grandi), le ordina per righe, scala, contorno scuro, palette.
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

src, out, nomi = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
hg = float(sys.argv[4]) if len(sys.argv) > 4 else 135
os.makedirs(out, exist_ok=True)
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
verde = (g > 120) & (g > r + 50) & (g > b + 50)
# frangia: pixel verdastri al bordo
fg = ~verde
fg = ndimage.binary_opening(fg, iterations=1)
# occhi verdi: piccole isole verdi chiuse dentro la figura restano (buchi sotto 400 pixel)
filled = ndimage.binary_fill_holes(fg)
hl, hn = ndimage.label(filled & ~fg)
if hn:
    sz = ndimage.sum(np.ones_like(hl), hl, range(1, hn + 1))
    small = np.isin(hl, np.nonzero(sz < 400)[0] + 1)
    fg = fg | small
OCCHI = small if hn else np.zeros_like(fg)
lab, n = ndimage.label(ndimage.binary_dilation(fg, iterations=int(os.environ.get('DIL','6'))))
objs = ndimage.find_objects(lab)
H = a.shape[0]
boxes = []
for i, sl in enumerate(objs):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    area = (lab[sl] == i + 1).sum()
    if h < H * float(os.environ.get('MINH','0.06')) or area < 1500: continue
    boxes.append((sl, i + 1))
# righe: raggruppa per centro verticale
boxes.sort(key=lambda x: (x[0][0].start + x[0][0].stop) / 2)
rows = []
for bx in boxes:
    cy = (bx[0][0].start + bx[0][0].stop) / 2
    if rows and abs(cy - rows[-1][0]) < H * 0.12:
        rows[-1][1].append(bx); rows[-1][0] = np.mean([(q[0][0].start + q[0][0].stop) / 2 for q in rows[-1][1]])
    else: rows.append([cy, [bx]])
ordered = []
for cy, rb in rows: ordered += sorted(rb, key=lambda x: x[0][1].start)
print('pose trovate', len(ordered), 'nomi', len(nomi))
crops = []
for (sl, idx) in ordered:
    m = (lab[sl] == idx) & fg[sl]
    c = a[sl].copy()
    # despill: dove il verde domina, abbassalo
    gg = c[..., 1]; mx = np.maximum(c[..., 0], c[..., 2])
    c[..., 1] = np.where((gg > mx + 10) & ~OCCHI[sl], mx + 10, gg)
    rgba = np.dstack([c, (m * 255)]).astype(np.uint8)
    crops.append(Image.fromarray(rgba, 'RGBA'))
# scala dalla guardia (prima posa)
k = (float(sys.argv[5]) if len(sys.argv) > 5 else hg / crops[0].height)
print('scala', round(k, 3))
ax = {}
for nm, c in zip(nomi, crops):
    w, h = max(1, round(c.width * k)), max(1, round(c.height * k))
    s = c.resize((w, h), Image.LANCZOS)
    A = np.asarray(s).copy(); al = A[..., 3] > 110
    A[..., 3] = np.where(al, 255, 0)
    # contorno scuro: pixel trasparenti adiacenti all'oggetto
    ring = ndimage.binary_dilation(al) & ~al
    A[ring] = [24, 16, 28, 255]
    img = Image.fromarray(A, 'RGBA')
    q = img.convert('RGB').quantize(48, method=Image.MEDIANCUT).convert('RGB')
    QQ = np.asarray(q).copy(); P = A[..., :3].astype(int)
    ge = (P[..., 1] > 150) & (P[..., 1] > P[..., 0] + 60) & (P[..., 1] > P[..., 2] + 60) & al
    QQ[ge] = np.where(P[ge][:, 1:2] > 200, [170, 255, 120], [60, 200, 60])
    Q = np.dstack([QQ, A[..., 3]]).astype(np.uint8)
    Image.fromarray(Q, 'RGBA').save(f'{out}/{nm}.png')
    # appoggio: mediana orizzontale della fascia del busto (35-60% dall'alto)
    al2 = Q[..., 3] > 0; y0, y1 = int(h * 0.35), int(h * 0.6)
    xs = np.nonzero(al2[y0:y1])[1]
    ax[nm] = round(float(np.median(xs)) / w, 3) if len(xs) else 0.5
    print(nm, (w, h), ax[nm])
import json
f = f'{out}/_ax.json'; old = json.load(open(f)) if os.path.exists(f) else {}
old.update(ax); json.dump(old, open(f, 'w'))
