import os, json, sqlite3, hashlib, hmac, time
from urllib.parse import parse_qsl
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB = Path(__file__).with_name("kids_games.db")
app = FastAPI(title="Kids Game Bot")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "webapp"), name="static")

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS scores(
            user_id TEXT PRIMARY KEY, username TEXT, points INTEGER NOT NULL DEFAULT 0,
            best INTEGER NOT NULL DEFAULT 0, games INTEGER NOT NULL DEFAULT 0)""")
init_db()

def valid_telegram_init_data(init_data: str) -> dict:
    # Telegram Mini Apps signature validation. In local browser mode, empty initData is accepted
    # for development only; production should set REQUIRE_TELEGRAM_AUTH=1.
    if not init_data:
        if os.getenv("REQUIRE_TELEGRAM_AUTH", "0") == "1":
            raise HTTPException(401, "Telegram orqali oching")
        return {"user": {"id": "demo", "first_name": "Mehmon", "username": "demo"}}
    if not BOT_TOKEN:
        raise HTTPException(500, "BOT_TOKEN sozlanmagan")
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.pop("hash", None)
    if not received_hash:
        raise HTTPException(401, "Noto‘g‘ri Telegram ma'lumoti")
    data_check = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
    secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculated, received_hash):
        raise HTTPException(401, "Telegram imzosi tekshirilmadi")
    auth_date = int(pairs.get("auth_date", "0"))
    if time.time() - auth_date > 86400:
        raise HTTPException(401, "Sessiya eskirgan")
    user = json.loads(pairs.get("user", "{}"))
    return {"user": user}

@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "webapp" / "index.html")

@app.get("/api/me")
async def me(request: Request):
    data = valid_telegram_init_data(request.headers.get("X-Telegram-Init-Data", ""))
    user = data["user"]
    uid = str(user.get("id", "demo"))
    with db() as con:
        con.execute("INSERT OR IGNORE INTO scores(user_id, username) VALUES(?,?)",
                    (uid, user.get("first_name", "O‘yinchi")))
        row = con.execute("SELECT * FROM scores WHERE user_id=?", (uid,)).fetchone()
    return dict(row)

@app.post("/api/score")
async def save_score(request: Request):
    data = valid_telegram_init_data(request.headers.get("X-Telegram-Init-Data", ""))
    body = await request.json()
    points = max(0, min(int(body.get("points", 0)), 1000))
    user = data["user"]
    uid = str(user.get("id", "demo"))
    username = user.get("first_name", "O‘yinchi")
    with db() as con:
        con.execute("INSERT OR IGNORE INTO scores(user_id, username) VALUES(?,?)", (uid, username))
        con.execute("""UPDATE scores SET points=points+?, best=MAX(best,?), games=games+1,
                    username=? WHERE user_id=?""", (points, points, username, uid))
        row = con.execute("SELECT * FROM scores WHERE user_id=?", (uid,)).fetchone()
    return dict(row)

@app.get("/api/leaderboard")
async def leaderboard():
    with db() as con:
        rows = con.execute("SELECT username, points, best, games FROM scores ORDER BY points DESC LIMIT 10").fetchall()
    return [dict(r) for r in rows]
