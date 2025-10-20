// src/components/ProtectedRoute.tsx
import React from "react";
import { Navigate } from "react-router-dom";
import { useUser } from "../pages/UserContext";

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const { user } = useUser();

    // If user is not logged in, redirect to /login
    if (!user) {
        return <Navigate to="/login" replace />;
    }

    // Otherwise, render the protected component
    return <>{children}</>;
};

export default ProtectedRoute;
