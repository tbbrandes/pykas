from dotenv import load_dotenv

load_dotenv()

NODE_HOST = os.getenv("NODE_HOST", "localhost")
NODE_PORT = os.getenv("NODE_PORT", "16110")
TLS_SECURE = os.getenv("TLS_SECURE", "True").lower()

