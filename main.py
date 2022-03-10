from flask import request, Flask, jsonify, redirect
import json

database = {}
app = Flask(__name__)
app.config.update(
    DEBUG = True
)


try:
    database = eval(open("database.json", "r", encoding="utf-8").read())
except:
    open("database.json", "w", encoding="utf-8").write("{}")

def update_database():
    open("database.json", "w", encoding="utf-8").write(json.dumps(database, indent=4))


@app.route("/")
def index():
    return '/short -POST {"url":"url you want to short"}'

@app.route("/short", methods=["POST","GET"])
def shorter():
    base_url = '/'.join(request.base_url.split("/")[0:3])
    out = {"error":True, "msg":"just post request BAKA :/"}
    if request.method.lower() == "post":
        url = request.form.get("url")
        if url == "":
            out["msg"] = 'hey you, haven\'t read the index?? I NEED URLLLLL({"url":"url you want to short"})'
        else:
            try:
                if url in list(database.values()):
                    lid = list(database.keys())[list(database.values()).index(url)]
                    short_link = f"{base_url}/{lid}"
                    # print(short_link)
                    out = {"error":False, "short_url":short_link}
                else:
                    lid = str(len(database)+1)
                    database[lid] = url
                    short_link = f"{base_url}/{lid}"
                    out = {"error":False, "short_url":short_link}
            except:
                out["msg"] = "something is wron i can feel it..."
    return jsonify(out)

@app.route("/<lid>")
def redirect_to_url(lid):
    out = jsonify({"error":True, "msg":"something is wrong but now i can't feel it :/ lots of lol"})
    try:
        url = database[lid]
        out = redirect(url)
    except:
        pass
    return out

app.run()
