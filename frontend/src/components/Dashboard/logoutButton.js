import React, { Component } from "react";

let styles = {
  marginRight: "20px",
  marginLeft: "20px",
  marginTop: "20px",
  marginDown: "20px",
};

export default class UserLogout extends Component {
  logout = () => {
    localStorage.clear();
    window.location.reload();
  };

  render() {
    return (
      <button className="position-absolute top-0 end-0 btn btn-primary" style={styles} onClick={this.logout}>
        Logout
      </button>
    );
  }
}
