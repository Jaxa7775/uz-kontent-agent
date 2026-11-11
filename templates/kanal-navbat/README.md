# Kanal navbati

Tasdiqlangan Telegram postlari shu yerda navbatda turadi. GitHub Actions `navbat.py` ni ishga tushiradi,
u vaqti kelgan (yoki 5 daqiqadan kam qolgan) postlarni kanalga joylaydi. Kompyuter o'chiq bo'lsa ham ishlaydi.

Uni ikkita taymer ishga tushiradi:

1. **Asosiy: cron-job.org (bepul).** Post vaqtlarida (masalan 08:00, 12:00, 15:00, 18:00, 21:00,
   vaqt zonasi `Asia/Tashkent`) GitHub API orqali workflow'ni chaqiradi:
   - `POST https://api.github.com/repos/<egasi>/<repo>/actions/workflows/navbat.yml/dispatches`
   - sarlavhalar: `Authorization: Bearer <PAT>`, `Accept: application/vnd.github+json`,
     `Content-Type: application/json`
   - tana: `{"ref":"main","inputs":{"rejim":"joyla"}}`
   - PAT: fine-grained, faqat shu repo, ruxsat Actions: Read and write. To'g'ri javob: `204`.
2. **Zaxira: GitHub'ning o'z cron'i** (har soat `:07` da, UTC). Unga yolg'iz tayanmang: yuklama
   paytida ishga tushishlarni soatlab o'tkazib yuboradi (bir kechada 14 tadan 2 tasigina ishlagan).

Ikkalasi bir vaqtda chaqirsa ham post ikki marta chiqmaydi: ishlar navbat bilan bajariladi
(`concurrency`), har biri eng oxirgi holatni oladi, joylangan post esa `yuborilgan/` ga ko'chadi.

- `navbat/` - kutayotgan postlar
- `yuborilgan/` - joylanganlar (meta.json da havola)
- `kechikkan/` - vaqtidan 6 soatdan ko'p o'tib ketgan, yuborilmagan
- `xato/` - Telegram xato bergan, qayta urinilmagan

Postni navbatga qo'yish (kompyuterda): `python joyla.py`ning yonidagi `navbatga.py`:

```bash
python navbatga.py post.txt --vaqt "2026-11-12 19:00" [--ovoz o.mp3 | --rasm r.jpg | --fayl f.xlsx]
python navbatga.py --royxat
python navbatga.py --bekor <id>
```

Sozlash: repo -> Settings -> Secrets and variables -> Actions:
- Secret `TELEGRAM_BOT_TOKEN` - bot tokeni
- Variable `TELEGRAM_KANAL` - standart kanal (`@kanal`)

Tekshirish: Actions -> "Kanal navbati" -> Run workflow -> rejim: `tekshir`.

Bepul chegara: yopiq repoda GitHub Actions oyiga 2000 daqiqa beradi; har soatlik zaxira taxminan
720 daqiqa, kuniga 5 ta taymer chaqiruvi taxminan 150 daqiqa ishlatadi. Taymer bilan post belgilangan
daqiqada chiqadi; taymer vaqtlari post vaqtlariga mos bo'lsin (masalan post 09:00 da, taymer 08:00 da
bo'lsa, post keyingi chaqiruvgacha kutib qoladi).

Repo yopiq (private) bo'lsin: navbatdagi postlarni joylanmaguncha hech kim ko'rmasin.
