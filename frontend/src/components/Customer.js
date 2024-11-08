import { Box, Grid2 as Grid, TextField } from "@mui/material";
import { useState } from "react";

const Customer = (props) => {
  const [customerID, setCustomerID] = useState("");
  return (
    <Grid size={{ xs: 12, md: 6 }}>
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
            color="warning"
            value={customerID}
            onChange={(e) => setCustomerID(e.target.value)}
          />
        </Grid>
      </Box>
    </Grid>
  );
};
export default Customer;
