export enum PayoutStatus {
    INITIATED = "INITIATED",
    PENDING = "PENDING",
    IN_TRANSIT = "IN_TRANSIT",
    AUTHORIZED = "AUTHORIZED",
    EXECUTED = "EXECUTED",
    PAID = "PAID",
    BOUNCED = "BOUNCED",
    BLOCKED = "BLOCKED",
    CANCELLED = "CANCELLED",
}

export interface ExistingPayout {
    amount: number;
    currency: string;
    status: PayoutStatus;
    date: string;
}

export interface NewPayout {
    amount: number;
    currency: string;
   idempotencyKey: string;
}

export interface PaginationResponse {
    total: number;
    currentOffset: number;
    hasMore: boolean;
}

export interface PaginatedPayouts {
    payouts: ExistingPayout[];
    pagination: PaginationResponse;
}
