import React, { useEffect, useState } from "react";
import { Box, Avatar, Typography, CircularProgress } from "@mui/material";
import { useNavigate } from "react-router-dom";

interface UserProfileDisplayProps {
    full_name?: string;
    email?: string;
    profile_pic_url?: string;
}

const UserProfileDisplay: React.FC<UserProfileDisplayProps> = ({ full_name, email, profile_pic_url }) => {
    const [user, setUser] = useState<any | null>(null);
    const [redirecting, setRedirecting] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        } else {
            setRedirecting(true);
            const timer = setTimeout(() => {
                navigate("/login", { replace: true });
            }, 3000); // 3 seconds
            return () => clearTimeout(timer);
        }
    }, [navigate]);

    if (redirecting) {
        return (
            <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                height="100vh"
                gap={2}
            >
                <CircularProgress />
                <Typography variant="h6" color="error">
                    You are not logged in, redirecting you to login...
                </Typography>
            </Box>
        );
    }

    const avatarSrc = user?.profile_pic_url ?? profile_pic_url ?? "https://cdn-icons-png.flaticon.com/512/149/149071.png";
    const displayName = user?.full_name || full_name;
    const displayEmail = user?.email || email;

    return (
        <Box display="flex" flexDirection="column" alignItems="center" gap={2} mt={4}>
            <Avatar src={avatarSrc} alt="Profile" sx={{ width: 120, height: 120 }} />
            {displayName && (
                <Typography variant="h6" fontWeight="bold">
                    Name: {displayName}
                </Typography>
            )}
            {displayEmail && (
                <Typography variant="body1">
                    Email: {displayEmail}
                </Typography>
            )}
        </Box>
    );
};

export default UserProfileDisplay;
