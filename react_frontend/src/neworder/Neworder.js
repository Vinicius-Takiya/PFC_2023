import React, { useState, useEffect } from "react";
import "./Neworder.css";
import { useNavigate } from "react-router-dom";
import backendUrl from "../Config";

function Neworder() {
  const navigate = useNavigate();
  const [orderName, setOrderName] = useState("");
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [selectedBase, setSelectedBase] = useState("");
  const [field_comments, setComments] = useState("");
  const [baseOperators, setBaseOperators] = useState([]); // State for base operators
  const [fieldOperator, setFieldOperator] = useState(null); // State for field operator
  const authToken = localStorage.getItem("authToken");
  const email = localStorage.getItem("email");
  const id = localStorage.getItem("id");
  const name = localStorage.getItem("name");

  useEffect(() => {
    setFieldOperator(id); // Set the field operator based on user info
    // Fetch the list of base operators from your backend API
    fetch(`${backendUrl}/api/base_operators/`, {
      headers: {
        Authorization: `Token ${authToken}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data)) {
          // Verify that data is an array
          setBaseOperators(data); // Populate the state variable with fetched data
        } else {
          console.error("Data is not an array:", data);
        }
      })
      .catch((error) => {
        console.error("Error fetching base operators:", error);
      });
  }, []);

  async function handleClick(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("order_name", orderName);
    formData.append("base_operator", selectedBase);
    formData.append("field_comments", field_comments);
    formData.append("field_operator", fieldOperator); // Include the field operator (user ID)

    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append("files", selectedFiles[i]);
    }

    try {
      const response = await fetch(`${backendUrl}/api/create_order/`, {
        method: "POST",
        body: formData,
      });

      if (response.status === 201) {
        alert("Order created successfully");
      } else {
        alert("Error creating order");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error creating order");
    }
  }

  return (
    <div>
      <h2 className="title_levantamento">Novo levantamento</h2>
      <div className="elements">
        <input
          className="nome_levantamento"
          type="text"
          placeholder="Nome do levantamento"
          value={orderName}
          onChange={(e) => setOrderName(e.target.value)}
        />
        <p></p>
        <input
          className="file"
          type="file"
          onChange={(e) => setSelectedFiles(e.target.files)}
          multiple
        />
        <p></p>
        <input
          className="sendto_levantamento"
          list="bases"
          placeholder="Enviar para"
          value={selectedBase}
          onChange={(e) => setSelectedBase(e.target.value)}
        />
        <p></p>
        <datalist id="bases">
          {baseOperators.map((operator) => (
            <option key={operator.id} value={operator.id}>
              {operator.name}
            </option>
          ))}
        </datalist>
        <textarea
          className="coment_levantamento"
          type="text"
          placeholder="Comentários"
          rows="5"
          value={field_comments}
          onChange={(e) => setComments(e.target.value)}
        />
      </div>
      <button type="button" onClick={handleClick} className="sendorder">
        Enviar
      </button>
      <p></p>
    </div>
  );
}

export default Neworder;
