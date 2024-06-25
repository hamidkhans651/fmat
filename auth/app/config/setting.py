from dotenv import find_dotenv, load_dotenv
import os

_ = load_dotenv(find_dotenv())

DATABASE_URL=os.environ.get("DATABASE_URL","postgresql://shoaib:mypassword@postgresCont:5432/mydatabase")
TEST_DATABASE_URL=os.environ.get("TEST_DATABASE_URL","")
JWT_SECRET = os.environ.get("JWT_SECRET",'JWT_SECRET_HERE')
JWT_ALGORITHM  = os.environ.get("JWT_ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES",5)
USER_CONTEXT = os.environ.get("USER_CONTEXT","USER_CONTEXT_VERIFICATION")
BACKEND_HOST = os.environ.get("BACKEND_HOST","http://127.0.0.1:8002")