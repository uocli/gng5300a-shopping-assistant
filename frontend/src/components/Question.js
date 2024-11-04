import { Box, Button, Grid2 as Grid, TextField } from "@mui/material";
import { useState } from "react";

const Question = (props) => {
  const [userQuery, setUserQuery] = useState("");
  const { loading } = props;
  return (
    <Grid container size={12}>
      <Grid size={2}></Grid>
      <Grid size={8}>
        <Box
          component="form"
          sx={{ m: 2 }}
          onSubmit={(e) => {
            e.preventDefault();
            props.handleSubmit(userQuery);
            setUserQuery("");
          }}
        >
          <Grid
            container
            direction="row"
            justifyContent="flex-end"
            alignItems="center"
          >
            <Grid size={9}>
              <TextField
                disabled={loading}
                fullWidth
                label="Type in your question here"
                id="fullWidth"
                value={userQuery}
                onChange={(e) => setUserQuery(e.target.value)}
              />
            </Grid>
            <Grid size={3}>
              <Button variant="contained" type="submit">
                Submit
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Grid>
      <Grid size={2}></Grid>
    </Grid>
  );
};
export default Question;
