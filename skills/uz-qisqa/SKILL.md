---
name: uz-qisqa
description: >-
  YouTube Shorts, Instagram Reels va TikTok uchun o'zbekcha qisqa video
  ssenariysi - yangi g'oyadan yoki uzun video transkriptidan kesib. Ekrandagi
  matn, birinchi 2 soniya, aylanma yakun. "Reels yoz", "shorts qil", "tiktok
  uchun", "qisqa video", "uzun videoni bo'lib ber" desa ishlating.
---

# uz-qisqa

Qisqa video - uzun videoning eng zo'r lahzasi emas. U **atrofidagi videosiz ham tushunarli**
bo'lgan lahza. Bunday lahzalar ancha kam.

## Boshlashdan oldin

1. `~/.claude/kontent-uz/yonalish.md` va `~/.claude/kontent-uz/ovoz.md` ni o'qing. `ovoz.md` yo'q
   yoki bo'sh bo'lsa, **uchta o'z videosi yoki postini** so'rang, ovozini aniqlab, faylni yozing.
2. Hech qachon raqam, natija yoki manba to'qimang.
3. `ovoz.md` dagi yozuvda yozing (standart: lotin).

## Ikki rejim

**A. Yangi g'oyadan.** Bitta muammo, bitta yechim. Rubrika: "Tezkor yechim" yoki "AI amaliyoti".

**B. Uzun videodan.** Transkriptni o'qing va 20-60 soniyalik shunday bo'laklarni toping, ularda
uchala shart bajarilsin:

1. To'liq fikr bilan boshlanadi. Birinchi gap oldingi daqiqaga muhtoj bo'lsa - bu qisqa video emas.
2. Ichida burilish bor - da'vo, keyin uni isbotlaydigan yoki murakkablashtiradigan narsa.
3. Gap bilan tugaydi, so'nib qolmaydi.

Nomzodlarni saralang va eng yaxshi beshtasini vaqti va birinchi gapi bilan ko'rsating - shunda
foydalanuvchi butun transkriptni o'qimasdan birini rad eta oladi.

## Har birini yozish

- **0-2 soniya: ekrandagi matn.** Ko'pchilik ovozsiz ko'radi. Ekrandagi matn gapirilgan gapdan
  boshqa so'zlarda bo'lsin, 3-5 so'z.
- **YANGI birinchi gap** (B rejimda). Uzun videodagi gap kontekstni taxmin qiladi, bu tomoshabinda
  kontekst yo'q. Almashtiruvchini yozing va `../uz-ssenariy/hook_baho.py` dan o'tkazing. Qisqa video
  uchun qisqaroq oraliq: `python ../uz-ssenariy/hook_baho.py --max 14 --hook "..."`.
- **Birinchi kadrda natija.** Darsda: tayyor jadval, ishlab ketgan printer, tozalangan rasm. Keyin
  "qanday".
- **Aylanma yakun.** Oxirgi gap birinchi gapga ulanadigan qilib yozing, shunda qayta ko'rish tabiiy.
- **Vertikal kadr.** Ekran yozuvi 16:9 - telefonda mayda. Faqat kerakli qismini kesib, kattalashtiring;
  sichqoncha kursorini ko'rinadigan qiling; matn katta va ekran markazida (pastki qismini platforma
  tugmalari yopadi).

## Platformalar farqi

Bitta video uchala platformaga ketadi, lekin har biriga alohida:

- **izohning birinchi qatori** - har platformada boshqacha (`/uz-seo` yozadi);
- **havola** - Instagram va TikTok izohida havola bosilmaydi, shuning uchun "to'liq dars - profildagi
  havolada"; YouTube Shorts'da tegishli uzun videoni bog'lash mumkin;
- **davomiylik** - platformalar cheklovi o'zgarib turadi, joylashdan oldin ilovada tekshiring. Bitta
  tezkor yechim odatda cheklovdan ancha qisqa bo'ladi - uzaytirmang.

## Nimani qaytarish kerak

Har bir qisqa video uchun: ekrandagi matn (0-2 s), gapiriladigan matn, kadrma-kadr `[EKRANDA: ...]`,
aylanma yakun, hook bahosi, va B rejimda - uzun videodagi aniq vaqt oralig'i.

## Darvoza

Bu skill hech narsani o'zi joylamaydi: u yozadi, siz joylaysiz. Har bir natija foydalanuvchi nusxa
oladigan blok bilan tugaydi, oxirgi qator esa doim savol: **Joylaymizmi yoki o'zgartiramizmi?**
