from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)
DATA_FILE = "data/kerkesa.json"

# Lexo kerkesa nga JSON
def lexo_kerkesa():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Shfaq dashboardin
@app.route('/')
def dashboard():
    return render_template("dashboard.html")

# API për me marrë kërkesat
@app.route('/api/kerkesa')
def kerkesa_api():
    return jsonify(lexo_kerkesa())

# Fshij të gjitha kërkesat
@app.route('/clear', methods=['POST'])
def fshi_kerkesa():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    return jsonify({"msg": "Kërkesat u fshinë!"})

# Fshij vetëm të përzgjedhurat me checkbox (sipas ID)
@app.route('/fshi-te-zgjedhura', methods=['POST'])
def fshi_te_zgjedhura():
    data = lexo_kerkesa()
    ids_to_delete = request.json.get("ids", [])

    updated = [k for k in data if str(k.get("id")) not in ids_to_delete]

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated, f, ensure_ascii=False, indent=4)

    return jsonify({"message": "Kërkesat e përzgjedhura u fshinë me sukses!"})

# Shto një kërkesë të re me ID automatike
@app.route('/shto', methods=['POST'])
def shto_kerkese():
    data = lexo_kerkesa()

    # Merr të dhënat nga frontend (JSON)
    info = request.json
    qyteti = info.get("qyteti")
    mesazhi = info.get("mesazhi")

    if not qyteti or not mesazhi:
        return jsonify({"error": "Të dhënat mungojnë"}), 400

    # Gjej ID-në më të madhe aktuale dhe shto +1
    id_max = max([int(k.get("id", 0)) for k in data], default=0)
    kerkese_re = {
        "id": str(id_max + 1),
        "qyteti": qyteti,
        "mesazhi": mesazhi
    }

    data.append(kerkese_re)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return jsonify({"message": "Kërkesa u shtua me sukses!"})

if __name__ == '__main__':
    app.run(port=6060, debug=True)
