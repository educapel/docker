from typing import Union
import pandas as pd
from fastapi import FastAPI, HTTPException
import uvicorn
import joblib
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel




class LoanPredictionInput(BaseModel):
    limit_bal: float
    sex: int
    education: int
    marriage: int
    age: int
    pay_0: int
    pay_2: int
    pay_3: int
    pay_4: int
    pay_5: int
    pay_6: int
    bill_amt1: float
    bill_amt2: float
    bill_amt3: float
    bill_amt4: float
    bill_amt5: float
    bill_amt6: float
    pay_amt1: float
    pay_amt2: float
    pay_amt3: float
    pay_amt4: float
    pay_amt5: float
    pay_amt6: float

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, for development only
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

model = joblib.load("app/default.pkl")

@app.get("/")
async def root():
    return {"message": "Hello, use /predict_loan_default for predicting loan defaults"}

@app.post("/predict_loan_default")
async def predict_loan_default(input_data: LoanPredictionInput):
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data.dict()])
        
        for column in input_df.columns:
            input_df[column] = pd.to_numeric(input_df[column])

        input_df.columns = [column.upper() for column in input_df.columns]

        # Assuming the columns are ordered correctly as per the model's expectation
        prediction = model.predict(input_df)

        # Returning a meaningful response based on the prediction
        if prediction[0] == 1:
            return {"prediction": "Loan will likely default"}
        else:
            return {"prediction": "Loan will likely not default"}
    except Exception as e:
        # Handle any errors that occur during the prediction
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)