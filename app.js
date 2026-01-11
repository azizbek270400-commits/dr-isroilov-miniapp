const ADMIN_ID = "5096290302";
const API = "https://dr-isroilov-miniapp-3.onrender.com";

const today = new Date().toISOString().split("T")[0];

fetch(`${API}/admin/${today}/${ADMIN_ID}`)
  .then(r => r.json())
  .then(data => {
    const list = document.getElementById("list");
    list.innerHTML = "";

    if (!data || data.length === 0) {
      list.innerHTML = "<p>Bugun uchun navbat yo‘q</p>";
      return;
    }

    data.forEach(p => {
      const div = document.createElement("div");
      div.style.padding = "10px";
      div.style.margin = "10px 0";
      div.style.border = "1px solid #444";
      div.style.borderRadius = "10px";

      div.innerHTML = `
        <b>${p.name}</b><br>
        📞 ${p.phone || ""}<br>
        ⏰ ${p.time}<br>
        <button onclick="confirmAppt('${p.uid}','${p.date}','${p.time}')">✅ Tasdiqlash</button>
        <button onclick="cancelAppt('${p.uid}','${p.date}','${p.time}')">❌ Bekor qilish</button>
      `;

      list.appendChild(div);
    });
  });

function confirmAppt(uid, date, time) {
  fetch(`${API}/confirm`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({uid, date, time})
  }).then(() => location.reload());
}

function cancelAppt(uid, date, time) {
  fetch(`${API}/cancel`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({uid, date, time})
  }).then(() => location.reload());
}
