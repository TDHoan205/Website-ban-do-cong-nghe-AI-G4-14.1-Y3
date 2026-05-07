import httpx
import asyncio

async def test_app():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        tests = [
            "/",
            "/Products/",
            "/Cart/",
            "/Auth/Login",
            "/Auth/Register",
        ]
        
        for url in tests:
            try:
                response = await client.get(url, follow_redirects=True)
                print(f"[{response.status_code}] GET {url}")
                if response.status_code >= 400:
                    print(f"ERROR on {url}: {response.text[:200]}")
            except Exception as e:
                print(f"FAILED GET {url}: {e}")

if __name__ == "__main__":
    asyncio.run(test_app())
