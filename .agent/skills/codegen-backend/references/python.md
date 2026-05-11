# Python Backend Reference (FastAPI / Django)

## FastAPI — idiomatic patterns

### Project structure

```
src/
├── main.py                  # App entry point
├── routers/
│   └── users.py             # Route definitions
├── services/
│   └── user_service.py      # Business logic
├── repositories/
│   └── user_repository.py   # DB access
├── schemas/
│   └── user.py              # Pydantic models
├── models/
│   └── user.py              # SQLAlchemy ORM models
├── dependencies.py          # Dependency injection
└── database.py              # DB session setup
```

### Pydantic schemas

```python
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}  # Pydantic v2
```

### Async route with dependency injection

```python
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        return await service.create_user(body)
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Email already registered")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### SQLAlchemy async session

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Repository pattern

```python
from sqlalchemy import select
from uuid import UUID

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        self.db.add(user)
        await self.db.flush()  # get the ID without committing
        await self.db.refresh(user)
        return user
```

### Testing

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, db_session):
    response = await client.post("/users/", json={
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data
```

## Django — idiomatic patterns

### Views with DRF

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

### Serializers

```python
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
```

## Package management

- Use `poetry` or `uv` for dependency management
- FastAPI apps: `uvicorn[standard]` as ASGI server
- Async DB: `asyncpg` (Postgres), `aiomysql` (MySQL)
- ORM: `SQLAlchemy[asyncio]` with `alembic` for migrations
