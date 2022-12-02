import React, { useState, useEffect, useMemo } from "react";
import ChiamateThirdPartyService from "./FetchData.js";
import { useParams } from "react-router-dom";
//import PropTypes from "prop-types";
import {useNavigate} from 'react-router-dom';

export default function EditTable() {
  const navigate = useNavigate();
  const params = useParams();
  const [inputs, setInputs] = useState({});
  const [infoSent, setInfoSent] = useState(false);

  const fetcher = useMemo(
    () => new ChiamateThirdPartyService(),
    [] //no dependencies so the value doesn't change
  );

  useEffect(() => {
    fetcher
      .getChiamata(params.id)
      .then((resp) => resp.json())
      .then((data) => {
        setInputs(data);
      });
  }, [params.id, fetcher]);

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs((values) => ({ ...values, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (params && params.id) {
      fetcher
        .updateChiamata(params.id, {
          chiamata: inputs.chiamata,
          status: inputs.status,
          server: inputs.server,
          risposta_server_terzo: inputs.risposta_server_terzo,
        })
        .then((response) => {
          setInfoSent(true);
          response.text();
        })
        .catch((error) => console.log("error", error));
    }
  };

  return (
    <div className="Edit-form-container">
      <form className="Edit-form" onSubmit={handleSubmit}>
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Edit id:{params.id}</h3>
          <div className="form-group mt-3">
            <label>Id</label>
            <input disabled type="text" className="form-control mt-1" onChange={handleChange} name="id" value={inputs.id || ""} readOnly={true} />
          </div>
          <div className="form-group mt-3">
            <label>Data di creazione</label>
            <input
              disabled
              type="text"
              className="form-control mt-1"
              onChange={handleChange}
              name="datetime_creation"
              value={inputs.datetime_creation || ""}
              readOnly={true}
            />
          </div>
          <div className="form-group mt-3">
            <label>Data di aggiornamento</label>
            <input
              disabled
              type="text"
              className="form-control mt-1"
              onChange={handleChange}
              name="datetime"
              value={inputs.datetime || ""}
              readOnly={true}
            />
          </div>
          <div className="form-group mt-3">
            <label>Chiamata</label>
            <textarea type="text" className="form-control mt-1" onChange={handleChange} name="chiamata" value={inputs.chiamata || ""} />
          </div>
          <div className="form-group mt-3">
            <label>Status</label>
            <input
              disabled
              type="text"
              className="form-control mt-1"
              onChange={handleChange}
              name="status"
              value={inputs.status || ""}
              readOnly={true}
            />
          </div>
          <div className="form-group mt-3">
            <label>Server</label>
            <input type="text" className="form-control mt-1" onChange={handleChange} name="server" value={inputs.server || ""} />
          </div>
          <div className="form-group mt-3">
            <label>Risposta Servizio Terzo</label>
            <textarea
              disabled
              className="form-control mt-1"
              onChange={handleChange}
              name="risposta_server_terzo"
              readOnly={true}
              value={inputs.risposta_server_terzo || ""}
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Update
            </button>
          </div>
          {infoSent === true ? (
            <div className="form-group mt-3" style={{ textAlign: "center", color: "#0d6efd" }}>
              Info aggiornate nel db
            </div>
          ) : (
            <></>
          )}
          <div className="d-grid gap-2 mt-3">
            <button onClick={() => navigate(-1)} className="btn btn-primary">
              Go Back
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
