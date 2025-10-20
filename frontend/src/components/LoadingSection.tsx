import { CircularProgress } from "@mui/material";
import React from "react";

interface Props {
}


const LoadingSection: React.FC<Props> = () => {
    return (
        <div className="bg-white rounded-md max-w-xl w-full flex gap-2 drop-shadow-md flex-col p-4 items-center justify-center">
            <CircularProgress color="secondary" size={50} />
            <p className="font-bold text-2xl">Fetching payouts...</p>
        </div>
    );
};

export default LoadingSection;