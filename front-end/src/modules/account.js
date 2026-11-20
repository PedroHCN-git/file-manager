const API_BASE_URL = "http://127.0.0.1:8080";
const accessToken = sessionStorage.getItem("access_token");
const accountForm = document.querySelector("#account-form");
const accountStatus = document.querySelector("#account-status");
const nameInput = document.querySelector("#account-name");
const categoryInput = document.querySelector("#account-category");
const emailInput = document.querySelector("#account-email");
const passwordInput = document.querySelector("#account-password");
const saveButton = document.querySelector("#account-save");
const editableInputs = [nameInput, emailInput, passwordInput];
let originalValues = null;

function showLogin() {
  sessionStorage.removeItem("access_token");
  window.location.replace("login.html");
}

function updateSaveButton() {
  if (originalValues === null) {
    saveButton.disabled = true;
    return;
  }

  const hasChanges =
    nameInput.value !== originalValues.name ||
    emailInput.value !== originalValues.email ||
    passwordInput.value.length > 0;
  saveButton.disabled = !hasChanges;
}

for (const input of editableInputs) {
  input.addEventListener("input", updateSaveButton);
}

async function loadAccount() {
  if (accessToken === null) {
    showLogin();
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    if (response.status === 401) {
      showLogin();
      return;
    }
    if (!response.ok) {
      throw new Error(`O servidor respondeu com o status ${response.status}.`);
    }

    const user = await response.json();
    if (
      typeof user.name !== "string" ||
      typeof user.category !== "string" ||
      typeof user.email !== "string"
    ) {
      throw new Error("O servidor retornou dados de conta inválidos.");
    }

    nameInput.value = user.name;
    categoryInput.value = user.category;
    emailInput.value = user.email;
    passwordInput.value = "";
    originalValues = { name: user.name, email: user.email };
    editableInputs.forEach((input) => {
      input.disabled = false;
    });
    accountStatus.textContent =
      "Altere um ou mais campos. A categoria não pode ser alterada.";
    updateSaveButton();
  } catch (error) {
    accountForm.querySelectorAll("input").forEach((input) => {
      input.disabled = true;
    });
    saveButton.disabled = true;
    accountStatus.textContent =
      `Não foi possível carregar sua conta. Verifique se o backend está em execução. ${error.message}`;
  }
}

accountForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (originalValues === null) {
    return;
  }

  const changes = {};
  if (nameInput.value !== originalValues.name) {
    changes.name = nameInput.value;
  }
  if (emailInput.value !== originalValues.email) {
    changes.email = emailInput.value;
  }
  if (passwordInput.value.length > 0) {
    changes.password = passwordInput.value;
  }
  if (Object.keys(changes).length === 0) {
    updateSaveButton();
    return;
  }

  editableInputs.forEach((input) => {
    input.disabled = true;
  });
  saveButton.disabled = true;
  accountStatus.textContent = "Salvando alterações...";

  try {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(changes),
    });

    if (response.status === 401) {
      showLogin();
      return;
    }
    if (response.status === 409) {
      accountStatus.textContent = "Já existe uma conta com este e-mail.";
      return;
    }
    if (!response.ok) {
      const error = await response.json().catch(() => null);
      throw new Error(
        error?.detail ?? `O servidor respondeu com o status ${response.status}.`,
      );
    }

    const updatedUser = await response.json();
    nameInput.value = updatedUser.name;
    categoryInput.value = updatedUser.category;
    emailInput.value = updatedUser.email;
    passwordInput.value = "";
    originalValues = {
      name: updatedUser.name,
      email: updatedUser.email,
    };
    accountStatus.textContent = "Seus dados foram atualizados com sucesso.";
  } catch (error) {
    accountStatus.textContent =
      `Não foi possível salvar as alterações. ${error.message}`;
  } finally {
    editableInputs.forEach((input) => {
      input.disabled = false;
    });
    updateSaveButton();
  }
});

loadAccount();
