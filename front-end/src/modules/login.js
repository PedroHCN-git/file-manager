const API_BASE_URL = "http://127.0.0.1:8080";
const loginForm = document.querySelector("#login-form");
const loginStatus = document.querySelector("#login-status");
const loginButton = loginForm.querySelector('button[type="submit"]');

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  loginButton.disabled = true;
  loginStatus.textContent = "Entrando...";

  const formData = new FormData(loginForm);

  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: formData.get("email"),
        password: formData.get("password"),
      }),
    });

    if (response.status === 401) {
      loginStatus.textContent = "E-mail ou senha incorretos.";
      return;
    }
    if (!response.ok) {
      throw new Error(`O servidor respondeu com o status ${response.status}.`);
    }

    const result = await response.json();
    if (typeof result.access_token !== "string") {
      throw new Error("O servidor retornou uma sessão inválida.");
    }

    sessionStorage.setItem("access_token", result.access_token);
    window.location.replace("index.html");
  } catch (error) {
    loginStatus.textContent =
      `Não foi possível entrar. Verifique se o backend está em execução. ${error.message}`;
  } finally {
    loginButton.disabled = false;
  }
});
