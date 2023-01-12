import logging
from connectors.binance_futures import BinanceFuturesClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio
from strategies import TechnicalStrategy, BreakoutStrategy
import typing
from fastapi.middleware.cors import CORSMiddleware
from strategies import TechnicalStrategy, BreakoutStrategy

class User(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_DETAILS = "mongodb+srv://developer89:Juww-sjwo-wlsw@cluster0.nw4tgmg.mongodb.net/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

db = client["test"]
collection = db.get_collection("users")

print("check down")
print(collection)

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
#
# stream_handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(logging.INFO)
#
# file_handler = logging.FileHandler('info.log')
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.DEBUG)
#
# logger.addHandler(stream_handler)
# logger.addHandler(file_handler)

@app.get("/websocketconnect")
async def root():
    BinanceFuturesClient("b060e27bd61e4942d4990fba88802cc4c4e803d2f23af9f10addef377411beb5",
                                   "0a1cfe7bffd303a2828b8a655f029a9526a0ed8f25c323db8e0302c3584ea805", True)
    return "Websocket connected success"


@app.get("/getcontract")
async def root():
    binance = BinanceFuturesClient("b060e27bd61e4942d4990fba88802cc4c4e803d2f23af9f10addef377411beb5",
                                   "0a1cfe7bffd303a2828b8a655f029a9526a0ed8f25c323db8e0302c3584ea805", True)
    return binance.get_contracts()

@app.get("/getbalance")
async def root():
    binance = BinanceFuturesClient("b060e27bd61e4942d4990fba88802cc4c4e803d2f23af9f10addef377411beb5",
                                   "0a1cfe7bffd303a2828b8a655f029a9526a0ed8f25c323db8e0302c3584ea805", True)
    return binance.get_balances()

@app.post("/register")
async def register(userdata: User):
    user = await db.users.find_one({"email": userdata.email})
    print(user)
    if user:
       return HTTPException(status_code=400, detail="Email already exists")
    else:
      db.users.insert_one({"email": userdata.email, "password": userdata.password, "name": userdata.name})
      return {"status": "success", "message": "registration successful"}

@app.post("/login")
async def login(loginuser: UserLogin):
    user = await db.users.find_one({"email":loginuser.email})
    print(user)
    if user:
        return {"message": "Welcome back, {}!"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

# @app.post("/breakoutstrategy")
# async def executestrat():
#     strategies: typing.Dict[int, typing.Union[TechnicalStrategy]] = dict()
#
#     BreakoutStrategy(client: str , Contract, exchange: str, timeframe: str, balance_pct: float, take_profit: float,
#                  stop_loss: float, other_params: Dict)
#     return "breakout strategy run"