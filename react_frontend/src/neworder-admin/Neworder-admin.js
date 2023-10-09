import React from 'react';
import './Neworder-admin.css';
import {useNavigate} from 'react-router-dom';

function Neworder_admin() {
  const navigate = useNavigate();
  
  function handleClick(event) {
  
    window.location.href = '/homepage_admin';
    alert("Enviado")
  }



  return (
    <div>
      <h1 class='title'>Gerar feedback sobre levantamento</h1>
      <div className="elements">
        <input class='nome' type="text" placeholder="	SaoPaulo_SP_1" />
        <p></p>
        Imagem_equipamento.jpg   Arquivos_Levantamento.rar   Misc.etc   
        <button >Download</button><p></p>
        <input class='sendto' list='bases' placeholder="Enviar para João Silva" /><p></p>
        <datalist id='bases'>
        <option value='1º CGEO'/>
        <option value='2º CGEO'/>
        <option value='3º CGEO'/>
        <option value='4º CGEO'/>
        <option value='5º CGEO'/>
        </datalist>
        <textarea class='coment' type="text" placeholder="Comentários do operador de campo" rows="5" /><p></p>
        <textarea class='coment' type="text" placeholder="Feedback" rows="5" />
      </div>
      <div style={{ flexDirection:"row" }}>
        <button onClick={handleClick} class='approve-reprove reprove'>Reprovar</button>
        <button onClick={handleClick} class='approve-reprove approve'>Aprovar</button>
      </div>
      <p></p>

    </div>
  );
}

export default Neworder_admin;