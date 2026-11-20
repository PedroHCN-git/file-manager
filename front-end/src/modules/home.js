const API_BASE_URL = "http://127.0.0.1:8080";
const documentStatus = document.querySelector("#document-status");
const documentList = document.querySelector("#document-list");
const documentSearch = document.querySelector("#document-search");
const logoutButton = document.querySelector("#logout-button");
const uploadForm = document.querySelector("#upload-form");
const uploadInput = document.querySelector("#document-file");
const uploadButton = document.querySelector("#upload-button");
const selectedFileName = document.querySelector("#selected-file-name");
const uploadQueue = document.querySelector("#upload-queue");
const uploadStatus = document.querySelector("#upload-status");
const accessToken = sessionStorage.getItem("access_token");
const selectedFiles = [];
let isUploading = false;
let documentLoadRequestId = 0;
let searchTimeout;

function showLogin() {
  sessionStorage.removeItem("access_token");
  window.location.replace("login.html");
}

function showStatus(message, isError = false) {
  documentStatus.textContent = message;
  documentStatus.hidden = false;
  documentStatus.classList.toggle("document-status-error", isError);
}

uploadInput.addEventListener("change", () => {
  selectedFiles.push(...uploadInput.files);
  uploadInput.value = "";
  renderUploadQueue();
});

function renderUploadQueue() {
  uploadQueue.replaceChildren();
  uploadQueue.hidden = selectedFiles.length === 0;

  selectedFiles.forEach((file, index) => {
    const item = document.createElement("li");
    item.className = "upload-queue-item";

    const name = document.createElement("span");
    name.className = "upload-queue-name";
    name.textContent = file.name;

    const removeButton = document.createElement("button");
    removeButton.className = "upload-queue-remove";
    removeButton.type = "button";
    removeButton.textContent = "Remover";
    removeButton.disabled = isUploading;
    removeButton.setAttribute("aria-label", `Remover ${file.name} da lista`);
    removeButton.addEventListener("click", () => {
      selectedFiles.splice(index, 1);
      renderUploadQueue();
    });

    item.append(name, removeButton);
    uploadQueue.append(item);
  });

  selectedFileName.textContent = selectedFiles.length === 0
    ? "Escolher arquivos"
    : `${selectedFiles.length} arquivo(s) selecionado(s)`;
  uploadButton.disabled = selectedFiles.length === 0 || isUploading;
  uploadInput.disabled = isUploading;
}

function renderDocuments(documents) {
  documentList.replaceChildren();

  if (documents.length === 0) {
    showStatus(
      documentSearch.value.trim()
        ? "Nenhum arquivo corresponde à busca."
        : "Nenhum arquivo encontrado.",
    );
    return;
  }

  documentStatus.hidden = true;

  for (const doc of documents) {
    const item = document.createElement("li");
    item.className = "document-item";

    const name = document.createElement("span");
    name.className = "document-name";
    name.textContent = doc.doc_name;

    const deleteButton = document.createElement("button");
    deleteButton.className = "document-delete";
    deleteButton.type = "button";
    deleteButton.textContent = "Excluir";
    deleteButton.setAttribute(
      "aria-label",
      `Excluir ${doc.doc_name}`,
    );
    deleteButton.addEventListener("click", () => deleteDocument(doc, deleteButton));

    const downloadButton = document.createElement("button");
    downloadButton.className = "document-download";
    downloadButton.type = "button";
    downloadButton.textContent = "Baixar";
    downloadButton.setAttribute(
      "aria-label",
      `Baixar ${doc.doc_name}`,
    );
    downloadButton.addEventListener(
      "click",
      () => downloadDocument(doc, downloadButton),
    );

    const actions = document.createElement("div");
    actions.className = "document-actions";
    actions.append(downloadButton, deleteButton);

    item.append(name, actions);
    documentList.append(item);
  }
}

async function loadDocuments() {
  const requestId = ++documentLoadRequestId;
  const searchTerm = documentSearch.value.trim();
  documentList.replaceChildren();
  showStatus("Carregando arquivos...");

  try {
    const query = new URLSearchParams();
    if (searchTerm) {
      query.set("name", searchTerm);
    }
    const queryString = query.toString();
    const response = await fetch(
      `${API_BASE_URL}/documents/all${queryString ? `?${queryString}` : ""}`,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      },
    );
    if (requestId !== documentLoadRequestId) {
      return;
    }
    if (response.status === 401) {
      showLogin();
      return;
    }
    if (!response.ok) {
      throw new Error(`O servidor respondeu com o status ${response.status}.`);
    }

    const documents = await response.json();
    if (
      !Array.isArray(documents) ||
      documents.some(
        (document) =>
          !Number.isInteger(document.doc_id) ||
          typeof document.doc_name !== "string",
      )
    ) {
      throw new Error("O servidor retornou uma lista de arquivos inválida.");
    }

    if (requestId === documentLoadRequestId) {
      renderDocuments(documents);
    }
  } catch (error) {
    if (requestId !== documentLoadRequestId) {
      return;
    }
    showStatus(
      `Não foi possível carregar os arquivos. Verifique se o backend está em execução. ${error.message}`,
      true,
    );
  }
}

documentSearch.addEventListener("input", () => {
  window.clearTimeout(searchTimeout);
  searchTimeout = window.setTimeout(() => {
    loadDocuments();
  }, 250);
});

async function deleteDocument(document, button) {
  const confirmed = window.confirm(`Deseja excluir "${document.doc_name}"?`);
  if (!confirmed) {
    return;
  }

  button.disabled = true;

  try {
    const query = new URLSearchParams({ doc_id: String(document.doc_id) });
    const response = await fetch(`${API_BASE_URL}/documents/?${query}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (response.status === 401) {
      showLogin();
      return;
    }
    if (!response.ok) {
      throw new Error(`O servidor respondeu com o status ${response.status}.`);
    }

    await loadDocuments();
  } catch (error) {
    button.disabled = false;
    showStatus(`Não foi possível excluir o arquivo. ${error.message}`, true);
  }
}

async function downloadDocument(doc, button) {
  button.disabled = true;

  try {
    const query = new URLSearchParams({ doc_id: String(doc.doc_id) });
    const response = await fetch(
      `${API_BASE_URL}/documents/download?${query}`,
      { headers: { Authorization: `Bearer ${accessToken}` } },
    );
    if (response.status === 401) {
      showLogin();
      return;
    }
    if (!response.ok) {
      const error = await response.json().catch(() => null);
      throw new Error(
        error?.detail ?? `O servidor respondeu com o status ${response.status}.`,
      );
    }

    const blob = await response.blob();
    const downloadUrl = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = doc.doc_name;
    link.click();
    window.setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
  } catch (error) {
    showStatus(`Não foi possível baixar o arquivo. ${error.message}`, true);
  } finally {
    button.disabled = false;
  }
}

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (selectedFiles.length === 0) {
    uploadStatus.textContent = "Selecione pelo menos um arquivo para enviar.";
    return;
  }

  isUploading = true;
  renderUploadQueue();
  uploadStatus.textContent =
    `Enviando ${selectedFiles.length} arquivo(s)...`;

  try {
    const formData = new FormData();
    for (const file of selectedFiles) {
      formData.append("files", file);
    }

    const response = await fetch(`${API_BASE_URL}/documents/`, {
      method: "POST",
      headers: { Authorization: `Bearer ${accessToken}` },
      body: formData,
    });

    if (response.status === 401) {
      showLogin();
      return;
    }
    if (!response.ok) {
      const error = await response.json().catch(() => null);
      throw new Error(
        error?.detail ?? `O servidor respondeu com o status ${response.status}.`,
      );
    }

    const uploadedDocuments = await response.json();
    if (
      !Array.isArray(uploadedDocuments) ||
      uploadedDocuments.length !== selectedFiles.length
    ) {
      throw new Error("O servidor retornou uma confirmação de envio inválida.");
    }

    const uploadedCount = selectedFiles.length;
    selectedFiles.length = 0;
    renderUploadQueue();
    uploadStatus.textContent =
      `${uploadedCount} arquivo(s) enviado(s) com sucesso.`;
    await loadDocuments();
  } catch (error) {
    uploadStatus.textContent =
      `Não foi possível enviar o arquivo. Verifique a conexão, a origem local do site e se o backend está em execução. ${error.message}`;
  } finally {
    isUploading = false;
    renderUploadQueue();
  }
});

logoutButton.addEventListener("click", async () => {
  try {
    await fetch(`${API_BASE_URL}/auth/logout`, {
      method: "POST",
      headers: { Authorization: `Bearer ${accessToken}` },
    });
  } catch (error) {
    console.error("Could not revoke the current session.", error);
  } finally {
    showLogin();
  }
});

if (accessToken === null) {
  showLogin();
} else {
  loadDocuments();
}
