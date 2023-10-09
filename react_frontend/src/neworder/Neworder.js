import React, { useState, useEffect } from "react";
import "./Neworder.css";
import { useNavigate, useParams } from "react-router-dom";
import backendUrl from "../Config";

function Neworder() {
  const navigate = useNavigate();
  const [orderName, setOrderName] = useState("");
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [selectedBase, setSelectedBase] = useState("");
  const [field_comments, setComments] = useState("");
  const [operator_comments, setFeedback] = useState("");
  const [baseOperators, setBaseOperators] = useState([]); // State for base operators
  const [fieldOperator, setFieldOperator] = useState(null); // State for field operator
  const authToken = localStorage.getItem("authToken");
  const email = localStorage.getItem("email");
  const id = localStorage.getItem("id");
  const name = localStorage.getItem("name");
  const field_op = localStorage.getItem("field_operator");
  const base_op = localStorage.getItem("base_operator");
  const { order_number } = useParams();
  const [orderData, setOrderData] = useState([]);

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
    if (order_number) {
      fetch(`${backendUrl}/api/get_orders_by_order_id/${order_number}/`, {})
        .then((response) => {
          if (response.status === 200) {
            return response.json();
          } else {
            throw new Error("Order not found");
          }
        })
        .then((data) => {
          // Set the order data in state
          setOrderData(data[0]);
          // Pre-fill the form fields with the order data
          setOrderName(data[0].order_name);
          setSelectedBase(data[0].base_operator);
          setComments(data[0].field_comments);
        })
        .catch((error) => {
          console.error("Error fetching order data:", error);
        });
    }
  }, []);
  async function handleApprove() {
    try {
      const response = await fetch(
        `${backendUrl}/api/update_order_status/${orderData.id}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            status: "Aprovado",
            operator_comments: operator_comments,
          }),
        }
      );

      if (response.status === 200) {
        alert("Ordem aprovada com sucesso");
        navigate("/Homepage");
      } else {
        alert("Erro ao aprovar ordem");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Erro ao aprovar ordem");
    }
  }

  async function handleReprove() {
    try {
      const response = await fetch(
        `${backendUrl}/api/update_order_status/${orderData.id}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            status: "Reprovado",
            operator_comments: operator_comments,
          }),
        }
      );

      if (response.status === 200) {
        alert("Ordem Reprovada");
        navigate("/Homepage");
      } else {
        alert("Erro ao reprovar ordem");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Erro ao reprovar ordem");
    }
  }
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
  } /*
  async function downloadFile(fileId) {
    try {
      // Fetch file details based on the fileId
      fetch(`${backendUrl}/api/get_file/${fileId}/`)
        .then((response) => {
          if (response.status === 200) {
            return response.json();
          } else {
            throw new Error("Order not found");
          }
        })
        .then((data) => {
          var downloadUrl = `${backendUrl}${data[0].file}`;
          return downloadUrl;
        });
    } catch (error) {
      console.error("Error:", error);
      alert("Error downloading file");
    }
  }*/

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
        {field_op === "true" && ( // Check if field_op is "True"
          <input
            className="file"
            type="file"
            onChange={(e) => setSelectedFiles(e.target.files)}
            multiple
          />
        )}
        <p></p>
        {base_op === "true" &&
          orderData.files &&
          orderData.files.length > 0 &&
          orderData.files.map((fileId) => (
            <div key={fileId}>
              <a href={`${backendUrl}/api/get_file/${fileId}/`} download>
                {" "}
                Download
              </a>
            </div>
          ))}
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
        {base_op === "true" && ( // Check if field_op is "True"
          <textarea
            className="coment_levantamento"
            type="text"
            placeholder="Feedback"
            value={operator_comments}
            onChange={(e) => setFeedback(e.target.value)}
            rows="5"
          />
        )}
      </div>
      {base_op === "true" && (
        <div style={{ flexDirection: "row" }}>
          <button onClick={handleReprove} className="approve-reprove reprove">
            Reprovar
          </button>
          <button onClick={handleApprove} className="approve-reprove approve">
            Aprovar
          </button>
        </div>
      )}
      {field_op === "true" && ( // Check if field_op is "True"
        <button type="button" onClick={handleClick} className="sendorder">
          Enviar
        </button>
      )}

      <p></p>
    </div>
  );
}

export default Neworder;
