# Boutique Suggestion App - AI-Powered Design System

Full-stack application for boutique design suggestions using FastAPI, React, and PostgreSQL.

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── core/           # Configuration, database, security
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── main.py             # FastAPI entry point
│   └── requirements.txt
└── frontend/                # React TypeScript frontend
    ├── src/
    │   ├── components/     # Reusable components
    │   ├── pages/          # Page components
    │   ├── services/       # API services
    │   ├── types/          # TypeScript types
    │   ├── context/        # React context (Auth)
    │   └── App.tsx
    ├── package.json
    └── tsconfig.json
```

## Features

### 🧩 Module 1: Authentication
- Email/Password registration and login
- JWT-based authentication
- Role-based access control (Admin, User)
- User profile management

### 🧩 Module 2: Dashboard
- **Admin Dashboard**: Upload stats, cloth type distribution, occasion breakdown, trending data
- **User Dashboard**: Upload management, design suggestions, saved designs

### 🧩 Module 3: Cloth Upload
- Image upload with validation
- Cloth type, occasion, gender, age group selection
- Budget range selection
- Fabric description

### 🧩 Module 4: AI Design Suggestion Engine
- Rule-based design suggestions
- Recommendations for:
  - Neck designs
  - Sleeve styles
  - Embroidery patterns
  - Color combinations
  - Border styles

### 🧩 Module 5: Unique Features
- ✨ **Occasion-Based Suggestions**: Wedding, Office, Festival, Party
- ✨ **Budget-Based Designs**: ₹1000-3000, ₹3000-8000, ₹10000+
- ✨ **Trend Detector**: Show trending colors and patterns
- ✨ **Design Comparison**: Side-by-side comparison
- ✨ **Save & Share**: Save, download (PDF/Image), and share designs

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **API Server**: Uvicorn

### Frontend
- **Framework**: React 18.2
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React
- **Export**: html2canvas, jsPDF
- **Build Tool**: Vite

### Database
- **PostgreSQL** with SQLAlchemy ORM
- Tables: users, uploads, design_suggestions, saved_designs

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.13 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database URL and settings

# Run API Server & creates tables 
python main.py

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## API Endpoints

### Authentication
- `POST /api/auth/register/user` - Register user
- `POST /api/auth/register/admin` - Register admin
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/me` - Update user profile

### Uploads
- `POST /api/uploads` - Upload cloth image
- `GET /api/uploads/my-uploads` - Get user uploads
- `GET /api/uploads/{id}` - Get upload details
- `GET /api/uploads/{id}/suggestions` - Get suggestions for upload

### Design Suggestions
- `GET /api/design-suggestions/{id}` - Get suggestion details
- `POST /api/design-suggestions/{id}/save` - Save design
- `GET /api/design-suggestions/saved/list` - Get saved designs
- `DELETE /api/design-suggestions/{id}/save` - Unsave design

### Admin
- `GET /api/admin/dashboard/stats` - Dashboard statistics
- `GET /api/admin/uploads` - Get all uploads
- `GET /api/admin/uploads/by-type/{type}` - Filter by type
- `GET /api/admin/trending` - Trending data

## Database Schema

### users
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  username VARCHAR UNIQUE NOT NULL,
  hashed_password VARCHAR NOT NULL,
  role ENUM('admin', 'user'),
  full_name VARCHAR,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### uploads
```sql
CREATE TABLE uploads (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FOREIGN KEY,
  image_path VARCHAR NOT NULL,
  cloth_type ENUM,
  occasion ENUM,
  gender ENUM,
  age_group ENUM,
  budget_range ENUM,
  fabric_description VARCHAR,
  created_at TIMESTAMP
);
```

### design_suggestions
```sql
CREATE TABLE design_suggestions (
  id INTEGER PRIMARY KEY,
  upload_id INTEGER FOREIGN KEY,
  user_id INTEGER FOREIGN KEY,
  neck_design VARCHAR,
  sleeve_style VARCHAR,
  embroidery_pattern VARCHAR,
  color_combination VARCHAR,
  border_style VARCHAR,
  description TEXT,
  confidence_score VARCHAR,
  created_at TIMESTAMP
);
```

### saved_designs
```sql
CREATE TABLE saved_designs (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FOREIGN KEY,
  design_suggestion_id INTEGER FOREIGN KEY,
  saved_at TIMESTAMP
);
```

## Usage

1. **Register/Login**: Access the login page and create an account as User or Admin
2. **Upload Cloth**: Users can upload cloth images with specifications
3. **View Suggestions**: Get AI-generated design suggestions based on inputs
4. **Save Designs**: Save favorite designs for later reference
5. **Download**: Export designs as PNG or PDF
6. **Admin Dashboard**: View statistics, trends, and user activity

## Future Enhancements

- [ ] Google OAuth integration
- [ ] Image-based AI suggestions using ML models
- [ ] WhatsApp sharing integration
- [ ] Design comparison feature
- [ ] Mobile app
- [ ] Real-time notifications
- [ ] Payment integration for premium features

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
