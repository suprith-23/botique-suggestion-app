# ⚡ Quick Start Guide

## 🏃 Get Running in 5 Minutes

### Prerequisites ✅
- Python 3.8+
- Node.js 16+
- PostgreSQL running

### Terminal 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python -m uvicorn main:app --reload --port 8000
```

**Backend ready at:** `http://localhost:8000`
**API Docs:** `http://localhost:8000/docs`

### Terminal 2: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

**Frontend ready at:** `http://localhost:5173`

## 🔐 Test Login

### Option 1: Quick Register
1. Open `http://localhost:5173`
2. Click "Sign up"
3. Fill registration form
4. Login with your credentials

### Option 2: Direct API Test
```bash
# Register User
curl -X POST "http://localhost:8000/api/auth/register/user" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "test123",
    "full_name": "Test User"
  }'

# Login
curl -X POST "http://localhost:8000/api/auth/login?email=test@example.com&password=test123"
```

## 📝 Key Files to Know

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI entry point |
| `backend/app/models/` | Database models |
| `backend/app/services/design_suggestion_service.py` | AI engine |
| `frontend/src/App.tsx` | Main React app |
| `frontend/src/pages/UserDashboard.tsx` | Upload & suggestions |
| `frontend/src/pages/AdminDashboard.tsx` | Analytics |

## 🎯 First Steps

1. **Register** as User or Admin
2. **Upload** a cloth image
3. **View** AI suggestions
4. **Save** your favorite designs
5. **Download** as PDF/Image

## 🛠 Common Commands

```bash
# Backend only
cd backend && python -m uvicorn main:app --reload

# Frontend only
cd frontend && npm run dev

# Build frontend
cd frontend && npm run build

# Stop servers
Ctrl+C (in terminal)
```

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `lsof -i :8000` then `kill -9 <PID>` |
| Port 5173 in use | `lsof -i :5173` then `kill -9 <PID>` |
| DB connection error | Verify `DATABASE_URL` in `.env` |
| Modules not found | Run `pip install -r requirements.txt` |
| npm not found | Install Node.js from nodejs.org |

## 📚 Documentation

- Detailed setup: [SETUP.md](./SETUP.md)
- Project overview: [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)
- Full docs: [README.md](./README.md)

## 🎉 You're All Set!

Start creating amazing design suggestions! 🎨

---

**Need Help?**
- Check API docs at `http://localhost:8000/docs`
- Check browser console for frontend errors
- Check terminal for backend errors
