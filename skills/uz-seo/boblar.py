#!/usr/bin/env python3
"""boblar.py - transkriptdan YouTube boblari (timestamps / chapters).

    python boblar.py transkript.srt              # .srt, .vtt yoki whisper .json
    python boblar.py transkript.srt --soni 8 --json

Video tavsifiga to'g'ridan-to'g'ri qo'yiladigan blok chiqaradi. YouTube qoidalari taxmin qilinmaydi,
tekshiriladi: ro'yxat 0:00 dan boshlanishi, kamida uchta bob bo'lishi va har bir bob kamida 10
soniya bo'lishi kerak. Shulardan birini buzgan blok indamay bob bo'lmay qoladi.

Chegaralar pauzalardan topiladi: pauza qancha uzun va undan oldin/keyin so'zlar qancha o'zgarsa,
shuncha yaxshi chegara. Sarlavhalar - mavzu so'zlari, qoralama. Ularni o'z so'zlaringiz bilan qayta
yozing.
"""
import json, os, re, sys
from collections import Counter

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

TOXTASH = set("""va bilan uchun bu shu u biz siz men sen ular bir ham esa emas edi ekan bo'ladi bo'lsa
qilib qiladi qilamiz qilsak qilsangiz kerak mumkin endi mana xullas ya'ni yani lekin ammo yoki agar
keyin oldin hozir juda eng yana faqat hamma har nima qanday qaysi kim nega bor yo'q shunday bunday
biroz ichida orqali kabi deb dedi degan bo'lib bo'lgan qilgan boshqa o'sha bizning sizning mening
uning ularning shuning chunki ana xo'sh okey koroche tipa ikki uch to'rt besh birinchi ikkinchi
mana bu yerda yerga shunaqa haligi bilasizmi ko'ramiz qaraymiz bosamiz kiramiz ochamiz""".split())
MIN = 10.0


def kalitlar(matn):
    return [w for w in re.findall(r"[a-z'][a-z']{3,}", tozala(matn)) if w.strip("'") not in TOXTASH]


def ildiz(w):
    # o'zbek tilida qo'shimcha ko'p: "kompyuter", "kompyuterni", "kompyuterda" bitta ildiz
    return w.strip("'")[:6]


def mmss(t):
    t = int(t)
    h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    soni = 7
    if "--soni" in a:
        i = a.index("--soni"); soni = int(a[i + 1]); del a[i:i + 2]
    if not a or not os.path.exists(a[0]):
        print(__doc__); sys.exit(1)
    q = yukla(a[0])
    if len(q) < 6:
        print("bob qilish uchun qatorlar juda kam"); sys.exit(1)
    uzunlik = max(x[1] for x in q)
    nomzod = []
    for i in range(1, len(q)):
        pauza = max(0.0, q[i][0] - q[i - 1][1])
        oldin = {ildiz(w) for w in kalitlar(" ".join(c[2] for c in q[max(0, i - 10):i]))}
        keyin = {ildiz(w) for w in kalitlar(" ".join(c[2] for c in q[i:i + 10]))}
        birlashma = oldin | keyin
        siljish = 1 - len(oldin & keyin) / len(birlashma) if birlashma else 0
        nomzod.append((pauza * 1.5 + siljish * 3.0, q[i][0]))
    nomzod.sort(reverse=True)
    tanlangan = [0.0]
    for _, t in nomzod:
        if len(tanlangan) >= soni:
            break
        if all(abs(t - p) >= MIN for p in tanlangan) and uzunlik - t >= MIN:
            tanlangan.append(t)
    tanlangan.sort()
    boblar = []
    for n, t in enumerate(tanlangan):
        oxiri = tanlangan[n + 1] if n + 1 < len(tanlangan) else uzunlik
        matn = " ".join(c[2] for c in q if c[0] >= t and c[0] < oxiri)
        sozlar = kalitlar(matn)
        sanoq = Counter(ildiz(w) for w in sozlar)
        shakl = {}
        for w in sozlar:
            shakl.setdefault(ildiz(w), Counter())[w.strip("'")] += 1
        sarlavha = " ".join(shakl[r].most_common(1)[0][0].capitalize() for r, _ in sanoq.most_common(3)) or "Bo'lim"
        boblar.append({"boshi": round(t, 2), "belgi": mmss(t), "qoralama": sarlavha,
                       "soniya": round(oxiri - t, 2)})
    sabab = []
    if len(boblar) < 3:
        sabab.append("kamida 3 ta bob kerak")
    if boblar and boblar[0]["boshi"] != 0:
        sabab.append("birinchi bob 0:00 bo'lishi kerak")
    qisqa = [b["belgi"] for b in boblar if b["soniya"] < MIN]
    if qisqa:
        sabab.append(f"10 soniyadan qisqa bob: {', '.join(qisqa)}")
    if as_json:
        print(json.dumps({"yaroqli": not sabab, "sabablar": sabab, "boblar": boblar},
                         ensure_ascii=False, indent=1))
        return
    print()
    for b in boblar:
        print(f"  {b['belgi']} {b['qoralama']}")
    holat = "yaroqli" if not sabab else "YAROQSIZ: " + "; ".join(sabab)
    print(f"\n  {len(boblar)} ta bob - {holat}")
    print("  Har bir qatorni qayta nomlang: bu mavzu so'zlari, sizning so'zlaringiz emas.\n")


if __name__ == "__main__":
    main()
