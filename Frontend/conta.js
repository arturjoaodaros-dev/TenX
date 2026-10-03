"use strict";

// Se o frontend for servido por outra origem, ajuste a base (ex.: "http://127.0.0.1:8000").
const API_BASE = "";
const SESSION_KEY = "tenx_usuario_id"; // gravado por app.js a partir da resposta do login

const el = (id) => document.getElementById(id);
const feedback = el("feedback");
const usuarioId = sessionStorage.getItem(SESSION_KEY);

function showFeedback(type, message) {
  feedback.className = `feedback ${type}`;
  feedback.textContent = message;
  feedback.hidden = false;
}

function logout() {
  sessionStorage.removeItem(SESSION_KEY);
  window.location.href = "index.html";
}

async function request(method, path, body) {
  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(body),
  });
  let data = null;
  try { data = await response.json(); } catch { /* resposta sem corpo */ }
  return { response, data };
}

function errorMessage({ response, data }, fallback) {
  if ([404, 405, 501].includes(response.status)) {
    return "Esta função ainda não está disponível no servidor (rota /usuarios incompleta).";
  }
  if (response.status === 401 || response.status === 403) return "Senha incorreta ou sem permissão.";
  if (response.status === 409) return "Já existe uma conta com este e-mail.";
  return (data && typeof data.detail === "string" && data.detail) || fallback;
}

// Sem ID (login não finalizado no backend) as ações ficam desabilitadas.
if (usuarioId) {
  el("usuario-id").textContent = usuarioId;
} else {
  showFeedback("error", "ID do usuário indisponível: o login ainda não informou o ID. Alterar e excluir ficam desabilitados.");
  ["update-submit", "delete-open"].forEach((id) => (el(id).disabled = true));
}

el("logout").addEventListener("click", logout);

// ---------- Alterar dados ----------
el("update-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  feedback.hidden = true;
  const values = {
    nome: el("nome").value.trim(),
    email: el("email").value.trim(),
    senha: el("senha").value,
  };
  const body = Object.fromEntries(Object.entries(values).filter(([, v]) => v));

  if (!Object.keys(body).length) return showFeedback("error", "Preencha ao menos um campo.");
  if (body.email && !el("email").validity.valid) return showFeedback("error", "Informe um e-mail válido.");
  if (body.senha && body.senha.length < 8) return showFeedback("error", "A senha deve ter ao menos 8 caracteres.");

  const submit = el("update-submit");
  submit.disabled = true;
  try {
    const result = await request("PATCH", `/usuarios/?id_usuario=${encodeURIComponent(usuarioId)}`, body);
    if (!result.response.ok) return showFeedback("error", errorMessage(result, "Não foi possível salvar."));
    el("update-form").reset();
    showFeedback("success", "Dados atualizados.");
  } catch {
    showFeedback("error", "Não foi possível conectar ao servidor.");
  } finally {
    submit.disabled = false;
  }
});

// ---------- Excluir conta ----------
const dialog = el("dialog");
const dialogError = el("dialog-error");

el("delete-open").addEventListener("click", () => {
  dialogError.hidden = true;
  el("delete-form").reset();
  dialog.showModal();
});
el("delete-cancel").addEventListener("click", () => dialog.close());

el("delete-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!el("delete-form").checkValidity()) return el("delete-form").reportValidity();

  const submit = el("delete-submit");
  submit.disabled = true;
  dialogError.hidden = true;
  try {
    const result = await request("DELETE", `/usuarios/${encodeURIComponent(usuarioId)}`, {
      senha: el("delete-senha").value,
    });
    if (!result.response.ok) {
      dialogError.textContent = errorMessage(result, "Não foi possível excluir a conta.");
      dialogError.hidden = false;
      return;
    }
    logout();
  } catch {
    dialogError.textContent = "Não foi possível conectar ao servidor.";
    dialogError.hidden = false;
  } finally {
    submit.disabled = false;
  }
});
