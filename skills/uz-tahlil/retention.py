#!/usr/bin/env python3
"""retention.py - YouTube Studio'dan olingan "auditoriyani ushlab qolish" faylini o'qib, qayerda
tomoshabin ketishini topadi.

    python retention.py video.csv
    python retention.py video.csv --davomiylik 615              # video uzunligi, soniya
    python retention.py video.csv --davomiylik 615 --transkript video.srt
    python retention.py video.csv --oq soniya                   # o'qni aniq ko'rsatish: soniya | foiz
    python retention.py v1.csv v2.csv v3.csv                    # bir nechta videoni solishtirish
    python retention.py video.csv --json

Fayl: ikki ustun - videodagi o'rin (foiz yoki soniya) va hali ko'rayotganlar foizi. Sarlavha
qatoridan o'q turi aniqlanadi; aniqlanmasa taxmin qilinadi va ogohlantiriladi.

Uchta alohida muammo, uchta alohida yechim:
  BOSHLANISH   birinchi 30 soniyada yo'qotilgan tomoshabin (bu - hook va kirish)
  KESKIN       bitta joyda keskin tushish - aniq bir lahza
  SEKIN        o'rtadagi bir tekis oqish (bu - temp, montaj)

UMUMIY "ME'YOR" YO'Q. Bu vosita "yaxshi" yoki "yomon" demaydi - o'z videolaringizni bir-biri bilan
solishtiring (bir nechta faylni bering). Eng foydali signal shu.
"""
import csv, json, os, re, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# --- transkript o'qish (montaj.py, boblar.py, retention.py da bir xil) ---------------------------
TEG = re.compile(r"<[^>]+>")


def vaqt(s):
    s = s.strip().replace(",", ".")
    p = s.split(":")
    if len(p) == 3:
        return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2])
    if len(p) == 2:
        return int(p[0]) * 60 + float(p[1])
    return float(p[0])


def yukla_transkript(yol):
    with open(yol, encoding="utf-8-sig", errors="replace") as f:
        raw = f.read()
    if yol.lower().endswith(".json"):
        d = json.loads(raw)
        segs = d.get("segments", []) if isinstance(d, dict) else d
        return [(float(s["start"]), float(s["end"]), str(s.get("text") or "").strip()) for s in segs]
    bloklar, joriy = [], None
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]*)\s*-->\s*(\d[\d:.,]*)", line)
        if m:
            joriy = [vaqt(m.group(1)), vaqt(m.group(2)), []]
            bloklar.append(joriy)
            continue
        s = line.strip()
        if not s:
            joriy = None
            continue
        if joriy is not None and not s.isdigit():
            s = TEG.sub("", s).strip()
            if s:
                joriy[2].append(s)
    natija, oldingi = [], []
    for a, b, qatorlar in bloklar:
        yangi = list(qatorlar)
        while yangi and yangi[0] in oldingi:
            yangi.pop(0)
        if qatorlar:
            oldingi = qatorlar
        matn = " ".join(yangi).strip()
        if matn:
            natija.append((a, b, matn))
    return natija
# -------------------------------------------------------------------------------------------------


def son(c):
    c = c.strip().replace("%", "").replace(" ", "").replace(" ", "")
    if c.count(",") == 1 and "." not in c:
        c = c.replace(",", ".")          # 12,5 -> 12.5 (vergulli kasr)
    else:
        c = c.replace(",", "")
    try:
        return float(c)
    except ValueError:
        return None


def yukla_csv(yol):
    qatorlar, sarlavha = [], None
    with open(yol, newline="", encoding="utf-8-sig", errors="replace") as fh:
        namuna = fh.read(4096)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(namuna, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        for r in csv.reader(fh, dialect):
            nums = [son(c) for c in r]
            vals = [n for n in nums if n is not None]
            if len(vals) >= 2:
                qatorlar.append((vals[0], vals[1]))
            elif sarlavha is None and r:
                sarlavha = [c.strip().lower() for c in r]
    return qatorlar, sarlavha or []


def oq_turi(xs, sarlavha, majburiy):
    if majburiy:
        return majburiy, None
    birinchi = sarlavha[0] if sarlavha else ""
    if re.search(r"%|foiz|percent|ratio", birinchi):
        return ("ulush" if max(xs) <= 1.0 else "foiz"), None
    if re.search(r"sec|soniya|time|vaqt|сек|время", birinchi):
        return "soniya", None
    if max(xs) <= 1.0:
        return "ulush", None
    if max(xs) > 100.5:
        return "soniya", None
    return "foiz", "o'q foizmi yoki soniyami aniq emas - foiz deb olindi; kerak bo'lsa --oq soniya deng"


def tahlil(yol, davomiylik=None, majburiy=None, transkript=None):
    rows, sarlavha = yukla_csv(yol)
    if len(rows) < 8:
        return {"fayl": yol, "xato": "fayldan kamida 8 ta nuqta o'qib bo'lmadi"}
    xs = [r[0] for r in rows]
    ys = [r[1] for r in rows]
    tur, ogoh = oq_turi(xs, sarlavha, majburiy)
    if tur == "ulush":
        xs = [x * 100 for x in xs]
        tur = "foiz"
    if max(ys) <= 1.5:
        ys = [y * 100 for y in ys]

    def soniyaga(x):
        if tur == "soniya":
            return x
        return x / 100.0 * davomiylik if davomiylik else None

    if tur == "soniya":
        chegara, chegara_nomi = 30.0, "birinchi 30 soniya"
    elif davomiylik:
        chegara, chegara_nomi = 30.0 / davomiylik * 100, "birinchi 30 soniya"
    else:
        chegara, chegara_nomi = 10.0, "birinchi 10% (davomiylik berilmagan)"
    boshi = ys[0]
    bosh_oxiri = min((y for x, y in zip(xs, ys) if x <= chegara), default=boshi)
    boshlanish = boshi - bosh_oxiri
    tushish = []
    for i in range(1, len(xs)):
        d = ys[i - 1] - ys[i]
        tushish.append((d, xs[i - 1], xs[i]))
    keskin = [{"dan": round(a, 2), "gacha": round(b, 2), "yoqotildi": round(d, 2),
               "soniya": (round(soniyaga(a), 1) if soniyaga(a) is not None else None)}
              for d, a, b in sorted(tushish, reverse=True)[:5] if d >= 1.0 and a > chegara]
    # sekin oqish: boshlanishdan keyin, oxirgi 10% dan oldin (oxiridagi tushish tabiiy - yakuniy ekran)
    oxir = max(xs) * 0.9
    orta = [(x, y) for x, y in zip(xs, ys) if chegara < x <= oxir]
    sekin = None
    if len(orta) >= 2 and orta[-1][0] > orta[0][0]:
        oraliq = orta[-1][0] - orta[0][0]
        birlik = (max(xs) / 10.0)        # videoning 10% i
        sekin = round((orta[0][1] - orta[-1][1]) / oraliq * birlik, 2)
    aytilgan = {}
    if transkript and os.path.exists(transkript):
        q = yukla_transkript(transkript)
        for k in keskin:
            if k["soniya"] is None:
                continue
            t = k["soniya"]
            yaqin = [c[2] for c in q if c[0] <= t + 4 and c[1] >= t - 4]
            k["aytilgan"] = " ".join(yaqin)[:160]
    return {"fayl": yol, "nuqtalar": len(rows), "oq": tur, "ogohlantirish": ogoh,
            "boshi": round(boshi, 1), "oxiri": round(ys[-1], 1), "chegara_nomi": chegara_nomi,
            "boshlanish": round(boshlanish, 1), "keskin": keskin, "sekin_10foizga": sekin}


def korsat(r):
    if "xato" in r:
        print(f"\n  {r['fayl']}: {r['xato']}"); return
    print(f"\n  {r['fayl']}   {r['nuqtalar']} nuqta   {r['boshi']}% -> {r['oxiri']}%   (o'q: {r['oq']})")
    if r["ogohlantirish"]:
        print(f"  ! {r['ogohlantirish']}")
    print(f"\n  BOSHLANISH  {r['chegara_nomi']}da {r['boshlanish']}% tomoshabin ketdi")
    print("              Bu hook va kirish. Birinchi shuni tuzating, keyin boshqasini.")
    print("\n  KESKIN      odamlar aynan ketgan lahzalar")
    for k in r["keskin"]:
        joy = f"{int(k['soniya'] // 60)}:{int(k['soniya'] % 60):02d}" if k["soniya"] is not None else f"{k['dan']}%"
        qosh = f'   "{k["aytilgan"]}"' if k.get("aytilgan") else ""
        print(f"    -{k['yoqotildi']:5.1f}%  {joy:>8}{qosh}")
    if not r["keskin"]:
        print("    1% dan keskin tushish yo'q - yo'qotish lahzalarda emas, sekin oqishda")
    if r["sekin_10foizga"] is not None:
        print(f"\n  SEKIN       o'rtada videoning har 10% ida o'rtacha {r['sekin_10foizga']}% tomoshabin ketadi")
        print("              Bir tekis oqish - bu temp. Yechim qayta yozish emas, qisqartirish.")
    print()


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    davomiylik = majburiy = transkript = None
    if "--davomiylik" in a:
        i = a.index("--davomiylik"); davomiylik = float(a[i + 1]); del a[i:i + 2]
    if "--oq" in a:
        i = a.index("--oq"); majburiy = a[i + 1].lower(); del a[i:i + 2]
    if "--transkript" in a:
        i = a.index("--transkript"); transkript = a[i + 1]; del a[i:i + 2]
    fayllar = [x for x in a if os.path.exists(x)]
    if not fayllar:
        print(__doc__); sys.exit(1)
    natija = [tahlil(f, davomiylik if len(fayllar) == 1 else None, majburiy, transkript) for f in fayllar]
    if as_json:
        print(json.dumps(natija if len(natija) > 1 else natija[0], ensure_ascii=False, indent=1)); return
    for r in natija:
        korsat(r)
    yaxshi = [r for r in natija if "xato" not in r]
    if len(yaxshi) > 1:
        print("  SOLISHTIRISH (boshlanishdagi yo'qotish bo'yicha, kamidan ko'piga)")
        for r in sorted(yaxshi, key=lambda r: r["boshlanish"]):
            sekin = "-" if r["sekin_10foizga"] is None else r["sekin_10foizga"]
            print(f"    {r['boshlanish']:5.1f}%   sekin {sekin!s:>5}   oxiri {r['oxiri']:5.1f}%   {os.path.basename(r['fayl'])}")
        print("  Eng yaxshi boshlangan video bilan eng yomonining birinchi 15 soniyasini yonma-yon o'qing.\n")


if __name__ == "__main__":
    main()
