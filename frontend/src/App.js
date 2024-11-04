import "./App.css";
import { Grid2 as Grid, Typography } from "@mui/material";
import Question from "./components/Question";
import Response from "./components/Response";
import { useState } from "react";
import axios from "axios";
import LinearProgressBar from "./components/LinearProgressBar";

const App = () => {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const handleSubmit = (userQuery) => {
    setLoading(true);
    axios
      .post("/api/query/", { query: userQuery })
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
  return (
    <Grid container className="App">
      <Grid size={12}>
        <Typography variant="h3" component="h3">
          LangChain Shopping Assistant
        </Typography>
      </Grid>
      <Question handleSubmit={handleSubmit} loading={loading} />
      <LinearProgressBar loading={loading} />
      <Response response={response} />
    </Grid>
  );
};

export default App;
