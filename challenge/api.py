import fastapi
import pandas as pd
from pydantic import BaseModel
from challenge.model import DelayModel

app = fastapi.FastAPI()
model = DelayModel()

class PredictionRequest(BaseModel):
    op: str  # Ajusta según los nombres de las columnas en tu DataFrame
    tipovue: str
    mes: int
    fecha_i: str  # Formato: 'YYYY-MM-DD HH:MM:SS'
    fecha_o: str  # Formato: 'YYYY-MM-DD HH:MM:SS'
    # Agrega más campos según sea necesario

@app.on_event("startup")
async def load_model():
    # Aquí puedes cargar tu modelo si es necesario
    # Por ejemplo, si tienes un método para cargar el modelo:
    # model.load_model("ruta/a/tu/modelo")
    pass

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: PredictionRequest) -> dict:
    # Convertir los datos de entrada a un DataFrame
    input_data = {
        "OPERA": request.op,
        "TIPOVUELO": request.tipovue,
        "MES": request.mes,
        "Fecha-I": request.fecha_i,
        "Fecha-O": request.fecha_o
        # Asegúrate de incluir todos los campos necesarios
    }
    
    # Preprocesar los datos
    features_df = pd.DataFrame([input_data])
    
    # Realizar la predicción
    predictions = model.predict(features_df)

    return {"predictions": predictions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

