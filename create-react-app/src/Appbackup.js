import * as React from 'react';
//import "./index.css";
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import ProTip from './ProTip';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

//To add login page
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import PrivateRoute from './utils/PrivateRoute';
import { AuthProvider } from './context/AuthContext';
import SignIn from './views/SignIn';
import Dashboard from './views/Dashboard';
import SignUp from './views/SignUp';
import LoginPage from './views/LoginPage';
import Home from './views/homePage';
import ProtectedPage from './utils/ProtectedPage';

// function Copyright() {
//   return (
//     <Typography variant="body2" color="text.secondary" align="center">
//       {'Copyright © '}
//       <Link color="inherit" href="https://mui.com/">
//         Your Website
//       </Link>{' '}
//       {new Date().getFullYear()}
//       {'.'}
//     </Typography>
//   );
// }

function App() {
  return (
  <Router>
    {/* <div className="flex flex-col min-h-screen overflow-hidden">  */}
    <div> 
      <AuthProvider>
      <Navbar />
      <Switch>
        <PrivateRoute component={Dashboard} path="/protected" exact />
        <Route component={Home} path="/" />
        <Route component={LoginPage} path="/login" />
        <Route component={SignUp} path="/register" />
      </Switch>
      </AuthProvider>
      <Footer />
    </div>
  </Router>
  );
}

// function App(){
//   return (
//     <Auth loginCall={SignIn}>
//       <ConfigureAuth>
//         <Router>
//           <Switch>
//             <GuestRoute path="/login" redirectTo='/'>
//               <Login />
//             </GuestRoute>
//             <AuthRoute path="/" exact redirectTo='/login'>
//               <AddressBook />
//             </AuthRoute>
//           </Switch>
//         </Router>
//       </ConfigureAuth>
//     </Auth>
//   );
// }

export default App;

// export default function App() {
//   return (
//     <Container maxWidth="sm">
//       <Box sx={{ my: 4 }}>
//         <Typography variant="h4" component="h1" gutterBottom>
//           Create React App example
//         </Typography>
//         <ProTip />
//         <Copyright />
//       </Box>
//     </Container>
//   );
// }
