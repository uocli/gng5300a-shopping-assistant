import "./App.css";
import { Grid2 as Grid, Typography } from "@mui/material";
import Question from "./components/Question";
import Response from "./components/Response";
import { useState } from "react";
import LinearProgressBar from "./components/LinearProgressBar";
import Customer from "./components/Customer";
import http from "./helpers/HttpCommon";

const App = () => {
  const [interrupted, setInterrupted] = useState(false);
  const [customerID, setCustomerID] = useState("");
  const [threadID, setThreadID] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const handleSubmit = (userQuery) => {
    setLoading(true);
    setChatHistory((prevState) => [
      {
        from: "User",
        message: userQuery,
        time: new Date().toLocaleTimeString(),
      },
      ...prevState,
    ]);
    http
      .post("/query/", {
        query: userQuery,
        customerID: +customerID,
        threadID,
        interrupted,
      })
      .then((r) => {
        setThreadID(r.data.threadID);
        setInterrupted(r.data.interrupted === true);
        setChatHistory((prevState) => [
          {
            from: "Bot",
            message: r.data.message,
            time: new Date().toLocaleTimeString(),
          },
          ...prevState,
        ]);
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
    <Grid className="App" container>
      <Grid size={12}>
        <Typography variant="h3" component="h3">
          LangChain Shopping Assistant
        </Typography>
      </Grid>
      <Customer handleSubmit={handleCustomerID} />
      <Question
        customerID={customerID}
        chatHistory={chatHistory}
        handleSubmit={handleSubmit}
        loading={loading}
      />
      <LinearProgressBar loading={loading} />
      <Response history={chatHistory} />
    </Grid>
  );
};

export default App;
