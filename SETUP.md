# 🚀 Complete Setup Guide - Boutique Suggestion App

## Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Git

## Step-by-Step Setup

### 1️⃣ Database Setup

#### Option A: Using PostgreSQL (Recommended)

```bash
# Start PostgreSQL (if not already running)
# macOS with Homebrew:
brew services start postgresql

# Or manually:
psql -U postgres

# Create database
createdb boutique_db

# Verify
psql boutique_db
```

### 2️⃣ Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your settings
cp .env.example .env

# Edit .env with your database URL
# Example: DATABASE_URL=postgresql://postgres:password@localhost:5432/boutique_db

# Run the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### 3️⃣ Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173` or `http://localhost:3000`

## 🔑 Database Connection

### PostgreSQL Connection String Format
```
postgresql://username:password@localhost:5432/boutique_db
```

### Example .env Configuration
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/boutique_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOADS_DIR=./uploads
```

## 📋 Quick Test Credentials

After setup, you can create test accounts or use:

### Register Admin
```
Email: admin@boutique.com
Username: admin
Password: admin123
Full Name: Boutique Admin
```

### Register User
```
Email: user@boutique.com
Username: user
Password: user123
Full Name: John Doe
```

## 🧪 API Testing

### Using cURL

**Register User**
```bash
curl -X POST "http://localhost:8000/api/auth/register/user" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@boutique.com",
    "username": "user",
    "password": "password123",
    "full_name": "User Name"
  }'
```

**Login**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=user@boutique.com&password=password123"
```

### Using Swagger UI
Visit: `http://localhost:8000/docs`

## 📁 File Structure Recap

```
boutique-suggestion-app/
├── backend/
│   ├── app/
│   │   ├── core/              # Config, DB, Security
│   │   ├── models/            # SQLAlchemy Models
│   │   ├── schemas/           # Pydantic Schemas
│   │   ├── routes/            # API Routes
│   │   ├── services/          # Business Logic
│   │   └── utils/             # Utilities
│   ├── uploads/               # Uploaded images
│   ├── main.py                # FastAPI app
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React Components
│   │   ├── pages/             # Page Components
│   │   ├── services/          # API Services
│   │   ├── types/             # TypeScript Types
│   │   ├── context/           # Auth Context
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── database/
│   └── init.sql               # Database initialization
│
└── README.md
```

## 🎯 Key Features Checklist

### Authentication ✅
- [x] User Registration
- [x] Admin Registration
- [x] JWT-based Login
- [x] Role-based Access Control
- [x] Token Management

### User Features ✅
- [x] Cloth Upload
- [x] Design Suggestions (Rule-based AI)
- [x] Save Designs
- [x] Download as PDF/Image
- [x] View Suggestions History

### Admin Features ✅
- [x] Dashboard with Statistics
- [x] View All Uploads
- [x] Analytics Charts
- [x] Trending Data
- [x] User Activity Overview

### Design Suggestions ✅
- [x] Neck Design Recommendations
- [x] Sleeve Style Suggestions
- [x] Embroidery Pattern Recommendations
- [x] Color Combination Suggestions
- [x] Border Style Recommendations

## 🐛 Troubleshooting

### PostgreSQL Connection Error
```
Error: Could not connect to database
```
Solution:
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify credentials are correct

### Port Already in Use
```
Error: Address already in use
```
Solution:
```bash
# For Backend (8000)
lsof -i :8000
kill -9 <PID>

# For Frontend (5173)
lsof -i :5173
kill -9 <PID>
```

### Module Not Found
```
ModuleNotFoundError: No module named 'fastapi'
```
Solution:
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### CORS Errors
- Check `allowed_origins` in `app/core/config.py`
- Ensure frontend URL is in the list
- Restart backend after changes

## 📝 Environment Variables

### Required Backend Variables
```env
DATABASE_URL          # PostgreSQL connection string
SECRET_KEY           # JWT secret key (use strong random string)
ALGORITHM            # JWT algorithm (default: HS256)
ACCESS_TOKEN_EXPIRE_MINUTES  # Token expiry (default: 30)
UPLOADS_DIR          # Directory for uploads (default: ./uploads)
```

### Optional Variables
```env
ALLOWED_ORIGINS      # CORS origins (comma-separated)
MAX_UPLOAD_SIZE      # Max file size in bytes (default: 10MB)
```

## 🚀 Production Deployment

### Backend (using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Frontend (Build & Deploy)
```bash
npm run build
# Copy dist/ folder to your web server
```

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Support & Issues

For issues or questions:
1. Check the [README.md](./README.md)
2. Review API logs in terminal
3. Check browser console for frontend errors
4. Verify database connectivity

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Happy Coding! 🎉**
