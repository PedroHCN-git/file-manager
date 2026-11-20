const API_BASE_URL = "http://127.0.0.1:8080";
const registerForm = document.querySelector("#register-form");
const registerStatus = document.querySelector("#register-status");
const registerButton = registerForm.querySelector('button[type="submit"]');

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  registerButton.disabled = true;
  registerStatus.textContent = "Criando sua conta...";

  const formData = new FormData(registerForm);
  const credentials = {
    name: formData.get("name"),
    category: formData.get("category"),
    email: formData.get("email"),
    password: formData.get("password"),
  };

  try {
    const registration = await fetch(`${API_BASE_URL}/users/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });

    if (registration.status === 409) {
      registerStatus.textContent = "Já existe uma conta com este e-mail.";
      return;
    }
    if (!registration.ok) {
      throw new Error(`O servidor respondeu com o status ${registration.status}.`);
    }

    const login = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });
    if (!login.ok) {
      throw new Error(
        "A conta foi criada, mas não foi possível iniciar a sessão. Entre pela tela de login.",
      );
    }

    const result = await login.json();
    if (typeof result.access_token !== "string") {
      throw new Error("O servidor retornou uma sessão inválida.");
    }

    sessionStorage.setItem("access_token", result.access_token);
    window.location.replace("index.html");
  } catch (error) {
    registerStatus.textContent =
      `Não foi possível criar a conta. Verifique se o backend está em execução. ${error.message}`;
  } finally {
    registerButton.disabled = false;
  }
});
