import React from 'react';
import {useNavigate} from 'react-router-dom';
import './Homepage.css';
import LevantamentosTable from './LevantamentosTable';

function Homepage() {
  const navigate = useNavigate();

  function handleClick(event) {

    window.location.href = '/neworder';
  }


  return (
    <div className="home-page">
      <h1 className="title">Levantamentos</h1>
      <button type="button" onClick={handleClick} className="neworder">
        Novo Levantamento
      </button>
      <p></p>
      <div className='tabela'>
        <LevantamentosTable/>
      </div>
      {/* <Link to="/">Login</Link> */}
    </div>
  );
}

export default Homepage;