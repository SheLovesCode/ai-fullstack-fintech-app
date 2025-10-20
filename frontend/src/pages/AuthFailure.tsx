import { Error } from "@mui/icons-material";
import React from "react";

const AuthFailurePage: React.FC = () => {
    return (
        <div className="text-center flex flex-col items-center mt-6 justtify-center gap-2">
            <Error color="error" fontSize="large" />
            <h1 className="text-3xl text-red-600">Login Failed</h1>
            <p className="text-lg">Oops! Something went wrong while logging in with Google.</p>
            <a className="bg-purple-300 font-bold rounded-lg py-2 px-4" href="/login">Try Again</a>
        </div>
    );
};

export default AuthFailurePage;