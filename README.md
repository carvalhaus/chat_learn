# chat_learn

This repository is a learning project for building a simple **chatbot application** using **FastAPI** for the backend and **React** for the frontend. The goal is to understand the integration of a modern Python backend with a JavaScript frontend, using Docker for containerization.

## 🚀 Tech Stack

-   **Backend:** FastAPI (Python)
-   **Frontend:** React + Vite
-   **Database:** MySQL 8
-   **Cache/Broker:** Redis
-   **Proxy/Reverse Proxy:** NGINX
-   **Containerization:** Docker & Docker Compose

---

## 📂 Project Structure

```tree
├── backend/ # FastAPI application
├── frontend/ # React application
├── nginx/ # NGINX configuration
├── docker-compose.yml
└── README.md
```

## ⚙️ How to Run the Project

### 1️⃣ Clone the repository

```bash
git clone https://github.com/carvalhaus/chat_learn.git
cd chat_learn
```

### 2️⃣ Run with Docker Compose

```bash
docker-compose up --build
```

### 3️⃣ Access the Applications

-   **Frontend:** [http://localhost](http://localhost)
-   **Backend API:** [http://localhost/api](http://localhost/api)
-   **Database:** MySQL on `localhost:3307`
-   **Redis:** on `localhost:6379`

## 🔗 API Endpoints Example

| Method | Endpoint | Description          |
| ------ | -------- | -------------------- |
| GET    | `/api`   | Health check / Hello |

## 🐳 Docker Services

| Service  | Description    | Port                     |
| -------- | -------------- | ------------------------ |
| frontend | React App      | 3001 → 80 (via NGINX)    |
| backend  | FastAPI API    | 8000 (proxied to `/api`) |
| db       | MySQL Database | 3307:3306                |
| redis    | Redis Cache    | 6379:6379                |
| nginx    | Reverse Proxy  | 80:80                    |

## 🚧 Development Notes

-   This project is for **learning purposes only**.
-   Not production-ready but provides a good foundation for building microservices with **Python** and **JavaScript**.
-   Open for improvements, optimizations, and feature additions.

## 🤝 Contributing

Feel free to open issues or pull requests to improve this project.

## 📜 License

This project is licensed under the **MIT License**.

## ✍️ Author

Made by [João Pedro de Carvalho Oliveira](https://www.linkedin.com/in/joao-pedro-carvalho-oliveira/).
