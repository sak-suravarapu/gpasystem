import Typography from '@mui/material/Typography';
function UserInfo({ user }) {
    return (
      
      <div>
        <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              Hello, {user.username}!
        </Typography>
      </div>
    );
  }
  
  export default UserInfo;  