import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/Login";
import UserDashboard from "./pages/UserDashboard";
import AuthSuccessPage from "./pages/AuthSuccess";
import AuthFailurePage from "./pages/AuthFailure";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/login/success" element={<AuthSuccessPage />} />
                <Route path="/login/failure" element={<AuthFailurePage />} />
                <Route path="/dashboard" element={<UserDashboard />} />
                <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
        </Router>
    );
}

export default App;
