from flask import Flask, render_template, request, jsonify
import socket
import json
import os

app = Flask(__name__)

ports = {
    "shkup": 5001,
    "tetove": 5002,
    "gostivar": 5003
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dergo', methods=['POST'])
def dergo():
    qyteti = request.json.get('qyteti')
    kerkesa = request.json.get('kerkesa')

    if qyteti not in ports:
        return jsonify({"msg": "Qyteti i pavlefshëm!"}), 400

    host = '127.0.0.1'
    port = ports[qyteti]

    try:
        # Lidhja me socket-in e qytetit
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(kerkesa.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        s.close()

        # Ruaj në kerkesa.json
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'admin_ui', 'data', 'kerkesa.json'))

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        else:
            all_data = []

        # Gjej ID maksimale dhe rrit për 1
        id_max = max([int(k.get("id", 0)) for k in all_data], default=0)

        new_data = {
            "id": str(id_max + 1),
            "qyteti": qyteti,
            "mesazhi": kerkesa
        }

        all_data.append(new_data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)

        return jsonify({"msg": "Kërkesa u dërgua me sukses ✅"})

    except Exception as e:
        print(f"[Gabim gjatë dërgimit apo ruajtjes]: {e}")
        return jsonify({"msg": "Nuk u lidh me serverin e qytetit."}), 500

if __name__ == '__main__':
    app.run(debug=True)
