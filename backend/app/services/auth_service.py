from app.models.user import User, UserRole
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.user import UserCreate, UserUpdate
from datetime import timedelta
from app.core.config import get_settings
from app.core.database import get_db_cursor

settings = get_settings()


class AuthService:
    """Authentication service"""
    
    @staticmethod
    def register_user(conn, user: UserCreate, role: UserRole = UserRole.USER) -> User:
        """Register a new user"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            # Check if user already exists
            cursor.execute(
                "SELECT id FROM users WHERE email = %s OR username = %s",
                (user.email, user.username)
            )
            existing_user = cursor.fetchone()
            
            if existing_user:
                raise ValueError("User already exists")
            
            # Create new user
            hashed_password = get_password_hash(user.password)
            cursor.execute(
                """INSERT INTO users (email, username, hashed_password, full_name, role)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id, email, username, hashed_password, role, full_name, is_active, created_at, updated_at""",
                (user.email, user.username, hashed_password, user.full_name, role.value)
            )
            result = cursor.fetchone()
            
            if result:
                return User(
                    id=result['id'],
                    email=result['email'],
                    username=result['username'],
                    hashed_password=result['hashed_password'],
                    role=result['role'],
                    full_name=result['full_name'],
                    is_active=result['is_active'],
                    created_at=result['created_at'],
                    updated_at=result['updated_at']
                )
            raise ValueError("Failed to create user")
    
    @staticmethod
    def authenticate_user(conn, email: str, password: str) -> User:
        """Authenticate user"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                "SELECT id, email, username, hashed_password, role, full_name, is_active, created_at, updated_at FROM users WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()
        
        if not result:
            return None
        
        user = User(
            id=result['id'],
            email=result['email'],
            username=result['username'],
            hashed_password=result['hashed_password'],
            role=result['role'],
            full_name=result['full_name'],
            is_active=result['is_active'],
            created_at=result['created_at'],
            updated_at=result['updated_at']
        )
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    @staticmethod
    def get_user_by_email(conn, email: str) -> User:
        """Get user by email"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                "SELECT id, email, username, hashed_password, role, full_name, is_active, created_at, updated_at FROM users WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()
        
        if result:
            return User(
                id=result['id'],
                email=result['email'],
                username=result['username'],
                hashed_password=result['hashed_password'],
                role=result['role'],
                full_name=result['full_name'],
                is_active=result['is_active'],
                created_at=result['created_at'],
                updated_at=result['updated_at']
            )
        return None
    
    @staticmethod
    def get_user_by_id(conn, user_id: int) -> User:
        """Get user by ID"""
        from app.core.database import get_db_cursor
        
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                "SELECT id, email, username, hashed_password, role, full_name, is_active, created_at, updated_at FROM users WHERE id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
        
        if result:
            return User(
                id=result['id'],
                email=result['email'],
                username=result['username'],
                hashed_password=result['hashed_password'],
                role=result['role'],
                full_name=result['full_name'],
                is_active=result['is_active'],
                created_at=result['created_at'],
                updated_at=result['updated_at']
            )
        return None
    
    @staticmethod
    def create_access_token_for_user(user: User) -> str:
        """Create access token for user"""
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        return access_token
    
    @staticmethod
    def update_user(conn, user: User, user_update: UserUpdate) -> User:
        """Update user"""
        from app.core.database import get_db_cursor
        
        updates = {}
        if user_update.full_name:
            updates['full_name'] = user_update.full_name
            user.full_name = user_update.full_name
        
        if user_update.password:
            updates['hashed_password'] = get_password_hash(user_update.password)
            user.hashed_password = updates['hashed_password']
        
        if updates:
            set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
            values = list(updates.values()) + [user.id]
            
            with get_db_cursor(conn) as cursor:
                cursor.execute(
                    f"UPDATE users SET {set_clause}, updated_at = NOW() WHERE id = %s",
                    values
                )
        
        return user
