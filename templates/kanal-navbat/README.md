# Kanal navbati

Tasdiqlangan Telegram postlari shu yerda navbatda turadi. GitHub Actions har soatda (`:07` da, UTC)
`navbat.py` ni ishga tushiradi va vaqti kelganini kanalga joylaydi. Kompyuter o'chiq bo'lsa ham ishlaydi.

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

Bepul chegara: yopiq repoda GitHub Actions oyiga 2000 daqiqa beradi; har soatlik ishga tushish
taxminan 720 daqiqa ishlatadi. Postlar rejalashtirilgan soatdan keyin taxminan 5-40 daqiqa ichida
chiqadi - shuning uchun vaqtni soat boshiga qo'ying.

Repo yopiq (private) bo'lsin: navbatdagi postlarni joylanmaguncha hech kim ko'rmasin.
