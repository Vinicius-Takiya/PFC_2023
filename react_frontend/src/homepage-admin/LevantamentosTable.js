import React from 'react';
import { Link } from 'react-router-dom';
import * as ReactBootStrap from 'react-bootstrap';

function LevantamentosTable() {
    // Mock data for the table
    
    const data = [
      {
        id: 1,
        levantamento: 'SaoPaulo_SP_1',
        nomeOperador: 'João Silva',
        dataHora: '2023-08-02 12:00',
        status: 'Aprovado',
      },
      {
        id: 2,
        levantamento: 'RioDeJaneiro_RJ_1',
        nomeOperador: 'Maria Souza',
        dataHora: '2023-08-03 14:30',
        status: 'Reprovado',
      },
      {
        id: 3,
        levantamento: 'PortoAlegre_RS_1',
        nomeOperador: 'Pedro Rocha',
        dataHora: '2023-08-04 10:45',
        status: 'Aguardando Análise',
      },
      {
        id: 4,
        levantamento: 'BeloHorizonte_MG_1',
        nomeOperador: 'Ana Oliveira',
        dataHora: '2023-08-05 09:15',
        status: 'Reprovado',
      },
      {
        id: 5,
        levantamento: 'Fortaleza_CE_1',
        nomeOperador: 'Lucas Santos',
        dataHora: '2023-08-06 15:20',
        status: 'Aguardando Análise',
      },
      {
        id: 6,
        levantamento: 'Salvador_BA_1',
        nomeOperador: 'Julia Mendes',
        dataHora: '2023-08-07 18:30',
        status: 'Aguardando Análise',
      },
      {
        id: 7,
        levantamento: 'Recife_PE_1',
        nomeOperador: 'Rodrigo Lima',
        dataHora: '2023-08-08 14:00',
        status: 'Aprovado',
      },
      {
        id: 8,
        levantamento: 'Brasilia_DF_1',
        nomeOperador: 'Mariana Fernandes',
        dataHora: '2023-08-09 11:45',
        status: 'Aprovado',
      },
      {
        id: 9,
        levantamento: 'Curitiba_PR_1',
        nomeOperador: 'Gustavo Costa',
        dataHora: '2023-08-10 16:20',
        status: 'Aprovado',
      },
      {
        id: 10,
        levantamento: 'Manaus_AM_1',
        nomeOperador: 'Camila Rodrigues',
        dataHora: '2023-08-11 13:15',
        status: 'Aprovado',
      },
      // Add more data rows as needed
  ];
    return (
        <ReactBootStrap.Table striped bordered hover>
        <thead>
            <tr>
            <th>ID</th>
            <th>Levantamento</th>
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
                <td>{row.levantamento}</td>
                <td>{row.nomeOperador}</td>
                <td>{row.dataHora}</td>
                <td>{row.status}</td>
                <td class="text-center">
                <Link to="/neworder_admin">
                  <button type="button">Visualizar</button>
                </Link>
                </td>
                
            </tr>
            ))}
        </tbody>
        </ReactBootStrap.Table >
    );
}
  

export default LevantamentosTable;