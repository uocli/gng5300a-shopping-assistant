import "./App.css";
import { Grid2 as Grid, Typography } from "@mui/material";
import Question from "./components/Question";
import Response from "./components/Response";
import { useState } from "react";
import axios from "axios";
import LinearProgressBar from "./components/LinearProgressBar";
import Customer from "./components/Customer";
import http from "./helpers/http-common";

const App = () => {
  const [customerID, setCustomerID] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const handleSubmit = (userQuery) => {
    setLoading(true);
    http
      .post("/query/", { query: userQuery, customerID: +customerID })
      .then((r) => {
        setResponse(r.data.message);
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        setLoading(false);
      });
  };
  const handleCustomerID = (customerID) => {
    setCustomerID(customerID);
  };
  return (
    <Grid container className="App">
      <Grid size={12}>
        <Typography variant="h3" component="h3">
          LangChain Shopping Assistant
        </Typography>
      </Grid>
      <Customer handleSubmit={handleCustomerID} />
      <Question
        customerID={customerID}
        handleSubmit={handleSubmit}
        loading={loading}
      />
      <LinearProgressBar loading={loading} />
      <Response response={response} />
    </Grid>
  );
};

export default App;
