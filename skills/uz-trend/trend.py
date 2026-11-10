#!/usr/bin/env python3
"""trend.py - kontentni o'z kanalining odatiy natijasiga nisbatan saralash va formulasini aniqlash.

    python trend.py yigilgan.json                 # boshqa kanallar (raqobatchilar)
    python trend.py postlarim.csv --min 1.5       # o'z kanalingiz / postlaringiz
    python trend.py a.json b.csv --past           # eng yomon chiqqanlarni ham ko'rsatish
    python trend.py yigilgan.json --json

Kiruvchi ma'lumot - siz yig'gan ro'yxat. Har bir element - bitta video yoki post:

    [{"manba": "Kanal nomi", "matn": "sarlavha yoki birinchi qator", "korishlar": 41200,
      "platforma": "youtube", "url": "...", "sana": "2026-10-01"}]

Inglizcha kalitlar ham tushuniladi (channel, title, views). CSV bo'lsa - xuddi shu nomli ustunlar.
yt-dlp --flat-playlist -J natijasi ham to'g'ridan-to'g'ri o'qiladi (entries, view_count).

Nega ko'rishlar soni emas: ko'rishlar soni kanal hajmini o'lchaydi, g'oyani emas. 1 million
obunachili kanalda 50 ming ko'rish - oddiy kun; odatda 5 ming ko'radigan kanalda 50 ming - o'rganishga
arziydigan narsa. Shuning uchun har bir element O'Z MANBASINING MEDIANASIGA KARRALIK bilan
baholanadi. Buning uchun har bir manbadan kamida 4 ta element kerak - kam bo'lsa, vosita o'sha
manbani tashlab, buni aytadi.

Formula ../uz-ssenariy/formulalar.json dan, MATN bo'yicha aniqlanadi. Bu ko'rinib turgan so'zlar
haqidagi xulosa, video nega ko'p ko'rilgani haqida da'vo emas.
"""
import csv, json, os, re, statistics, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# --- o'zbek matnini normallashtirish (har bir vositada bir xil) ---------------------------------
APOS = "ʻʼ‘’`´"
KIR = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "j", "з": "z",
       "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
       "с": "s", "т": "t", "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh",
       "ъ": "'", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya", "ў": "o'", "қ": "q", "ғ": "g'",
       "ҳ": "h"}
UNLI = set("аеёиоуэюяўaeiou")


def lotinla(t):
    out, prev = [], " "
    for ch in t:
        lo = ch.lower()
        if lo in KIR:
            if lo == "е" and (not prev.isalpha() or prev.lower() in UNLI or prev in "ъьЪЬ"):
                r = "ye"
            else:
                r = KIR[lo]
            if ch != lo and r:
                r = r[0].upper() + r[1:]
            out.append(r)
        else:
            out.append(ch)
        prev = ch
    return "".join(out)


def tozala(t):
    t = lotinla(t)
    for a in APOS:
        t = t.replace(a, "'")
    return t.lower()
# -------------------------------------------------------------------------------------------------

KALIT = {
    "manba": ["manba", "kanal", "channel", "uploader", "playlist_uploader", "author"],
    "matn": ["matn", "sarlavha", "title", "text", "caption", "izoh"],
    "korishlar": ["korishlar", "ko'rishlar", "views", "view_count", "korish"],
    "platforma": ["platforma", "platform", "ie_key", "extractor_key"],
    "url": ["url", "webpage_url", "link", "havola"],
    "sana": ["sana", "date", "upload_date", "timestamp"],
}


def ol(d, nom, standart=""):
    for k in KALIT[nom]:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return standart


def raqam(v):
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().lower().replace(" ", "").replace(" ", "")
    s = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", s)      # 41,200 -> 41200
    s = s.replace(",", ".")                               # 1,2k -> 1.2k
    kar = 1
    for q, k in (("k", 1e3), ("ming", 1e3), ("m", 1e6), ("mln", 1e6)):
        if s.endswith(q):
            kar, s = k, s[: -len(q)]
            break
    try:
        return float(s) * kar
    except ValueError:
        return 0.0


def yukla(yol):
    with open(yol, encoding="utf-8-sig", errors="replace") as f:
        raw = f.read()
    if yol.lower().endswith(".csv"):
        return [dict(r) for r in csv.DictReader(raw.splitlines())], ""
    d = json.loads(raw)
    if isinstance(d, list):
        return d, ""
    standart = ol(d, "manba") or d.get("title", "")
    for k in ("entries", "videos", "postlar", "items"):
        if isinstance(d.get(k), list):
            return d[k], standart
    return [], standart


def formulalar():
    yol = os.path.join(HERE, "..", "uz-ssenariy", "formulalar.json")
    if not os.path.exists(yol):
        return []
    with open(yol, encoding="utf-8") as f:
        return json.load(f)["formulalar"]


def aniqla(matn, formulas):
    tz = tozala(matn).strip()
    eng = []
    for f in formulas:
        n = sum(1 for p in f["naqsh"] if re.search(p, tz))
        if n:
            eng.append((n, f["nomi"]))
    eng.sort(key=lambda x: -x[0])
    return eng[0][1] if eng else ("Aniqlanmadi" if formulas else "-")


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    past = "--past" in a
    a = [x for x in a if x != "--past"]
    chegara = 2.0
    if "--min" in a:
        i = a.index("--min"); chegara = float(a[i + 1]); del a[i:i + 2]
    fayllar = [x for x in a if os.path.exists(x)]
    if not fayllar:
        print(__doc__); sys.exit(1)
    elementlar = []
    for f in fayllar:
        rows, standart = yukla(f)
        for r in rows:
            elementlar.append({"manba": str(ol(r, "manba", standart) or "?"),
                               "matn": str(ol(r, "matn")), "korishlar": raqam(ol(r, "korishlar", 0)),
                               "platforma": str(ol(r, "platforma")), "url": str(ol(r, "url"))})
    formulas = formulalar()
    guruh = {}
    for e in elementlar:
        guruh.setdefault(e["manba"], []).append(e)
    natija, kam = [], []
    for manba, items in guruh.items():
        if len(items) < 4:
            kam.append((manba, len(items)))
            continue
        med = statistics.median(e["korishlar"] for e in items)
        for e in items:
            k = e["korishlar"] / med if med else 0
            natija.append({**e, "korishlar": int(e["korishlar"]), "mediana": int(med),
                           "karra": round(k, 2), "formula": aniqla(e["matn"], formulas)})
    yuqori = sorted([r for r in natija if r["karra"] >= chegara], key=lambda r: -r["karra"])
    quyi = sorted([r for r in natija if r["karra"] <= 1 / chegara], key=lambda r: r["karra"]) if past else []
    if as_json:
        print(json.dumps({"yuqori": yuqori, "quyi": quyi, "kam_manbalar": kam},
                         ensure_ascii=False, indent=1))
        return
    print(f"\n  {len(elementlar)} ta element, {len(guruh)} ta manba, {chegara}x va undan yuqori\n")
    for r in yuqori[:25]:
        print(f"    {r['karra']:5.2f}x  {r['korishlar']:>9,}  / {r['mediana']:>9,} mediana   "
              f"{r['manba'][:20]:<20} {r['matn'][:56]}")
        print(f"            {r['formula']}")
    if not yuqori:
        print("    chegaradan o'tgan element yo'q - har manbadan ko'proq yig'ing yoki --min ni pasaytiring")
    if past:
        print(f"\n  ENG PAST ({1 / chegara:.2f}x va undan past) - nima ishlamadi")
        for r in quyi[:15]:
            print(f"    {r['karra']:5.2f}x  {r['korishlar']:>9,}  / {r['mediana']:>9,}   "
                  f"{r['manba'][:20]:<20} {r['matn'][:56]}")
    if kam:
        print(f"\n  {len(kam)} ta manba tashlandi (4 tadan kam element) - bir-ikki elementdan mediana chiqmaydi:")
        print("    " + ", ".join(f"{m} ({n})" for m, n in kam[:8]))
    sanoq = {}
    for r in yuqori:
        sanoq[r["formula"]] = sanoq.get(r["formula"], 0) + 1
    if sanoq:
        print("\n  yuqori natijalardagi formulalar")
        for f, n in sorted(sanoq.items(), key=lambda x: -x[1]):
            print(f"    {n:2d}x  {f}")
    print()


if __name__ == "__main__":
    main()
