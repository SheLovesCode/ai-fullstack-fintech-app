import React from "react";
import { ExistingPayout } from "../types/Payout";

interface Props {
    transactions: ExistingPayout[];
}

const CurrencyList: React.FC<Props> = ({ transactions }) => {
    const thisMonth = new Date().getMonth();
    const thisYear = new Date().getFullYear();

    const filteredTransactions = transactions.filter((t) => {
        const date = new Date(t.date);
        return (
            (t.status === "PAID") &&
            date.getMonth() === thisMonth &&
            date.getFullYear() === thisYear
        );
    });

    const totalsByCurrency: Record<string, number> = {};
    filteredTransactions.forEach((t) => {
        const amount = Number(t.amount);
        totalsByCurrency[t.currency] = (totalsByCurrency[t.currency] || 0) + amount;
    });

    const topCurrencies = Object.entries(totalsByCurrency)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 4);

    return (
        <div className="flex flex-row w-full justify-between mb-6 max-w-4xl items-center gap-6">
            {topCurrencies.map(([currency, total]) => (
                <div
                    key={currency}
                    className="border bg-white flex flex-col gap-4 rounded-lg w-full p-4 drop-shadow-md"
                >
                    <p className="text-md text-left font-bold">{currency}</p>
                    <p className="text-md text-left text-gray-500 font-bold">
                        {total.toFixed(2)}
                    </p>
                </div>
            ))}
        </div>
    );
};

export default CurrencyList;
