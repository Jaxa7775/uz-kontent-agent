---
name: uz-trend
description: >-
  Yo'nalishda haqiqatan nima ishlayotganini topish: YouTube, Telegram,
  Instagram/TikTok kontentini o'z kanalining odatiy natijasiga nisbatan
  saralash va formulasini aniqlash. "Nima ishlayapti", "trend", "viral
  videolar", "raqobatchilar", "nega bu video ko'p ko'rildi" desa ishlating.
---

# uz-trend

Ko'rishlar soni kanal hajmini o'lchaydi, g'oyani emas. Bu vosita **har bir kontentni o'z kanalining
medianasiga karralik** bilan saralaydi - savolning video haqidagi yagona varianti shu.

```bash
python trend.py yigilgan.json --min 2.0
python trend.py postlarim.csv --past         # o'z kanalingiz: eng yaxshi va eng yomon
```

(Windows'da `python`, macOS/Linux'da `python3`.)

## Ma'lumot yig'ish

Har bir manbadan **kamida 4 ta element** kerak, aks holda mediana hech narsani anglatmaydi - vosita
o'sha manbani tashlab, buni aytadi. 10-30 ta bo'lsa yaxshi.

- **Qo'lda ro'yxat** - eng toza yo'l. Kanal sahifasini ochib, sarlavha va ko'rishlarni yozib olish.
- **YouTube Data API** - foydalanuvchining o'z API kaliti bilan, rasmiy yo'l.
- **yt-dlp** (`yt-dlp --flat-playlist -J <kanal havolasi>`) - qulay, natijasi to'g'ridan-to'g'ri
  o'qiladi. Lekin YouTube shartlari avtomatik yig'ishni cheklaydi; buni foydalanuvchiga ayting,
  qaror unda.
- **Telegram** - ochiq kanallarning so'nggi postlari va ko'rishlari `t.me/s/<kanal>` sahifasida
  ko'rinadi; TGStat kabi xizmatlar ham bor.
- **Instagram/TikTok** - profil sahifasidagi ko'rishlar, qo'lda.

Faqat ochiq ma'lumot. Hech qachon foydalanuvchi akkauntiga kirmang va parol so'ramang.

Format (JSON yoki shu ustunli CSV):

```json
[{"manba": "...", "matn": "sarlavha yoki birinchi qator", "korishlar": 41200, "platforma": "youtube"}]
```

## Natijani o'qish

Karralik - signal. Formula qatori - [formulalar.json](../uz-ssenariy/formulalar.json) bo'yicha MATN
haqidagi xulosa, video nega ishlagani haqida da'vo emas. Taqdim etganda shuni ayting.

## Nimani qaytarish kerak

- karraligi bilan eng yaxshi beshtasi va har birining formulasi
- ularni birlashtirgan BITTA tuzilmaviy narsa (masalan: "hammasi natijani birinchi kadrda
  ko'rsatadi", "hammasi aniq dastur versiyasini aytadi")
- keyin qiyinroq qator: shulardan qaysi birini foydalanuvchi SHU HAFTA, o'z ovozida, bor narsasi
  bilan qila oladi. Nusxa emas - tuzilmani oling, mazmun o'ziniki bo'lsin.

## Darvoza

Bu skill hech narsani o'zi joylamaydi: u yozadi, siz joylaysiz. Har bir natija foydalanuvchi nusxa
oladigan blok bilan tugaydi, oxirgi qator esa doim savol: **Joylaymizmi yoki o'zgartiramizmi?**
