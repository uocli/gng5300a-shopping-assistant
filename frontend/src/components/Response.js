import { Box, Grid2 as Grid, TextField } from "@mui/material";

const Response = (props) => {
  const { response } = props || {};
  return (
    <Grid container size={12}>
      <Grid size={2}></Grid>
      <Grid size={8}>
        <Box component="form" sx={{ m: 2 }}>
          <Grid
            container
            direction="row"
            justifyContent="flex-end"
            alignItems="center"
          >
            <Grid size={9}>
              <TextField
                label="Response"
                fullWidth
                defaultValue=""
                value={response || ""}
                slotProps={{
                  input: {
                    readOnly: true,
                  },
                }}
              />
            </Grid>
            <Grid size={3}></Grid>
          </Grid>
        </Box>
      </Grid>
      <Grid size={2}></Grid>
    </Grid>
  );
};
export default Response;
