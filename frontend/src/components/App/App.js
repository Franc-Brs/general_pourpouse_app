import React from "react";

import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Dashboard from "../Dashboard/Dashboard";
import Login from "../Login/Login";
import useToken from "./useToken";
import UserLogout from "../Dashboard/logoutButton";
import EditTable from "../Dashboard/editTable";

function App() {
  const { token, setToken } = useToken();

  return (
    <>
      {!token ? (
        <Login setToken={setToken} />
      ) : (
        <div className="wrapper">
          <h1>Gter S.r.l</h1>
          <UserLogout />
          <BrowserRouter>
            <Routes>
              <Route path="/chiamata/:id" element={<EditTable />}></Route>
              <Route path="/:pageNr" element={<Dashboard />}></Route>
              <Route path="" element={<Navigate to="/1" replace />} />
            </Routes>
          </BrowserRouter>
        </div>
      )}
    </>
  );
}

export default App;
