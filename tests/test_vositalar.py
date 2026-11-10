#!/usr/bin/env python3
"""Vositalar uchun testlar. Faqat standart kutubxona.

    python tests/test_vositalar.py
"""
import json, os, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "skills")


def run(script, *args, cwd=None):
    p = subprocess.run([sys.executable, os.path.join(S, script), *args], capture_output=True, cwd=cwd)
    return p.returncode, p.stdout.decode("utf-8"), p.stderr.decode("utf-8", "replace")


def js(script, *args, cwd=None):
    code, out, err = run(script, *args, "--json", cwd=cwd)
    assert code == 0, err or out
    return json.loads(out)


class Tmp(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def w(self, name, text):
        p = os.path.join(self.d, name)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        return p


class HookBaho(Tmp):
    def test_kuchli_zaifdan_yuqori(self):
        r = js("uz-ssenariy/hook_baho.py", self.w("h.txt",
               "Siz Word'da jadvalni Space bosib tekislayapsiz va har safar 10 daqiqa yo'qotasiz.\n"
               "Assalomu alaykum hurmatli obunachilar bugungi videoda ajoyib narsa\n"))
        self.assertGreater(r[0]["baho"], r[1]["baho"])
        self.assertTrue(r[0]["hook"].startswith("Siz"))

    def test_kirill_va_lotin_bir_xil(self):
        lot = js("uz-ssenariy/hook_baho.py", "--hook", "Nega printer ulangan bo'lsa ham oflayn deb ko'rsatadi?")
        kir = js("uz-ssenariy/hook_baho.py", "--hook", "Нега принтер уланган бўлса ҳам офлайн деб кўрсатади?")
        self.assertEqual(lot[0]["xususiyatlar"], kir[0]["xususiyatlar"])
        self.assertEqual(lot[0]["formula"], "Savol")

    def test_tutuq_belgilari_bir_xil(self):
        a = js("uz-ssenariy/hook_baho.py", "--hook", "Ko'pchilik bilmaydi: Windows'da yashirin oyna bor")
        b = js("uz-ssenariy/hook_baho.py", "--hook", "Koʻpchilik bilmaydi: Windows`da yashirin oyna bor")
        self.assertEqual(a[0]["baho"], b[0]["baho"])
        self.assertEqual(a[0]["formula"], "Ko'pchilik bilmaydi")

    def test_utf8_fayl_va_chiqish(self):
        code, out, err = run("uz-ssenariy/hook_baho.py", self.w("u.txt", "Oʻqituvchilar uchun 5 ta maslahat\n"))
        self.assertEqual(code, 0, err)
        self.assertIn("Oʻqituvchilar", out)


class Sarlavha(Tmp):
    def test_muqova_4_soz_xato(self):
        r = js("uz-sarlavha/sarlavha.py", "--sarlavha", "Excel'da 1000 qatorni 3 soniyada tozalash",
               "--muqova", "BU USUL HAMMANI HAYRATDA")
        self.assertIn("muqova-uzun", [k for k, _ in r[0]["xatolar"]])

    def test_takror_qoshimcha_bilan(self):
        r = js("uz-sarlavha/sarlavha.py", "--sarlavha", "Printer oflayn bo'lsa nima qilish kerak",
               "--muqova", "PRINTERNI TUZAT")
        self.assertIn("takror", [k for k, _ in r[0]["xatolar"]])

    def test_tutuq_aralash(self):
        r = js("uz-sarlavha/sarlavha.py", "--sarlavha", "O'qituvchi uchun 5 ta qoʻllanma")
        self.assertIn("tutuq", [k for k, _ in r[0]["xatolar"]])

    def test_telegram_caption_chegarasi(self):
        p = self.w("post.txt", "Word'da mundarija bitta tugma bilan\n\n" + "Matn. " * 250)
        r = js("uz-sarlavha/sarlavha.py", "--platforma", "telegram", "--fayl", p, "--rasm")
        self.assertIn("post-uzun", [k for k, _ in r[0]["xatolar"]])
        r2 = js("uz-sarlavha/sarlavha.py", "--platforma", "telegram", "--fayl", p)
        self.assertNotIn("post-uzun", [k for k, _ in r2[0]["xatolar"]])


AYLANMA_VTT = """WEBVTT
Kind: captions
Language: uz

00:00:00.000 --> 00:00:03.000
bugun biz Excel jadvalini

00:00:01.500 --> 00:00:04.500
bugun biz Excel jadvalini
<00:00:02.000><c> tozalashni</c><00:00:02.500><c> o'rganamiz</c>

00:00:04.490 --> 00:00:04.500
tozalashni o'rganamiz

00:00:04.500 --> 00:00:07.500
tozalashni o'rganamiz
birinchi qadam fayl ochish
"""

SRT = """1
00:00:00,000 --> 00:00:02,000
bugun biz Excel jadvalini

2
00:00:02,500 --> 00:00:03,000
ee

3
00:00:03,100 --> 00:00:05,000
bugun biz Excel jadvalini tozalaymiz

4
00:00:07,000 --> 00:00:09,000
xullas

5
00:00:09,100 --> 00:00:12,000
birinchi qadam faylni ochish
"""


class Montaj(Tmp):
    def test_aylanma_subtitrda_soxta_takror_yoq(self):
        r = js("uz-montaj/montaj.py", self.w("a.vtt", AYLANMA_VTT))
        self.assertEqual([c for c in r["kesishlar"] if c["tur"] == "TAKROR"], [])

    def test_parazit_takror_jim(self):
        r = js("uz-montaj/montaj.py", self.w("b.srt", SRT))
        turlar = sorted(c["tur"] for c in r["kesishlar"])
        self.assertIn("TAKROR", turlar)
        self.assertEqual(turlar.count("PARAZIT"), 2)
        self.assertIn("JIM", turlar)
        self.assertLessEqual(r["olinadi"], r["uzunlik"])

    def test_himoya(self):
        r = js("uz-montaj/montaj.py", self.w("c.srt", SRT), "--himoya", "0:05-0:07")
        self.assertGreater(r["himoya_sababli_tashlandi"], 0)
        for c in r["kesishlar"]:
            self.assertFalse(c["boshi"] < 7 and c["oxiri"] > 5)

    def test_kesishlar_ustma_ust_ikki_marta_sanalmaydi(self):
        srt = "1\n00:00:00,000 --> 00:00:01,000\nmana\n\n2\n00:00:00,500 --> 00:00:01,500\nxullas\n\n3\n00:00:01,600 --> 00:00:03,000\nendi asosiy gap boshlanadi\n"
        r = js("uz-montaj/montaj.py", self.w("d.srt", srt))
        self.assertAlmostEqual(r["olinadi"], 1.5, places=2)


class Boblar(Tmp):
    def test_yaroqli_boblar(self):
        qism = [("printer ulash kabel drayver o'rnatish printer", 0),
                ("excel jadval formula ustun qator excel", 60),
                ("parol xavfsizlik menejer parol saqlash", 120)]
        bloklar, n = [], 1
        for matn, boshi in qism:
            for k in range(8):
                a = boshi + k * 6
                bloklar.append(f"{n}\n00:{a // 60:02d}:{a % 60:02d},000 --> 00:{(a + 5) // 60:02d}:{(a + 5) % 60:02d},000\n{matn} {k}\n")
                n += 1
        r = js("uz-seo/boblar.py", self.w("b.srt", "\n".join(bloklar)), "--soni", "3")
        self.assertTrue(r["yaroqli"], r)
        self.assertEqual([b["boshi"] for b in r["boblar"]], [0.0, 60.0, 120.0])


class Imlo(unittest.TestCase):
    def out(self, *a):
        code, out, err = run("uz-seo/imlo.py", *a)
        self.assertEqual(code, 0, err)
        return out.strip()

    def test_kirill(self):
        self.assertEqual(self.out("--kirill", "yo'q o'qituvchi yangi eng Excel"), "йўқ ўқитувчи янги энг Excel")

    def test_lotin(self):
        self.assertEqual(self.out("--lotin", "Ўқитувчи ер юзи"), "O'qituvchi yer yuzi")

    def test_teg(self):
        out = self.out("--teg", "o'qituvchi darslari")
        self.assertIn("#oqituvchidarslari", out)
        self.assertIn("#ўқитувчидарслари", out)

    def test_variant(self):
        out = self.out("--variant", "o'zbek")
        for v in ["o'zbek", "oʻzbek", "o`zbek", "ozbek", "ўзбек"]:
            self.assertIn(v, out)


class Retention(Tmp):
    def csv(self, name, boshi_tushish):
        rows = ["Video position (%),Absolute audience retention (%)"]
        for i in range(0, 101):
            y = 100 - (boshi_tushish if i >= 5 else boshi_tushish * i / 5) - 0.3 * i - (8 if i >= 50 else 0)
            rows.append(f"{i},{y:.2f}")
        return self.w(name, "\n".join(rows))

    def test_davomiylik_tartibi_muhim_emas(self):
        p = self.csv("r.csv", 30)
        a = js("uz-tahlil/retention.py", p, "--davomiylik", "600")
        b = js("uz-tahlil/retention.py", "--davomiylik", "600", p)
        self.assertEqual(a, b)
        self.assertEqual(a["oq"], "foiz")
        self.assertTrue(any(abs(k["soniya"] - 294) < 7 for k in a["keskin"]), a["keskin"])

    def test_qisqa_video_soniya_sarlavhadan(self):
        rows = ["Seconds,Retention"] + [f"{i},{100 - i * 0.8:.1f}" for i in range(0, 58)]
        a = js("uz-tahlil/retention.py", self.w("s.csv", "\n".join(rows)))
        self.assertEqual(a["oq"], "soniya")
        self.assertEqual(a["chegara_nomi"], "birinchi 30 soniya")

    def test_solishtirish(self):
        code, out, err = run("uz-tahlil/retention.py", self.csv("a.csv", 20), self.csv("b.csv", 45))
        self.assertEqual(code, 0, err)
        self.assertIn("SOLISHTIRISH", out)


class Trend(Tmp):
    def test_karra_va_kam_manba(self):
        data = [{"manba": "A", "matn": f"oddiy video {i}", "korishlar": 1000} for i in range(5)]
        data.append({"manba": "A", "matn": "Nega printer oflayn bo'ladi?", "korishlar": "5,000"})
        data += [{"manba": "B", "matn": "x", "korishlar": 10}]
        r = js("uz-trend/trend.py", self.w("t.json", json.dumps(data, ensure_ascii=False)))
        self.assertEqual(len(r["yuqori"]), 1)
        self.assertEqual(r["yuqori"][0]["karra"], 5.0)
        self.assertEqual(r["yuqori"][0]["formula"], "Savol")
        self.assertEqual(r["kam_manbalar"], [["B", 1]])

    def test_ytdlp_format(self):
        d = {"channel": "Kanal", "entries": [{"title": f"t{i}", "view_count": v}
                                              for i, v in enumerate([100, 120, 90, 110, 600])]}
        r = js("uz-trend/trend.py", self.w("y.json", json.dumps(d)))
        self.assertEqual(r["yuqori"][0]["manba"], "Kanal")
        self.assertEqual(r["yuqori"][0]["korishlar"], 600)

    def test_csv(self):
        csvt = "kanal,sarlavha,ko'rishlar\n" + "\n".join(f"K,s{i},{v}" for i, v in enumerate(["1 000", "1200", "900", "1,1k", "4500"]))
        r = js("uz-trend/trend.py", self.w("c.csv", csvt))
        self.assertEqual(r["yuqori"][0]["korishlar"], 4500)


def joyla_moduli():
    import importlib.util
    spec = importlib.util.spec_from_file_location("joyla", os.path.join(S, "uz-telegram", "joyla.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class Joyla(Tmp):
    def test_html_format(self):
        j = joyla_moduli()
        h = j.html_ga("**Excel** darsi <yangi> & `Ctrl + C` va `**emas**`\n> iqtibos\n[havola](https://t.me/x?a=1&b=2) ||javob||")
        self.assertIn("<b>Excel</b>", h)
        self.assertIn("&lt;yangi&gt; &amp;", h)
        self.assertIn("<code>Ctrl + C</code>", h)
        self.assertIn("<code>**emas**</code>", h)
        self.assertIn("<blockquote>iqtibos</blockquote>", h)
        self.assertIn('<a href="https://t.me/x?a=1&amp;b=2">havola</a>', h)
        self.assertIn("<tg-spoiler>javob</tg-spoiler>", h)

    def test_kod_bloki(self):
        j = joyla_moduli()
        h = j.html_ga("**Skript:**\n```\n$a = 1 -> <b>\n**emas**\n```\nTugadi `x`")
        self.assertIn("<pre>$a = 1 -&gt; &lt;b&gt;\n**emas**</pre>", h)
        self.assertIn("<b>Skript:</b>", h)
        self.assertIn("<code>x</code>", h)
        self.assertNotIn("```", h)

    def test_uzunlik_utf16(self):
        j = joyla_moduli()
        self.assertEqual(j.tg_uzunlik("ab😀"), 4)
        self.assertEqual(j.tg_uzunlik(j.korinadigan(j.html_ga("**ab**"))), 2)

    def test_reja_izoh_chegarasi(self):
        j = joyla_moduli()
        _, _, q = j.reja_tuz("qisqa", ("rasm", "r.jpg"))
        self.assertEqual([m for m, _ in q], ["sendPhoto"])
        _, _, q = j.reja_tuz("a" * 1500, ("fayl", "f.xlsx"))
        self.assertEqual([m for m, _ in q], ["sendMessage", "sendDocument"])
        _, _, q = j.reja_tuz("qisqa", ("ovoz", "o.mp3"))
        self.assertEqual([m for m, _ in q], ["sendVoice"])
        _, _, q = j.reja_tuz("a" * 1500, ("ovoz", "o.mp3"))
        self.assertEqual([m for m, _ in q], ["sendVoice", "sendMessage"])

    def test_korib_chiqish_yubormaydi(self):
        env = dict(os.environ, TELEGRAM_KANAL="https://t.me/sinov_kanal", TELEGRAM_BOT_TOKEN="123456:" + "A" * 35)
        p = subprocess.run([sys.executable, os.path.join(S, "uz-telegram", "joyla.py"),
                            self.w("post.txt", "**Sarlavha** qatori\n\nMatn")], capture_output=True, env=env)
        out = p.stdout.decode("utf-8")
        self.assertEqual(p.returncode, 0, p.stderr.decode("utf-8", "replace"))
        self.assertIn("hech narsa yuborilmadi", out)
        self.assertIn("@sinov_kanal", out)
        self.assertIn('"Sarlavha qatori"', out)
        self.assertNotIn("A" * 35, out)

    def test_kanal_bayrogi(self):
        env = dict(os.environ, TELEGRAM_KANAL="@birinchi", TELEGRAM_BOT_TOKEN="123456:" + "A" * 35)
        p = subprocess.run([sys.executable, os.path.join(S, "uz-telegram", "joyla.py"),
                            self.w("p.txt", "Matn"), "--kanal", "https://t.me/ikkinchi"], capture_output=True, env=env)
        out = p.stdout.decode("utf-8")
        self.assertIn("@ikkinchi", out)
        self.assertIn("--kanal @ikkinchi --yubor", out)

    def test_kanal_qiymatsiz(self):
        p = subprocess.run([sys.executable, os.path.join(S, "uz-telegram", "joyla.py"), "--tekshir", "--kanal"],
                           capture_output=True)
        self.assertEqual(p.returncode, 1)
        self.assertIn("qiymat kerak", p.stdout.decode("utf-8"))
        self.assertNotIn("Traceback", p.stderr.decode("utf-8", "replace"))


def oqi_json(yol):
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def modul(nom, yol):
    import importlib.util
    spec = importlib.util.spec_from_file_location(nom, yol)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class Navbat(Tmp):
    """templates/kanal-navbat/navbat.py - GitHub Actions'dagi joylovchi (Telegram soxtalashtirilgan)."""

    def setUp(self):
        super().setUp()
        import datetime
        self.dt = datetime
        self.n = modul("navbat", os.path.join(ROOT, "templates", "kanal-navbat", "navbat.py"))
        self.j = joyla_moduli()
        self.chaqiruvlar = []
        sanoq = iter(range(100, 200))

        def soxta_api(token, metod, maydon=None, fayllar=None):
            self.chaqiruvlar.append((metod, maydon.get("chat_id"), fayllar))
            if self.xato_berilsin:
                raise self.j.TgXato("Bad Request: chat not found")
            return {"message_id": next(sanoq), "voice": {}} if metod == "sendVoice" else {"message_id": next(sanoq)}

        self.xato_berilsin = False
        self.j.api = soxta_api
        self.hozir = datetime.datetime(2026, 11, 12, 14, 7, tzinfo=datetime.timezone.utc)   # 19:07 Toshkent

    def post(self, pid, vaqt, media=None, matn="Sarlavha\n\nMatn"):
        d = os.path.join(self.d, "navbat", pid)
        os.makedirs(d)
        with open(os.path.join(d, "post.txt"), "w", encoding="utf-8") as f:
            f.write(matn)
        if media:
            with open(os.path.join(d, media[1]), "wb") as f:
                f.write(b"ID3")
        with open(os.path.join(d, "meta.json"), "w", encoding="utf-8") as f:
            json.dump({"vaqt": vaqt, "kanal": "@sinov", "media": media, "ovozsiz": False}, f)

    def ishla(self):
        return self.n.ishla(ildiz=self.d, hozir=self.hozir, joyla=self.j, token="t", kanal_std="@std")

    def test_vaqti_kelgani_joylanadi_kutayotgani_qoladi(self):
        self.post("a", "2026-11-12T19:00+05:00", ["ovoz", "o.mp3"])
        self.post("b", "2026-11-12T20:00+05:00")
        self.assertEqual(self.ishla(), 0)
        self.assertEqual([c[0] for c in self.chaqiruvlar], ["sendVoice"])
        self.assertTrue(os.path.isdir(os.path.join(self.d, "navbat", "b")))
        m = oqi_json(os.path.join(self.d, "yuborilgan", "a", "meta.json"))
        self.assertEqual(m["havolalar"], ["https://t.me/sinov/100"])

    def test_kechikkani_yuborilmaydi(self):
        self.post("eski", "2026-11-12T09:00+05:00")
        self.assertEqual(self.ishla(), 0)
        self.assertEqual(self.chaqiruvlar, [])
        self.assertTrue(os.path.isdir(os.path.join(self.d, "kechikkan", "eski")))

    def test_xato_qayta_urinilmaydi(self):
        self.post("x", "2026-11-12T19:00+05:00")
        self.xato_berilsin = True
        self.assertEqual(self.ishla(), 1)
        self.assertTrue(os.path.isdir(os.path.join(self.d, "xato", "x")))
        self.assertFalse(os.path.isdir(os.path.join(self.d, "navbat", "x")))

    def test_bir_safarda_3_tadan_kop_emas(self):
        for i in range(5):
            self.post(f"p{i}", f"2026-11-12T18:{i:02d}+05:00")
        self.assertEqual(self.ishla(), 0)
        self.assertEqual(len(self.chaqiruvlar), 3)
        self.assertEqual(len(os.listdir(os.path.join(self.d, "navbat"))), 2)

    def test_vaqt_zonasiz_xato(self):
        self.post("z", "2026-11-12T19:00")
        self.assertEqual(self.ishla(), 1)
        self.assertEqual(self.chaqiruvlar, [])


class Navbatga(Tmp):
    def test_navbatga_qoyish(self):
        import datetime
        ertaga = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d 19:00")
        os.makedirs(os.path.join(self.d, "repo"))
        mp3 = self.w("o.mp3", "ID3")
        env = dict(os.environ, NAVBAT_PAPKA=os.path.join(self.d, "repo"), NAVBAT_ZONA="+05:00", NAVBAT_GITSIZ="1")
        p = subprocess.run([sys.executable, os.path.join(S, "uz-telegram", "navbatga.py"),
                            self.w("post.txt", "**Printer oflayn** bo'lsa\n\nMatn"), "--vaqt", ertaga,
                            "--ovoz", mp3, "--kanal", "@sinov"], capture_output=True, env=env)
        self.assertEqual(p.returncode, 0, p.stderr.decode("utf-8", "replace") + p.stdout.decode("utf-8", "replace"))
        navbat = os.listdir(os.path.join(self.d, "repo", "navbat"))
        self.assertEqual(len(navbat), 1)
        self.assertTrue(navbat[0].endswith("_1900_printer-oflayn-bolsa"))
        m = oqi_json(os.path.join(self.d, "repo", "navbat", navbat[0], "meta.json"))
        self.assertTrue(m["vaqt"].endswith("19:00+05:00"))
        self.assertEqual(m["media"], ["ovoz", "o.mp3"])
        self.assertEqual(m["kanal"], "@sinov")

    def test_toplam_hammasi_yoki_hech_biri(self):
        import datetime
        ertaga = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        repo = os.path.join(self.d, "repo")
        os.makedirs(repo)
        env = dict(os.environ, NAVBAT_PAPKA=repo, NAVBAT_ZONA="+05:00", NAVBAT_GITSIZ="1")
        a, b = self.w("a.txt", "**Birinchi** post"), self.w("b.txt", "Ikkinchi post")
        yomon = self.w("yomon.json", json.dumps([{"post": a, "vaqt": f"{ertaga} 09:00", "kanal": "@s"},
                                                 {"post": b, "vaqt": "2020-01-01 09:00", "kanal": "@s"}]))
        p = subprocess.run([sys.executable, os.path.join(S, "uz-telegram", "navbatga.py"), "--toplam", yomon],
                           capture_output=True, env=env)
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse(os.path.isdir(os.path.join(repo, "navbat")) and os.listdir(os.path.join(repo, "navbat")))
        yaxshi = self.w("yaxshi.json", json.dumps([{"post": a, "vaqt": f"{ertaga} 09:00", "kanal": "@s"},
                                                   {"post": b, "vaqt": f"{ertaga} 12:00", "kanal": "@s", "ovozsiz": True}]))
        p = subprocess.run([sys.executable, os.path.join(S, "uz-telegram", "navbatga.py"), "--toplam", yaxshi],
                           capture_output=True, env=env)
        self.assertEqual(p.returncode, 0, (p.stdout + p.stderr).decode("utf-8", "replace"))
        idlar = sorted(os.listdir(os.path.join(repo, "navbat")))
        self.assertEqual(len(idlar), 2)
        self.assertTrue(oqi_json(os.path.join(repo, "navbat", idlar[1], "meta.json"))["ovozsiz"])

    def test_otgan_vaqt_rad_etiladi(self):
        os.makedirs(os.path.join(self.d, "repo"))
        env = dict(os.environ, NAVBAT_PAPKA=os.path.join(self.d, "repo"), NAVBAT_GITSIZ="1")
        p = subprocess.run([sys.executable, os.path.join(S, "uz-telegram", "navbatga.py"),
                            self.w("p.txt", "Matn"), "--vaqt", "2020-01-01 10:00", "--kanal", "@s"],
                           capture_output=True, env=env)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("kelajakda", (p.stdout + p.stderr).decode("utf-8", "replace"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
