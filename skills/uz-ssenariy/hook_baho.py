#!/usr/bin/env python3
"""hook_baho.py - o'zbekcha hook (birinchi gap)ni yozib olishdan oldin baholash.

    python hook_baho.py --hook "bitta gap"
    python hook_baho.py hooklar.txt              # har qatorda bitta hook, saralab chiqaradi
    python hook_baho.py --json hooklar.txt
    python hook_baho.py --min 5 --max 16 hooklar.txt   # qisqalik oralig'ini o'zgartirish

Lotin va kirill yozuvini, hamda ' ʻ ’ ` kabi turli tutuq belgilarini tushunadi.

Beshta xususiyat (har biri 0-100) va umumiy baho: 60% o'rtacha + 40% eng zaif xususiyat. Eng zaifiga
og'irlik ataylab berilgan: to'rtta kuchli va bitta o'lik xususiyatli hook aynan o'lik joyidan
"oqadi", o'rtacha esa buni yashiradi.

BU NIMA EMAS. Bu so'zlarga qarab hisoblanadigan taxminiy baho, bashorat emas. U hech qanday real
statistika bo'yicha kalibrlanmagan. Past ball - qayta qarash uchun sabab; yuqori ball - va'da emas.
Eng ishonchli o'lchov - o'z videolaringizning retention grafigi (uz-tahlil).
"""
import json, os, re, sys

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
    """Kirilldan lotinga (o'zbek). Lotin matnga tegmaydi."""
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


RAQAM = re.compile(r"\d+(?:[.,]\d+)?")
MUROJAAT = re.compile(
    r"\b(siz|sizning|sizga|sizni|sizda|sizdan|sizlar|sen|sening|senga|seni|o'zingiz\w*)\b"
    r"|\b\w{2,}(ingiz|ingizni|ingizda|ingizga|ingizdan|yapsiz|yapsizmi|dingiz|dingizmi|gansiz|"
    r"gansizmi|asizmi|aysizmi|asiz|aysiz)\b"
    r"|\b\w{2,}(?<!n)ing\b|\b\w{2,}lang\b")
MUROJAAT_EMAS = {"ming", "ring", "qiyin", "boring"}
XAVF = re.compile(
    r"\b(yo'qot|behuda|xato|zarar|to'xtat|bekor|buzil|buzad|o'chib|o'chirib|xavf|jarima|aldan|"
    r"aldov|virus|xaker|o'g'irla|pul|vaqt|afsus|muammo|qotib|sekin|tejay|tejash)\w*"
    r"|\b\w{2,}(mang|mangiz)\b")
QIZIQISH = re.compile(
    r"\b(nega|nimaga|nimadan|qanday|qanaqa|qaysi|nima|kim|qachon|hech kim|hech qachon|ko'pchilik|"
    r"faqat|lekin|ammo|biroq|aslida|haqiqatda|hatto|bilmaysiz|bilmagan|yashirin|sir|sabab|bitta)\b"
    # so'roq qo'shimchasi fe'lda: qolyaptimi, bilasizmi, ishlaydimi ("hajmi" kabi otlar emas)
    r"|\b\w+(siz|di|ti|dingiz|gan|man|miz)(mi|mikan)\b|\b(bormi|yo'qmi|kerakmi|mumkinmi)\b")
YOPIQ = re.compile(r"\b(chunki|shuning uchun|sababi|ya'ni|demak)\b")
NOANIQ = re.compile(
    r"\b(ajoyib|zo'r|zo'rr|super|mega|dahshat|dahshatli|hayratlanarli|sehrli|mukammal|ideal|"
    r"juda|rosa|shok|bomba|top|aql bovar qilmaydigan|gap yo'q|eng zo'r)\b")
TOLDIRUVCHI = {"assalomu", "alaykum", "salom", "do'stlar", "hurmatli", "obunachilar", "kanal",
               "kanalimga", "kanalimizga", "obuna", "layk", "video", "videoda", "videoni", "bugun",
               "bugungi", "xullas", "ya'ni", "yani", "endi", "mana", "qisqasi", "demak", "haligi"}


def nomlar_soni(t):
    """Gap boshida turmagan bosh harfli so'zlar - nomlangan narsalar (Excel, Windows, Claude...)."""
    n = 0
    for gap in re.split(r"[.!?]+\s*", lotinla(t)):
        tok = re.findall(r"[^\W\d_][\w'’ʻ]*", gap)
        n += sum(1 for w in tok[1:] if w[:1].isupper())
    return n


def aniqlik(t):
    tz = tozala(t)
    w = sozlar(t)
    if not w:
        return 0
    s = 30 + 20 * min(3, len(RAQAM.findall(t))) + min(30, 15 * nomlar_soni(t))
    s -= 15 * len(NOANIQ.findall(tz)) + 5 * sum(1 for x in w if x in TOLDIRUVCHI)
    return max(0, min(100, s))


def murojaat_topilmalar(tz):
    return [m.group(0) for m in MUROJAAT.finditer(tz) if m.group(0) not in MUROJAAT_EMAS]


def murojaat(t):
    tz = tozala(t)
    n = len(murojaat_topilmalar(tz))
    bosh = 25 if murojaat_topilmalar(" ".join(tz.split()[:5])) else 0
    return max(0, min(100, 25 + 20 * n + bosh))


def xavf(t):
    tz = tozala(t)
    return max(0, min(100, 20 + 25 * len(XAVF.findall(tz)) + (10 if RAQAM.search(t) else 0)))


def qiziqish(t):
    tz = tozala(t)
    s = 30 + 15 * len(QIZIQISH.findall(tz)) + (15 if "?" in t else 0)
    s -= 20 if YOPIQ.search(tz) else 0
    return max(0, min(100, s))


def qisqalik_fn(lo, hi):
    def qisqalik(t):
        n = len(sozlar(t))
        if n == 0:
            return 0
        if lo <= n <= hi:
            return 100
        if n < lo:
            return max(30, 100 - (lo - n) * 12)
        return max(10, 100 - (n - hi) * 7)
    return qisqalik


TUZATISH = {
    "ANIQLIK": "bitta sifatni raqam, nom yoki sana bilan almashtiring",
    "MUROJAAT": "birinchi besh so'zda 'siz' deng yoki fe'lni sizga qarating (qiling, ko'ring)",
    "XAVF": "hozirgi usulda davom etsa nima yo'qotishini ayting (vaqt, pul, fayl)",
    "QIZIQISH": "gapning o'zi javob beradigan yarmini olib tashlang ('chunki...' qismini)",
    "QISQALIK": "ovoz chiqarib o'qing va nafasingiz tugagan joyda to'xtating",
}


def formulalar():
    yol = os.path.join(HERE, "formulalar.json")
    if not os.path.exists(yol):
        return []
    with open(yol, encoding="utf-8") as f:
        return json.load(f)["formulalar"]


def aniqla(t, formulas):
    tz = tozala(t).strip()
    eng, soni = None, 0
    for f in formulas:
        n = sum(1 for p in f["naqsh"] if re.search(p, tz))
        if n > soni:
            eng, soni = f, n
    return (eng["nomi"] if eng else "Aniqlanmadi"), soni


def bahola(t, props, formulas):
    qism = {nom: fn(t) for nom, fn in props}
    v = list(qism.values())
    umumiy = round(0.6 * (sum(v) / len(v)) + 0.4 * min(v))
    nomi, soni = aniqla(t, formulas)
    return qism, umumiy, nomi, soni


def daraja(v):
    return "KUCHLI" if v >= 62 else "ISHLAYDI" if v >= 45 else "ZAIF"


def chiqar(r):
    t = r["hook"]
    print(f"\n  {t}")
    print(f"  {'-' * min(72, max(20, len(t)))}")
    for k, v in r["xususiyatlar"].items():
        print(f"    {k:<10} {v:3d}  {'#' * (v // 5)}")
    print(f"    {'UMUMIY':<10} {r['baho']:3d}  {r['daraja']}")
    if r["mos"]:
        print(f"    formula    {r['formula']}  ({r['mos']} ta naqsh mos keldi)")
    else:
        print(f"    formula    {r['formula']}  (hech bir formula mos kelmadi - bu odatda hook emas, xulosa)")
    zaif = min(r["xususiyatlar"], key=r["xususiyatlar"].get)
    print(f"    eng zaif   {zaif} - {TUZATISH[zaif]}")


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    lo, hi = 6, 20
    if "--min" in a:
        i = a.index("--min"); lo = int(a[i + 1]); del a[i:i + 2]
    if "--max" in a:
        i = a.index("--max"); hi = int(a[i + 1]); del a[i:i + 2]
    if "--hook" in a:
        qatorlar = [a[a.index("--hook") + 1]]
    elif a and os.path.exists(a[0]):
        with open(a[0], encoding="utf-8-sig", errors="replace") as f:
            qatorlar = [l for l in f.read().splitlines() if l.strip()]
    else:
        print(__doc__)
        sys.exit(1 if a else 0)
    props = [("ANIQLIK", aniqlik), ("MUROJAAT", murojaat), ("XAVF", xavf),
             ("QIZIQISH", qiziqish), ("QISQALIK", qisqalik_fn(lo, hi))]
    formulas = formulalar()
    natija = []
    for t in qatorlar:
        qism, umumiy, nomi, soni = bahola(t, props, formulas)
        natija.append({"hook": t.strip(), "xususiyatlar": qism, "baho": umumiy,
                       "daraja": daraja(umumiy), "formula": nomi, "mos": soni,
                       "sozlar": len(sozlar(t))})
    natija.sort(key=lambda r: -r["baho"])
    if as_json:
        print(json.dumps(natija, ensure_ascii=False, indent=1))
        return
    for r in natija:
        chiqar(r)
    if len(natija) > 1:
        print(f"\n  g'olib: {natija[0]['hook']}  ({natija[0]['baho']}, {natija[0]['daraja']})")
    print()


if __name__ == "__main__":
    main()
