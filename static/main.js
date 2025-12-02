function escapeHtml(s) {
  return s.replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");
}

function highlight(text, query) {
  let out = escapeHtml(text);
  let tokens = query.toLowerCase().split(/\s+/);
  tokens.forEach(t => {
    if (!t) return;
    let re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g,"\\$&") + ")", "ig");
    out = out.replace(re, '<span class="highlight">$1</span>');
  });
  return out;
}

async function post(url, body) {
  let res = await fetch(url, {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify(body)
  });
  return res.json();
}

document.getElementById("retrieveBtn").onclick = async () => {
  let q = document.getElementById("question").value.trim();
  let alpha = document.getElementById("alpha").value;
  let out = document.getElementById("evidenceList");
  out.innerHTML = "Loading...";
  let data = await post("/retrieve", {question:q, alpha});
  out.innerHTML = "";
  data.results.forEach((r,i) => {
    out.innerHTML += `
      <div class="evidence">
        <h3>${i+1}. ${escapeHtml(r.title)} — score ${r.score.toFixed(3)}</h3>
        <p>${highlight(r.text, q)}</p>
      </div>
    `;
  });
};

document.getElementById("askBtn").onclick = async () => {
  let q = document.getElementById("question").value.trim();
  let alpha = document.getElementById("alpha").value;
  document.getElementById("answerBox").textContent = "Thinking...";
  let data = await post("/ask", {question:q, alpha});
  document.getElementById("answerBox").textContent = data.answer;

  let out = document.getElementById("evidenceList");
  out.innerHTML = "";
  data.retrieved.forEach((r,i) => {
    out.innerHTML += `
      <div class="evidence">
        <h3>${i+1}. ${escapeHtml(r.title)} — score ${r.score.toFixed(3)}</h3>
        <p>${highlight(r.text, q)}</p>
      </div>
    `;
  });
};
