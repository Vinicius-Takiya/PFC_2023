import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios"; // Import Axios for making API requests
import eb from "../components/brazilian-army-symbol.png";
import "./Login.css";
import backendUrl from "../Config";

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState(""); // Add state for password
  const [errorMessage, setErrorMessage] = useState(null);

  function handleUsernameChange(event) {
    setUsername(event.target.value);
  }

  function handlePasswordChange(event) {
    setPassword(event.target.value); // Update the password state
  }

  function handleLogin() {
    setErrorMessage(null);

    // Make a POST request to your backend login API
    axios
      .post(`${backendUrl}/api/login`, { email: username, password })
      .then((response) => {
        localStorage.setItem("authToken", response.data["token"]);
        localStorage.setItem("email", response.data["user"]["email"]);
        localStorage.setItem("id", response.data["user"]["id"]);
        localStorage.setItem("name", response.data["user"]["name"]);
        localStorage.setItem(
          "field_operator",
          response.data["user"]["field_operator"]
        );
        localStorage.setItem(
          "base_operator",
          response.data["user"]["base_operator"]
        );
        navigate("/Homepage");
      })
      .catch((error) => {
        console.error("Authentication error:", error);
        setErrorMessage(
          "Authentication failed. Please check your credentials."
        );
      });
  }

  return (
    <div>
      <div className="logo-container">
        <img src={eb} alt="Logo" className="logo" />
      </div>
      <h3 className="titleLogin">Sistema de gerenciamento de dados</h3>
      <div className="elements">
        <input
          className="username input"
          type="text"
          placeholder="Usuário"
          value={username}
          onChange={handleUsernameChange}
        />
        <p></p>
        <input
          className="username input" // Use 'password' class for password input
          type="password" // Use 'password' type for password input
          placeholder="Senha"
          value={password}
          onChange={handlePasswordChange}
        />
        <p></p>
        <button type="button" onClick={handleLogin} className="button">
          Login
        </button>
        <p></p>
        <Link to="/register" className="register">
          Cadastro
        </Link>
        <p></p>
        <Link to="/register" className="register">
          Esqueci minha senha
        </Link>
        <p></p>
        {/* Display error message if there's an error */}
        {errorMessage && (
          <p className="error-message">
            Autenticação falhou. Por favor cheque suas credenciais.
          </p>
        )}
      </div>
    </div>
  );
}

export default Login;
