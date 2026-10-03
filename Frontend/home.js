"use strict";

// Se o frontend for servido por outra origem, ajuste a base (ex.: "http://127.0.0.1:8000").
const API_BASE = "";

const feedback = document.getElementById("feedback");
const el = (id) => document.getElementById(id);
const state = { materias: [], bobicas: [] };

function showFeedback(type, message) {
  feedback.className = `feedback ${type}`;
  feedback.textContent = message;
  feedback.hidden = false;
}

async function api(path, options) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    ...options,
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json().catch(() => null);
}

// O backend responde 200 com "status" textual mesmo em falha ("erro na criacao...").
function statusOk(data) {
  return !!data && typeof data.status === "string" && !data.status.toLowerCase().includes("erro");
}

function button(label, className, onClick) {
  const b = document.createElement("button");
  b.type = "button";
  b.textContent = label;
  b.className = className;
  b.addEventListener("click", onClick);
  return b;
}

// items: [{ key, text, onEdit, onDelete }]
function renderList(listEl, items, emptyText) {
  if (!items.length) {
    const li = document.createElement("li");
    li.textContent = emptyText;
    listEl.replaceChildren(li);
    return;
  }
  listEl.replaceChildren(
    ...items.map((item) => {
      const li = document.createElement("li");
      li.className = "row";
      li.dataset.key = item.key;
      const span = document.createElement("span");
      span.textContent = item.text;
      const actions = document.createElement("span");
      actions.className = "actions";
      actions.append(
        button("Editar", "secondary", item.onEdit),
        button("Excluir", "danger", item.onDelete)
      );
      li.append(span, actions);
      return li;
    })
  );
}

function renderOptions(select, names) {
  select.replaceChildren(
    ...names.map((name) => {
      const option = document.createElement("option");
      option.value = option.textContent = name;
      return option;
    })
  );
}

// ---------- Diálogo (editar / excluir) ----------
const dialog = el("dialog");
const dialogForm = el("dialog-form");
const dialogTitle = el("dialog-title");
const dialogBody = el("dialog-body");
const dialogError = el("dialog-error");
const dialogSubmit = el("dialog-submit");
let dialogHandler = null;

function fieldEl({ id, label, type, value, options }) {
  const wrap = document.createElement("div");
  wrap.className = "field";
  const lab = document.createElement("label");
  lab.htmlFor = `dlg-${id}`;
  lab.textContent = label;
  let input;
  if (type === "select") {
    input = document.createElement("select");
    renderOptions(input, options);
  } else {
    input = document.createElement("input");
    input.type = type;
    if (type === "number") Object.assign(input, { min: "0", step: "0.01" });
    if (type === "password") input.autocomplete = "off";
  }
  input.id = `dlg-${id}`;
  input.required = true;
  if (value !== undefined) input.value = value;
  wrap.append(lab, input);
  return wrap;
}

function openDialog({ title, submitLabel, danger, intro, fields, onSubmit }) {
  dialogTitle.textContent = title;
  dialogSubmit.textContent = submitLabel;
  dialogSubmit.className = danger ? "danger solid" : "primary";
  dialogError.hidden = true;
  const children = [];
  if (intro) {
    const p = document.createElement("p");
    p.textContent = intro;
    children.push(p);
  }
  children.push(...fields.map(fieldEl));
  dialogBody.replaceChildren(...children);
  dialogHandler = onSubmit;
  dialog.showModal();
}

el("dialog-cancel").addEventListener("click", () => dialog.close());

dialogForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!dialogForm.checkValidity()) {
    dialogForm.reportValidity();
    return;
  }
  dialogSubmit.disabled = true;
  dialogError.hidden = true;
  try {
    const value = (id) => el(`dlg-${id}`).value;
    await dialogHandler(value);
    dialog.close();
  } catch (error) {
    dialogError.textContent = error.message || "Não foi possível concluir a operação.";
    dialogError.hidden = false;
  } finally {
    dialogSubmit.disabled = false;
  }
});

// ---------- Operações ----------
function put(path, body, success) {
  return async () => {
    const data = await api(path, { method: "PUT", body: JSON.stringify(body) }).catch(() => {
      throw new Error("Não foi possível conectar ao servidor.");
    });
    if (!statusOk(data)) throw new Error((data && data.status) || "Não foi possível atualizar.");
    showFeedback("success", success);
    await refresh();
  };
}

// DELETE exige a senha de destruição do backend, digitada pelo usuário (nunca guardada no front).
// O backend responde 200 mesmo com senha errada; por isso conferimos se o item sumiu da lista.
async function remove(path, senha, key, success) {
  await api(`${path}?senha=${encodeURIComponent(senha)}`, { method: "DELETE" }).catch(() => {
    throw new Error("Não foi possível conectar ao servidor.");
  });
  await refresh();
  if (document.querySelector(`[data-key="${CSS.escape(key)}"]`)) {
    throw new Error("Não foi excluído. Confira a senha de exclusão.");
  }
  showFeedback("success", success);
}

function confirmDelete(what, path, key, success) {
  openDialog({
    title: `Excluir ${what}`,
    submitLabel: "Excluir",
    danger: true,
    intro: "Esta ação não pode ser desfeita. Informe a senha de exclusão para confirmar.",
    fields: [{ id: "senha", label: "Senha de exclusão", type: "password" }],
    onSubmit: (v) => remove(path, v("senha"), key, success),
  });
}

function editMateria(nome) {
  openDialog({
    title: "Editar matéria",
    submitLabel: "Salvar",
    fields: [{ id: "nome", label: "Nome", type: "text", value: nome }],
    onSubmit: (v) =>
      put(`/materias/?nome_materia=${encodeURIComponent(nome)}`, { nome: v("nome").trim() }, "Matéria atualizada.")(),
  });
}

function editBobica(nome) {
  openDialog({
    title: "Editar bobica",
    submitLabel: "Salvar",
    fields: [
      { id: "nome", label: "Nome", type: "text", value: nome },
      { id: "preco", label: "Preço médio (R$)", type: "number" },
    ],
    onSubmit: (v) =>
      put(
        `/bobicas/?nome_bobica=${encodeURIComponent(nome)}`,
        { nome: v("nome").trim(), preco_medio: Number(v("preco")) },
        "Bobica atualizada."
      )(),
  });
}

function editProva(materia) {
  openDialog({
    title: `Editar prova de ${materia}`,
    submitLabel: "Salvar",
    fields: [
      { id: "materia", label: "Matéria", type: "select", options: state.materias, value: materia },
      { id: "bobica", label: "Bobica", type: "select", options: state.bobicas },
    ],
    onSubmit: (v) =>
      put(
        `/provas/?nome_materia=${encodeURIComponent(materia)}`,
        { nome_materia: v("materia"), nome_bobica: v("bobica") },
        "Prova atualizada."
      )(),
  });
}

// ---------- Carregamento ----------
async function loadMaterias() {
  const { nomes } = await api("/materias/");
  state.materias = nomes;
  renderList(
    el("lista-materias"),
    nomes.map((n) => ({
      key: n,
      text: n,
      onEdit: () => editMateria(n),
      onDelete: () => confirmDelete(`matéria "${n}"`, `/materias/${encodeURIComponent(n)}`, n, "Matéria excluída."),
    })),
    "Nenhuma matéria cadastrada."
  );
  renderOptions(el("prova-materia"), nomes);
  return nomes;
}

async function loadBobicas() {
  const { nomes } = await api("/bobicas/");
  state.bobicas = nomes;
  renderList(
    el("lista-bobicas"),
    nomes.map((n) => ({
      key: n,
      text: n,
      onEdit: () => editBobica(n),
      onDelete: () => confirmDelete(`bobica "${n}"`, `/bobicas/${encodeURIComponent(n)}`, n, "Bobica excluída."),
    })),
    "Nenhuma bobica cadastrada."
  );
  renderOptions(el("prova-bobica"), nomes);
}

// GET /provas/{materia} devolve [[materia, quantidade]]
async function loadProvas(materias) {
  const rows = await Promise.all(
    materias.map((m) => api(`/provas/${encodeURIComponent(m)}`).catch(() => []))
  );
  renderList(
    el("lista-provas"),
    rows.flat().map(([materia, qtd]) => ({
      key: `prova:${materia}`,
      text: `${materia}: ${qtd} prova(s)`,
      onEdit: () => editProva(materia),
      onDelete: () =>
        confirmDelete(
          `provas de "${materia}"`,
          `/provas/${encodeURIComponent(materia)}`,
          `prova:${materia}`,
          "Provas excluídas."
        ),
    })),
    "Nenhuma prova cadastrada."
  );
}

async function refresh() {
  try {
    const materias = await loadMaterias();
    await Promise.all([loadBobicas(), loadProvas(materias)]);
  } catch {
    showFeedback("error", "Não foi possível carregar os dados do servidor.");
  }
}

// ---------- Cadastro ----------
function bindForm(formId, buildRequest, successMessage) {
  const form = el(formId);
  const submit = form.querySelector("button[type=submit]");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    feedback.hidden = true;
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    submit.disabled = true;
    try {
      const { path, body } = buildRequest();
      const data = await api(path, { method: "POST", body: JSON.stringify(body) });
      if (!statusOk(data)) {
        showFeedback("error", (data && data.status) || "Não foi possível cadastrar.");
        return;
      }
      form.reset();
      showFeedback("success", successMessage);
      await refresh();
    } catch {
      showFeedback("error", "Não foi possível conectar ao servidor.");
    } finally {
      submit.disabled = false;
    }
  });
}

bindForm(
  "form-materia",
  () => ({ path: "/materias/", body: { nome: el("materia-nome").value.trim() } }),
  "Matéria cadastrada."
);
bindForm(
  "form-bobica",
  () => ({
    path: "/bobicas/",
    body: { nome: el("bobica-nome").value.trim(), preco_medio: Number(el("bobica-preco").value) },
  }),
  "Bobica cadastrada."
);
bindForm(
  "form-prova",
  () => ({
    path: "/provas/",
    body: { nome_materia: el("prova-materia").value, nome_bobica: el("prova-bobica").value },
  }),
  "Prova cadastrada."
);

refresh();
