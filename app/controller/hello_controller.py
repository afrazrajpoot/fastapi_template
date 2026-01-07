from fastapi import Request, Response
from app.services.hello_service import HelloService

class HelloController:
    def __init__(self):
        self.hello_service = HelloService()

    async def get_hello(self, request: Request) -> dict:
        """Handle hello world request"""
        return await self.hello_service.get_hello_message()
