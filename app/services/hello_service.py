class HelloService:
    async def get_hello_message(self) -> dict:
        """Return hello world message"""
        return {"message": "Hello World from Purposify API!"}
