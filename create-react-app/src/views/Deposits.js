import * as React from 'react';
import Link from '@mui/material/Link';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Title from './Title';
import Grid from '@mui/material/Grid';
import { useEffect, useState } from "react";
import useAxios from "../utils/useAxios";
import Paper from '@mui/material/Paper';
import Container from '@mui/material/Container';
//Auth related things below
import { useContext } from 'react';
import UserInfo from '../components/UserInfo';
import AuthContext from '../context/AuthContext';

 function preventDefault(event) {
   event.preventDefault();
 }
 const mdTheme = createTheme();
 
function Accounts({}){
  const { user, logoutUser } = useContext(AuthContext);
  const [res, setRes] = useState([]);
  const api = useAxios();
  //const resp = api.get("/accounts/");

  useEffect(() => {
    
    const fetchData = async () => {
      try {

        const response = await api.get(`/accounts`,{params:{user_id:user.user_id}});
        setRes(response.data);

      } catch {
        setRes("Something went wrong");
      }
    };
    fetchData();
    
  }, []);
  
  return (
    <>
    <ThemeProvider theme={mdTheme}>
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
    <Grid container spacing={3}>

    {res.map((data,id)=>{
      return (
         <Grid item xs={12} md={4} lg={3}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: 240,
                  }}
                >
              <React.Fragment>
              <Title>Account Number</Title>
              <Typography component="p" variant="h7" sx={{ mt: 2 }}>
                {data.account_number.padStart(16,'0')}
              </Typography>
              <Box
                            sx={{
                              display: 'flex',
                              justifyContent: 'center',
                              alignItems: 'baseline',
                              mb: 2,
                            }}
                          >
              <Typography color="text.secondary" sx={{ flex: 1 }} variant="h7">
                Current Balance       ${data.current_balance}
              </Typography>
              </Box>
              <div>
                <Link color="primary" href="/transactions" >
                  View Transactions
                </Link>
              </div>
            </React.Fragment>
                  {/* <Accounts /> */}
                </Paper>
              </Grid> 
      )    
//          console.log(data.current_balance);
//          console.log(id);
    })}
    </Grid>
    </Container>   
    </ThemeProvider> 
  </> 
  );
}

export default Accounts;

