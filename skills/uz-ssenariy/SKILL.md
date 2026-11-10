---
name: uz-ssenariy
description: >-
  Xom g'oyadan o'zbekcha YouTube video ssenariysi: 18 formuladan hook
  variantlari, baholangan, keyin [EKRANDA] belgilari bilan to'liq ssenariy.
  Foydalanuvchi "ssenariy yoz", "video matni", "hook", "nima deb boshlay",
  "keyingi videoni yoz" desa yoki yozib olishga tayyor-u birinchi 15 soniyasi
  yo'q bo'lsa ishlating.
---

# uz-ssenariy

Bitta g'oyadan oxirigacha ko'riladigan ssenariy.

Shu papkada ikkita fayl bor va ikkalasi ham haqiqatan ishlaydi. Ulardan foydalaning, hookni ko'z
bilan chamalamang.

```bash
python hook_baho.py hooklar.txt              # hook variantlarini saralash
python hook_baho.py --hook "bitta gap"       # bittasini baholash
```

(Windows'da `python`, macOS/Linux'da `python3`.)

## Boshlashdan oldin

1. `~/.claude/kontent-uz/yonalish.md` (yo'nalish, auditoriya, rubrikalar, nimalar qilinmaydi) va
   `~/.claude/kontent-uz/ovoz.md` (foydalanuvchi qanday gapiradi) ni o'qing. `ovoz.md` yo'q yoki
   bo'sh bo'lsa, **uchta o'z videosi yoki postini** so'rang, ulardan ovozini aniqlab, faylni yozing.
   Begona ovozda yozilgan ssenariy yo'qidan yomon: uni kamerada ovoz chiqarib aytish kerak.
2. Hech qachon raqam, natija yoki manba to'qimang. Raqam kerak bo'lsa-yu, sizda bo'lmasa, so'rang
   yoki gapni raqamsiz yozing.
3. `ovoz.md` dagi yozuvda yozing (standart: lotin). Kirill kerak bo'lsa:
   `python ../uz-seo/imlo.py --kirill "matn"`.

## Tuzilma

**Birinchi 15 soniya - butun ish shu.** U uchta narsani qiladi, aks holda video "oqadi": sarlavha
va'dasini tasdiqlaydi, tomoshabin o'zi yopa olmaydigan savol ochadi, natija borligini isbotlaydi.

1. **Hook.** [formulalar.json](formulalar.json) dan BESHTA variant yozing, `hook_baho.py` dan
   o'tkazing, eng yaxshi ikkitasini baholari bilan foydalanuvchiga ko'rsating. Hech qachon bitta
   hook bermang.
2. **Kirish (0:15-0:45).** Video nima qilishini bitta gapda ayting va darhol boshlang. Uzun
   salomlashish ("Assalomu alaykum, hurmatli obunachilar, kanalimizga xush kelibsiz...") va boshida
   "obuna bo'ling" - 0:30 dagi keskin tushishning eng ko'p uchraydigan sababi. Salom kerak bo'lsa -
   bitta qisqa gap, hookdan keyin.
3. **Asosiy qism.** Har bir bo'lakda bitta g'oya. Har bir bo'lakka EKRANDA nima borligini yozing,
   faqat aytiladigan gapni emas. Darslarda bu majburiy: qaysi oyna ochiq, qaysi tugma bosiladi,
   qayerga yaqinlashtiriladi (zoom), qaysi tugmalar birikmasi ekranda yoziladi.
4. **Natija.** Hook va'da qilgan narsani aniq bering va berayotganingizni ayting: "mana shu fayl,
   u Telegram kanalda".
5. **Yakun.** Bitta chaqiriq, uchta emas. Yo'nalishda Telegram - "uy", shuning uchun eng tabiiy
   chaqiriq: "shu darsning fayli/qo'llanmasi Telegram kanalda".

## Dars videolari uchun qoidalar

- Avval yakuniy natijani 3-5 soniya ko'rsating, keyin qanday qilinishini.
- Dastur versiyasini ayting (Windows 10/11, Office 2016/2021, telefon modeli) - boshqa versiyada
  menyu boshqacha bo'lsa, tomoshabin adashadi va ketadi.
- Qadamlarni raqamlang va har bir qadamni ekranda ham yozing.
- Pirat dastur, aktivator, "crack" ko'rsatmang - `yonalish.md` dagi "nimalarni qilmaymiz"ga qarang.

## Nimani qaytarish kerak

- eng yaxshi ikkita hook va ularning baho panellari
- ssenariy, bo'lakma-bo'lak, har bo'lakda `[EKRANDA: ...]`
- davomiylik: so'zlar soni / `ovoz.md` dagi gapirish tezligi. Tezlik yozilmagan bo'lsa, taxmin
  qilmang - foydalanuvchidan bir daqiqalik matnni ovoz chiqarib o'qib, so'zlarni sanashni so'rang.
- g'olib hook qaysi formulani ishlatgani va nega aynan shu g'oyaga mosligi - bitta qator
- ssenariydan qisqa video (Shorts/Reels/TikTok) bo'la oladigan 2-3 lahza, vaqti bilan - keyin
  `/uz-qisqa` ularni yozadi

## Darvoza

Bu skill hech narsani o'zi joylamaydi: u yozadi, siz joylaysiz. Har bir natija foydalanuvchi nusxa
oladigan blok bilan tugaydi, oxirgi qator esa doim savol: **Joylaymizmi yoki o'zgartiramizmi?**
