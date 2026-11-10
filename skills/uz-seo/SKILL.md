---
name: uz-seo
description: >-
  Qidiruv uchun o'zbekcha matn: YouTube tavsifi, boblar (timestamps) va
  teglar; Instagram/TikTok izohi va hashtaglar; Telegram kanal nomi va
  tavsifi. Lotin/kirill va tutuq belgisi variantlari. "Tavsif yoz", "teglar",
  "hashtag", "SEO", "boblar", "timestamps", "qidiruvda chiqsin", "kirillga
  o'gir" desa ishlating.
---

# uz-seo

Qidiruv - doimiy darslar uchun katta dastak: "printer oflayn" ni odamlar yil davomida qidiradi.
Faqat obunachilar lentasi uchun mo'ljallangan video uchun buni ayting va kuchni `/uz-sarlavha` ga
sarflang.

```bash
python boblar.py transkript.srt --soni 7              # YouTube boblari, qoidalar tekshiriladi
python imlo.py --variant "o'qituvchi uchun Excel"     # qidiruvdagi turli yozilishlar
python imlo.py --teg "excel darslari" "o'qituvchi"    # hashtaglar (tutuq belgisisiz)
python imlo.py --kirill "matn"   |   python imlo.py --lotin "матн"
python imlo.py --tekshir post.txt                     # tutuq belgisi va yozuv aralashuvi
```

(Windows'da `python`, macOS/Linux'da `python3`.)

## Boshlashdan oldin

1. `~/.claude/kontent-uz/yonalish.md` va `~/.claude/kontent-uz/ovoz.md` ni o'qing.
2. Hech qachon raqam, natija yoki manba to'qimang.
3. `ovoz.md` dagi yozuvda yozing (standart: lotin).

## O'zbek tilida qidiruvning o'ziga xosligi

Bitta so'zni odamlar `o'qituvchi`, `o`qituvchi`, `oʻqituvchi`, `oqituvchi` va `ўқитувчи` deb yozadi.
Bular qidiruvda turli natija berishi mumkin. Shuning uchun:

- sarlavha va tavsifda BITTA yozilishni izchil ishlating;
- boshqa variantlarni teglarga qo'ying (`imlo.py --variant`) - YouTube teglarni aynan ko'p xato
  yoziladigan so'zlar uchun foydali deb biladi;
- texnik mavzularda ko'pchilik ruscha qidiradi ("как подключить принтер"). Ruscha so'rovlarni nishonga
  olish-olmaslik - foydalanuvchining qarori; so'rang.

## YouTube tavsifi

- **Birinchi ikki qator** - "...yana" dan oldin ko'rinadigan va qidiruvda chiqadigan yagona qism.
  Video nima berishini odam qidiruvga yozadigan so'zlar bilan ayting.
- Keyin havola: Telegram kanal (fayl, shablon) - yuqorida, ko'rinib turgan joyda.
- Keyin boblar (`boblar.py`). YouTube qoidasi: 0:00 dan boshlanadi, kamida 3 ta, har biri kamida 10
  soniya. Vosita sarlavhalarni qoralama qilib beradi - har birini bo'lim va'dasi sifatida, 3-5 so'zda
  qayta yozing.
- Keyin uzun qism: nima o'rgatiladi, kimga, qaysi dastur versiyasida.

## Teglar, halol

Teglar kuchsiz signal va YouTube buni o'zi aytadi. Ulardan farqlash uchun foydalaning: yozilish
variantlari, dastur nomlari, qisqartmalar. O'n beshta yetarli. Aloqasiz teglar bilan to'ldirish
qoidalarga zid.

## Instagram / TikTok izohi

- Birinchi qator - kalit so'z bilan (ikkala ilovada ham ichki qidiruv izoh matnini o'qiydi).
- Havola bosilmaydi: "to'liq dars - profildagi havolada".
- 3-5 ta aniq hashtag, ko'p emas. **Hashtagda tutuq belgisi ishlamaydi**: `#o'qituvchi` aslida `#o`
  bo'lib qoladi. `imlo.py --teg` to'g'ri variantni beradi.

## Telegram

- Kanal nomi va @username - Telegram global qidiruvi ochiq kanallarni shular bo'yicha topadi. Nomda
  yo'nalish so'zi bo'lsin ("Kompyuter darslari | ...").
- Kanal tavsifida: kimga, nima, qaysi rubrikalar.
- Kanal ichidagi navigatsiya uchun rubrika hashtaglari: `#excel #word #ai #printer`.

## So'rov testi

Topshirishdan oldin bu kontent yutishi kerak bo'lgan uchta qidiruv so'rovini yozing - odam qanday
yozsa shunday (tutuq belgisisiz variant bilan). Sarlavha va tavsifning birinchi ikki qatorida o'sha
so'zlar borligini tekshiring. Bo'lmasa, muammo tavsifda emas, sarlavhada.

## Darvoza

Bu skill hech narsani o'zi joylamaydi: u yozadi, siz joylaysiz. Har bir natija foydalanuvchi nusxa
oladigan blok bilan tugaydi, oxirgi qator esa doim savol: **Joylaymizmi yoki o'zgartiramizmi?**
