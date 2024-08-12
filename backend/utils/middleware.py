from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Hoặc ["*"] để cho phép tất cả các nguồn
        allow_credentials=True,
        allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, ...)
        allow_headers=["*"],  # Cho phép tất cả các headers
    )
