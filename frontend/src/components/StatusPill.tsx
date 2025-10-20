import React from "react";
import { PayoutStatus } from "../types/Payout";

interface Props {
    status: PayoutStatus,
}
const Status = {
    INITIATED: {
        color: "#3b194f",
        background: "#e1d6fe",
        title: 'Initiated'
    },
    PENDING: {
        color: "#2655d7",
        background: "#a4c7ff",
        title: 'Pending'
    },
    IN_TRANSIT: {
        color:  '#771b49',
        title: 'In transit',
        background: "#d6bdd8",
    },
    AUTHORIZED: {
        color: '#14a799',
        title: 'Authorized',
        background: "#a9ca9b",
    },
    EXECUTED: {
        // not
        color: '#90692b',
        title: 'Executed',
        background: "#f0d285",
    },
    PAID: {
        // not
        color: '#2a5d48',
        title: 'Paid',
        background: "#b0d2a1",
    },
    BOUNCED: {
        // not
        color: '#cf4f00',
        title: 'Bounced',
        background: "#f5d6ba",
    },
    BLOCKED: {
        // not
        color: '#a10a34',
        title: 'Blocked',
        background: "#d38f9d",
    },
    CANCELLED: {
        color: '#d9001c',
        title: 'Cancelled',
        background: "#e57c74",
    },
}

const StatusPill: React.FC<Props> = (props) => {
    return (
        <div className="flex flex-row gap-2">
            <div style={{backgroundColor: Status[props.status].background}} className="w-6 h-6 rounded-md flex justify-center items-center">
                <div style={{backgroundColor: Status[props.status].color}} className="w-2 h-2 rounded-full"></div>
            </div>
            <p style={{color: Status[props.status].color}} className="font-bold">{Status[props.status].title}</p>
        </div>
    );
};

export default StatusPill;