# examples/main.py
# https://github.com/deepmancer/fastapi-auth-jwt/

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="127.0.0.1", log_level="info")
