#!/usr/bin/env python3
"""navbatga.py - tasdiqlangan postni rejali joylash navbatiga qo'yish (GitHub Actions joylaydi).

    python navbatga.py post.txt --vaqt "2026-11-12 19:00"              # mahalliy vaqt
    python navbatga.py post.txt --vaqt "2026-11-12 19:00" --ovoz o.mp3  # --rasm / --fayl ham bo'ladi
    python navbatga.py post.txt --vaqt "..." --kanal '@boshqa' --ovozsiz
    python navbatga.py --toplam reja.json                              # ko'p postni bitta commit bilan
    python navbatga.py --royxat                                        # navbat, oxirgi joylanganlar, xatolar
    python navbatga.py --bekor <id>                                    # navbatdan olib tashlash

reja.json: [{"post": "yo'l/post.txt", "vaqt": "2026-11-12 09:00", "ovozsiz": false,
             "media": ["ovoz", "yo'l/o.mp3"] yoki null, "kanal": "@ixtiyoriy"}, ...]
To'plamda avval HAMMASI tekshiriladi; bittasi xato bo'lsa, hech biri navbatga qo'yilmaydi.

Sozlamalar ~/.claude/kontent-uz/telegram.json da:
    "navbat_papka": "D:/Dasturlar/kanal-navbat"   - navbat reposining kompyuterdagi nusxasi
    "vaqt_zonasi": "+05:00"                        - --vaqt shu zonada tushuniladi (Toshkent)

Navbatga qo'yish = joylashga tasdiq. Faqat foydalanuvchi aynan shu post va shu vaqtga "ha" degandan
keyin ishlating. Joylanmaguncha --bekor bilan olib tashlash mumkin.
GitHub har soatda (:07, UTC) tekshiradi; post rejalashtirilgan vaqtdan keyin taxminan 5-40 daqiqada chiqadi.
"""
import datetime, importlib.util, json, os, re, shutil, subprocess, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("joyla", os.path.join(HERE, "joyla.py"))
joyla = importlib.util.module_from_spec(spec)
spec.loader.exec_module(joyla)


def sozlama():
    c = {}
    if os.path.exists(joyla.SOZLAMA):
        with open(joyla.SOZLAMA, encoding="utf-8-sig") as f:
            c = json.load(f)
    papka = os.environ.get("NAVBAT_PAPKA") or c.get("navbat_papka")
    zona = os.environ.get("NAVBAT_ZONA") or c.get("vaqt_zonasi") or "+05:00"
    return (os.path.expanduser(papka) if papka else None), zona, joyla.kanal_nomi(c.get("kanal"))


def git_yoli():
    return shutil.which("git") or r"C:\Program Files\Git\cmd\git.exe"


def git(papka, *args, tekshir=True):
    if os.environ.get("NAVBAT_GITSIZ"):          # testlar uchun
        return ""
    p = subprocess.run([git_yoli(), "-C", papka, *args], capture_output=True)
    if tekshir and p.returncode != 0:
        raise SystemExit("git xatosi: " + p.stderr.decode("utf-8", "replace").strip())
    return p.stdout.decode("utf-8", "replace")


def zona_ol(z):
    m = re.fullmatch(r"([+-])(\d{2}):?(\d{2})", z)
    if not m:
        raise SystemExit(f"vaqt zonasi noto'g'ri: {z} (masalan +05:00)")
    d = datetime.timedelta(hours=int(m.group(2)), minutes=int(m.group(3)))
    return datetime.timezone(d if m.group(1) == "+" else -d)


def vaqt_ol(s, zona):
    s = s.strip().replace("T", " ")
    for f in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.datetime.strptime(s, f).replace(tzinfo=zona)
        except ValueError:
            pass
    raise SystemExit(f'vaqt tushunilmadi: "{s}" (masalan "2026-11-12 19:00")')


def slug(matn):
    birinchi = joyla.korinadigan(joyla.html_ga(matn)).strip().splitlines()[0] if matn.strip() else "post"
    s = re.sub(r"[^a-z0-9]+", "-", birinchi.lower().replace("'", "").replace("ʻ", ""))
    return s.strip("-")[:40] or "post"


def tekshir_element(post, vaqt, media, kanal, hozir):
    """Navbatga qo'yishdan oldingi tekshiruv. (matn, uzunlik, qadamlar) qaytaradi."""
    if not os.path.exists(post):
        raise SystemExit(f"post fayli topilmadi: {post}")
    if media and not os.path.exists(media[1]):
        raise SystemExit(f"fayl topilmadi: {media[1]}")
    if vaqt <= hozir + datetime.timedelta(minutes=5):
        raise SystemExit(f"{post}: vaqt kelajakda bo'lishi kerak (kamida 5 daqiqa keyin)")
    if not kanal:
        raise SystemExit("kanal yo'q: telegram.json dagi \"kanal\" yoki --kanal")
    with open(post, encoding="utf-8-sig", errors="replace") as f:
        matn = f.read().strip("\n")
    _, n, qadamlar = joyla.reja_tuz(matn, media)
    if n > joyla.MATN_CHEGARA:
        raise SystemExit(f"{post}: {n} belgi - {joyla.MATN_CHEGARA} dan uzun")
    return matn, n, qadamlar


def yarat(papka, zona, pid, post, vaqt, media, kanal, ovozsiz, hozir):
    manzil = os.path.join(papka, "navbat", pid)
    os.makedirs(manzil)
    shutil.copyfile(post, os.path.join(manzil, "post.txt"))
    meta = {"vaqt": vaqt.isoformat(timespec="minutes"), "kanal": kanal, "media": None,
            "ovozsiz": ovozsiz, "qoyildi": hozir.astimezone(zona).isoformat(timespec="seconds")}
    if media:
        nom = os.path.basename(media[1])
        shutil.copyfile(media[1], os.path.join(manzil, nom))
        meta["media"] = [media[0], nom]
    with open(os.path.join(manzil, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)


def toplam(reja_yoli, papka, zona, kanal_std):
    with open(reja_yoli, encoding="utf-8-sig") as f:
        reja = json.load(f)
    hozir = datetime.datetime.now(datetime.timezone.utc)
    git(papka, "pull", "--rebase", "-q")
    tayyor, idlar = [], set()
    for e in reja:                                     # 1) hammasini tekshirish
        vaqt = vaqt_ol(e["vaqt"], zona)
        media = tuple(e["media"]) if e.get("media") else None
        kanal = joyla.kanal_nomi(e.get("kanal")) or kanal_std
        matn, n, qadamlar = tekshir_element(e["post"], vaqt, media, kanal, hozir)
        pid = vaqt.strftime("%Y-%m-%d_%H%M") + "_" + slug(matn)
        if pid in idlar or os.path.exists(os.path.join(papka, "navbat", pid)):
            raise SystemExit(f"takroriy id: {pid}")
        idlar.add(pid)
        tayyor.append((pid, e["post"], vaqt, media, kanal, bool(e.get("ovozsiz")), n))
    for pid, post, vaqt, media, kanal, ovozsiz, _ in tayyor:   # 2) yaratish
        yarat(papka, zona, pid, post, vaqt, media, kanal, ovozsiz, hozir)
    git(papka, "add", "-A")
    git(papka, "commit", "-q", "-m", f"navbatga: {len(tayyor)} ta post")
    git(papka, "push", "-q")
    print(f"\n  ok navbatga {len(tayyor)} ta post qo'yildi ({zona_nomi(zona)})")
    for pid, _, vaqt, _, _, ovozsiz, n in sorted(tayyor, key=lambda x: x[2]):
        print(f"    {vaqt.strftime('%Y-%m-%d %H:%M')}  {n:>4} belgi{'  ovozsiz' if ovozsiz else ''}   {pid}")
    print()


def qoy(a, papka, zona, kanal_std):
    def qiymat(kalit):
        i = a.index(kalit)
        if i + 1 >= len(a):
            raise SystemExit(f"{kalit} dan keyin qiymat kerak")
        v = a[i + 1]
        del a[i:i + 2]
        return v

    if "--vaqt" not in a:
        raise SystemExit('--vaqt kerak, masalan --vaqt "2026-11-12 19:00"')
    vaqt = vaqt_ol(qiymat("--vaqt"), zona)
    kanal = joyla.kanal_nomi(qiymat("--kanal")) if "--kanal" in a else kanal_std
    ovozsiz = "--ovozsiz" in a
    a[:] = [x for x in a if x != "--ovozsiz"]
    media = [(t, qiymat("--" + t)) for t in joyla.MEDIA if "--" + t in a]
    if len(media) > 1:
        raise SystemExit("bitta postga bitta media")
    media = media[0] if media else None
    if not a:
        raise SystemExit("post fayli ko'rsatilmagan")
    hozir = datetime.datetime.now(datetime.timezone.utc)
    matn, n, qadamlar = tekshir_element(a[0], vaqt, media, kanal, hozir)
    git(papka, "pull", "--rebase", "-q")
    pid = vaqt.strftime("%Y-%m-%d_%H%M") + "_" + slug(matn)
    if os.path.exists(os.path.join(papka, "navbat", pid)):
        raise SystemExit(f"navbatda shu nomli post bor: {pid}")
    yarat(papka, zona, pid, a[0], vaqt, media, kanal, ovozsiz, hozir)
    git(papka, "add", "-A")
    git(papka, "commit", "-q", "-m", f"navbatga: {pid}")
    git(papka, "push", "-q")
    print(f"\n  ok navbatga qo'yildi: {pid}")
    print(f"     kanal:    {kanal}")
    print(f"     vaqt:     {vaqt.strftime('%Y-%m-%d %H:%M')} ({zona_nomi(zona)})")
    print(f"     xabarlar: {' + '.join(q[1] for q in qadamlar)}, {n} belgi")
    print("     GitHub soatiga bir marta tekshiradi: post taxminan 5-40 daqiqa kechikib chiqadi.")
    print(f"     Bekor qilish: python navbatga.py --bekor {pid}\n")


def zona_nomi(z):
    s = int(z.utcoffset(None).total_seconds() // 60)
    return f"UTC{'+' if s >= 0 else '-'}{abs(s) // 60:02d}:{abs(s) % 60:02d}"


def royxat(papka, zona):
    git(papka, "pull", "--rebase", "-q", tekshir=False)

    def oqi(bolim):
        yol = os.path.join(papka, bolim)
        natija = []
        for nom in sorted(os.listdir(yol)) if os.path.isdir(yol) else []:
            mp = os.path.join(yol, nom, "meta.json")
            if os.path.isfile(mp):
                with open(mp, encoding="utf-8-sig") as f:
                    natija.append((nom, json.load(f)))
        return natija

    navbat = oqi("navbat")
    print(f"\n  NAVBATDA ({len(navbat)})")
    for nom, m in navbat:
        v = datetime.datetime.fromisoformat(m["vaqt"]).astimezone(zona)
        media = f" + {m['media'][0]}" if m.get("media") else ""
        print(f"    {v.strftime('%Y-%m-%d %H:%M')}  {m.get('kanal')}{media}   {nom}")
    if not navbat:
        print("    bo'sh")
    for bolim, sarlavha in (("yuborilgan", "OXIRGI JOYLANGANLAR"), ("kechikkan", "KECHIKKAN (yuborilmagan)"),
                            ("xato", "XATO (yuborilmagan)")):
        r = oqi(bolim)
        if not r:
            continue
        print(f"\n  {sarlavha}")
        for nom, m in r[-5:]:
            izoh = " ".join(m.get("havolalar", [])) or m.get("xato") or m.get("kechikdi", "")
            print(f"    {nom}   {izoh}")
    print()


def bekor(papka, pid):
    git(papka, "pull", "--rebase", "-q")
    manzil = os.path.join(papka, "navbat", pid)
    if not os.path.isdir(manzil):
        raise SystemExit(f"navbatda yo'q: {pid} (allaqachon joylangan bo'lishi mumkin - --royxat)")
    shutil.rmtree(manzil)
    git(papka, "add", "-A")
    git(papka, "commit", "-q", "-m", f"bekor: {pid}")
    git(papka, "push", "-q")
    print(f"\n  ok navbatdan olib tashlandi: {pid}\n")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    papka, zona_s, kanal_std = sozlama()
    if not papka or not os.path.isdir(papka):
        raise SystemExit("navbat papkasi topilmadi: telegram.json dagi \"navbat_papka\"")
    zona = zona_ol(zona_s)
    if a[0] == "--royxat":
        royxat(papka, zona)
    elif a[0] == "--bekor" and len(a) > 1:
        bekor(papka, a[1])
    elif a[0] == "--toplam" and len(a) > 1:
        toplam(a[1], papka, zona, kanal_std)
    else:
        qoy(a, papka, zona, kanal_std)


if __name__ == "__main__":
    main()
