---
name: uz-tahlil
description: >-
  O'z natijalaringizni o'qish: YouTube retention (auditoriyani ushlab qolish)
  faylidan tomoshabin aynan qayerda ketishini topish, va Telegram/Instagram
  postlaringizdan eng yaxshi va eng yomon chiqqanlarini ajratish. "Nega
  oxirigacha ko'rishmayapti", "retention past", "statistikani tahlil qil",
  "qaysi postlar ishladi" desa ishlating.
---

# uz-tahlil

Retention grafigi - YouTube beradigan yagona halol fikr-mulohaza. Deyarli hech kim uni eksport
qilmaydi.

```bash
python retention.py video.csv --davomiylik 615                       # bitta video
python retention.py video.csv --davomiylik 615 --transkript video.srt  # ketish lahzasida nima aytilgan
python retention.py v1.csv v2.csv v3.csv                             # o'z videolaringizni solishtirish
python ../uz-trend/trend.py postlarim.csv --past                     # o'z postlaringiz: eng yaxshi va eng yomon
```

(Windows'da `python`, macOS/Linux'da `python3`.)

## Ma'lumotni olish

- **YouTube:** YouTube Studio -> Analitika -> kerakli video -> auditoriyani ushlab qolish grafigi ->
  eksport (yuklab olish). Menyu nomlari o'zgarib turadi; topa olmasa, foydalanuvchidan ekran rasmini
  so'rang. Video uzunligini (`--davomiylik`, soniyada) ham so'rang - fayl foizda bo'lsa, usiz
  "birinchi 30 soniya"ni hisoblab bo'lmaydi.
- **Telegram:** har bir postning ko'rishlar soni (ko'z belgisi) yoki kanal statistikasi. Oddiy CSV
  yetarli: `matn,korishlar` (+ `sana`). `manba` ustuni bo'lmasa, hammasi bitta manba hisoblanadi.
- **Instagram/TikTok:** professional akkaunt statistikasidan har bir Reels uchun qamrov yoki
  ko'rishlar - xuddi shu CSV ko'rinishida.

## Uchta alohida muammo

- **BOSHLANISH** - birinchi 30 soniyada yo'qotilgan tomoshabin. Bu doim birinchi tuzatiladigan narsa
  va u doim ssenariyning birinchi 15 soniyasi (`/uz-ssenariy`), montaj emas.
- **KESKIN** - bitta joyda keskin tushish. Bu lahza: signalsiz mavzu almashishi, uzun tayyorgarlik,
  reklama, yuklanishni kutish. `--transkript` bilan vosita o'sha joyda nima aytilganini chiqaradi - shu
  hisobotni "qiziq"dan "amaliy"ga aylantiradi.
- **SEKIN** - o'rtadagi bir tekis oqish. Bu temp. Yechim - qayta yozish emas, qisqartirish
  (`/uz-montaj`).

## Umumiy me'yor yo'q

"Yaxshi retention - X%" degan raqam bermang: u video uzunligi, mavzu va auditoriyaga bog'liq, va
bizda ishonchli umumiy raqam yo'q. O'rniga **foydalanuvchining o'z videolarini solishtiring**: eng
yaxshi boshlangan va eng yomon boshlangan videoning birinchi 15 soniyasini yonma-yon o'qing. Farq -
javob.

## Nimani qaytarish kerak

Eng katta BITTA oqishni nomlang va unga bitta o'zgartirish. Beshta ro'yxat emas. Qolganini - faqat
so'ralsa. Agar boshlanish yaxshi va o'rta tekis bo'lsa, video yaxshi, muammo - o'rash (sarlavha,
muqova) ekanini ayting va `/uz-sarlavha` ga yuboring.

Postlar uchun: eng yaxshi 3 ta va eng yomon 3 ta, ularni ajratib turgan BITTA narsa (tur, birinchi
qator, mavzu, vaqt) va keyingi haftaga bitta xulosa.

## Darvoza

Bu skill hech narsani o'zi joylamaydi va hech qayerga kirmaydi: u siz bergan fayllarni o'qiydi.
Natija nusxa olinadigan blok bilan tugaydi, oxirgi qator esa doim savol: **Joylaymizmi yoki
o'zgartiramizmi?**
