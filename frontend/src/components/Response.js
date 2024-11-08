import {
  Avatar,
  Box,
  Divider,
  Grid2 as Grid,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Typography,
} from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import Face6Icon from "@mui/icons-material/Face6";
import { deepOrange, green } from "@mui/material/colors";

const Response = (props) => {
  const { history } = props || {};
  return (
    <Grid container size={12}>
      <Box component="form" sx={{ m: 2 }}>
        <List sx={{ width: "100%", bgcolor: "background.paper" }}>
          {history.map(({ message, from, time }, index) => {
            return (
              <>
                {index === 0 ? null : (
                  <Divider variant="inset" component="li" />
                )}
                <ListItem alignItems="flex-start">
                  <ListItemAvatar>
                    <Avatar
                      sx={{
                        bgcolor: from === "User" ? deepOrange[500] : green[500],
                      }}
                    >
                      {from === "User" ? <Face6Icon /> : <SmartToyIcon />}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={from}
                    secondary={
                      <>
                        <Typography
                          component="span"
                          variant="body2"
                          sx={{ color: "text.primary", display: "block" }}
                        >
                          {time}
                        </Typography>
                        <Typography
                          component="span"
                          variant="body2"
                          sx={{ color: "text.primary", display: "inline" }}
                        >
                          {message}
                        </Typography>
                      </>
                    }
                  />
                </ListItem>
              </>
            );
          })}
        </List>
      </Box>
    </Grid>
  );
};
export default Response;
