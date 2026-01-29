console.log("script.js loaded");

/* ================= MAP INIT ================= */
const map = L.map("map").setView([11.0168, 76.9558], 7);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap"
}).addTo(map);

let markersLayer = L.layerGroup().addTo(map);
let heatLayer = null;
let lastMapUpdate = 0;

/* ================= WEBSOCKET ================= */
const ws = new WebSocket("ws://127.0.0.1:8000/ws/realtime");

ws.onopen = () => {
  console.log("✅ WebSocket connected");
};

ws.onerror = (e) => {
  console.error("❌ WebSocket error", e);
};

ws.onmessage = (event) => {
  console.log("WS DATA:", event.data);
  const data = JSON.parse(event.data);

  updateUI(data);
  updateMap(data);
};

/* ================= UI UPDATE ================= */
function animateNumber(element, start, end) {
  const duration = 300;
  const startTime = performance.now();

  function update(time) {
    const progress = Math.min((time - startTime) / duration, 1);
    const value = Math.round(start + (end - start) * progress);
    element.innerText = value + "%";
    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

function updateUI(data) {
  const zoneA = document.getElementById("zoneA");
  const zoneAConf = document.getElementById("zoneA_conf");
  const alertBanner = document.getElementById("alertBanner");

  if (!zoneA || !zoneAConf) return;

  const conf = Math.round(data.confidence * 100);

  zoneAConf.innerText = conf + "%";

  if (data.status === "FIRE") {
    zoneA.className = "zone fire";
    alertBanner.style.display = "block";
    if(!telegramSent){
    telegramSent = true;
    telegramBtn.click();
    }
  } else {
    zoneA.className = "zone safe";
    alertBanner.style.display = "none";
    telegramSent = false;
  }
}


/* ================= MAP UPDATE ================= */
function updateMap(data) {
  const now = Date.now();
  if (now - lastMapUpdate < 3000) return; // throttle
  lastMapUpdate = now;

  if (data.lat == null || data.lon == null) return;

  markersLayer.clearLayers();

  L.circleMarker([data.lat, data.lon], {
    radius: 12,
    color: data.status === "FIRE" ? "red" : "green",
    fillOpacity: 0.9
  })
  .bindPopup(`🔥 Confidence: ${Math.round(data.confidence * 100)}%`)
  .addTo(markersLayer);

  if (heatLayer) map.removeLayer(heatLayer);

  heatLayer = L.heatLayer(
    [[data.lat, data.lon, data.confidence]],
    { radius: 40, blur: 25 }
  ).addTo(map);
}

const telegramBtn = document.getElementById("telegramAlertBtn");

telegramBtn.addEventListener("click", async () => {
  const confidence = document.getElementById("zoneA_conf").innerText;

  const message = `
🚨 <b>FOREST FIRE ALERT</b> 🚨

🔥 Status: FIRE DETECTED
📊 Confidence: ${confidence}
📍 Location: Zone A
⏰ Time: ${new Date().toLocaleString()}
`;

  try {
    const res = await fetch("http://127.0.0.1:8000/send-telegram-alert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();

    if (data.status === "sent") {
      M.toast({ html: "✅ Telegram alert sent!", classes: "green" });
    } else {
      M.toast({ html: "❌ Failed to send alert", classes: "red" });
    }
  } catch (err) {
    console.error(err);
    M.toast({ html: "❌ Server error", classes: "red" });
  }
});
