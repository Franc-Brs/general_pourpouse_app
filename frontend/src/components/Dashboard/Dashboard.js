import React, { useState, useEffect, useMemo } from "react";
import ChiamateThirdPartyService from "./FetchData";
import ReactPaginate from "react-paginate";
import { useNavigate, useParams } from "react-router-dom";

export default function Dashboard() {
  const params = useParams();
  const history = useNavigate();

  const paginate = (n) => {
    history(`/${n}`);
  };

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(params.pageNr);
  const [recordsPerPage, setRecordsPerPage] = useState();
  const [apiError, setApiError] = useState(false);

  const fetcher = useMemo(() => new ChiamateThirdPartyService(), []);

  useEffect(() => {
    fetcher
      .getChiamate(currentPage)
      .then((resp) => resp.json())
      .then(
        (result) => {
          setData(result);
          setRecordsPerPage(result.page_size);
          setLoading(false);
        },
        (error) => {
          setApiError(true);
          console.log(error);
        }
      );
  }, [fetcher, currentPage]);

  const handlePageChange = (event) => {
    setCurrentPage(event.selected + 1);
    paginate(event.selected + 1);
  };
  if (apiError === true) {
    return (
      <div>
        <h3 style={{ textAlign: "center" }}>404 page not found</h3>
        <p style={{ textAlign: "center" }}>We are sorry but the page you are looking for does not exist.</p>
      </div>
    );
  }
  return (
    <div>
      <h2>List of request to the third-party service</h2>
      {loading === true ? (
        <div>Loading</div>
      ) : (
        <>
          <table className="table">
            <thead>
              <tr>
                <th>Id</th>
                <th>Creation date</th>
                <th>Modification date</th>
                <th>Request</th>
                <th>Status</th>
                <th>Server</th>
                <th>Response</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {data.results.map((emp) => (
                <tr key={emp.id}>
                  <td>{emp.id}</td>
                  <td>{emp.datetime_creation}</td>
                  <td>{emp.datetime}</td>
                  <td>{emp.chiamata.length > 50 ? `${emp.chiamata.substring(0, 50)} ...` : emp.chiamata}</td>
                  <td>{emp.status}</td>
                  <td>{emp.server}</td>
                  <td>{emp.risposta_server_terzo.length > 50 ? `${emp.risposta_server_terzo.substring(0, 50)} ...` : emp.risposta_server_terzo}</td>
                  <td>
                    <a href={"/chiamata/" + emp.id}> Update</a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <ReactPaginate
            pageCount={Math.ceil(data.count / recordsPerPage)}
            onPageChange={handlePageChange}
            previousLabel="Previous"
            nextLabel="Next"
            pageClassName="page-item"
            pageLinkClassName="page-link"
            previousClassName="page-item"
            previousLinkClassName="page-link"
            nextClassName="page-item"
            nextLinkClassName="page-link"
            breakLabel="..."
            breakClassName="page-item"
            breakLinkClassName="page-link"
            marginPagesDisplayed={2}
            pageRangeDisplayed={5}
            containerClassName="pagination"
            activeClassName="active"
          />
        </>
      )}
    </div>
  );
}
