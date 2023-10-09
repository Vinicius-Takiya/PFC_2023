import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import * as ReactBootStrap from "react-bootstrap";
import axios from "axios";
import backendUrl from "../Config";

function LevantamentosTable() {
  const [reversedData, setData] = useState([]);
  const [operators, setOperators] = useState([]);
  const authToken = localStorage.getItem("authToken");
  const id = localStorage.getItem("id");

  useEffect(() => {
    // Make an HTTP GET request to your Django backend API endpoint
    fetch(`${backendUrl}/api/get_orders/${id}/`, {})
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data)) {
          // Verify that data is an array
          setData(data.reverse()); // Populate the state variable with fetched data
        } else {
          console.error("Data is not an array:", data);
        }
      })
      .catch((error) => {
        console.error("Error fetching orders:", error);
      });
    fetch(`${backendUrl}/api/operators/`, {})
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data)) {
          // Verify that data is an array
          setOperators(data); // Populate the state variable with fetched data
        } else {
          console.error("Data is not an array:", data);
        }
      })
      .catch((error) => {
        console.error("Error fetching operators:", error);
      });
  }, []); // Empty dependency array to fetch data only once on component mount

  // Helper function to determine the background color based on the status
  function getStatusColor(status) {
    switch (status) {
      case "Aprovado":
        return "green";
      case "Reprovado":
        return "red";
      case "Aguardando Análise":
        return "yellow";
      default:
        return "white"; // Default color if status is not recognized
    }
  }

  // Function to handle order deletion
  const handleDeleteOrder = (orderId) => {
    const shouldDelete = window.confirm(
      "Are you sure you want to delete this order?"
    );
    if (shouldDelete) {
      axios
        .delete(`${backendUrl}/api/delete_order/${orderId}/`)
        .then((response) => {
          if (response.status === 204) {
            // Deletion was successful
            // Now, update the state to remove the deleted order
            const updatedData = reversedData.filter(
              (order) => order.id !== orderId
            );
            setData(updatedData);
          } else {
            // Handle any errors that occur during deletion
            console.error("Error deleting order:", response);
          }
        })
        .catch((error) => {
          console.error("Error deleting order:", error);
        });
    }
  };

  return (
    <div
      className="table-container"
      style={{ maxHeight: "400px", overflowY: "scroll" }}
    >
      <ReactBootStrap.Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Levantamento</th>
            <th>Operador de campo</th>
            <th>Operador de base</th>
            <th>Data/Hora</th>
            <th>Status</th>
            <th>Visualizar ordem</th>
            <th>Excluir</th>
          </tr>
        </thead>
        <tbody>
          {reversedData.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.order_name}</td>
              <td>
                {
                  operators.find(
                    (operator) => operator.id === row.field_operator
                  )?.name
                }
              </td>
              <td>
                {
                  operators.find(
                    (operator) => operator.id === row.base_operator
                  )?.name
                }
              </td>
              <td>{row.datetime_of_sending}</td>
              <td style={{ backgroundColor: getStatusColor(row.status) }}>
                {row.status}
              </td>
              <td className="text-center">
                <Link to={`/order/${row.id}`}>
                  <button type="button">Visualizar</button>
                </Link>
              </td>
              <td className="text-center">
                <button type="button" onClick={() => handleDeleteOrder(row.id)}>
                  Excluir
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </ReactBootStrap.Table>
    </div>
  );
}

export default LevantamentosTable;
