import React, { useState } from "react";
import PropTypes from "prop-types";
import Cookies from "js-cookie";

async function loginUser(credentials) {
  var myHeaders = new Headers({
    accept: "application/json",
    "X-CSRFToken": Cookies.get("csrftoken"),
    "Content-Type": "application/x-www-form-urlencoded",
  });

  var urlencoded = new URLSearchParams();
  urlencoded.append("email", credentials.username);
  urlencoded.append("password", credentials.password);

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: urlencoded,
    redirect: "follow",
  };

  return await fetch(`${process.env.REACT_APP_API_SERVICE_URL}/api/user/token/`, requestOptions)
    .then((response) => {
      if (response.status !== 200) {
        throw new Error("Bad response from server");
      }
      return response;
    })
    .then((response) => response.json());
}

export default function Login({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const [apiError, setApiError] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = await loginUser({
      username,
      password,
    }).then(
      (result) => {
        return result;
      },
      (error) => {
        setApiError(true);
        throw new Error(error);
      }
    );
    setToken(token);
  };

  return (
    <div className="Auth-form-container">
      <form className="Auth-form" onSubmit={handleSubmit}>
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign In</h3>
          <div className="form-group mt-3">
            <label>Email address</label>
            <input type="email" onChange={(e) => setUserName(e.target.value)} className="form-control mt-1" placeholder="Enter email" />
          </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input type="password" onChange={(e) => setPassword(e.target.value)} className="form-control mt-1" placeholder="Enter password" />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Log In
            </button>
          </div>
          {
            apiError === true ?
            <div className="form-group mt-3" style={{ textAlign: "center", color: "red" }}>
              Provare a inserire le credenziali nuovamente
            </div>
            :
            <></>
          }
        </div>
      </form>
    </div>
  );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired,
};
