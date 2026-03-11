# 🏥 MedSync AI — AI-Powered HCP Interaction Management System

<div align="center">

![MedSync AI](https://img.shields.io/badge/MedSync-AI-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql)
![LangChain](https://img.shields.io/badge/LangChain-gray?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-purple?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-red?style=for-the-badge)

**A full-stack AI-powered CRM system for managing Healthcare Professional (HCP) interactions in the pharmaceutical industry.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Architecture](#-architecture) • [Setup](#-setup--installation) • [API Docs](#-api-documentation)

</div>

---

## 🌟 Features

- 🔐 **JWT Authentication** — Secure login/register with role-based access control
- 👨‍⚕️ **HCP Management** — Full CRUD for Healthcare Professionals
- 📋 **Interaction Logging** — Track every meeting, call, and email with HCPs
- 🤖 **AI Agent** — LangChain + LangGraph powered agent with 6 intelligent tools
- 📊 **Dashboard** — Real-time activity and performance overview
- 💬 **AI Chat Interface** — Natural language interface for interaction management
- 📝 **Follow-up Suggestions** — AI-generated actionable follow-up recommendations
- 🔍 **Sentiment Analysis** — Automatic sentiment scoring on every interaction

---

## 🤖 AI Agent Tools

Built using **LangChain Tools** + **LangGraph State Machine**:

| Tool | Description |
|------|-------------|
| `log_interaction` | Log a new HCP interaction with AI summarization |
| `edit_interaction` | Edit an existing interaction using natural language |
| `get_hcp_profile` | Retrieve complete HCP profile with full interaction history |
| `suggest_followup` | Generate AI-powered prioritized follow-up suggestions |
| `analyze_sentiment` | Analyze and score sentiment of interaction content |
| `search_interactions` | Search past interactions using natural language queries |

---

## 🛠 Tech Stack

### Backend
- **Python 3.10+** — Core programming language
- **FastAPI** — High-performance REST API framework
- **SQLAlchemy** — ORM for database modeling and queries
- **MySQL** — Relational database for persistent storage
- **PyJWT** — JSON Web Token based authentication
- **Passlib + Bcrypt** — Secure password hashing
- **Pydantic** — Data validation and schema enforcement

### AI / Agent Layer
- **LangChain** — Tool definition, LLM integration, and agent orchestration
- **LangGraph** — Stateful agent graph with conditional tool routing
- **Groq API** — Ultra-fast LLM inference (`llama-3.1-8b-instant`)

### Frontend
- **React 18** — Component-based UI library
- **Vite** — Lightning-fast frontend build tool
- **React Router** — Client-side routing and navigation
- **Axios** — Promise-based HTTP client for API calls

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│           React + Vite (Port 5173)               │
└───────────────────────┬─────────────────────────┘
                        │ HTTP / REST
┌───────────────────────▼─────────────────────────┐
│                   Backend                        │
│             FastAPI (Port 8000)                  │
│                                                  │
│  ┌──────────┐  ┌─────────────┐  ┌────────────┐  │
│  │   Auth   │  │     HCP     │  │Interactions│  │
│  │   API    │  │     API     │  │    API     │  │
│  └──────────┘  └─────────────┘  └────────────┘  │
│                                                  │
│  ┌───────────────────────────────────────────┐   │
│  │              AI Agent API                 │   │
│  │   LangGraph State Machine                 │   │
│  │   ┌─────────────────────────────────┐    │   │
│  │   │         LangChain Tools         │    │   │
│  │   │  log · edit · profile · search  │    │   │
│  │   │  suggest_followup · sentiment   │    │   │
│  │   └────────────────┬────────────────┘    │   │
│  │                    │                     │   │
│  │          Groq LLM (llama-3.1-8b)        │   │
│  └───────────────────────────────────────────┘   │
│                                                  │
│  ┌───────────────────────────────────────────┐   │
│  │     SQLAlchemy ORM + MySQL Database       │   │
│  │   users · hcps · interactions · followups │   │
│  └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
medsync-ai/
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── graph.py                  # LangGraph state machine
│   │   │   └── tools/
│   │   │       ├── log_interaction.py
│   │   │       ├── edit_interaction.py
│   │   │       ├── get_hcp_profile.py
│   │   │       ├── suggest_followup.py
│   │   │       ├── analyze_sentiment.py
│   │   │       └── search_interactions.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── hcp.py
│   │   │   ├── interactions.py
│   │   │   └── agent.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── hcp.py
│   │   │   ├── interaction.py
│   │   │   └── followup.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── hcp.py
│   │   │   └── interaction.py
│   │   └── main.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── package.json
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

Make sure the following are installed on your machine:

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Groq API Key — Get it free at [console.groq.com](https://console.groq.com)

---

### 1. Clone the Repository

```bash
git clone https://github.com/itskie/medsync-ai.git
cd medsync-ai
```

---

### 2. MySQL Database Setup

```sql
-- Login to MySQL
mysql -u root -p

-- Create the database
CREATE DATABASE medsync_db;
EXIT;
```

---

### 3. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# Install all required dependencies
pip install -r requirements.txt

# Create your environment file from the provided example
cp .env.example .env
```

#### Configure your `.env` file:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=medsync_db

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Groq AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# Application Settings
APP_NAME=MedSync AI
DEBUG=True
```

#### Start the backend server:

```bash
python -m uvicorn app.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

---

### 4. Frontend Setup

```bash
# Open a new terminal and navigate to the frontend directory
cd frontend

# Install all dependencies
npm install

# Start the development server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 📖 API Documentation

Once the backend is running, visit the interactive Swagger UI at:

```
http://127.0.0.1:8000/docs
```

### Available Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | ❌ |
| POST | `/auth/login` | Login and receive JWT token | ❌ |
| GET | `/hcps/` | Get all HCPs | ✅ |
| POST | `/hcps/` | Create a new HCP | ✅ |
| GET | `/hcps/{id}` | Get HCP by ID | ✅ |
| PUT | `/hcps/{id}` | Update HCP details | ✅ |
| DELETE | `/hcps/{id}` | Delete an HCP | ✅ |
| GET | `/interactions/` | Get all interactions | ✅ |
| POST | `/interactions/` | Log a new interaction | ✅ |
| GET | `/interactions/{id}` | Get interaction by ID | ✅ |
| PUT | `/interactions/{id}` | Update an interaction | ✅ |
| DELETE | `/interactions/{id}` | Delete an interaction | ✅ |
| POST | `/agent/chat` | Chat with the AI Agent | ✅ |
| GET | `/agent/tools` | List all available AI tools | ✅ |
| GET | `/health` | Server health check | ❌ |

---

## 🔐 Authentication

This project uses **JWT Bearer Token** authentication.

1. Register or Login to receive an `access_token`
2. Include the token in all protected requests:

```
Authorization: Bearer <your_token>
```

---

## 💡 Usage Examples

### Register a User

```json
POST /auth/register
{
  "name": "John Doe",
  "email": "john@medsync.com",
  "password": "SecurePass@123",
  "role": "sales_rep"
}
```

### Create an HCP

```json
POST /hcps/
{
  "name": "Dr. Jane Smith",
  "specialization": "Oncologist",
  "hospital": "City Medical Center",
  "city": "Mumbai",
  "email": "jane.smith@citymed.com",
  "phone": "9800000000"
}
```

### Log an Interaction

```json
POST /interactions/
{
  "hcp_id": 1,
  "interaction_type": "meeting",
  "date": "2026-03-11",
  "topics_discussed": "Phase III clinical trial results and efficacy data",
  "sentiment": "positive",
  "outcomes": "Doctor expressed interest in prescribing the product"
}
```

### Chat with AI Agent

```json
POST /agent/chat
{
  "message": "Use suggest_followup tool with interaction_id 1",
  "interaction_id": 1
}
```

---

## 🌐 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | MySQL host address | `localhost` |
| `DB_PORT` | MySQL port number | `3306` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | `yourpassword` |
| `DB_NAME` | Database name | `medsync_db` |
| `SECRET_KEY` | JWT signing secret key | `random_secure_string` |
| `ALGORITHM` | JWT hashing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time in minutes | `30` |
| `GROQ_API_KEY` | Groq LLM API key | `gsk_...` |
| `DEBUG` | Enable debug mode | `True` / `False` |

---

## 🚀 Deployment Notes

For production deployment:

- Set `DEBUG=False` in environment variables
- Use a strong randomly generated `SECRET_KEY`
- Store all secrets using environment variables — never hardcode them
- Use **AWS RDS** or **PlanetScale** for managed MySQL
- Deploy backend on **Railway**, **Render**, or **AWS EC2**
- Deploy frontend on **Vercel** or **Netlify**

---

## 👨‍💻 Author

**Shobhit Kumar Singh**

- GitHub: [@itskie](https://github.com/itskie)
- LinkedIn: [linkedin.com/in/itskie](https://linkedin.com/in/itskie)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
Built with ❤️ by Shobhit Singh &nbsp;|&nbsp; MedSync AI © 2026
</div>
