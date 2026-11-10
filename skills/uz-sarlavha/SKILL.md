---
name: uz-sarlavha
description: >-
  O'zbekcha sarlavha va muqova (prevyu, thumbnail) matnini bitta juftlik
  sifatida yozish va tekshirish - YouTube, Reels/Shorts/TikTok va Telegram
  uchun. Uzunlik, takror, noaniq so'zlar, tutuq belgisi va yozuv aralashuvi
  tekshiriladi. "Sarlavha o'yla", "nima deb nomlay", "prevyu matni", "muqova",
  "CTR past", "videoni qayta nomlash" desa ishlating.
---

# uz-sarlavha

Sarlavha va muqova - BITTA birlik. Ularni alohida yozish - ko'p sarlavhalar ishlamasligining sababi:
muqova sarlavhani takrorlaydi va bosish maydonining yarmi bir gapni ikki marta aytadi.

```bash
python sarlavha.py --sarlavha "..." --muqova "3 SO'Z"                 # YouTube
python sarlavha.py --platforma reels --sarlavha "..." --muqova "..."   # Reels/Shorts/TikTok
python sarlavha.py sarlavhalar.txt                                     # har qatorda bittasi, saralanadi
```

(Windows'da `python`, macOS/Linux'da `python3`.)

## Boshlashdan oldin

1. `~/.claude/kontent-uz/yonalish.md` va `~/.claude/kontent-uz/ovoz.md` ni o'qing. `ovoz.md` yo'q
   yoki bo'sh bo'lsa, **uchta o'z videosi yoki postini** so'rang, ovozini aniqlab, faylni yozing.
2. Hech qachon raqam, natija yoki manba to'qimang. Sarlavhadagi raqam videoda ko'rinishi shart.
3. `ovoz.md` dagi yozuvda yozing (standart: lotin).

## Vosita tekshiradigan qoidalar va sababi

- **YouTube sarlavhasi 100 belgigacha.** Qancha ko'rinishi qurilmaga bog'liq; vosita taxminiy
  chegaralarni ishlatadi (kompyuter ~60, telefon ~40) - asosiy so'z boshida bo'lsin.
- **Muqova sarlavhani takrorlamasin.** Boshqa so'zlar, bir xil va'da. Vosita qo'shimchalarni hisobga
  oladi: "printer" va "printerni" - bir so'z.
- **Muqovada uchtadan ko'p so'z yo'q.** Lenta o'lchamida to'rtinchi so'z o'qilmaydi. O'zbek so'zlari
  uzun bo'ladi - bu yanada muhim.
- **Raqam, nom yoki sana** har qanday sifatdan kuchli: "ajoyib", "dahshat", "zo'r" o'rniga "3
  soniyada", "Excel 2021", "Windows 11".
- **Ikkitadan ko'p KATTA HARFLI so'z** spamga o'xshaydi.
- **Tutuq belgisi bir xil** (`'` yoki `ʻ`, aralash emas) va **yozuv bir xil** (lotin yoki kirill).
  Brend nomlari (Excel, Windows) bundan mustasno.

## O'nta yozing, ikkitasini qoldiring

O'nta sarlavha yozing, hammasini `sarlavha.py` dan o'tkazing, eng yaxshi uchtasini baholari va har
biridagi aniq muammo bilan ko'rsating. G'olib uchun muqova topshirig'ini yozing:

- **Muqovadagi uch so'z** (sarlavhada yo'q so'zlar).
- **Asosiy tasvir.** Darslarda eng kuchlisi - natija yoki "oldin/keyin": xato oynasi va ishlab ketgan
  holat, tartibsiz va tozalangan jadval. Yuz ko'rsatilsa - his-tuyg'u aniq bo'lsin.
- **Kontrast.** Lenta o'lchamida (telefonda kichik) o'qilishi uchun fon oddiy, matn yirik.

Reels/TikTok uchun "muqova" - videoning birinchi kadri yoki tanlangan muqova kadri; unda ham uch so'z
qoidasi ishlaydi.

## Darvoza

Bu skill hech narsani o'zi joylamaydi: u yozadi, siz joylaysiz. Har bir natija foydalanuvchi nusxa
oladigan blok bilan tugaydi, oxirgi qator esa doim savol: **Joylaymizmi yoki o'zgartiramizmi?**
