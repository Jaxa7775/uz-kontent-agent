---
name: uz-montaj
description: >-
  Xom yozuv transkriptidan montaj ro'yxati (EDL): uzun pauzalar, "ee",
  "xullas", "koroche" kabi parazit so'zlar va qayta boshlangan gaplar, vaqti
  bilan. Ekran yozuvidagi jim namoyishlarni himoya qiladi. "Montaj qil",
  "bo'sh joylarni kes", "videoni qisqartir", "ko'p gapirib yubordim" desa
  ishlating.
---

# uz-montaj

Vaqt belgili transkriptdan montaj ro'yxati. U kesishlarni chiqaradi, kesishni siz qilasiz.

```bash
python montaj.py transkript.srt                       # srt, vtt yoki whisper json
python montaj.py transkript.srt --chegara 0.35 --json
python montaj.py transkript.srt --himoya 1:20-2:05    # jim namoyish qismini kesmaslik
```

(Windows'da `python`, macOS/Linux'da `python3`.)

Transkript yo'qmi? Avval uni oling: `whisper` yoki `faster-whisper` o'zbek tilini qo'llab-quvvatlaydi
(xatolar bo'ladi, lekin vaqt belgilari montaj uchun yetarli), yoki montaj dasturidagi avtomatik
subtitr funksiyasi. Vaqtlarni taxmin qilmang.

## Nimani topadi

- **JIM** - chegaradan uzun pauzalar, O'RTASIDAN kesiladi, ikki tomonda nafas qoladi. Gapga yopishtirib
  kesish ovozni "bo'g'ilgan" qiladi.
- **PARAZIT** - faqat "ee", "mm", "xullas", "ya'ni", "mana", "haligi", "koroche", "tipa", "vot" kabi
  so'zlardan iborat qatorlar (lotin va kirillda).
- **TAKROR** - qayta boshlangan gap. Oxirgi HAQIQIY nutq qatori bilan solishtiriladi, chunki ko'p
  dubllar orasida "ee" bo'ladi.

YouTube avtomatik subtitrlaridagi aylanma qatorlar (har qator oldingisini takrorlaydi) avval
tozalanadi - aks holda har qator soxta TAKROR bo'lib chiqardi. Ustma-ust kesishlar ikki marta
sanalmaydi.

## Ekran yozuvi darslari uchun muhim

Darsda jimlik har doim ham bo'sh joy emas: sichqoncha bilan sozlama ko'rsatilayotgan, yuklanish
kutilayotgan, natija ko'rsatilayotgan joylar ham jim. Montajdan oldin foydalanuvchidan shunday
oraliqlarni so'rang va `--himoya` bilan bering. Bilmasa, ro'yxatdagi uzun JIM kesishlarni (2 s dan
uzun) alohida ajratib, "bu yerda ekranda nima bo'lyapti?" deb so'rang.

Uzun kutishni (yuklanish, o'rnatish) butunlay kesish o'rniga tezlashtirish (2x-8x) ko'pincha
yaxshiroq - tomoshabin jarayon bo'lganini ko'radi.

## Nima qilmaydi

Mediaga tegmaydi. B-roll, musiqa haqida fikri yo'q. Hisobotdagi "30% qisqaroq" - NUTQ bo'yicha 30%;
video ichida uzun jim namoyish bo'lsa, bu raqam noto'g'ri. Pastdagi uzunlikka ishonishdan oldin
videoga solishtirib ko'ring.

## Nimani qaytarish kerak

- kesishlar ro'yxati (vaqt, tur, sabab) - montaj dasturiga qo'lda kiritish uchun qulay tartibda
- jami olinadigan vaqt va natijaviy uzunlik
- foydalanuvchi tekshirishi kerak bo'lgan uzun JIM joylar ro'yxati

## Darvoza

Bu skill hech narsani o'zi joylamaydi va mediaga tegmaydi: u ro'yxat yozadi, siz kesasiz. Natija
nusxa olinadigan blok bilan tugaydi, oxirgi qator esa doim savol: **Joylaymizmi yoki o'zgartiramizmi?**
