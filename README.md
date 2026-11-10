# O'zbekcha kontent agenti

YouTube, Reels/Shorts/TikTok va Telegram uchun o'n ikkita o'zbekcha Claude skill. Bepul, MIT litsenziya,
ro'yxatdan o'tish, API kalit yoki akkaunt ulash shart emas.

Yo'nalish: **Kompyuter va sun'iy intellekt - o'zbek tilida amaliy darslar.** Har bir skill shu
yo'nalishga moslangan: misollar, hook formulalari, auditoriya. Yo'nalishni o'zgartirish uchun bitta
fayl - [`templates/yonalish.md`](templates/yonalish.md) - qayta yoziladi.

Bittasi g'oyangizdan ssenariy yozadi va hookni yozib olishdan oldin baholaydi. Bittasi sarlavha va
muqovani bitta juftlik sifatida tekshiradi. Bittasi transkriptingizdan "ee", "xullas", "koroche" va
qayta boshlangan gaplarni topib, montaj ro'yxatini beradi. Bittasi bitta videodan bir haftalik
kontent yasaydi - qisqa videolar, Telegram postlar, karusel. Bittasi retention faylingizdan tomoshabin
aynan qaysi soniyada ketganini va o'sha paytda nima deganingizni ko'rsatadi.

Vositalar lotin va kirill yozuvini, `'` `ʻ` `` ` `` kabi turli tutuq belgilarini bir xil tushunadi.

**Siz joylamaguningizcha hech narsa joylanmaydi.** Skill'lar yozadi. Siz yuklaysiz.

## Sxema: bitta g'oya, uch platforma

```
            g'oya  <-----------------------------------------------+
              |                                                    |
        /uz-ssenariy  (hook baholanadi)                            |
              |                                                    |
   YouTube: to'liq dars  --/uz-montaj--/uz-sarlavha--/uz-seo        |
              |                                                    |
         /uz-moslash                                               |
        /           \                                              |
  /uz-qisqa        /uz-telegram                                    |
  Shorts, Reels,   anons, qo'llanma + fayl,                        |
  TikTok           so'rovnoma, savol-javob                         |
        \           /                                              |
         /uz-izoh  -- takrorlanuvchi savollar ---------------------+
              |                                                    |
   /uz-tahlil  /uz-trend  -- nima ishladi -------------------------+
              |
          /uz-reja  (keyingi hafta)        /uz-audit (oyda bir marta)

  Zanjir: qisqa video tanishtiradi -> YouTube o'rgatadi -> Telegram ushlab qoladi
```

## O'rnatish

Claude Code'da:

```bash
git clone https://github.com/Jaxa7775/uz-kontent-agent.git
```

Windows (PowerShell):

```powershell
Copy-Item -Recurse uz-kontent-agent\skills\uz-* $HOME\.claude\skills\
New-Item -ItemType Directory -Force $HOME\.claude\kontent-uz
Copy-Item uz-kontent-agent\templates\*.md $HOME\.claude\kontent-uz\
```

macOS / Linux:

```bash
cp -r uz-kontent-agent/skills/uz-* ~/.claude/skills/
mkdir -p ~/.claude/kontent-uz && cp uz-kontent-agent/templates/*.md ~/.claude/kontent-uz/
```

Yoki plagin sifatida:

```
/plugin marketplace add Jaxa7775/uz-kontent-agent
/plugin install uz-kontent-agent
```

(Plagin bilan o'rnatsangiz ham `templates/*.md` ni `~/.claude/kontent-uz/` ga ko'chiring.)

Skill'larni BIRGA o'rnating: ba'zilari boshqasining vositasini ishlatadi (masalan, `uz-qisqa`
`uz-ssenariy` dagi `hook_baho.py` ni).

Keyin o'n daqiqa [`ovoz.md`](templates/ovoz.md) ga sarflang: `~/.claude/kontent-uz/ovoz.md` ni
to'ldiring yoki Claude'ga uchta o'z videongizni berib "shulardan ovoz.md yoz" deng. Har bir skill
shuni o'qiydi. Bu yerda ayniqsa muhim, chunki so'zlarni kamerada ovoz chiqarib aytasiz.

## O'n ikkita skill

| buyruq | nima qiladi |
| --- | --- |
| `/uz-ssenariy` | G'oyadan YouTube ssenariysi. [18 formula](skills/uz-ssenariy/formulalar.json)dan beshta hook, baholangan, keyin har bo'lakda `[EKRANDA]` bilan ssenariy. |
| `/uz-qisqa` | Shorts/Reels/TikTok: yangi g'oyadan yoki uzun videodan. Ekrandagi matn, birinchi 2 soniya, aylanma yakun. |
| `/uz-telegram` | Telegram post: qo'llanma, maslahat, so'rovnoma, anons, savol-javob. Birinchi qator va chegaralar tekshiriladi. |
| `/uz-sarlavha` | Sarlavha va muqova bitta juftlik: uzunlik, takror, noaniqlik, tutuq belgisi, yozuv aralashuvi. |
| `/uz-moslash` | Bitta kontentdan: 2-3 qisqa video, 3-5 Telegram post, Instagram karusel. |
| `/uz-reja` | Haqiqiy vaqtingizga sig'adigan hafta: bitta asosiy video, undan qisqa videolar, atrofida Telegram. |
| `/uz-montaj` | Transkriptdan montaj ro'yxati: pauzalar, parazit so'zlar, dubllar. Ekran yozuvidagi jim namoyishlarni himoya qiladi. |
| `/uz-seo` | YouTube tavsifi va boblar, Instagram/TikTok izohi va hashtaglar, Telegram nomi. Lotin/kirill va yozilish variantlari. |
| `/uz-izoh` | Izohlar beshta guruhga, keyin sizning ovozingizda javoblar. Qaysini qadashni aytadi, savollarni mavzuga aylantiradi. |
| `/uz-tahlil` | Retention fayli: boshlanish, keskin tushishlar, sekin oqish. Postlaringizning eng yaxshisi va eng yomoni. |
| `/uz-trend` | Yo'nalishda nima ishlayapti - har bir kanalning o'z medianasiga karralik bo'yicha. |
| `/uz-audit` | Uchala platforma, oxirida yigirmata emas, BITTA tuzatish. |

## Sakkizta vosita

Hammasi toza Python 3 da, qo'shimcha kutubxonasiz ishlaydi. Skill'lar shunchaki so'rov emas -
sababi shular. (Windows'da `python`, macOS/Linux'da `python3`.)

```bash
python skills/uz-ssenariy/hook_baho.py --hook "bitta gap"          # hookning 5 xususiyati
python skills/uz-sarlavha/sarlavha.py --sarlavha "..." --muqova "..." # sarlavha + muqova
python skills/uz-montaj/montaj.py transkript.srt                    # montaj ro'yxati
python skills/uz-seo/boblar.py transkript.srt                       # YouTube boblari
python skills/uz-seo/imlo.py --variant "o'qituvchi"                 # yozilish variantlari, lotin<->kirill
python skills/uz-tahlil/retention.py video.csv --davomiylik 600     # tomoshabin qayerda ketdi
python skills/uz-trend/trend.py yigilgan.json --min 2.0             # o'z kanaliga nisbatan saralash
python skills/uz-telegram/joyla.py post.txt                         # Telegram: ko'rib chiqish (--yubor bilan yuboradi)
```

### Telegram kanalga joylash

`joyla.py` rasmiy Bot API orqali postni (rasm, fayl yoki ovozli xabar bilan) kanalga yuboradi.
O'zbekcha sun'iy ovoz kerak bo'lsa: `pip install edge-tts`, keyin
`edge-tts --voice uz-UZ-SardorNeural --file matn.txt --write-media ovoz.mp3` (yoki `uz-UZ-MadinaNeural`)
va `joyla.py post.txt --ovoz ovoz.mp3`. Bu Microsoft'ning onlayn xizmati va ovoz sun'iy eshitiladi.
Sozlash:

1. [@BotFather](https://t.me/BotFather) da bot oching (yoki borini ishlating), tokenni faylga saqlang.
2. Botni kanalga **"Xabar joylash"** huquqi bilan admin qiling.
3. [`templates/telegram.example.json`](templates/telegram.example.json) ni
   `~/.claude/kontent-uz/telegram.json` deb nusxalang, kanal va token fayli yo'lini yozing.
4. `python skills/uz-telegram/joyla.py --tekshir`

`--yubor` bo'lmasa hech narsa yuborilmaydi - faqat ko'rib chiqish. Token repoda ham, ekranda ham
ko'rinmaydi.

YouTube, Instagram va TikTok'ga avtomatik joylash yo'q: YouTube API orqali tekshiruvdan o'tmagan
loyihalar yuklagan videolar "private" holatda qulflanadi, Instagram va TikTok API'lari esa biznes
akkaunt va ilova tekshiruvini talab qiladi. Ular uchun skill'lar matnni tayyorlaydi, joylash - sizda.

Testlar: `python tests/test_vositalar.py`

## Halol izohlar

Ko'p to'plamlar yozmaydigan qism.

**Tasdiqsiz hech narsani joylamaydi.** Har bir skill nusxa olinadigan blok va savol bilan tugaydi:
joylaymizmi yoki o'zgartiramizmi? Yagona istisno - Telegram'ga `joyla.py --yubor`, va u ham faqat siz
aynan shu postga "ha" degandan keyin ishga tushiriladi. O'zi kanalingizni boshqaraman degan har qanday
narsaga shu farqni yodda tutib qarang.

**`hook_baho.py` - taxminiy hisob, bashorat emas.** U so'zlarga qaraydi (raqamlar, "siz", savol
so'zlari, xavf so'zlari) va hech qanday real statistika bo'yicha kalibrlanmagan. Ataylab yomon yozilgan
hookni ("Assalomu alaykum hurmatli obunachilar...") yaxshisidan ajratadi. Sizning yaxshi videongizni
yomonidan ajratishiga kafolat yo'q. Past ball - qayta qarash uchun sabab; yuqori ball - va'da emas. Eng
ishonchli o'lchov - o'z retention grafigingiz.

**Formula aniqlash - so'zlar haqida, natija haqida emas.** `/uz-trend` "bu sarlavha Savol formulasida"
desa, bu ko'rinib turgan so'zlar haqidagi xulosa, video nega ko'p ko'rilgani haqida da'vo emas.

**Umumiy "me'yor" raqamlari yo'q.** "Yaxshi retention - 50%" kabi raqamlar ataylab berilmaydi:
ishonchli manba yo'q. O'rniga o'z videolaringiz bir-biri bilan solishtiriladi.

**`/uz-trend` faqat ochiq ma'lumotni o'qiydi.** Hech qachon akkauntingizga kirmaydi va parol
so'ramaydi. yt-dlp ishlatish YouTube shartlari bilan cheklangan - bu haqda ochiq aytiladi.

**Teglar deyarli ahamiyatsiz** - va bu to'plam teg generatori sotish o'rniga shuni aytadi. Istisno:
o'zbek tilidagi yozilish variantlari.

**Hech narsa raqam to'qimaydi.** Skill'ga raqam kerak bo'lsa-yu, unda bo'lmasa, sizdan so'raydi yoki
gapni raqamsiz yozadi.

**Lotin -> kirill o'girish mukammal emas.** Ruscha o'zlashma so'zlarning bir qismi lug'atda bor
(kompyuter -> компьютер, oylar), qolganlarini bir ko'zdan kechiring.

## Yo'nalishni o'zgartirish

1. `~/.claude/kontent-uz/yonalish.md` ni yangi yo'nalish bilan qayta yozing (auditoriya, rubrikalar,
   mavzular banki, nimalar qilinmaydi).
2. Xohlasangiz `skills/uz-ssenariy/formulalar.json` dagi `misol` maydonlarini yangi yo'nalishga
   moslang. `naqsh` maydonlariga tegmasangiz ham bo'ladi.

## Minnatdorchilik

Tuzilma g'oyasi (skill + haqiqiy ishlaydigan vosita + "joylamaydi" darvozasi)
[Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill)
(MIT) dan ilhomlangan. Kod va matnlar o'zbek tili, uch platforma va shu yo'nalish uchun noldan yozilgan.

## Litsenziya

MIT. Foydalaning, o'zgartiring, tarqating.
