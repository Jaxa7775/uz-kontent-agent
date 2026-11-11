#!/usr/bin/env python3
"""navbat.py - navbatdagi postlarni vaqti kelganda Telegram kanalga joylaydi.
GitHub Actions'da ishga tushadi (.github/workflows/navbat.yml): asosan tashqi taymer (cron-job.org)
post vaqtlarida chaqiradi, GitHub'ning o'z cron'i har soatda zaxira (u ishonchsiz, ba'zan soatlab o'tkazib yuboradi).
Vaqtiga 5 daqiqadan kam qolgan post ham yuboriladi - taymer bir oz erta ishlasa post 3 soat kutib qolmasin.

    python3 navbat.py             # vaqti kelganlarni joylash
    python3 navbat.py --tekshir   # bot va kanalni tekshirish (hech narsa yubormaydi)

Tuzilma:
    navbat/<id>/post.txt
    navbat/<id>/meta.json   {"vaqt": "2026-11-12T19:00:00+05:00", "kanal": "@kanal",
                             "media": ["ovoz", "ovoz.mp3"] yoki null, "ovozsiz": false}
    navbat/<id>/<media fayl>

Natija:
    yuborilgan/<id>/   - joylandi, meta.json ga havola va vaqt yoziladi
    kechikkan/<id>/    - vaqtidan 6 soatdan ko'p o'tib ketgan, YUBORILMAYDI (eskirgan post chiqmasin)
    xato/<id>/         - Telegram xato berdi; qayta urinilmaydi (takroriy post chiqmasin), ish
                         "muvaffaqiyatsiz" bo'lib tugaydi va GitHub sizga xat yuboradi

Bir ishga tushishda ko'pi bilan 3 ta post (sozlama xatosida kanal to'lib ketmasin).
Muhit: TELEGRAM_BOT_TOKEN (GitHub secret), TELEGRAM_KANAL (standart kanal, ixtiyoriy).
"""
import datetime, importlib.util, json, os, shutil, sys

ILDIZ = os.path.dirname(os.path.abspath(__file__))
KECHIKISH = datetime.timedelta(hours=6)
ERTA = datetime.timedelta(minutes=5)
MAKS = 3


def joyla_moduli():
    for yol in (os.environ.get("JOYLA_YOLI"), os.path.join(ILDIZ, "tools", "joyla.py"),
                os.path.join(ILDIZ, "joyla.py")):
        if yol and os.path.exists(yol):
            spec = importlib.util.spec_from_file_location("joyla", yol)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    raise SystemExit("joyla.py topilmadi (tools/joyla.py)")


def kochir(papka, ildiz, qayerga):
    manzil = os.path.join(ildiz, qayerga, os.path.basename(papka))
    os.makedirs(os.path.dirname(manzil), exist_ok=True)
    if os.path.exists(manzil):
        shutil.rmtree(manzil)
    shutil.move(papka, manzil)
    return manzil


def yoz_meta(papka, m):
    with open(os.path.join(papka, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)


def ishla(ildiz=ILDIZ, hozir=None, joyla=None, token=None, kanal_std=None):
    """0 - hammasi joyida, 1 - kamida bitta xato."""
    joyla = joyla or joyla_moduli()
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    kanal_std = kanal_std or os.environ.get("TELEGRAM_KANAL")
    if not token:
        print("x  TELEGRAM_BOT_TOKEN yo'q (GitHub -> Settings -> Secrets -> Actions)")
        return 1
    hozir = hozir or datetime.datetime.now(datetime.timezone.utc)
    navbat = os.path.join(ildiz, "navbat")
    postlar, xato = [], False
    for nom in sorted(os.listdir(navbat)) if os.path.isdir(navbat) else []:
        papka = os.path.join(navbat, nom)
        meta_yol = os.path.join(papka, "meta.json")
        if not os.path.isfile(meta_yol):
            continue
        with open(meta_yol, encoding="utf-8-sig") as f:
            m = json.load(f)
        try:
            vaqt = datetime.datetime.fromisoformat(m["vaqt"])
            if vaqt.tzinfo is None:
                raise ValueError("vaqt zonasi yo'q")
        except (KeyError, ValueError) as e:
            m["xato"] = f"vaqt noto'g'ri: {e}"
            yoz_meta(papka, m)
            kochir(papka, ildiz, "xato")
            print(f"x  {nom}: {m['xato']}")
            xato = True
            continue
        postlar.append((vaqt, nom, papka, m))
    postlar.sort(key=lambda p: (p[0], p[1]))
    yuborildi = 0
    for vaqt, nom, papka, m in postlar:
        if vaqt > hozir + ERTA:
            print(f".  {nom}: {vaqt.isoformat()} ni kutmoqda")
            continue
        if hozir - vaqt > KECHIKISH:
            m["kechikdi"] = hozir.isoformat(timespec="seconds")
            yoz_meta(papka, m)
            kochir(papka, ildiz, "kechikkan")
            print(f"!  {nom}: vaqtidan {hozir - vaqt} o'tib ketgan - yuborilmadi (kechikkan/)")
            continue
        if yuborildi >= MAKS:
            print(f".  {nom}: bu safar chegara ({MAKS} ta) to'ldi, keyingi ishga tushishda")
            continue
        kanal = joyla.kanal_nomi(m.get("kanal") or kanal_std)
        with open(os.path.join(papka, "post.txt"), encoding="utf-8-sig") as f:
            matn = f.read().strip("\n")
        media = m.get("media")
        media = (media[0], os.path.join(papka, media[1])) if media else None
        try:
            havolalar = joyla.yubor(token, kanal, matn, media, bool(m.get("ovozsiz")))
        except joyla.TgXato as e:
            m["xato"] = str(e)
            m["qisman_yuborilgan"] = getattr(e, "yuborilgan", [])
            yoz_meta(papka, m)
            kochir(papka, ildiz, "xato")
            print(f"x  {nom}: Telegram xatosi: {e}")
            xato = True
            continue
        m["yuborildi"] = hozir.isoformat(timespec="seconds")
        m["havolalar"] = havolalar
        yoz_meta(papka, m)
        kochir(papka, ildiz, "yuborilgan")
        yuborildi += 1
        print(f"ok {nom}: {' '.join(havolalar)}")
    if not postlar:
        print(".  navbat bo'sh")
    return 1 if xato else 0


def main():
    if "--tekshir" in sys.argv:
        j = joyla_moduli()
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        kanal = j.kanal_nomi(os.environ.get("TELEGRAM_KANAL"))
        try:
            sys.exit(j.tekshir(kanal, token))
        except j.TgXato as e:
            print(f"x  Telegram xatosi: {e}")
            sys.exit(1)
    sys.exit(ishla())


if __name__ == "__main__":
    main()
