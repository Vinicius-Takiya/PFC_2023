import "./App.css";
import Login from "./login/Login.js";
import Homepage from "./homepage/Homepage.js";
import Homepage_admin from "./homepage-admin/Homepage-admin.js";
import Neworder from "./neworder/Neworder.js";
import Neworder_admin from "./neworder-admin/Neworder-admin.js";
import Register from "./register/Register.js";
import "bootstrap/dist/css/bootstrap.min.css";
import Header from "./Header";

import { BrowserRouter, Routes, Route, Switch } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route exact path="/" element={<Login />} />
        <Route path="/homepage" element={<Homepage />} />
        <Route path="/homepage_admin" element={<Homepage_admin />} />
        <Route path="/neworder" element={<Neworder />} />
        <Route path="/order/:order_number" element={<Neworder />} />
        <Route path="/neworder_admin" element={<Neworder_admin />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
