import { Box, Grid2 as Grid, TextField } from "@mui/material";
import { useState } from "react";

const Customer = (props) => {
  const [customerID, setCustomerID] = useState("");
  return (
    <Grid container size={12}>
      <Grid size={3}></Grid>
      <Grid size={6}>
        <Box
          component="form"
          sx={{ m: 2 }}
          onSubmit={(e) => {
            e.preventDefault();
            props.handleSubmit(customerID);
          }}
        >
          <Grid
            container
            direction="row"
            justifyContent="flex-end"
            alignItems="center"
          >
            <TextField
              fullWidth
              label="Type in your Customer ID"
              placeholder="Press Enter to submit"
              id="fullWidth"
              value={customerID}
              onChange={(e) => setCustomerID(e.target.value)}
            />
          </Grid>
        </Box>
      </Grid>
      <Grid size={3}></Grid>
    </Grid>
  );
};
export default Customer;
