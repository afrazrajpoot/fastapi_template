# Purposify Backend

A FastAPI backend with PostgreSQL and Prisma ORM.

## Setup

### Prerequisites
- Python 3.12+
- PostgreSQL database

### Installation

1. Create a virtual environment (if not already created):
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your database and environment variables:
   - Create a PostgreSQL database
   - Create a `.env` file in the backend directory with your database URL and JWT secret:
   ```
   DATABASE_URL="postgresql://username:password@localhost:5432/purposify_db?schema=public"
   SECRET_KEY="your-super-secret-jwt-key-change-this-in-production"
   ```

5. Run database migrations:
```bash
prisma db push
```

6. Generate Prisma client (if needed):
```bash
prisma generate
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

## API Endpoints

### Public Endpoints
- `GET /` - Root endpoint with welcome message
- `GET /health` - Health check endpoint
- `GET /db-test` - Database connection test
- `GET /api/v1/hello` - Public hello world endpoint

### Authentication Endpoints
- `POST /api/v1/auth/signin` - Sign in with email, returns JWT token (user must exist in database)
- `GET /api/v1/auth/me` - Get current user info (requires authentication)

### Protected Endpoints (require JWT token)
- `GET /api/v1/hello/protected` - Protected hello world endpoint

### Authentication Headers
For protected endpoints, include the JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## NextAuth Integration

This backend is designed to work seamlessly with NextAuth.js on the client side. The JWT tokens returned from `/api/v1/auth/signin` and `/api/v1/auth/signup` can be used directly with NextAuth's JWT strategy.

### NextAuth Configuration Example
```typescript
// In your NextAuth configuration
providers: [
  CredentialsProvider({
    name: "credentials",
    credentials: {
      email: { label: "Email", type: "email" }
    },
    async authorize(credentials) {
      const res = await fetch(`${process.env.NEXTAUTH_URL}/api/v1/auth/signin`, {
        method: 'POST',
        body: JSON.stringify({ email: credentials?.email }),
        headers: { "Content-Type": "application/json" }
      })

      const user = await res.json()

      if (res.ok && user) {
        return user
      }
      return null
    }
  })
]
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Schema

The application uses a simple User model with:
- `id`: Auto-incrementing primary key
- `email`: Unique email address
- `name`: Optional name field
- `createdAt`: Creation timestamp
- `updatedAt`: Last update timestamp


uvicorn app.main:app --reload --port 8000
running command
