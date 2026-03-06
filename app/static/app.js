async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  return res.json();
}

let currentQuestion = null;

function getCodeInput() {
  return document.getElementById("code");
}

function setResultMessage(message, ok) {
  const result = document.getElementById("result");
  result.textContent = message;
  result.className = ok ? "ok" : "bad";
}

function resetSolutionBlock() {
  document.getElementById("solution").textContent = "";
  document.getElementById("solutionBlock").open = false;
}

function renderQuestion(question) {
  const panel = document.getElementById("questionPanel");
  if (!question) {
    panel.innerHTML = "<h2>全部完成</h2><p>你已完成今天分配到的題目。</p>";
    currentQuestion = null;
    return;
  }

  currentQuestion = question;
  document.getElementById("qTitle").textContent = `[${question.tags.join(", ")}] ${question.title}`;
  document.getElementById("qDesc").textContent = question.description;
  document.getElementById("starter").textContent = question.starter_code;
  getCodeInput().value = question.starter_code;
  resetSolutionBlock();
}

async function loadMe() {
  const data = await api("/api/me");
  document.getElementById("me").textContent = `玩家: ${data.nickname} (${data.ip})`;
  document.getElementById("progress").textContent = `進度: ${data.progress.current}/${data.progress.total}`;
  document.getElementById("score").textContent = `分數: ${data.score}`;
  document.getElementById("solutionViews").textContent = `看解答次數: ${data.solutions_viewed}`;
  document.getElementById("nickname").value = data.nickname;
  renderQuestion(data.question);
}

async function loadBoard() {
  const data = await api("/api/leaderboard");
  const body = document.getElementById("leaderboard");
  body.innerHTML = data.items
    .map(
      (row) =>
        `<tr><td>${row.nickname}</td><td>${row.score}</td><td>${row.solved}</td><td>${row.solution_views}</td><td>${row.ip}</td></tr>`,
    )
    .join("");
}

async function saveNickname() {
  const nickname = document.getElementById("nickname").value;
  const data = await api("/api/nickname", {
    method: "POST",
    body: JSON.stringify({ nickname }),
  });

  setResultMessage(data.message || "暱稱已更新", Boolean(data.ok));
  await loadMe();
  await loadBoard();
}

async function submitCode() {
  if (!currentQuestion) {
    return;
  }
  const code = getCodeInput().value;
  const data = await api("/api/submit", {
    method: "POST",
    body: JSON.stringify({ code }),
  });

  setResultMessage(data.message, Boolean(data.ok));
  await loadMe();
  await loadBoard();
}

async function viewSolution() {
  if (!currentQuestion) {
    return;
  }
  const data = await api("/api/solution");
  if (!data.ok) {
    setResultMessage(data.message || "目前無法顯示解答", false);
    return;
  }

  document.getElementById("solution").textContent = data.solution_code;
  document.getElementById("solutionBlock").open = true;
  setResultMessage(data.message, true);
  await loadMe();
  await loadBoard();
}

function handleTabIndent(event) {
  const textarea = event.target;
  if (event.key === "Tab") {
    event.preventDefault();
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;

    if (start !== end) {
      const lineStart = value.lastIndexOf("\n", start - 1) + 1;
      const selected = value.slice(lineStart, end);
      const lines = selected.split("\n");
      const updated = lines.map((line) => {
        if (event.shiftKey) {
          if (line.startsWith("    ")) return line.slice(4);
          if (line.startsWith("\t")) return line.slice(1);
          return line;
        }
        return `    ${line}`;
      });
      const replacement = updated.join("\n");
      textarea.value = value.slice(0, lineStart) + replacement + value.slice(end);
      textarea.selectionStart = lineStart;
      textarea.selectionEnd = lineStart + replacement.length;
      return;
    }

    const insertion = event.shiftKey ? "" : "    ";
    textarea.value = value.slice(0, start) + insertion + value.slice(end);
    const next = start + insertion.length;
    textarea.selectionStart = next;
    textarea.selectionEnd = next;
    return;
  }

  if (event.key === "Enter") {
    const start = textarea.selectionStart;
    const value = textarea.value;
    const lineStart = value.lastIndexOf("\n", start - 1) + 1;
    const currentLine = value.slice(lineStart, start);
    const indentMatch = currentLine.match(/^\s*/);
    const indent = indentMatch ? indentMatch[0] : "";

    event.preventDefault();
    const extraIndent = currentLine.trimEnd().endsWith(":") ? "    " : "";
    const insertText = `\n${indent}${extraIndent}`;
    textarea.value = value.slice(0, start) + insertText + value.slice(textarea.selectionEnd);
    const pos = start + insertText.length;
    textarea.selectionStart = pos;
    textarea.selectionEnd = pos;
  }
}

function bindEditorShortcuts() {
  getCodeInput().addEventListener("keydown", handleTabIndent);
}

document.getElementById("saveNick").addEventListener("click", saveNickname);
document.getElementById("submitBtn").addEventListener("click", submitCode);
document.getElementById("viewSolutionBtn").addEventListener("click", viewSolution);
bindEditorShortcuts();

loadMe();
loadBoard();
setInterval(loadBoard, 5000);
