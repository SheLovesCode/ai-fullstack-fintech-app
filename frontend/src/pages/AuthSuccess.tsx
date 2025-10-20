import { CheckCircle, ErrorOutline } from "@mui/icons-material";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API_URL from "../config/Config";
import axios from "axios";
import { Box, Typography, CircularProgress } from "@mui/material";

const AuthSuccessPage: React.FC = () => {
    const navigate = useNavigate();
    const [error, setError] = useState(false);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const { data } = await axios.get(`${API_URL}/user/me`, {
                    withCredentials: true,
                });
                localStorage.setItem("user", JSON.stringify(data));
                navigate("/dashboard");
            } catch (err) {
                console.error("Failed to fetch user:", err);
                setError(true);

                const timer = setTimeout(() => {
                    navigate("/login", { replace: true });
                }, 3000);

                return () => clearTimeout(timer);
            }
        };

        const timer = setTimeout(fetchUser, 3000);
        return () => clearTimeout(timer);
    }, [navigate]);

    return (
        <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            gap={2}
            mt={6}
        >
            {!error ? (
                <>
                    <CheckCircle fontSize="large" color="success" />
                    <Typography variant="h4">Login Successful!</Typography>
                    <Typography variant="body1">
                        Successfully authorized, redirecting you to dashboard...
                    </Typography>
                    <CircularProgress sx={{ mt: 2 }} />
                </>
            ) : (
                <>
                    <ErrorOutline fontSize="large" color="error" />
                    <Typography variant="h4" color="error">
                        Failed to fetch user
                    </Typography>
                    <Typography variant="body1">
                        Redirecting you to login in 3 seconds...
                    </Typography>
                    <CircularProgress sx={{ mt: 2 }} />
                </>
            )}
        </Box>
    );
};

export default AuthSuccessPage;
