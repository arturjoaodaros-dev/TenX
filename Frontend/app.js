"use strict";

// Endpoint de login (rota /usuarios ainda incompleta no backend).
// Se o frontend for servido por outra origem, ajuste a base aqui (ex.: "http://127.0.0.1:8000").
const API_BASE = "";
const LOGIN_URL = `${API_BASE}/usuarios`;

const form = document.getElementById("login-form");
const submitBtn = document.getElementById("submit");
const feedback = document.getElementById("feedback");
const toggleBtn = document.getElementById("toggle-senha");
const fields = {
  email: document.getElementById("email"),
  senha: document.getElementById("senha"),
};

function setFieldError(name, message) {
  const input = fields[name];
  const error = document.getElementById(`${name}-error`);
  error.textContent = message || "";
  error.hidden = !message;
  input.setAttribute("aria-invalid", message ? "true" : "false");
}

function showFeedback(type, message) {
  feedback.className = `feedback ${type}`;
  feedback.textContent = message;
  feedback.hidden = false;
}

function setLoading(loading) {
  submitBtn.disabled = loading;
  submitBtn.textContent = loading ? "Entrando…" : "Entrar";
  form.setAttribute("aria-busy", String(loading));
  Object.values(fields).forEach((input) => (input.disabled = loading));
}

function validate() {
  const email = fields.email.value.trim();
  const senha = fields.senha.value;
  let firstInvalid = null;

  if (!email) setFieldError("email", "Informe o e-mail.");
  else if (!fields.email.validity.valid) setFieldError("email", "Informe um e-mail válido.");
  else setFieldError("email", "");
  if (fields.email.getAttribute("aria-invalid") === "true") firstInvalid = fields.email;

  if (!senha) setFieldError("senha", "Informe a senha.");
  else setFieldError("senha", "");
  if (!firstInvalid && fields.senha.getAttribute("aria-invalid") === "true") firstInvalid = fields.senha;

  if (firstInvalid) firstInvalid.focus();
  return !firstInvalid;
}

async function readBody(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

function errorMessage(response, body) {
  if (response.status === 401 || response.status === 403) return "E-mail ou senha incorretos.";
  if (response.status === 404 || response.status === 405 || response.status === 501) {
    return "O login ainda não está disponível no servidor (rota /usuarios incompleta).";
  }
  if (body && typeof body.detail === "string") return body.detail;
  return "Não foi possível entrar. Tente novamente.";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  feedback.hidden = true;
  if (!validate()) return;

  setLoading(true);
  try {
    const response = await fetch(LOGIN_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ email: fields.email.value.trim(), senha: fields.senha.value }),
    });
    const body = await readBody(response);

    if (!response.ok) {
      showFeedback("error", errorMessage(response, body));
      return;
    }

    // Assume que o backend devolve o ID do usuário em { "id": ... } (ver TODO.mkup).
    if (body && body.id !== undefined) sessionStorage.setItem("tenx_usuario_id", String(body.id));
    form.reset();
    showFeedback("success", "Login realizado com sucesso.");
    window.location.href = "home.html";
  } catch {
    showFeedback("error", "Não foi possível conectar ao servidor.");
  } finally {
    setLoading(false);
  }
});

["email", "senha"].forEach((name) =>
  fields[name].addEventListener("input", () => setFieldError(name, ""))
);

toggleBtn.addEventListener("click", () => {
  const show = fields.senha.type === "password";
  fields.senha.type = show ? "text" : "password";
  toggleBtn.textContent = show ? "Ocultar" : "Mostrar";
  toggleBtn.setAttribute("aria-pressed", String(show));
});
