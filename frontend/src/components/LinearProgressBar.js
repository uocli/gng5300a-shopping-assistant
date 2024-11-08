import { Grid2 as Grid, LinearProgress } from "@mui/material";

const LinearProgressBar = (props) => {
  const { loading } = props;
  return (
    <Grid container size={12}>
      {!!loading ? (
        <Grid size={12}>
          <LinearProgress />
        </Grid>
      ) : null}
    </Grid>
  );
};
export default LinearProgressBar;
