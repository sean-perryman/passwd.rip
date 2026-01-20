import os
import random
from flask import Flask, jsonify, render_template, Response, request, make_response

app = Flask(__name__)

SYMBOLS = "!@#$^&*+?"  # excludes %
WORDS = [
    "foxhall","services","trouncer","earhart","rowboat","zipper","mailbox","riverbed","sundial","notepad",
    "workshop","sandbox","pinecone","starship","oakwood","harvest","sunbeam","garden","handler","stadium",
    "pancake","monitor","laptop","backyard","gateway","painter","thunder","treasure","orchard","station",
    "balcony","captain","diamond","folding","bracket","canyoned","freight","journey","kindle","lantern",
    "magneto","network","pacific","pendant","picture","pioneers","pipeline","restless","rainbow","doorway",
    "justice","fortune","volcano","emerald","granite","hamster","factory","library","marriage","visitor",
    "weathered","mountain","seawater","freeware","baseline","coastline","checklist","doorbell","hardware",
    "keyboard","engineer","overhead","midnight","sunlight","wildfire","blueprint","framework","hillside",
    "shipyard","postcard","beverage","headline","schedule","lifelong","backpack","stairway","computer",
    "terminal","sidewalk","roadway","playful","mindful","hopeful","careful","central","digital","account",
    "content","traffic","program","payment","support","customer","security","snapshot","thermal","nuclear",
    "booklet","speaker","dentist","teacher","builder","circuit","compass","coolant","gemstone","cheerful",
    "graceful","fearless","priceless","reckless","endless","triangle","rectangle","shipment","focused",
    "catalog","elastic","organic","silicon","carbonic"
]

def generate_password() -> str:
    word = random.choice([w for w in WORDS if 6 <= len(w) <= 9]).lower()
    word = word[:1].upper() + word[1:]

    symbol = random.choice(SYMBOLS)

    if random.randint(0, 1) == 0:
        digits = str(random.randint(0, 9))
    else:
        digits = f"{random.randint(0, 99):02d}"

    return f"{word}{symbol}{digits}"

def wants_plain_text(req) -> bool:
    accept = (req.headers.get("Accept") or "").lower()
    ua = (req.headers.get("User-Agent") or "").lower()

    if "text/plain" in accept:
        return True

    if "curl" in ua or "wget" in ua or "httpie" in ua:
        return True

    return False

@app.get("/")
def index():
    pw = generate_password()

    if wants_plain_text(request):
        resp = make_response(pw + "\n")
        resp.mimetype = "text/plain"
        resp.headers["Cache-Control"] = "no-store"
        return resp

    return render_template("index.html", password=pw)

@app.get("/api/password")
def api_password():
    return jsonify({"password": generate_password()})

@app.get("/raw")
def raw_password():
    return Response(generate_password() + "\n", mimetype="text/plain")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
