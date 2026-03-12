# 🧠 SmartCalc — Full-Stack Scientific Calculator

SmartCalc is a production-ready full-stack scientific calculator web application built with:

- ⚡ FastAPI (Backend)
- 🐘 PostgreSQL (Database)
- 🔐 JWT Authentication
- ⚛️ React + Vite (Frontend)
- 🎨 TailwindCSS (Modern UI)
- 🧮 Custom Math Parser (No eval)

---

## 🚀 Features

### 🔐 Authentication
- User Registration
- User Login
- JWT Token-based Authentication
- Protected Routes
- Token-based API security

---

### 🧮 Scientific Calculator Engine (Backend)

Custom-built mathematical expression engine:

- Tokenizer
- Shunting Yard Algorithm (Infix → Postfix)
- Stack-based Postfix Evaluator

#### Supported Operations:
```
+  -  *  /  %  ^
(  )
negative numbers
decimals
```

#### Supported Functions:
```
sin(x)
cos(x)
tan(x)
sqrt(x)
log(x)
log10(x)
ln(x)
factorial(x)
```

#### Constants:
```
pi
e
```

⚠️ No use of `eval()` or `ast.literal_eval()`.

---

### 📜 History System
- Each user has isolated history
- Click history to reuse expression
- Delete single history item
- Clear entire history

---

### 🎨 Modern UI (Frontend)

- Glassmorphism design
- Dark / Light theme toggle
- Smooth animations
- Keyboard input support
- Copy result button
- Responsive layout
- Sidebar history
- Micro-interactions

---

## 🏗️ Project Structure

```
SmartCalc/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── engine/
│   └── alembic/
│
└── frontend/
    └── src/
        ├── pages/
        ├── components/
        ├── context/
        └── layouts/
```

---

## ⚙️ Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

## ⚛️ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## 🏭 Production Build

### Frontend

```bash
npm run build
```

### Backend

Use:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or use Gunicorn in production.

---

## 🔒 Security Notes

- Passwords hashed with bcrypt
- JWT expiration enforced
- Protected API endpoints
- CORS configured
- No unsafe code execution

---

## 📌 Author

Aononto Jahan  
Full-Stack Developer

---

## ⭐ Future Improvements

- Refresh tokens
- Rate limiting
- Docker containerization
- CI/CD pipeline
- Cloud deployment (Render / Railway / VPS)

---

## ⭐ How to Run:
- Backend:(Run this below command in the backend)
- cd /e/SmartCalc/backend
- source .venv/Scripts/activate
- python -m uvicorn app.main:app --reload

- Forntend
- cd /e/SmartCalc/frontend
- npm run dev

---

## Run the Project Locally

### 1. Clone the repository
git clone https://github.com/aonontojahan/Smart-Calculator.git
cd Smart-Calculator

### 2. Start the backend
cd backend
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

Backend will run at:
http://127.0.0.1:8000

### 3. Start the frontend (open new terminal)
cd frontend
npm install
npm run dev

Frontend will run at:
http://localhost:5173

---

## 📄 License


MIT License

