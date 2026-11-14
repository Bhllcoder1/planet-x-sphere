import numpy as np, glob
F = r"stage0\data\D\frames"
def load(sub):
    p = [q for q in glob.glob(F + "\\*_image.npy") if sub in q][0]
    return np.load(p), np.load(p.replace("_image", "_flags")).astype(np.int64)
np.set_printoptions(linewidth=250, precision=2, suppress=True)
for sub, name, x, y in [("2025W52_1A_0355_3D2", "Cybele", 1521.33, 1082.48), ("2025W51_2A_0573_1D1", "Massalia", 1296.44, 678.67),
                        ("2025W52_2A_0007_4D3", "Cybele", 1061.19, 1375.02), ("2025W52_1A_0355_3D2", "Russia", 1391.58, 894.64)]:
    im, fl = load(sub); xi, yi = int(round(x)), int(round(y))
    print("\n", sub, name, x, y)
    print(im[yi - 6:yi + 7, xi - 6:xi + 7])
    w = im[yi - 20:yi + 21, xi - 20:xi + 21]
    md = np.nanmedian(w)
    print("max41", np.nanmax(w), "median", md, "madsd", 1.48 * np.nanmedian(abs(w - md)), "argmax(dx,dy)", np.unravel_index(np.nanargmax(w), w.shape)[::-1])
    fs = fl[yi - 4:yi + 5, xi - 4:xi + 5]
    print("code: 1=OUTLIER 2=SOURCE 4=TRANSIENT 8=HALO")
    print((fs >> 19 & 1) * 1 + (fs >> 21 & 1) * 2 + (fs & 1) * 4 + (fs >> 28 & 1) * 8)
