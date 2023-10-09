import React, { useState, useEffect } from "react";
import "./Register.css";
import { useNavigate } from "react-router-dom";
import backendUrl from "../Config";

function Neworder() {
  const navigate = useNavigate();
  const [selectedBase, setSelectedBase] = useState("");
  const [selectedPermission, setSelectedPermission] = useState("");
  const [name, setName] = useState("");
  const [idtMil, setIdtMil] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [comments, setComments] = useState("");
  const [csrfToken, setCsrfToken] = useState("");

  useEffect(() => {
    // Fetch the CSRF token from the Django API endpoint
    fetch(`${backendUrl}/api/get_csrf_token/`) // Replace with the actual API endpoint
      .then((response) => response.json())
      .then((data) => {
        setCsrfToken(data.csrfToken);
      })
      .catch((error) => {
        console.error("Error fetching CSRF token:", error);
      });
  }, []);

  useEffect(() => {
    // Add an event listener for the "Nº Idt Mil" input
    const idtMilInput = document.querySelector(".idt-mil-input");
    if (idtMilInput) {
      idtMilInput.addEventListener("keypress", handleIdtMilKeyPress);
    }

    // Cleanup: Remove the event listener when the component unmounts
    return () => {
      if (idtMilInput) {
        idtMilInput.removeEventListener("keypress", handleIdtMilKeyPress);
      }
    };
  }, []); // The empty dependency array ensures this effect runs once on component mount

  function handleIdtMilKeyPress(event) {
    if (event.charCode < 48 || event.charCode > 57) {
      event.preventDefault();
    }
  }

  async function handleClick(event) {
    if (selectedBase === "") {
      alert("Please select a base from the list.");
      return;
    }

    if (selectedPermission === "") {
      alert("Please select a permission from the list.");
      return;
    }
    const headers = {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken, // Add the CSRF token from the JavaScript variable
    };
    // Send the form data to the Django endpoint
    try {
      const response = await fetch(`${backendUrl}/api/send_email/`, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
          name: name,
          idt_mil: idtMil,
          email: email,
          password: password,
          comments: comments,
        }),
      });

      if (response.status === 200) {
        alert("Email sent successfully");
      } else {
        alert("Error sending email");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error sending email");
    }
  }

  return (
    <div>
      <h2 className="titleRegister">Solicitar cadastro</h2>
      <div className="elements">
        <input
          className="nome"
          type="text"
          placeholder="Nome completo"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <p></p>
        <input
          className="nome idt-mil-input"
          type="text"
          placeholder="Nº Idt Mil"
          value={idtMil}
          onChange={(e) => setIdtMil(e.target.value)}
        />
        <p></p>
        <input
          className="nome"
          type="email"
          placeholder="E-mail"
          pattern=".+@.*eb\.br"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <p></p>
        <input
          className="nome"
          type="text"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <p></p>
        <input
          className="nome"
          list="bases"
          placeholder="CGEO responsável"
          onChange={(e) => setSelectedBase(e.target.value)}
        />
        <p></p>
        <datalist id="bases">
          <option value="1º CGEO" />
          <option value="2º CGEO" />
          <option value="3º CGEO" />
          <option value="4º CGEO" />
          <option value="5º CGEO" />
        </datalist>
        <input
          className="nome"
          list="permissoes"
          placeholder="Permissão de usuário"
          onChange={(e) => setSelectedPermission(e.target.value)}
        />
        <p></p>
        <datalist id="permissoes">
          <option value="Operador de campo" />
          <option value="Operador de base" />
          <option value="Administrador" />
        </datalist>
        <textarea
          className="nome"
          type="text"
          placeholder="Comentários"
          rows="5"
        />
      </div>
      <button type="button" onClick={handleClick} className="sendorder">
        Solicitar Cadastro
      </button>
      <p></p>
    </div>
  );
}

export default Neworder;
