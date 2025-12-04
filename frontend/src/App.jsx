import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Layout from './components/Layout';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Plans from './pages/Plans';
import Vouchers from './pages/Vouchers';
import Customers from './pages/Customers';
import Shop from './pages/Shop';
import AdminRoute from './components/AdminRoute';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  const location = useLocation();
  return token ? children : <Navigate to="/login" state={{ from: location }} replace />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/shop" element={<Shop />} />
        <Route element={<PrivateRoute><Layout /></PrivateRoute>}>
          <Route path="/" element={<AdminRoute><Dashboard /></AdminRoute>} />
          <Route path="/plans" element={<AdminRoute><Plans /></AdminRoute>} />
          <Route path="/vouchers" element={<AdminRoute><Vouchers /></AdminRoute>} />
          <Route path="/customers" element={<AdminRoute><Customers /></AdminRoute>} />
        </Route>
      </Routes>
    </Router>
  );
}


export default App;
