import { Grid2 as Grid, LinearProgress } from "@mui/material";

const LinearProgressBar = (props) => {
  const { loading } = props;
  return (
    <Grid container size={12}>
      {!!loading ? (
        <>
          <Grid size={2}></Grid>
          <Grid size={6} sx={{ p: 2 }}>
            <LinearProgress />
          </Grid>
          <Grid size={4}></Grid>
        </>
      ) : null}
    </Grid>
  );
};
export default LinearProgressBar;
