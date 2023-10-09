import React from "react";
import { useNavigate } from "react-router-dom";
import "./Homepage.css";
import LevantamentosTable from "./LevantamentosTable";

function Homepage() {
  const navigate = useNavigate();
  const field_op = localStorage.getItem("field_operator");
  const base_op = localStorage.getItem("base_operator");

  function handleClick(event) {
    window.location.href = "/neworder";
  }

  return (
    <div className="home-page">
      <h1 className="title">Levantamentos</h1>
      {field_op === "true" && ( // Check if field_op is "True"
        <button type="button" onClick={handleClick} className="neworder">
          Novo Levantamento
        </button>
      )}
      <p></p>
      <div className="tabela">
        <LevantamentosTable />
      </div>
      {/* <Link to="/">Login</Link> */}
    </div>
  );
}

export default Homepage;
