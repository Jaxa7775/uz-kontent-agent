#!/usr/bin/env python3
"""sarlavha.py - sarlavha va muqova (prevyu) matnini joylashdan oldin tekshirish.

    python sarlavha.py --sarlavha "..." --muqova "3 SO'Z"                  # YouTube (standart)
    python sarlavha.py --platforma reels --sarlavha "..." --muqova "..."    # Reels/Shorts/TikTok
    python sarlavha.py --platforma telegram --fayl post.txt [--rasm]        # Telegram post
    python sarlavha.py sarlavhalar.txt                                      # har qatorda bittasi
    python sarlavha.py --json ...

Birlik - sarlavha emas, SARLAVHA + MUQOVA juftligi. Muqova sarlavhani takrorlasa, bosish maydonining
yarmi bekor ketadi - eng ko'p uchraydigan xato shu.

Uzunlik cheklovlari: YouTube sarlavhasi 100 belgigacha. Qidiruv va lentada qancha ko'rinishi
qurilmaga bog'liq; bu yerda taxminiy chegaralar ishlatiladi (kompyuter ~60, telefon ~40).
Telegram: matnli xabar 4096 belgi, rasm/video izohi oddiy akkauntda 1024 belgi. Bildirishnoma va
kanal ro'yxatida asosan birinchi qator ko'rinadi.
"""
import json, os, re, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

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


def sozlar(t):
    return [w.strip("'") for w in re.findall(r"[a-z0-9']+", tozala(t)) if w.strip("'")]
# -------------------------------------------------------------------------------------------------

PLATFORMA = {
    "youtube":  {"qattiq": 100, "yumshoq": 60, "telefon": 40, "nomi": "YouTube sarlavhasi"},
    "reels":    {"qattiq": 2200, "yumshoq": 60, "telefon": 40, "nomi": "Reels/Shorts/TikTok izohining birinchi qatori"},
    "telegram": {"qattiq": 4096, "yumshoq": 60, "telefon": 40, "nomi": "Telegram postining birinchi qatori"},
}
NOANIQ = {"ajoyib", "zo'r", "zo'rr", "super", "mega", "dahshat", "dahshatli", "hayratlanarli",
          "sehrli", "mukammal", "ideal", "shok", "bomba", "top", "eng", "juda", "rosa", "sirli",
          "maxfiy", "hamma", "hammasi", "barcha"}
TOXTASH = {"va", "bilan", "uchun", "bu", "shu", "u", "bir", "ham", "esa", "eng", "juda", "siz",
           "sizning", "men", "mening", "biz", "qanday", "nima", "nega", "qilib", "qilish", "orqali",
           "haqida", "yoki", "yangi", "video", "salom", "do'stlar", "bugun", "bugungi", "mana"}
TOLDIRUVCHI = {"salom", "assalomu", "alaykum", "do'stlar", "hurmatli", "bugun", "bugungi", "yangi",
               "video", "mana", "xullas", "endi", "bu", "shu", "eng"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def tutuq_turlari(t):
    return sorted({m.group(1) for m in re.finditer(r"[oOgG]([" + re.escape(APOS) + "'])", t)})


def yozuv_aralash(t):
    """Kirill matn ichida kichik harfli lotin so'zlar (brend nomlari bosh harfli, ular hisobga olinmaydi)."""
    kir = len(re.findall(r"[Ѐ-ӿ]{2,}", t))
    lot = len([w for w in re.findall(r"\b[A-Za-z']{2,}\b", t) if w[0].islower()])
    return kir > 0 and lot > 0


def tekshir(sarlavha, muqova=None, platforma="youtube"):
    p = PLATFORMA[platforma]
    t = sarlavha.strip()
    n = len(t)
    xato, yaxshi, eslatma = [], [], []
    if n > p["qattiq"]:
        xato.append(("uzunlik", f"{n} belgi - {p['nomi']} uchun qat'iy chegara {p['qattiq']}"))
    elif n > p["yumshoq"]:
        xato.append(("uzunlik", f"{n} belgi - kompyuterda taxminan {p['yumshoq']} belgidan keyin kesiladi"))
    else:
        yaxshi.append(f"{n} belgi, taxminiy {p['yumshoq']} belgilik chegaradan ichkarida")
    if n > p["telefon"]:
        bosh = t[:p["telefon"]].rsplit(" ", 1)[0]
        eslatma.append(f'telefonda taxminan "{bosh}..." ko\'rinadi - asosiy so\'z shu qismda qolganini tekshiring')
    katta = [w for w in t.split() if len(w) > 2 and w.isupper() and re.search(r"[^\W\d_]", w)]
    if len(katta) > 2:
        xato.append(("baqiriq", f"{len(katta)} ta KATTA HARFLI so'z - ikkitadan oshsa spamga o'xshaydi"))
    elif katta:
        yaxshi.append(f"{len(katta)} ta katta harfli so'z urg'u uchun")
    w = sozlar(t)
    noaniq = sorted({x for x in w if x in NOANIQ})
    if noaniq:
        xato.append(("noaniq", f"{', '.join(noaniq)} - raqam, nom yoki sana bilan almashtiring"))
    raqamlar = re.findall(r"\d[\d,.]*%?", t)
    nomlar = [x for x in re.findall(r"[^\W\d_][\w'’ʻ]*", lotinla(t))[1:] if x[:1].isupper() and not x.isupper()]
    if raqamlar:
        yaxshi.append(f"aniq raqam bor ({', '.join(raqamlar[:3])})")
    elif nomlar:
        yaxshi.append(f"nomlangan narsa bor ({', '.join(nomlar[:3])})")
    else:
        xato.append(("raqamsiz", "raqam, sana yoki nom yo'q - eng ishonchli bitta tuzatish"))
    if t.endswith("?"):
        yaxshi.append("sarlavhada ochiq savol")
    bosh3 = w[:3]
    if bosh3 and all(x in TOLDIRUVCHI for x in bosh3):
        xato.append(("boshi-bo'sh", "birinchi uch so'z bo'sh - asosiy so'zni oldinga suring"))
    tur = tutuq_turlari(t + " " + (muqova or ""))
    if len(tur) > 1:
        xato.append(("tutuq", f"tutuq belgilari aralash ({' '.join(tur)}) - bittasini tanlang, qidiruvda farq qilishi mumkin"))
    if yozuv_aralash(t):
        xato.append(("yozuv", "lotin va kirill aralashgan - bitta yozuvni tanlang"))
    if platforma == "youtube" and len(EMOJI.findall(t)) > 2:
        xato.append(("emoji", "sarlavhada ikkitadan ko'p emoji - joy so'zlar uchun kerak"))
    if muqova:
        sw = set(sozlar(t)) - TOXTASH
        mw = set(sozlar(muqova)) - TOXTASH
        # o'zbek tilida qo'shimchalar ko'p: "excel" va "excelda" bir so'z deb hisoblanadi
        umumiy = sorted({m for m in mw for s in sw if m[:5] == s[:5] and len(m) >= 3 and len(s) >= 3})
        if umumiy:
            xato.append(("takror", f"muqova sarlavhani takrorlaydi ({', '.join(umumiy)}) - muqova sarlavha aytmaganini aytsin"))
        else:
            yaxshi.append("muqova va sarlavha turli so'zlardan iborat")
        if len(sozlar(muqova)) > 3:
            xato.append(("muqova-uzun", f"muqovada {len(sozlar(muqova))} so'z - lenta o'lchamida uchtadan ortig'i o'qilmaydi"))
    return {"sarlavha": t, "belgi": n, "baho": baholash(xato, yaxshi), "xatolar": xato,
            "yaxshi": yaxshi, "eslatma": eslatma}


def baholash(xato, yaxshi):
    b = 100 - 12 * len(xato) + 4 * len(yaxshi)
    return max(0, min(100 if not xato else 95, b))


def telegram_post(matn, rasm=False):
    matn = matn.strip("\n")
    birinchi = matn.splitlines()[0] if matn else ""
    r = tekshir(birinchi, None, "telegram")
    r["sarlavha"] = birinchi
    chegara = 1024 if rasm else 4096
    n = len(matn)
    if n > chegara:
        r["xatolar"].append(("post-uzun", f"post {n} belgi - {'rasm izohi' if rasm else 'matnli xabar'} uchun chegara {chegara}"))
    else:
        r["yaxshi"].append(f"post {n} belgi, {chegara} chegaradan ichkarida")
    uzun = [p for p in re.split(r"\n\s*\n", matn) if len(p) > 600]
    if uzun:
        r["xatolar"].append(("devor", f"{len(uzun)} ta xatboshi 600 belgidan uzun - telefonda devor bo'lib ko'rinadi, bo'ling"))
    r["post_belgi"] = n
    r["baho"] = baholash(r["xatolar"], r["yaxshi"])
    return r


def korsat(r):
    print(f'\n  "{r["sarlavha"]}"')
    print(f"  {r['belgi']} belgi   baho {r['baho']}/100")
    for k, m in r["xatolar"]:
        print(f"    x   {k:<12} {m}")
    for m in r["yaxshi"]:
        print(f"    ok               {m}")
    for m in r.get("eslatma", []):
        print(f"    i                {m}")


def olish(a, kalit):
    if kalit in a:
        i = a.index(kalit)
        v = a[i + 1] if i + 1 < len(a) else None
        del a[i:i + 2]
        return v
    return None


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    rasm = "--rasm" in a
    a = [x for x in a if x != "--rasm"]
    platforma = (olish(a, "--platforma") or "youtube").lower()
    if platforma in ("shorts", "tiktok", "instagram", "reel"):
        platforma = "reels"
    if platforma not in PLATFORMA:
        print(f"noma'lum platforma: {platforma} (youtube | reels | telegram)"); sys.exit(1)
    muqova = olish(a, "--muqova")
    sarlavha = olish(a, "--sarlavha")
    fayl = olish(a, "--fayl")
    matn = olish(a, "--matn")
    if platforma == "telegram" and (fayl or matn):
        if fayl:
            with open(fayl, encoding="utf-8-sig", errors="replace") as f:
                matn = f.read()
        natija = [telegram_post(matn, rasm)]
    elif sarlavha:
        natija = [tekshir(sarlavha, muqova, platforma)]
    elif a and os.path.exists(a[0]):
        with open(a[0], encoding="utf-8-sig", errors="replace") as f:
            natija = [tekshir(l, muqova, platforma) for l in f.read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1)
    natija.sort(key=lambda r: -r["baho"])
    if as_json:
        print(json.dumps(natija, ensure_ascii=False, indent=1)); return
    for r in natija:
        korsat(r)
    print()


if __name__ == "__main__":
    main()
