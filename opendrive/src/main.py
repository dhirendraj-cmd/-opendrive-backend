from fastapi import FastAPI


app = FastAPI()



@app.get("/")
def checkpoint():
    return {
        "msg": "checking open pi drive"
    }
