---
name: uz-telegram
description: >-
  O'zbekcha Telegram kanal posti: qo'llanma, tezkor maslahat, so'rovnoma,
  video anonsi, savol-javob. Birinchi qator, format, uzunlik chegaralari
  tekshiriladi. "Telegram post yoz", "kanalga post", "anons", "so'rovnoma
  tuz", "kanal uchun matn" desa ishlating.
---

# uz-telegram

Telegram - yo'nalishdagi "uy". Qisqa video tanishtiradi, YouTube o'rgatadi, Telegram ushlab qoladi:
fayllar, shablonlar, savol-javob, yangi video haqida xabar shu yerda.

```bash
python ../uz-sarlavha/sarlavha.py --platforma telegram --fayl post.txt          # matnli post
python ../uz-sarlavha/sarlavha.py --platforma telegram --fayl post.txt --rasm   # rasm/video izohi
```

## Boshlashdan oldin

1. `~/.claude/kontent-uz/yonalish.md` va `~/.claude/kontent-uz/ovoz.md` ni o'qing. `ovoz.md` yo'q
   yoki bo'sh bo'lsa, **uchta o'z postini** so'rang, ovozini aniqlab, faylni yozing.
2. Hech qachon raqam, natija yoki manba to'qimang.
3. `ovoz.md` dagi yozuvda yozing. Auditoriyaning bir qismi kirill o'qisa, ikkala variantni bering:
   `python ../uz-seo/imlo.py --kirill "matn"`.

## Post turlari

1. **Qo'llanma** - qadam-baqadam, raqamlangan, oxirida fayl yoki shablon. Eng ko'p saqlanadigan
   (va ulashiladigan) tur.
2. **Tezkor maslahat** - bitta muammo, bitta yechim, 3-6 qator.
3. **So'rovnoma** - keyingi video mavzusini auditoriya tanlaydi. Variantlar aniq va 4 tadan oshmasin.
4. **Video anonsi** - YouTube'dagi yangi video: nima o'rganiladi (bitta gap), kimga kerak, havola.
   "Yangi video chiqdi!" emas, videodan olinadigan foyda.
5. **Savol-javob** - izohlarda ko'p takrorlangan savolga javob. Savol egasiga minnatdorchilik.
6. **Sahna ortidan** - qanday ishlayapsiz, qaysi dasturda, nima chiqmadi. Ishonch quradi.

## Qoidalar

- **Birinchi qator - sarlavha.** Bildirishnomada va kanal ro'yxatida asosan shu ko'rinadi. U
  yolg'iz o'zi ham postni ochishga sabab bo'lsin.
- **Qisqa xatboshilar.** Telefonda 600 belgidan uzun xatboshi devorga aylanadi.
- **Format kam va maqsadli:** **qalin** - bitta-ikkita asosiy gap uchun; `kod` - tugmalar birikmasi va
  buyruqlar uchun (`Win + Shift + S`); spoiler - viktorina javobi uchun.
- **Chegaralar:** matnli xabar 4096 belgi, rasm yoki video izohi (oddiy akkauntda) 1024 belgi. Rasm
  bilan uzun post kerak bo'lsa - rasmni alohida, matnni alohida yuboring.
- **Hashtag** - kanal ichidagi rubrikalar uchun (`#excel #word #ai`), tutuq belgisisiz:
  `python ../uz-seo/imlo.py --teg "o'qituvchi"`.
- **Izohlar** uchun kanalga muhokama guruhi ulangan bo'lishi kerak. Guruh yo'q bo'lsa, foydalanuvchiga
  ayting.
- Telegram Desktop'da `**qalin**` va `` `kod` `` belgilari yuborishda avtomatik formatlanadi; telefonda
  matnni belgilab, formatni menyudan tanlang.

## Ritm

Necha marta post qilishni `/uz-reja` foydalanuvchining vaqtiga qarab belgilaydi. Bu yerda bitta qoida:
obunachini charchatadigan va o'zingiz uzoq ushlab tura olmaydigan ritm - eng yomon ritm.

## Nimani qaytarish kerak

- tayyor post (nusxa olish uchun blokda), kerak bo'lsa kirill varianti ham
- `sarlavha.py` natijasi: birinchi qator va uzunlik
- qaysi tur va nega aynan shu (bitta qator)
- rasm yoki fayl kerak bo'lsa - nima bo'lishi kerakligi (masalan: "Excel shablon, 2 varaq: ...")

## Kanalga joylash (ixtiyoriy)

Foydalanuvchi botini sozlagan bo'lsa (`~/.claude/kontent-uz/telegram.json`), postni shu papkadagi
`joyla.py` bilan kanalga yuborish mumkin:

```bash
python joyla.py --tekshir                        # bot kanalda admin va post joylay oladimi
python joyla.py post.txt [--rasm r.jpg | --fayl f.xlsx | --ovoz o.mp3]   # faqat ko'rib chiqish
python joyla.py post.txt [--rasm ... | --fayl ... | --ovoz ...] --yubor   # yuborish
```

Ovozli post so'ralsa: avval foydalanuvchining o'z ovozini taklif qiling (ishonchliroq). Sun'iy ovoz
xohlasa - `edge-tts` (`uz-UZ-SardorNeural` yoki `uz-UZ-MadinaNeural`), og'zaki matnni alohida yozing
(inglizcha nomlarni o'zbekcha talaffuzda: "Eksel", "Vord"), ikkala ovozni yasab, foydalanuvchi
eshitib tanlaganidan keyingina yuboring. Erkak yoki ayol ovozini o'zingiz tanlamang.

Qat'iy tartib:

1. Postni faylga yozing va avval `--yubor` qo'shmasdan ishga tushiring. Chiqqan ko'rib chiqishni
   (uzunlik, xabarlar soni, kanalda ko'rinadigan matn) foydalanuvchiga ko'rsating.
2. `--yubor` ni faqat foydalanuvchi AYNAN SHU postga "ha" degandan keyin ishga tushiring. Matn
   o'zgarsa - qaytadan ko'rib chiqish va qaytadan tasdiq. Bitta tasdiq bitta post uchun.
3. Yuborilgandan keyin havolani bering. Tokenni hech qachon chiqarmang va so'ramang.

Kanalga chiqqan postni hamma ko'radi. Xato post o'chirilsa ham, obunachilarga bildirishnoma ketib
bo'lgan bo'ladi.

## Rejali joylash (kompyuter o'chiq bo'lsa ham)

Foydalanuvchi navbat reposini sozlagan bo'lsa (`telegram.json` dagi `navbat_papka`, shablon:
`templates/kanal-navbat/`), postni belgilangan vaqtga navbatga qo'yish mumkin. GitHub Actions har
soatda (`:07`, UTC) tekshiradi va vaqti kelganini joylaydi.

```bash
python navbatga.py post.txt --vaqt "2026-11-12 19:00" [--ovoz o.mp3 | --rasm r.jpg | --fayl f.xlsx]
python navbatga.py --royxat          # navbat, oxirgi joylanganlar, xatolar
python navbatga.py --bekor <id>      # joylanmaguncha olib tashlash
```

- Navbatga qo'yish = joylashga tasdiq. Avval `joyla.py` bilan ko'rib chiqishni ko'rsating, keyin
  foydalanuvchi AYNAN SHU post va SHU vaqtga "ha" desa, navbatga qo'ying.
- Vaqt foydalanuvchining mahalliy vaqti (`vaqt_zonasi`, standart Toshkent +05:00). Soat boshiga
  qo'yishni tavsiya qiling: post taxminan 5-40 daqiqa kechikib chiqadi.
- Matnda "bugun", "hozir" kabi so'zlar bo'lsa, ular joylanish kuniga to'g'ri kelishini tekshiring.
- Vaqtidan 6 soatdan ko'p kechikkan post yuborilmaydi (`kechikkan/`), xato bergani qayta urinilmaydi
  (`xato/`). `--royxat` bularni ko'rsatadi.

## Darvoza

Bu skill foydalanuvchi tasdiqlamaguncha hech narsani joylamaydi. Har bir natija foydalanuvchi nusxa
oladigan blok bilan tugaydi, oxirgi qator esa doim savol: **Joylaymizmi yoki o'zgartiramizmi?**
