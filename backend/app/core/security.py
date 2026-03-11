from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Use sha256_crypt instead of bcrypt for Python 3.14 compatibility
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Compare plain password with hashed password during login
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Encrypt password before saving to database during registration
def get_password_hash(password):
    return pwd_context.hash(password)

# Create JWT token after successful login
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Verify JWT token on every protected API request
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None