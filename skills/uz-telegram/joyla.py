#!/usr/bin/env python3
"""joyla.py - Telegram kanalga post joylash (rasmiy Bot API orqali).

    python joyla.py --tekshir                       # bot va kanal tayyormi
    python joyla.py post.txt                        # KO'RIB CHIQISH: nima yuborilishini ko'rsatadi, yubormaydi
    python joyla.py post.txt --rasm rasm.jpg        # rasm bilan
    python joyla.py post.txt --fayl shablon.xlsx    # fayl (hujjat) bilan
    python joyla.py post.txt --yubor                # HAQIQATAN yuborish
    python joyla.py post.txt --yubor --ovozsiz      # obunachilarga bildirishnomasiz

Sozlamalar ~/.claude/kontent-uz/telegram.json da:
    {"kanal": "@kanal_nomi", "token_fayl": "C:/yo'l/bot_token.txt"}
yoki muhit o'zgaruvchilarida: TELEGRAM_BOT_TOKEN, TELEGRAM_KANAL.
Bot kanalda "Xabar joylash" huquqi bilan admin bo'lishi kerak (--tekshir buni ko'rsatadi).
Token hech qachon ekranga chiqarilmaydi.

Post matnida format: **qalin**, __qiya__, ~~ustidan chizilgan~~, `kod`, ||spoiler||,
[matn](https://havola), "> " bilan boshlangan qatorlar - iqtibos. Hammasi Telegram HTML formatiga
o'giriladi, qolgan belgilar (<, >, &) xavfsiz qilinadi.

Chegaralar: matnli xabar 4096 belgi, rasm/fayl izohi 1024 belgi (Telegram belgini UTF-16 bo'yicha
sanaydi: emoji 2 ta hisoblanadi). Izoh sig'masa, rasm va matn ikki xabar bo'lib ketadi - ko'rib
chiqishda buni oldindan aytadi.

DARVOZA: --yubor bo'lmasa hech narsa yuborilmaydi. Kanalga chiqqan postni hamma ko'radi.
Yuborilgan postlar ~/.claude/kontent-uz/telegram_jurnal.csv ga yoziladi.
"""
import csv, datetime, html as htmlmod, json, mimetypes, os, re, sys, uuid
import urllib.error, urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PAPKA = os.path.join(os.path.expanduser("~"), ".claude", "kontent-uz")
SOZLAMA = os.path.join(PAPKA, "telegram.json")
JURNAL = os.path.join(PAPKA, "telegram_jurnal.csv")
MATN_CHEGARA, IZOH_CHEGARA = 4096, 1024


class TgXato(Exception):
    pass


def kanal_nomi(k):
    k = (k or "").strip()
    if not k:
        return None
    if k.lstrip("-").isdigit() or k.startswith("@"):
        return k
    return "@" + k.rstrip("/").rsplit("/", 1)[-1]      # https://t.me/kanal -> @kanal


def sozlamalar():
    kanal = os.environ.get("TELEGRAM_KANAL")
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if os.path.exists(SOZLAMA):
        with open(SOZLAMA, encoding="utf-8-sig") as f:
            c = json.load(f)
        kanal = kanal or c.get("kanal")
        if not token and c.get("token_fayl"):
            p = os.path.expanduser(c["token_fayl"])
            if os.path.exists(p):
                with open(p, encoding="utf-8-sig", errors="replace") as f:
                    m = re.search(r"\d{5,}:[A-Za-z0-9_-]{30,}", f.read())
                token = m.group(0) if m else None
    return kanal_nomi(kanal), token


# --- format: oddiy belgilash -> Telegram HTML --------------------------------------------------
def _qator_format(t):
    t = re.sub(r"\[([^\]\n]+)\]\((https?://[^\s)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"__(.+?)__", r"<i>\1</i>", t)
    t = re.sub(r"~~(.+?)~~", r"<s>\1</s>", t)
    t = re.sub(r"\|\|(.+?)\|\|", r"<tg-spoiler>\1</tg-spoiler>", t)
    return t


def html_ga(matn):
    t = matn.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    qatorlar, natija, iqtibos = t.split("\n"), [], []
    for q in qatorlar:
        if q.startswith("&gt; ") or q == "&gt;":
            iqtibos.append(q[5:])
            continue
        if iqtibos:
            natija.append("<blockquote>" + "\n".join(iqtibos) + "</blockquote>")
            iqtibos = []
        natija.append(q)
    if iqtibos:
        natija.append("<blockquote>" + "\n".join(iqtibos) + "</blockquote>")
    t = "\n".join(natija)
    # `kod` ichidagi belgilar formatlanmaydi
    qism = re.split(r"(`[^`\n]+`)", t)
    return "".join("<code>" + q[1:-1] + "</code>" if q.startswith("`") and q.endswith("`") and len(q) > 1
                   else _qator_format(q) for q in qism)


def korinadigan(h):
    return htmlmod.unescape(re.sub(r"<[^>]+>", "", h))


def tg_uzunlik(t):
    return len(t.encode("utf-16-le")) // 2
# -------------------------------------------------------------------------------------------------


def _multipart(maydon, fayllar):
    b = uuid.uuid4().hex
    out = []
    for k, v in maydon.items():
        out += [f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n'.encode(),
                str(v).encode("utf-8"), b"\r\n"]
    for k, yol in fayllar.items():
        nom = os.path.basename(yol).replace('"', "")
        ct = mimetypes.guess_type(yol)[0] or "application/octet-stream"
        with open(yol, "rb") as f:
            data = f.read()
        out += [f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{nom}"\r\n'
                f"Content-Type: {ct}\r\n\r\n".encode("utf-8"), data, b"\r\n"]
    out.append(f"--{b}--\r\n".encode())
    return b"".join(out), f"multipart/form-data; boundary={b}"


def api(token, metod, maydon=None, fayllar=None):
    url = f"https://api.telegram.org/bot{token}/{metod}"
    if fayllar:
        body, ct = _multipart({k: v for k, v in (maydon or {}).items() if v is not None}, fayllar)
    else:
        body, ct = json.dumps({k: v for k, v in (maydon or {}).items() if v is not None}).encode(), "application/json"
    req = urllib.request.Request(url, data=body, headers={"Content-Type": ct})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        try:
            d = json.load(e)
        except Exception:
            raise TgXato(f"HTTP {e.code}")
    except urllib.error.URLError as e:
        raise TgXato(f"Telegram'ga ulanib bo'lmadi: {e.reason}")
    if not d.get("ok"):
        raise TgXato(d.get("description", "noma'lum xato"))
    return d["result"]


def tekshir(kanal, token):
    if not token:
        print("  x  token topilmadi - telegram.json dagi token_fayl yoki TELEGRAM_BOT_TOKEN ni tekshiring"); return 1
    if not kanal:
        print("  x  kanal ko'rsatilmagan - telegram.json dagi \"kanal\""); return 1
    me = api(token, "getMe")
    print(f"  ok bot:    @{me.get('username')}")
    try:
        chat = api(token, "getChat", {"chat_id": kanal})
        print(f"  ok kanal:  {chat.get('title')} ({kanal}, {chat.get('type')})")
    except TgXato as e:
        print(f"  x  kanal topilmadi: {e}"); return 1
    try:
        a = api(token, "getChatMember", {"chat_id": kanal, "user_id": me["id"]})
    except TgXato as e:
        print(f"  x  bot kanalda admin emas ({e})")
        print("     Kanal -> Boshqarish -> Administratorlar -> Admin qo'shish -> botni tanlang -> 'Xabar joylash' yoqilsin")
        return 1
    holat = a.get("status")
    if holat == "creator" or (holat == "administrator" and a.get("can_post_messages")):
        print("  ok huquq:  bot kanalga post joylay oladi")
        return 0
    print(f"  x  bot holati: {holat}; 'Xabar joylash' huquqi yo'q")
    print("     Kanal -> Boshqarish -> Administratorlar -> botni oching -> 'Xabar joylash' ni yoqing")
    return 1


def reja_tuz(matn, rasm, fayl):
    h = html_ga(matn)
    n = tg_uzunlik(korinadigan(h))
    media = rasm or fayl
    if not media:
        return h, n, [("sendMessage", "matn")]
    if n <= IZOH_CHEGARA:
        return h, n, [("sendPhoto" if rasm else "sendDocument", "izohli " + ("rasm" if rasm else "fayl"))]
    if rasm:
        return h, n, [("sendPhoto", "rasm (izohsiz)"), ("sendMessage", "matn")]
    return h, n, [("sendMessage", "matn"), ("sendDocument", "fayl (izohsiz)")]


def main():
    a = sys.argv[1:]
    yubor = "--yubor" in a
    ovozsiz = "--ovozsiz" in a
    a = [x for x in a if x not in ("--yubor", "--ovozsiz")]
    rasm = fayl = None
    if "--rasm" in a:
        i = a.index("--rasm"); rasm = a[i + 1]; del a[i:i + 2]
    if "--fayl" in a:
        i = a.index("--fayl"); fayl = a[i + 1]; del a[i:i + 2]
    kanal, token = sozlamalar()
    try:
        if "--tekshir" in a:
            print(); kod = tekshir(kanal, token); print(); sys.exit(kod)
        if not a or not os.path.exists(a[0]):
            print(__doc__); sys.exit(1)
        if rasm and fayl:
            print("bitta postga yo rasm, yo fayl - ikkalasi emas"); sys.exit(1)
        for m in (rasm, fayl):
            if m and not os.path.exists(m):
                print(f"fayl topilmadi: {m}"); sys.exit(1)
        with open(a[0], encoding="utf-8-sig", errors="replace") as f:
            matn = f.read().strip("\n")
        h, n, qadamlar = reja_tuz(matn, rasm, fayl)
        birinchi = korinadigan(h).splitlines()[0] if matn else ""
        sarlavha = "YUBORILMOQDA" if yubor else "KO'RIB CHIQISH - hech narsa yuborilmadi"
        print(f"\n  {sarlavha}")
        kanal_k = kanal or "(ko'rsatilmagan)"
        print(f"  kanal:          {kanal_k}")
        print(f"  token:          {'bor' if token else 'TOPILMADI'}")
        print(f"  uzunlik:        {n} / {MATN_CHEGARA} belgi" + (f"   (izoh chegarasi {IZOH_CHEGARA})" if (rasm or fayl) else ""))
        print(f"  xabarlar:       {' + '.join(q[1] for q in qadamlar)}")
        print(f'  birinchi qator: "{birinchi[:80]}"')
        if n > MATN_CHEGARA:
            print(f"\n  x  post {MATN_CHEGARA} belgidan uzun - ikkiga bo'ling"); sys.exit(1)
        if not yubor:
            print("\n  ---- kanalda ko'rinadigan matn (format belgilari olib tashlangan) ----")
            for q in korinadigan(h).splitlines():
                print("  | " + q)
            print("  ---------------------------------------------------------------------")
            print(f"\n  Yuborish uchun: python joyla.py {a[0]}"
                  + (f" --rasm {rasm}" if rasm else "") + (f" --fayl {fayl}" if fayl else "") + " --yubor\n")
            return
        if not token or not kanal:
            print("  x  token yoki kanal yo'q - avval: python joyla.py --tekshir"); sys.exit(1)
        havolalar = []
        for metod, _ in qadamlar:
            maydon = {"chat_id": kanal, "disable_notification": "true" if ovozsiz else None}
            fayllar = None
            if metod == "sendMessage":
                maydon.update({"text": h, "parse_mode": "HTML"})
            else:
                kalit = "photo" if metod == "sendPhoto" else "document"
                fayllar = {kalit: rasm or fayl}
                if len(qadamlar) == 1:
                    maydon.update({"caption": h, "parse_mode": "HTML"})
            if not fayllar and maydon.get("disable_notification"):
                maydon["disable_notification"] = True
            r = api(token, metod, maydon, fayllar)
            mid = r["message_id"]
            havolalar.append(f"https://t.me/{kanal[1:]}/{mid}" if kanal.startswith("@") else str(mid))
        os.makedirs(PAPKA, exist_ok=True)
        yangi = not os.path.exists(JURNAL)
        with open(JURNAL, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            if yangi:
                w.writerow(["sana", "kanal", "havola", "birinchi_qator", "uzunlik"])
            w.writerow([datetime.datetime.now().isoformat(timespec="seconds"), kanal, havolalar[0], birinchi, n])
        print("\n  ok joylandi: " + "  ".join(havolalar) + "\n")
    except TgXato as e:
        print(f"\n  x  Telegram xatosi: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
