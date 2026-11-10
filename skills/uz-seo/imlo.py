#!/usr/bin/env python3
"""imlo.py - o'zbekcha yozuv vositalari: qidiruv variantlari, lotin-kirill, hashtag, tekshiruv.

    python imlo.py --variant "o'qituvchi uchun Excel"     # odamlar qidiruvga yozadigan variantlar
    python imlo.py --kirill "Kompyuterni tezlashtirish"   # lotin -> kirill
    python imlo.py --lotin "Компьютерни тезлаштириш"      # kirill -> lotin
    python imlo.py --teg "excel darslari" "o'qituvchi"    # hashtaglar (tutuq belgisisiz)
    python imlo.py --tekshir post.txt                     # tutuq belgisi va yozuv aralashuvi

Nega kerak: bir so'zni odamlar o'qituvchi, o`qituvchi, oʻqituvchi, oqituvchi va ўқитувчи deb
yozadi. Bular qidiruvda turli natija berishi mumkin. Hashtagda esa tutuq belgisi ishlamaydi:
#o'qituvchi aslida #o bo'lib qoladi.

Cheklovlar: lotin -> kirill o'girishda ruscha o'zlashma so'zlar (kompyuter -> компьютер, sentyabr ->
сентябрь) yumshoq belgisiz chiqadi; "ts" har doim "тс" bo'ladi. C, W kabi o'zbek alifbosida yo'q
harfli so'zlar (Excel, Word, Windows) o'zgarishsiz qoldiriladi. Natijani bir ko'zdan kechiring.
"""
import os, re, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

APOS = "ʻʼ‘’`´"
KIR = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "j", "з": "z",
       "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
       "с": "s", "т": "t", "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh",
       "ъ": "'", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya", "ў": "o'", "қ": "q", "ғ": "g'",
       "ҳ": "h"}
UNLI = set("аеёиоуэюяўaeiou")
LAT = {"a": "а", "b": "б", "d": "д", "f": "ф", "g": "г", "h": "ҳ", "i": "и", "j": "ж", "k": "к",
       "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т",
       "u": "у", "v": "в", "x": "х", "y": "й", "z": "з"}
SAQLA = {"youtube", "tiktok", "google", "chatgpt", "claude", "gemini", "android", "iphone", "ios",
         "pdf", "usb", "wi-fi", "wifi", "ai"}


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


def apos_norm(t):
    for a in APOS:
        t = t.replace(a, "'")
    return t


# ruscha o'zlashma so'zlar: kirillda yumshoq belgi bilan yoziladi (so'z boshi bo'yicha)
OZLASHMA = {"kompyuter": "компьютер", "film": "фильм", "yanvar": "январь", "fevral": "февраль",
            "aprel": "апрель", "iyun": "июнь", "iyul": "июль", "sentyabr": "сентябрь",
            "oktyabr": "октябрь", "noyabr": "ноябрь", "dekabr": "декабрь"}


def soz_kirill(w):
    lo = w.lower()
    if lo in SAQLA or re.search(r"c(?!h)|w", lo):
        return w
    for k, v in OZLASHMA.items():
        if lo.startswith(k):
            return moslash(w, v + soz_kirill(lo[len(k):]) if len(lo) > len(k) else v)
    res, i, n = [], 0, len(lo)
    while i < n:
        c, nx = lo[i], lo[i + 1] if i + 1 < n else ""
        if c in "og" and nx == "'":
            r, i = ("ў" if c == "o" else "ғ"), i + 2
        elif c == "s" and nx == "h":
            r, i = "ш", i + 2
        elif c == "c" and nx == "h":
            r, i = "ч", i + 2
        elif c == "y" and nx in "aoue":
            if nx == "o" and i + 2 < n and lo[i + 2] == "'":
                r, i = "й", i + 1                      # yo'q -> йўқ
            else:
                r, i = {"a": "я", "o": "ё", "u": "ю", "e": "е"}[nx], i + 2
        elif c == "e":
            r, i = ("э" if i == 0 else "е"), i + 1
        elif c == "'":
            r, i = "ъ", i + 1
        else:
            r, i = LAT.get(c, c), i + 1
        res.append(r)
    return moslash(w, "".join(res))


def moslash(w, out):
    """Asl so'zning katta-kichik harfini natijaga ko'chirish."""
    if len(w) > 1 and w.isupper():
        return out.upper()
    if w[:1].isupper():
        return out[:1].upper() + out[1:]
    return out


def kirillla(t):
    t = apos_norm(t)
    return re.sub(r"[A-Za-z]+(?:'[A-Za-z]+)*", lambda m: soz_kirill(m.group(0)), t)


def variantlar(t):
    t = apos_norm(lotinla(t)).strip()
    v = []
    for belgi in ["'", "ʻ", "`", ""]:
        x = re.sub(r"([oOgG])'", lambda m: m.group(1) + belgi, t)
        if x not in v:
            v.append(x)
    k = kirillla(t)
    if k not in v:
        v.append(k)
    return v


def teg(t):
    lot = re.sub(r"[^\w]", "", apos_norm(lotinla(t)).replace("'", "")).lower()
    kir = re.sub(r"[^\w]", "", kirillla(apos_norm(lotinla(t)))).lower()
    # brend nomi lotincha qolgan bo'lsa, aralash hashtag yasamaymiz
    return ["#" + lot] + (["#" + kir] if kir != lot and not re.search(r"[a-z]", kir) else [])


def tekshir(matn):
    topildi = []
    for n, qator in enumerate(matn.splitlines(), 1):
        tur = sorted({m.group(1) for m in re.finditer(r"[oOgG]([" + re.escape(APOS) + "'])", qator)})
        kir = re.findall(r"[Ѐ-ӿ]{2,}", qator)
        lot = [w for w in re.findall(r"\b[A-Za-z']{2,}\b", qator) if w[0].islower()]
        if len(tur) > 1:
            topildi.append((n, f"tutuq belgilari aralash: {' '.join(tur)}"))
        if kir and lot:
            topildi.append((n, f"lotin va kirill aralash: {lot[0]} / {kir[0]}"))
        if re.search(r"#\w*[oOgG][" + re.escape(APOS) + "']", qator):
            topildi.append((n, "hashtagda tutuq belgisi - hashtag shu joyda uziladi"))
    butun = sorted({m.group(1) for m in re.finditer(r"[oOgG]([" + re.escape(APOS) + "'])", matn)})
    return topildi, butun


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    rejim, qolgan = a[0], a[1:]
    if rejim == "--variant" and qolgan:
        for t in qolgan:
            print(f"\n  {t}")
            for v in variantlar(t):
                print(f"    {v}")
        print()
    elif rejim == "--kirill" and qolgan:
        print(kirillla(" ".join(qolgan)))
    elif rejim == "--lotin" and qolgan:
        print(apos_norm(lotinla(" ".join(qolgan))))
    elif rejim == "--teg" and qolgan:
        for t in qolgan:
            print(f"  {t:<30} {'  '.join(teg(t))}")
    elif rejim == "--tekshir" and qolgan:
        matn = open(qolgan[0], encoding="utf-8-sig", errors="replace").read() if os.path.exists(qolgan[0]) else " ".join(qolgan)
        topildi, butun = tekshir(matn)
        print()
        for n, m in topildi:
            print(f"    {n:>4}-qator   {m}")
        if len(butun) > 1:
            print(f"\n  butun matnda {len(butun)} xil tutuq belgisi: {' '.join(butun)} - bittasini tanlang")
        if not topildi and len(butun) <= 1:
            print("  muammo topilmadi")
        print()
    else:
        print(__doc__); sys.exit(1)


if __name__ == "__main__":
    main()
