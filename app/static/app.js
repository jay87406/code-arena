async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  return res.json();
}

let currentQuestion = null;

function renderQuestion(question) {
  const panel = document.getElementById("questionPanel");
  if (!question) {
    panel.innerHTML = "<h2>全部完成</h2><p>你已完成今天分配到的題目。</p>";
    return;
  }

  currentQuestion = question;
  document.getElementById("qTitle").textContent = `[${question.tags.join(", ")}] ${question.title}`;
  document.getElementById("qDesc").textContent = question.description;
  document.getElementById("starter").textContent = question.starter_code;
  document.getElementById("code").value = question.starter_code;
}

async function loadMe() {
  const data = await api("/api/me");
  document.getElementById("me").textContent = `玩家: ${data.nickname} (${data.ip})`;
  document.getElementById("progress").textContent = `進度: ${data.progress.current}/${data.progress.total}`;
  document.getElementById("score").textContent = `分數: ${data.score}`;
  document.getElementById("nickname").value = data.nickname;
  renderQuestion(data.question);
}

async function loadBoard() {
  const data = await api("/api/leaderboard");
  const body = document.getElementById("leaderboard");
  body.innerHTML = data.items
    .map((row) => `<tr><td>${row.nickname}</td><td>${row.score}</td><td>${row.solved}</td><td>${row.ip}</td></tr>`)
    .join("");
}

async function saveNickname() {
  const nickname = document.getElementById("nickname").value;
  const data = await api("/api/nickname", {
    method: "POST",
    body: JSON.stringify({ nickname }),
  });

  const result = document.getElementById("result");
  result.textContent = data.message || "暱稱已更新";
  result.className = data.ok ? "ok" : "bad";
  await loadMe();
  await loadBoard();
}

async function submitCode() {
  if (!currentQuestion) return;
  const code = document.getElementById("code").value;
  const data = await api("/api/submit", {
    method: "POST",
    body: JSON.stringify({ code }),
  });

  const result = document.getElementById("result");
  result.textContent = data.message;
  result.className = data.ok ? "ok" : "bad";

  await loadMe();
  await loadBoard();
}

document.getElementById("saveNick").addEventListener("click", saveNickname);
document.getElementById("submitBtn").addEventListener("click", submitCode);

loadMe();
loadBoard();
setInterval(loadBoard, 5000);

