// src/pages/UserDashboard.tsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import CreatePayoutModal from "../components/CreatePayoutModal";
import DisplayUserProfileCard from "../components/DisplayUserProfileCard";
import { NewPayout } from "../types/Payout";
import PayoutTable from "../components/DisplayPayoutsTable";
import { Box, CircularProgress, Typography } from "@mui/material";
import API_URL from "../config/Config";

const UserDashboard: React.FC = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState<any | null>(null);
    const [isModalOpen, setModalOpen] = useState(false);
    const [refreshTable, setRefreshTable] = useState(false);
    const [redirecting, setRedirecting] = useState(false);

    useEffect(() => {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        } else {
            setRedirecting(true);
            const timer = setTimeout(() => {
                navigate("/login", { replace: true });
            }, 3000);
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

    const handleCreatePayout = async (data: NewPayout) => {
        try {
            const payload = {
                amount: Number(data.amount),
                currency: data.currency,
                idempotency_key: data.idempotencyKey,
            };

            const response = await fetch(`${API_URL}/payouts/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error(`Failed to create payout: ${response.statusText}`);
            }

            setModalOpen(false);
            setRefreshTable((prev) => !prev);
        } catch (err) {
            console.error("Failed to create payout:", err);
            alert("Failed to create payout. Please try again.");
        }
    };

    if (!user) return <p>Loading...</p>;
    return (
        <div style={styles.container}>
            <DisplayUserProfileCard
                full_name={user.full_name}
                email={user.email}
                profile_pic_url={user.profile_pic_url}
            />

            <div style={{ marginTop: "1.5rem" }}>
                <button
                    className="bg-purple-300 rounded-md py-2 px-4 hover:bg-purple-400"
                    onClick={() => setModalOpen(true)}
                >
                    Create Payout
                </button>
            </div>

            <CreatePayoutModal
                open={isModalOpen}
                onClose={() => setModalOpen(false)}
                onSave={handleCreatePayout}
            />

            <div style={{ marginTop: "2rem" }}>
                <PayoutTable refreshTable={refreshTable} />
            </div>
        </div>
    );
};

export default UserDashboard;

const styles: { [key: string]: React.CSSProperties } = {
    container: {
        height: "100%",
        textAlign: "center",
        fontFamily: "Arial, sans-serif",
        backgroundColor: "#f2f3f7",
        padding: "1rem",
        minHeight: "100vh",
    },
};
