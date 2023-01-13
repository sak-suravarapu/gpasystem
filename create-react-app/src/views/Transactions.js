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

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';


 function preventDefault(event) {
   event.preventDefault();
 }
 const mdTheme = createTheme();
 
function Transactions({}){
  const { user, logoutUser } = useContext(AuthContext);
  const [res, setRes] = useState([]);
  const api = useAxios();
  //const resp = api.get("/accounts/");

  useEffect(() => {
    
    const fetchData = async () => {
      try {
        const response = await api.get(`/accounts/`);
        const resp=response.data.filter(rsp => rsp.user_id == user.user_id);        
        const response1 = await api.get('/transactions/')
        console.log(response1);
        //setRes(response1.data);
        const filteredArray = []; 
        const i = 0;
        response1.data.map((data)=>{
          resp.map((data1)=>{
            if (data.account_id == data1.account_number){
              filteredArray.push(data);
            }

          });
        //     if (data.account_id == resp[i].account_number){
        //       filteredArray.push(data);
        //     }

         });
        //console.log(filteredArray);
        console.log(filteredArray);
        setRes(filteredArray);
        
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
        <Grid item xs={12}>
        <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                    <React.Fragment>
                      <Title>Transactions</Title>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>ID</TableCell>
                            <TableCell>Date</TableCell>
                            <TableCell>Transaction Type</TableCell>
                            <TableCell>Account Number</TableCell>
                            <TableCell>Note</TableCell>
                            <TableCell align="right">Sale Amount</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {res.map((row) => (
                            <TableRow key={row.id}>
                              <TableCell>{row.id}</TableCell>
                              <TableCell>{row.date}</TableCell>
                              <TableCell>{row.transaction_type}</TableCell>
                              <TableCell>{row.account_id}</TableCell>
                              <TableCell>{row.note}</TableCell>
                              <TableCell align="right">{`$${row.amount}`}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                      <Link color="primary" href="#" onClick={preventDefault} sx={{ mt: 3 }}>
                        See more orders
                      </Link>
                    </React.Fragment>
                </Paper>
              </Grid>       
    </Grid>
    </Container>   
    </ThemeProvider> 
  </> 
  );
}

export default Transactions;

