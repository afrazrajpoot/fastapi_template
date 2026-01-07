from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
import os
from dotenv import load_dotenv
from app.routes.routes import router as api_router
from app.routes.auth_routes import router as auth_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Purposify API",
    description="Backend API for Purposify application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1", tags=["API"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])

# Global Prisma client
prisma = Prisma()

@app.on_event("startup")
async def startup():
    """Initialize database connection on startup"""
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown"""
    await prisma.disconnect()

@app.get("/")
async def root():
    """Hello World endpoint"""
    return {"message": "Hello World! Welcome to Purposify API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "purposify-backend"}

@app.get("/db-test")
async def database_test():
    """Test database connection"""
    try:
        # Test database connection by counting users
        user_count = await prisma.user.count()
        return {
            "message": "Database connection successful",
            "user_count": user_count
        }
    except Exception as e:
        return {
            "message": "Database connection failed",
            "error": str(e)
        }
