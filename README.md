# Kids Game Bot — Telegram Web App

50 ta kichik, xavfsiz va bepul mini-o‘yinli Telegram bot loyihasi.

## Talablar
- Python 3.11+
- Telegram bot tokeni (BotFather'dan yangi token oling)
- Web App uchun HTTPS manzil (masalan, Render, Railway yoki VPS domeni)

## Ishga tushirish
1. `cp .env.example .env` qilib, `.env` faylini to‘ldiring.
2. `pip install -r requirements.txt`
3. Web server: `uvicorn app:app --host 0.0.0.0 --port 8000`
4. HTTPS domeningizni `.env` dagi `WEBAPP_URL` ga yozing.
5. Alohida terminalda: `python bot.py`

Telegram Web App faqat Telegram ichida va HTTPS manzilda to‘liq ishlaydi.
Lokal sinov uchun web sahifani `http://localhost:8000` orqali ko‘rish mumkin, lekin Telegram ichida ochish uchun HTTPS kerak.

## Muhim xavfsizlik
Oldingi xabarda bot tokeni oshkor bo‘lgan. Uni BotFather'da bekor qiling (`/revoke`) va YANGI token yarating.
Tokenni chatga yubormang. Faqat `.env` fayliga kiriting.
`.env` faylini hech qachon GitHub'ga yuklamang.

## Deploy
Render/Railway/VPS'da Python web service sifatida deploy qiling:
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- `BOT_TOKEN` va `WEBAPP_URL` environment variables qo‘shing.
Bot polling jarayonini alohida worker sifatida `python bot.py` bilan ishga tushiring.

## Izoh
Loyiha 50 ta o‘yin kartasi, kategoriyalar, ball, rekord va SQLite saqlashni o‘z ichiga oladi.
Mini-o‘yinlar bolalar uchun qonsiz, zo‘ravonliksiz multfilm uslubida. Jang mavzusi faqat
xavfsiz fantaziya musobaqalari (qalqon, robotni to‘xtatish, ajdarhoni tinchlantirish) tarzida.
