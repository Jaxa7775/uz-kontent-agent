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


if __name__ == "__main__":
    unittest.main(verbosity=1)
