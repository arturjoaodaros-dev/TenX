"use strict";

// Endpoint de criação de usuário (rota /usuarios ainda incompleta no backend).
// Se o frontend for servido por outra origem, ajuste a base aqui (ex.: "http://127.0.0.1:8000").
const API_BASE = "";
const SIGNUP_URL = `${API_BASE}/usuarios`;
const MIN_PASSWORD = 8;

const form = document.getElementById("signup-form");
const submitBtn = document.getElementById("submit");
const feedback = document.getElementById("feedback");
const fields = {
  nome: document.getElementById("nome"),
  email: document.getElementById("email"),
  senha: document.getElementById("senha"),
  confirmar: document.getElementById("confirmar"),
};

function setFieldError(name, message) {
  const error = document.getElementById(`${name}-error`);
  error.textContent = message || "";
  error.hidden = !message;
  fields[name].setAttribute("aria-invalid", message ? "true" : "false");
}

function showFeedback(type, message) {
  feedback.className = `feedback ${type}`;
  feedback.textContent = message;
  feedback.hidden = false;
}

function setLoading(loading) {
  submitBtn.disabled = loading;
  submitBtn.textContent = loading ? "Cadastrando…" : "Cadastrar";
  form.setAttribute("aria-busy", String(loading));
  Object.values(fields).forEach((input) => (input.disabled = loading));
}

function validate() {
  const nome = fields.nome.value.trim();
  const email = fields.email.value.trim();
  const { senha, confirmar } = { senha: fields.senha.value, confirmar: fields.confirmar.value };

  const errors = {
    nome: nome ? "" : "Informe o nome.",
    email: !email ? "Informe o e-mail." : fields.email.validity.valid ? "" : "Informe um e-mail válido.",
    senha: !senha ? "Informe a senha." : senha.length < MIN_PASSWORD ? `A senha deve ter ao menos ${MIN_PASSWORD} caracteres.` : "",
    confirmar: !confirmar ? "Confirme a senha." : confirmar !== senha ? "As senhas não coincidem." : "",
  };

  let firstInvalid = null;
  for (const name of Object.keys(errors)) {
    setFieldError(name, errors[name]);
    if (errors[name] && !firstInvalid) firstInvalid = fields[name];
  }
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
  if (response.status === 409) return "Já existe uma conta com este e-mail.";
  if (response.status === 404 || response.status === 405 || response.status === 501) {
    return "O cadastro ainda não está disponível no servidor (rota /usuarios incompleta).";
  }
  if (body && typeof body.detail === "string") return body.detail;
  return "Não foi possível concluir o cadastro. Tente novamente.";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  feedback.hidden = true;
  if (!validate()) return;

  setLoading(true);
  try {
    const response = await fetch(SIGNUP_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({
        nome: fields.nome.value.trim(),
        email: fields.email.value.trim(),
        senha: fields.senha.value,
      }),
    });
    const body = await readBody(response);

    if (!response.ok) {
      showFeedback("error", errorMessage(response, body));
      return;
    }

    form.reset();
    showFeedback("success", "Cadastro realizado com sucesso. Você já pode entrar.");
  } catch {
    showFeedback("error", "Não foi possível conectar ao servidor.");
  } finally {
    setLoading(false);
  }
});

Object.keys(fields).forEach((name) =>
  fields[name].addEventListener("input", () => setFieldError(name, ""))
);
