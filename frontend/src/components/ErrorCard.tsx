import React from "react";
import { ExistingPayout } from "../types/Payout";
import { ReportProblemRounded } from "@mui/icons-material";

interface Props {
    handleReAttempt: () => void;
    error: string;
}

const ErrorCard: React.FC<Props> = (props) => {
    return (
        <div className="bg-red-100 rounded-md max-w-xl w-full flex gap-2 drop-shadow-md flex-col p-4 items-center justify-center">
          <ReportProblemRounded fontSize="large" color="error" />


          <p className="font-xl text-red-500 font-bold">Error</p>
          <p className="text-gray-700 font-semibold">{props.error}</p>


          <button className="font-bold bg-white rounded-lg py-2 px-3 hover:bg-gray-200 hover:border hover:border-gray-700" onClick={props.handleReAttempt}>Try again</button>
        </div>
    );
};


export default ErrorCard;