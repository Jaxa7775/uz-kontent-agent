---
name: uz-audit
description: >-
  YouTube kanal, Telegram kanal va Reels/TikTok profilini boshidan oxirigacha
  audit qilish va BITTA eng muhim tuzatishni topish. "Kanalimni tekshir",
  "nega o'smayapti", "auditoriya ko'paymayapti", "videolarimni ko'rib chiq"
  desa yoki kanal havolasi tashlansa ishlating.
---

# uz-audit

Yigirmata muammoni sanaydigan audit - muhim bittasidan qochish usuli. Bu audit BITTA tuzatish bilan
tugaydi.

## Boshlashdan oldin

1. `~/.claude/kontent-uz/yonalish.md` va `~/.claude/kontent-uz/ovoz.md` ni o'qing.
2. Hech qachon raqam to'qimang. Ko'rmagan statistikangizni bilgandek gapirmang - so'rang.

## Nimaga qarash kerak, shu tartibda

1. **Oxirgi o'nta YouTube sarlavhasi - to'plam sifatida.** Kanal sahifasidagidek ro'yxat qilib o'qing.
   Ular har xil narsa va'da qiladimi? Hammasini `../uz-sarlavha/sarlavha.py` dan o'tkazing. Hamma
   sarlavha bir xil shaklda bo'lsa - bu format muammosi, sarlavha muammosi emas.
2. **Muqovalar - lenta o'lchamida.** Kichraytiring. Nima qoladi? Uchtasi o'qilmasa - tuzatish shu va
   hozircha boshqa hech narsa muhim emas.
3. **Oxirgi uchta videoning birinchi 15 soniyasi.** Transkript qiling va
   `../uz-ssenariy/hook_baho.py` bilan baholang. Ko'p kanallar shu yerda yo'qotadi - ayniqsa uzun
   salomlashish bilan.
4. **Qisqa videolar: oxirgi beshtasining birinchi 2 soniyasi.** Ekranda matn bormi? Natija birinchi
   kadrdami?
5. **Telegram: oxirgi 20 post.** Birinchi qatorlar alohida o'qilsa, ochishga sabab bo'ladimi? Ko'rishlar
   (`../uz-trend/trend.py --past`): qaysi tur ishlaydi, qaysi biri yo'q?
6. **Zanjir.** Har bir platforma keyingisiga olib boradimi? Qisqa video -> YouTube -> Telegram.
   Tavsifda Telegram havolasi bormi? Telegram'da yangi video anons qilinadimi? Bo'g'inlardan biri
   uzilgan bo'lsa - auditoriya bir platformada qolib ketadi.
7. **Ritm.** Tez-tezlik emas - IZCHILLIK. Bir haftada oltita video, keyin bir oy hech narsa - har ikki
   haftada bitta videodan yomonroq.
8. **Retention**, agar eksport qila olsa - `/uz-tahlil`.
9. **Yo'nalish xavfsizligi.** Pirat dastur, aktivator ko'rsatilgan videolar bormi? Bo'lsa - bu kanal
   uchun xavf (YouTube qoidalari), birinchi navbatdagi tuzatish shu.

## Nimani qaytarish kerak

- **Eng katta BITTA tuzatish**, nomi bilan va shu hafta nima qilish kerakligi bilan.
- **Allaqachon ishlayotgan uchta narsa** - ularni buzib qo'ymaslik uchun. Aniq bo'ling; "energiyangiz
  yaxshi" - kuzatuv emas.
- **Hozircha NIMA QILMASLIK kerak** va nega.

Hech qachon auditni yolg'on maqtov bilan boshlamang va yigirmata band bilan tugatmang.

## Darvoza

Bu skill hech narsani o'zi joylamaydi: u yozadi, siz joylaysiz. Har bir natija foydalanuvchi nusxa
oladigan blok bilan tugaydi, oxirgi qator esa doim savol: **Joylaymizmi yoki o'zgartiramizmi?**
