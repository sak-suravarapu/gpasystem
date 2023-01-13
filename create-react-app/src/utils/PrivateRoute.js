import { Route, Redirect } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";

const PrivateRoute = ({ children, ...rest }) => {
    let { user } = useContext(AuthContext);
    //If user is present, it passes the properties to the child component and that route will be served, otherwise, it will redirect to login
    return <Route {...rest}>{!user ? <Redirect to="/login" /> : children}</Route>;

};

export default PrivateRoute;