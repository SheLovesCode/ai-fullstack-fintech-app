# 💻 AI-Assisted Full-Stack Fintech App

This is a full-stack web application that allows users to log in via Google OAuth, submit payout requests, and track the status of those payouts in real time. The backend simulates integration with a third-party payments provider while demonstrating secure, observable, and reliable flows.

The project consists of four main parts:

- **Frontend**: React (TypeScript) Single Page Application (SPA)  
- **Backend**: FastAPI (Python) RESTful API  
- **Database**: PostgreSQL for storing users and payouts  
- **Mock Payment Gateway**: Containerized service simulating a third-party payments provider  

The application is fully dockerized for easy development.

---

## 🧭 Project Overview

Users can log in via Google OAuth, create payout requests (amount + currency), and view a paginated list of payouts with live status updates. The backend handles idempotent payout creation, simulates payment provider webhooks, and includes retries, rate-limiting, and observability with correlation IDs.

### ✨ Features
- 🔑 Login with Google OAuth 2.0  
- 💰 Create payouts (amount + currency)  
- 📃 View paginated list of payouts with live status updates  
- 🛡 Safe error handling and structured logs  
- 🔄 Simulated third-party payments integration with webhooks  

### 🏦 Mock Payment Gateway
- **Mock Payments Service**: A lightweight service that simulates a third-party payments provider.
  - Handles payout requests sent by the backend  
  - Sends asynchronous webhook updates back to the backend  
  - Supports retries, rate-limiting, and idempotent processing to mimic real-world behavior  
  - Uses a shared callback secret to verify webhook authenticity  

### 🔒 Security

Since security was a critical aspect of this assignment, all backend endpoints require a logged-in user. We implemented a session-based authentication strategy where a secure cookie is set upon login. This cookie is accessible on the frontend to manage user state but is designed to prevent tampering.  

Additionally, all webhook requests from the mock payment service are verified using HMAC signatures, ensuring that updates to payout statuses are authenticated and cannot be spoofed. This combination of session-based authentication, secure cookies, and signed webhooks ensures robust security while maintaining smooth frontend integration.

---

## 🛠 Technologies Used

- **Frontend**: React.js, TypeScript, CSS  
- **Backend**: FastAPI, Python  
- **Database**: PostgreSQL  
- **Containerization**: Docker  

---

## ⚡ Installation

### Prerequisites

Make sure you have the following installed on your local machine:

- **Docker** (version 20.10 or higher) – [Install Docker](https://docs.docker.com/get-docker/)  
- **Docker Compose** (only required if Docker version is below 20.10) – [Install Docker Compose](https://docs.docker.com/compose/install/)  

---

### 🔐 Google OAuth 2.0 Setup

> You need a Google account. If you don’t have one, [create a Google account](https://accounts.google.com/signup) first.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)  
2. Create a **new project** or select an existing one  
3. Navigate to **APIs & Services → OAuth consent screen**:
   - User type: **External**  
   - Fill in **App name**, **User support email**, and **Developer contact email**  
   - Save and continue  
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth Client ID**:
   - Application type: **Web application**  
   - Name: e.g., `Fintech App Local`  
   - **Authorized redirect URIs**:  
     ```text
     http://localhost/api/auth/callback
     ```  
   - Click **Create**  
5. Copy the generated **Client ID** and **Client Secret** — you will use them in your backend `.env` file  

---

### 📂 Clone the Repository

```bash
    git clone git@github.com:SheLovesCode/ai-fullstack-fintech-app.git
    cd ai-fullstack-fintech-app
```

## 🚀 Start the Services

Make sure Docker Desktop is open and no other services are running on ports `80`, `5432`, `8080`, `8000`, or `9000`.

```bash
# For Docker 20.10+:
docker compose up --build

# For older Docker versions:
docker-compose up --build
```

## 🚀 Running the Services

This will start the following services:

- **PostgreSQL Database**: [http://localhost:5432](http://localhost:5432)  
- **FastAPI Backend**: [http://localhost:8000](http://localhost:8000)  
- **React Frontend**: [http://localhost](http://localhost)  
- **Mock 3rd Party Payment Service**: [http://localhost:9000](http://localhost:9000)  

The app will be accessible at: [http://localhost](http://localhost)

---

## 🛑 Stopping the Services

To stop the running containers:

```bash
# For Docker 20.10+:
docker compose down -v

# For older Docker versions:
docker-compose down -v
```

## 🐞 Troubleshooting

If you encounter a `Connection to server at "postgres", port 5432 failed` after running `docker compose up --build`:

1. Stop your containers with `CTRL+C`  
2. Run `docker compose up` again  

Ensure all required ports (`5432`, `8000`, `9000`, `8080`) are free before starting the services.

---

## 📬 API Reference & Documentation

A `postman_collection.json` file is included in the root folder for reference.

> **Note:** Because Google OAuth uses redirects, this collection is mainly for reference — showing request/response flows, headers, and payloads. Full automation of OAuth login is not supported.

The project also includes `ai_usage.md`, detailing how AI tools were used, the prompts given, decisions made, and validations performed throughout development.

---

**Author:** Diana Munyaradzi
