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
    event.preventDefault();

    // Determine the permission level based on the selectedPermission
    let isFieldOperator = false;
    let isBaseOperator = false;
    let isAdmin = false;

    if (selectedPermission === "Operador de campo") {
      isFieldOperator = true;
    } else if (selectedPermission === "Operador de base") {
      isBaseOperator = true;
    } else if (selectedPermission === "Administrador") {
      isAdmin = true;
    }

    // Create a user object based on the form data
    const userData = {
      name: name,
      email: email,
      militar_idt: idtMil,
      password: password,
      comments: comments,
      is_field_operator: isFieldOperator,
      is_base_operator: isBaseOperator,
      is_admin: isAdmin,
    };

    // Send the user data to the Django endpoint for user creation
    try {
      const response = await fetch(`${backendUrl}/api/create_user/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (response.status === 201) {
        alert("User created successfully");
        navigate("/");
      } else {
        alert("Error creating user");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error creating user");
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
