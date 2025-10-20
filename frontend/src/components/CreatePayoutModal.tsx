import React, { useEffect, useState } from "react";
import {
    Modal,
    Box,
    Button,
    TextField,
    Typography,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
} from "@mui/material";
import { useForm } from "react-hook-form";
import { NewPayout } from "../types/Payout";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

interface Props {
    open: boolean;
    onClose: () => void;
    onSave: (createPayoutData: NewPayout) => void; // Parent handles API call
}

const CURRENCIES = ["USD", "EUR", "ZAR", "GBP"];

const CreatePayoutModal: React.FC<Props> = ({ open, onClose, onSave }) => {
    const {
        register,
        handleSubmit,
        reset,
        getValues,
        formState: { errors, isValid },
    } = useForm<NewPayout>({
        defaultValues: { amount: undefined, currency: "USD" },
        mode: "onChange",
    });

    const [idempotencyKey, setIdempotencyKey] = useState<string>("");
    const [confirmationOpen, setConfirmationOpen] = useState(false);
    const [formData, setFormData] = useState<NewPayout | null>(null);

    useEffect(() => {
        if (open) {
            setIdempotencyKey(crypto.randomUUID());
        } else {
            reset({ amount: undefined, currency: "USD" });
            setIdempotencyKey("");
            setConfirmationOpen(false);
            setFormData(null);
        }
    }, [open, reset]);

    const handleCreate = (data: NewPayout) => {
        setFormData(data);        // Pass the form data as-is
        setConfirmationOpen(true); // Open confirmation modal
    };

    const handleConfirm = () => {
        if (!formData) return;

        const payload: NewPayout = {
            ...formData,
            amount: Number(formData.amount),
            idempotencyKey,
        };

        try {
            onSave(payload);
            toast.success("Payout created successfully!");
            setConfirmationOpen(false);
            onClose();
            reset();
            setIdempotencyKey("");
        } catch (err: any) {
            toast.error(err?.message || "Failed to create payout");
        }
    };

    return (
        <>
            {/* Form Modal */}
            <Modal open={open} onClose={onClose} sx={{ backgroundColor: "rgba(0,0,0,0.5)" }}>
                <Box
                    sx={{
                        position: "absolute",
                        top: "50%",
                        left: "50%",
                        transform: "translate(-50%, -50%)",
                        width: 400,
                        bgcolor: "background.paper",
                        p: 4,
                        borderRadius: 2,
                        boxShadow: 24,
                    }}
                >
                    <form onSubmit={handleSubmit(handleCreate)}>
                        <Typography sx={{ textAlign: "center", mb: 2 }} variant="h6">
                            Create Payout
                        </Typography>

                        <TextField
                            label="Amount"
                            variant="outlined"
                            fullWidth
                            margin="normal"
                            type="number"
                            inputProps={{ min: 1, max: 1000000, step: 0.01 }}
                            error={!!errors.amount}
                            helperText={errors.amount?.message}
                            {...register("amount", {
                                required: "Amount is required",
                                min: { value: 1, message: "Minimum amount is R1" },
                                max: { value: 1000000, message: "Maximum amount is R1,000,000" },
                            })}
                        />

                        <FormControl fullWidth margin="normal" error={!!errors.currency}>
                            <InputLabel>Currency</InputLabel>
                            <Select
                                defaultValue="USD"
                                {...register("currency", { required: "Currency is required" })}
                            >
                                {CURRENCIES.map((cur) => (
                                    <MenuItem key={cur} value={cur}>
                                        {cur}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>

                        <Box sx={{ mt: 3, display: "flex", gap: 2 }}>
                            <Button variant="outlined" fullWidth onClick={onClose}>
                                Cancel
                            </Button>
                            <Button variant="contained" type="submit" fullWidth disabled={!isValid}>
                                Create
                            </Button>
                        </Box>
                    </form>
                </Box>
            </Modal>

            {/* Confirmation Modal */}
            <Modal
                open={confirmationOpen}
                onClose={() => setConfirmationOpen(false)}
                sx={{ backgroundColor: "rgba(0,0,0,0.5)" }}
            >
                <Box
                    sx={{
                        position: "absolute",
                        top: "50%",
                        left: "50%",
                        transform: "translate(-50%, -50%)",
                        width: 350,
                        bgcolor: "background.paper",
                        p: 4,
                        borderRadius: 2,
                        boxShadow: 24,
                        textAlign: "center",
                    }}
                >
                    <Typography variant="h6" gutterBottom>
                        Confirm Payout
                    </Typography>
                    <Typography>
                        Amount: <strong>{formData?.amount}</strong>
                    </Typography>
                    <Typography>
                        Currency: <strong>{formData?.currency}</strong>
                    </Typography>

                    <Box sx={{ mt: 3, display: "flex", gap: 2 }}>
                        <Button
                            variant="outlined"
                            fullWidth
                            onClick={() => setConfirmationOpen(false)}
                        >
                            Cancel
                        </Button>
                        <Button
                            variant="contained"
                            fullWidth
                            onClick={handleConfirm}
                        >
                            Confirm
                        </Button>
                    </Box>
                </Box>
            </Modal>

            <ToastContainer position="top-right" autoClose={3000} />
        </>
    );
};

export default CreatePayoutModal;
