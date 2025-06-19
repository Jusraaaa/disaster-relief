const qytetet = {
    "shkup": [42.0, 21.4],
    "tetove": [42.01, 20.97],
    "gostivar": [41.8, 20.9]
};

const map = L.map('map').setView([41.6, 21.7], 8);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Vendos markerat në hartë për referencë vizuale
for (const [emri, koord] of Object.entries(qytetet)) {
    L.marker(koord).addTo(map).bindPopup(emri.toUpperCase());
}

function dergoKerkesen() {
    const qyteti = document.getElementById("qyteti").value;
    const kerkesa = document.getElementById("kerkesa").value.trim();
    const kategoria = document.querySelector('input[name="kategoria"]:checked');

    if (!kerkesa || !kategoria) {
        alert("Ju lutem plotësoni të gjitha fushat.");
        return;
    }

    const mesazhi = `[${kategoria.value}] ${kerkesa}`;

    fetch('/dergo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            qyteti: qyteti,
            kerkesa: mesazhi
        })
    })
    .then(response => response.json())
    .then(data => {
        const msg = document.getElementById("pergjigje");
        msg.innerText = data.msg;
        msg.classList.remove("out");

        // Pastrim formës
        document.getElementById("kerkesa").value = "";
        document.querySelector('input[name="kategoria"]:checked').checked = false;

        setTimeout(() => {
            msg.classList.add("out");
        }, 2500);
    });
}

console.log("✅ index.js u ngarkua me sukses!");

