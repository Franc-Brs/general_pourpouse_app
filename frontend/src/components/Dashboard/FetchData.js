import Cookies from "js-cookie";
const API_URL = process.env.REACT_APP_API_SERVICE_URL;

export default class ChiamateThirdPartyService {
  constructor() {
    this.token = JSON.parse(localStorage.getItem("token")).token;
    this.myHeaders = new Headers({
      accept: "application/json",
      Authorization: "Token " + this.token,
      "X-CSRFToken": Cookies.get("csrftoken"),
      "Content-Type": "application/json",
    });
    this.getRequestOptions = {
      method: "GET",
      headers: this.myHeaders,
      redirect: "follow",
    };
  }

  async getChiamate(pageNr) {
    return await fetch(`${API_URL}/api/chiamate/chiamate/?page=${pageNr}`, this.getRequestOptions).then((response) => {
      if (response.status !== 200) {
        throw new Error("Bad response from server");
      }
      return response;
    });
  }

  async getChiamata(id) {
    const link = `${API_URL}/api/chiamate/chiamate/${id}/`;
    return await fetch(link, this.getRequestOptions);
  }

  async updateChiamata(id, chiamata) {
    this.putRequestOptions = {
      method: "PUT",
      headers: this.myHeaders,
      redirect: "follow",
      body: JSON.stringify(chiamata),
    };
    const link = `${API_URL}/api/chiamate/chiamate/${id}/`;
    return await fetch(link, this.putRequestOptions);
  }
}
