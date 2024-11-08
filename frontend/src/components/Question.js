import { Box, Grid2 as Grid, TextField } from "@mui/material";
import { useEffect, useRef, useState } from "react";

const Question = ({ customerID, handleSubmit, loading, chatHistory }) => {
  const [userQuery, setUserQuery] = useState("");
  const inputRef = useRef();
  useEffect(() => {
    inputRef.current?.focus(); // Focus on the input field
  }, [customerID, chatHistory]);

  return (
    <Grid size={{ xs: 12, md: 6 }}>
      <Box
        component="form"
        sx={{ m: 2 }}
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmit(userQuery);
          setUserQuery("");
        }}
      >
        <Grid
          container
          direction="row"
          justifyContent="flex-end"
          alignItems="center"
        >
          <TextField
            inputRef={inputRef}
            disabled={loading || !customerID}
            fullWidth
            label="Type in your question here"
            value={userQuery}
            onChange={(e) => setUserQuery(e.target.value)}
          />
        </Grid>
      </Box>
    </Grid>
  );
};
export default Question;
