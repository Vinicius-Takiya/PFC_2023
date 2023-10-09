import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import * as ReactBootStrap from "react-bootstrap";
import axios from "axios"; // Import Axios
import backendUrl from "../Config";

function LevantamentosTable() {
  const [data, setData] = useState([]); // Initialize state for data

  useEffect(() => {
    // Make an HTTP GET request to your Django backend API endpoint
    axios
      .get(`${backendUrl}/api/orders`) // Replace with your actual API endpoint
      .then((response) => {
        const reversedData = response.data.reverse(); // Reverse the data array to get the latest orders
        setData(reversedData); // Update the state with the reversed data
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []); // Empty dependency array to fetch data only once on component mount

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
          {data.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.order_name}</td>
              <td>{row.field_operator__name}</td>
              <td>{row.base_operator__name}</td>
              <td>{row.datetime_of_sending}</td>
              <td>{row.status}</td>
              <td className="text-center">
                <Link to={`/neworder/${row.id}`}>
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
