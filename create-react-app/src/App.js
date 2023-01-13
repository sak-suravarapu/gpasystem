import React from "react";
//import "./index.css";
//import Footer from "./components/Footer";
//import Navbar from "./components/Navbar";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";
//import Home from "./views/homePage";
import Login from "./views/LoginPage";
import Accounts from "./views/Deposits";
import AccountsContent from "./views/Accounts";
import Transactions from "./views/Transactions";
//import Register from "./views/RegisterPage";
//import ProtectedPage from "./views/ProtectedPage";
import Dashboard from "./views/Dashboard";

function App() {
  return (
    <Router>
      {/* <div className="flex flex-col min-h-screen overflow-hidden"> */}
        <div>
        <AuthProvider>
          {/* <Navbar /> */}
          <Switch>
            <PrivateRoute component={AccountsContent} path="/protected" exact />
            <PrivateRoute component={AccountsContent} path="/transactions" exact />
            <Route component={Login} path="/login" />
            {/* <Route component={Register} path="/register" /> */}
            <Route component={Login} path="/" />
          </Switch>
        </AuthProvider>
        {/* <Footer /> */}
      </div>
    </Router>
  );
}

export default App;