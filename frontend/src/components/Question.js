import { Box, Grid2 as Grid, TextField } from "@mui/material";
import { forwardRef, useImperativeHandle, useState } from "react";

const Question = forwardRef(({ customerID, handleSubmit, loading }, ref) => {
  const [userQuery, setUserQuery] = useState("");
  useImperativeHandle(ref, () => ({
    focus: () => {
      document.querySelectorAll("input")[1].focus();
    },
  }));

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
});
export default Question;
