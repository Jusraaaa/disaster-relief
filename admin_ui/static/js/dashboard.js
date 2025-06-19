const qytetet = {
    "shkup": [42.0, 21.4],
    "tetove": [42.01, 20.97],
    "gostivar": [41.8, 20.9]
};

const map = L.map('map').setView([41.9, 21.2], 8);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Ngarko kufirin e Maqedonisë
fetch("/static/macedonia.geojson")
    .then(res => res.json())
    .then(data => {
        L.geoJSON(data, {
            style: {
                color: "#4a90e2",
                weight: 2,
                fillOpacity: 0
            }
        }).addTo(map);
    });

let kerkesaCount = 0;

function ngarkoKerkesa() {
    fetch('/api/kerkesa')
        .then(response => response.json())
        .then(data => {
            // 🔔 Kontrollo për kërkesa të reja
            if (data.length > kerkesaCount) {
                const alarm = document.getElementById("alertSound");
                const pulse = document.getElementById("alertPulse");

                if (alarm) alarm.play().catch(() => {});
                if (pulse) {
                    pulse.style.display = "block";
                    setTimeout(() => {
                        pulse.style.display = "none";
                    }, 4000);
                }
            }
            kerkesaCount = data.length;

            const selectedCity = document.getElementById("filterCity").value;
            const listContainer = document.getElementById("kerkesaList");
            const statsContainer = document.getElementById("statsList");

            listContainer.innerHTML = "";
            statsContainer.innerHTML = "";

            let statistika = {};

            // Hiq marker-at e vjetër
            map.eachLayer(layer => {
                if (layer instanceof L.Marker) map.removeLayer(layer);
            });

            data.forEach(k => {
                const emri = k.qyteti.toLowerCase();
                if (selectedCity !== "tegjitha" && emri !== selectedCity) return;

                if (!statistika[emri]) statistika[emri] = 0;
                statistika[emri]++;

                const pozita = qytetet[emri];
                if (pozita) {
                    const customIcon = L.icon({
                        iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
                        iconSize: [30, 30],
                        iconAnchor: [15, 30],
                        popupAnchor: [0, -30]
                    });

                    L.marker(pozita, { icon: customIcon }).addTo(map).bindPopup(k.mesazhi);
                }

                const kerkeseId = k.id;

                const div = document.createElement("div");
                div.className = "kerkese";
                div.innerHTML = `
                    <label style="display: flex; align-items: center; gap: 10px;">
                        <input type="checkbox" class="zgjedhurKerkese" value="${kerkeseId}">
                        <div>
                            <strong>${k.qyteti.toUpperCase()}</strong><br>${k.mesazhi}
                        </div>
                    </label>
                `;
                listContainer.appendChild(div);
            });

            for (let qytet in statistika) {
                const li = document.createElement("li");
                li.textContent = `${qytet.toUpperCase()}: ${statistika[qytet]} kërkesa`;
                statsContainer.appendChild(li);
            }
        });
}

function fshiKerkesat() {
    fetch('/clear', { method: 'POST' })
        .then(() => {
            alert("Të gjitha kërkesat u fshinë!");
            kerkesaCount = 0;
            ngarkoKerkesa();
        });
}

function fshiTeZgjedhura() {
    const zgjedhjet = document.querySelectorAll('.zgjedhurKerkese:checked');
    const ids = Array.from(zgjedhjet).map(checkbox => checkbox.value);

    if (ids.length === 0) {
        alert("Zgjedh të paktën një kërkesë për fshirje.");
        return;
    }

    fetch('/fshi-te-zgjedhura', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ids: ids })
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message);
        ngarkoKerkesa();
    });
}

ngarkoKerkesa();
setInterval(ngarkoKerkesa, 5000);
