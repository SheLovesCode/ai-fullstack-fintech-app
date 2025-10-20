import React from "react";
import { ExistingPayout } from "../types/Payout";
import { ArrowBack, ArrowForward } from "@mui/icons-material";
import StatusPill from "./StatusPill";

interface Props {
  transactions: ExistingPayout[];
  total: number;
  offset: number;
  limit: number;
  handlePrev: () => void;
  handleNext: () => void;
  handleLimitChange: (newLimit: number) => void;
}

const TransactionTable: React.FC<Props> = ({
  transactions,
  total,
  offset,
  limit,
  handlePrev,
  handleNext,
  handleLimitChange,
}) => {
  const safeLimit = limit > 0 ? limit : 1;
  const totalPages = total > 0 ? Math.ceil(total / safeLimit) : 1;
  const currentPage = total > 0 ? Math.floor(offset / safeLimit) + 1 : 1;

  return (
    <div className="w-full flex flex-col items-center max-w-4xl bg-white rounded-lg p-4 drop-shadow-md gap-4">
      <div className="flex flex-row justify-between items-center w-full">
        <p className="font-bold text-left text-xl self-baseline">Payouts by date</p>

        <div className="flex items-center gap-2">
          <label htmlFor="limit" className="text-sm font-semibold text-gray-700">
            Rows per page:
          </label>
          <select
            id="limit"
            value={limit}
            onChange={(e) => handleLimitChange(Number(e.target.value))}
            className="border border-gray-300 rounded-md p-1 text-sm focus:ring-purple-400 focus:outline-none"
          >
            {[5, 10, 15, 20, 50].map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </div>
      </div>

      <table className="w-full">
        <thead>
          <tr className="text-left">
            <th className="pb-4">Date</th>
            <th className="pb-4">Currency</th>
            <th className="pb-4">Amount</th>
            <th className="pb-4">Status</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr
              key={`${transaction.currency}-${transaction.date}-${transaction.amount}`}
              className="text-left border-b border-b-gray-200"
            >
              <td className="py-3">
                {new Date(transaction.date)
                  .toLocaleString("en-GB", {
                    weekday: "long",
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: false,
                  })
                  .replace(",", " at")}
              </td>
              <td className="py-3">{transaction.currency}</td>
              <td className="py-3">{Number(transaction.amount).toFixed(2)}</td>
              <td className="py-3">
                <StatusPill status={transaction.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="flex items-center gap-2 mt-4">
        <button
          onClick={handlePrev}
          disabled={currentPage === 1}
          className={`rounded-l-md px-2 py-1 flex items-center gap-1 ${
            currentPage === 1
              ? "bg-gray-200 cursor-not-allowed"
              : "bg-purple-300 hover:bg-purple-400"
          }`}
        >
          <ArrowBack /> Prev
        </button>

        <div className="border-t border-b py-1 px-3 text-center text-sm">
          Page {currentPage} of {totalPages}
        </div>

        <button
          onClick={handleNext}
          disabled={currentPage >= totalPages}
          className={`rounded-r-md px-2 py-1 flex items-center gap-1 ${
            currentPage >= totalPages
              ? "bg-gray-200 cursor-not-allowed"
              : "bg-purple-300 hover:bg-purple-400"
          }`}
        >
          Next <ArrowForward />
        </button>
      </div>

      <div className="text-sm text-gray-600 mt-1">
        Showing {offset + 1} – {Math.min(offset + limit, total)} of {total}
      </div>
    </div>
  );
};

export default TransactionTable;
