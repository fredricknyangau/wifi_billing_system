import React from 'react';
import { Navigate } from 'react-router-dom';

const AdminRoute = ({ children }) => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const isAdmin = user.is_staff || user.is_superuser;

    if (!isAdmin) {
        return <Navigate to="/shop" replace />;
    }

    return children;
};

export default AdminRoute;
