import React from 'react';
import header_cgeo from './components/header_cgeo.png'
import './Header.css'; // Import your CSS file for styling (create your own Header.css)
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header>
      <img src={header_cgeo} alt="Header Logo" />      
      <Link to="/" class="sair">Sair</Link>
    </header>
  );
};

export default Header;