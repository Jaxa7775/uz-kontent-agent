#!/usr/bin/env python3
"""montaj.py - vaqt belgili transkriptdan montaj ro'yxati (EDL).

    python montaj.py transkript.srt                    # .srt, .vtt yoki whisper .json
    python montaj.py transkript.srt --chegara 0.35 --json
    python montaj.py transkript.srt --himoya 1:20-2:05 --himoya 5:00-5:40

Uch narsani topadi va kesishlar ro'yxatini chiqaradi:
  JIM      gapirilgan qatorlar orasidagi chegaradan uzun pauza (o'rtasidan kesiladi, ikki tomonda
           nafas qoladi)
  PARAZIT  faqat "ee", "xullas", "ya'ni", "koroche" kabi so'zlardan iborat qator
  TAKROR   qayta boshlangan gap - bir xil boshlanishning birinchi urinishi

--himoya: ekran yozuvidagi jim namoyish qismlari (sichqoncha bilan ish ko'rsatilayotgan joy). Shu
oraliqqa tegadigan kesishlar tashlab yuboriladi. Darslarda bu muhim: jimlik har doim ham bo'sh joy
emas.

YouTube avtomatik subtitrlaridagi "aylanma" qatorlar (har qator oldingisini takrorlaydi) va <c> kabi
teglar tozalanadi, aks holda har bir qator soxta TAKROR bo'lib chiqardi.

NIMA QILMAYDI. Faylni kesmaydi va mediaga tegmaydi. Ro'yxat, jami kesiladigan vaqt va natijaviy
uzunlikni chiqaradi - kesishni o'zingiz montaj dasturida qilasiz.
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
# -------------------------------------------------------------------------------------------------

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


def yukla(yol):
    """[(boshi, oxiri, matn)] qaytaradi. Aylanma subtitr qatorlari va teglar tozalanadi."""
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

PARAZIT = ["e+", "ee+", "eh+", "m+", "mm+", "a+", "aa+", "xm+", "hm+", "ha", "xo'sh", "xullas",
           "ya'ni", "yani", "endi", "mana", "qisqasi", "demak", "bilasizmi", "tushunyapsizmi",
           "shunaqa", "haligi", "anu", "nima edi", "nima deyishim kerak", "koroche", "tipa", "vot",
           "nu", "eto", "kak bi", "okey", "ok", "xop", "xo'p"]
FAQAT_PARAZIT = re.compile(r"^[\s,.!?…-]*(?:(?:" + "|".join(PARAZIT) + r")[\s,.!?…-]*)+$")
IZOH = re.compile(r"^\s*[\[(].*[\])]\s*$")   # [musiqa], (qarsaklar)


def parazitmi(t):
    return bool(FAQAT_PARAZIT.match(tozala(t)))


def nutqmi(t):
    return bool(t.strip()) and not parazitmi(t) and not IZOH.match(t)


def norm(t):
    return re.sub(r"[^a-z' ]", "", tozala(t)).split()


def oraliq(s):
    a, b = s.split("-", 1)
    return vaqt(a), vaqt(b)


def birlashtir(kesishlar):
    jami, oxiri = 0.0, None
    for k in sorted(kesishlar, key=lambda c: c["boshi"]):
        if oxiri is None or k["boshi"] > oxiri:
            jami += k["oxiri"] - k["boshi"]
            oxiri = k["oxiri"]
        elif k["oxiri"] > oxiri:
            jami += k["oxiri"] - oxiri
            oxiri = k["oxiri"]
    return jami


def mmss(t):
    t = max(0, t)
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:05.2f}"


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    chegara, himoya = 0.45, []
    while "--chegara" in a:
        i = a.index("--chegara"); chegara = float(a[i + 1]); del a[i:i + 2]
    while "--himoya" in a:
        i = a.index("--himoya"); himoya.append(oraliq(a[i + 1])); del a[i:i + 2]
    if not a or not os.path.exists(a[0]):
        print(__doc__); sys.exit(1)
    qatorlar = yukla(a[0])
    if not qatorlar:
        print("qator topilmadi - bu srt, vtt yoki whisper json faylimi?"); sys.exit(1)
    uzunlik = max(q[1] for q in qatorlar)
    kesish = []
    for i, (s, e, t) in enumerate(qatorlar):
        if parazitmi(t):
            kesish.append({"tur": "PARAZIT", "boshi": s, "oxiri": e, "sabab": t.strip()[:48]})
        if i:
            pauza = s - qatorlar[i - 1][1]
            if pauza > chegara:
                qol = chegara / 2
                kesish.append({"tur": "JIM", "boshi": round(qatorlar[i - 1][1] + qol, 3),
                               "oxiri": round(s - qol, 3), "sabab": f"{pauza:.2f} s pauza"})
        # Qayta boshlash oxirgi HAQIQIY nutq qatori bilan solishtiriladi: ko'p dubllar orasida "ee" bor.
        if nutqmi(t):
            j = i - 1
            while j >= 0 and not nutqmi(qatorlar[j][2]):
                j -= 1
            if j >= 0:
                x, y = norm(qatorlar[j][2]), norm(t)
                k = min(4, len(x), len(y))
                if k >= 3 and x[:k] == y[:k]:
                    kesish.append({"tur": "TAKROR", "boshi": qatorlar[j][0], "oxiri": qatorlar[j][1],
                                   "sabab": f'"{" ".join(x[:k])}" qayta boshlandi'})
    kesish = [c for c in kesish if c["oxiri"] > c["boshi"]]
    tashlandi = 0
    if himoya:
        oldin = len(kesish)
        kesish = [c for c in kesish if not any(c["boshi"] < hb and c["oxiri"] > ha for ha, hb in himoya)]
        tashlandi = oldin - len(kesish)
    kesish.sort(key=lambda c: c["boshi"])
    olinadi = birlashtir(kesish)
    if as_json:
        print(json.dumps({"manba": a[0], "uzunlik": round(uzunlik, 3), "kesishlar": kesish,
                          "olinadi": round(olinadi, 3), "natija": round(uzunlik - olinadi, 3),
                          "himoya_sababli_tashlandi": tashlandi}, ensure_ascii=False, indent=1))
        return
    print(f"\n  {a[0]}   {mmss(uzunlik)} uzunlik, {len(qatorlar)} qator, pauza chegarasi {chegara} s\n")
    for c in kesish:
        print(f"    {c['tur']:<8} {mmss(c['boshi']):>9} -> {mmss(c['oxiri']):>9}   "
              f"{c['oxiri'] - c['boshi']:5.2f} s   {c['sabab']}")
    foiz = olinadi / uzunlik * 100 if uzunlik else 0
    print(f"\n  {len(kesish)} ta kesish, {olinadi:.2f} s olinadi, natija {mmss(uzunlik - olinadi)} "
          f"({foiz:.1f}% qisqaroq)")
    if tashlandi:
        print(f"  himoyalangan oraliqlar sababli {tashlandi} ta kesish tashlab yuborildi")
    print("  Bu NUTQ bo'yicha hisob. Jim namoyish qismlari bo'lsa, ularni --himoya bilan belgilang.\n")


if __name__ == "__main__":
    main()
