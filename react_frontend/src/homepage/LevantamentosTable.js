import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import * as ReactBootStrap from "react-bootstrap";
import axios from "axios"; // Import Axios
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
        console.error("Error fetching base operators:", error);
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
        console.error("Error fetching base operators:", error);
      });
  }, []); // Empty dependency array to fetch data only once on component mount
  const operatorNameMap = {};
  operators.forEach((operator) => {
    operatorNameMap[operator.id] = operator.name;
  });
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
            <th>Operador de base</th>
            <th>Operador de campo</th>
            <th>Data/Hora</th>
            <th>Status</th>
            <th>Visualizar ordem</th>
          </tr>
        </thead>
        <tbody>
          {reversedData.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.order_name}</td>
              <td>{operatorNameMap[row.field_operator]}</td>
              <td>{operatorNameMap[row.base_operator]}</td>
              <td>{row.datetime_of_sending}</td>
              <td>{row.status}</td>
              <td className="text-center">
                <Link to={`/order/${row.id}`}>
                  <button type="button">Visualizar</button>
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </ReactBootStrap.Table>
    </div>
  );
}

export default LevantamentosTable;
