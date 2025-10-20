import React, { useEffect, useState } from "react";
import axios from "axios";
import { ExistingPayout, PaginatedPayouts } from "../types/Payout";
import API_URL from "../config/Config";
import CurrencyList from "./CurrencyList";
import ErrorCard from "./ErrorCard";
import TransactionTable from "./TransactionTable";
import LoadingSection from "./LoadingSection";

interface Props {
  refreshTable?: boolean;
}

const PayoutTable: React.FC<Props> = ({ refreshTable }) => {
  const [payouts, setPayouts] = useState<ExistingPayout[]>([]);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(10);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPayouts = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await axios.get<PaginatedPayouts>(`${API_URL}/payouts`, {
        params: { offset, limit },
        withCredentials: true,
      });

      setPayouts(res.data.payouts);
      setTotal(res.data.pagination.total);
    } catch (err) {
      setError("Failed to fetch payouts");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayouts();
  }, [offset, limit, refreshTable]);

  const handlePrev = () => {
    if (offset > 0) setOffset(Math.max(offset - limit, 0));
  };

  const handleNext = () => {
    const totalPages = Math.ceil(total / limit);
    const currentPage = Math.floor(offset / limit) + 1;
    if (currentPage < totalPages) setOffset(offset + limit);
  };

  const handleLimitChange = (newLimit: number) => {
    setLimit(newLimit);
    setOffset(0); // reset to first page
  };

  return (
    <div className="mt-6 w-full">
      {loading ? (
        <div className="flex justify-center">
          <LoadingSection />
        </div>
      ) : error ? (
        <div className="flex justify-center">
          <ErrorCard handleReAttempt={fetchPayouts} error={error} />
        </div>
      ) : payouts.length === 0 ? (
        <p>No payouts found</p>
      ) : (
        <div className="flex flex-col justify-center items-center">
          <TransactionTable
            transactions={payouts}
            limit={limit}
            offset={offset}
            total={total}
            handleNext={handleNext}
            handlePrev={handlePrev}
            handleLimitChange={handleLimitChange}
          />
        </div>
      )}
    </div>
  );
};

export default PayoutTable;
