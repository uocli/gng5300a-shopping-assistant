import "./App.css";
import { Grid2 as Grid, Typography } from "@mui/material";
import Question from "./components/Question";
import Response from "./components/Response";
import { useRef, useState } from "react";
import LinearProgressBar from "./components/LinearProgressBar";
import Customer from "./components/Customer";
import http from "./helpers/HttpCommon";

const App = () => {
  const questionRef = useRef();
  const [interrupted, setInterrupted] = useState(false);
  const [customerID, setCustomerID] = useState("");
  const [threadID, setThreadID] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const handleSubmit = (userQuery) => {
    setLoading(true);
    http
      .post("/query/", {
        query: userQuery,
        customerID: +customerID,
        threadID,
        interrupted,
      })
      .then((r) => {
        setThreadID(r.data.threadID);
        setResponse(r.data.message);
        setInterrupted(r.data.interrupted === true);
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
    questionRef.current?.focus();
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
        ref={questionRef}
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
