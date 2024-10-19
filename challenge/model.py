import pandas as pd
import numpy as np
from typing import Tuple, Union, List
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import xgboost as xgb

class DelayModel:

    def __init__(self):
        self._model = None  # El modelo se guardará en este atributo.
        self.features = None
        self.target = None
        self.scale = None  # Para el balanceo de clases

    def load_data(self, filepath: str) -> pd.DataFrame:
        """Cargar datos desde un archivo CSV."""
        return pd.read_csv(filepath)

    def preprocess(self, data: pd.DataFrame, target_column: str = 'delay') -> Union[Tuple[pd.DataFrame, pd.Series], pd.DataFrame]:
        """Preparar datos en bruto para el entrenamiento o la predicción."""
        data['period_day'] = data['Fecha-I'].apply(self.get_period_day)
        data['high_season'] = data['Fecha-I'].apply(self.is_high_season)
        data['min_diff'] = data.apply(self.get_min_diff, axis=1)
        
        threshold_in_minutes = 15
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)

        # Establecer características y objetivo
        self.features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES'),
            data[['high_season', 'period_day']]
        ], axis=1)

        self.target = data[target_column]

        return self.features, self.target

    def fit(self, features: pd.DataFrame, target: pd.Series) -> None:
        """Ajustar el modelo con datos preprocesados."""
        self.scale = len(target[target == 0]) / len(target[target == 1])  # Balanceo de clases
        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)

        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=self.scale)
        self._model.fit(x_train, y_train)

        # Imprimir informe de clasificación para el conjunto de prueba
        y_preds = self._model.predict(x_test)
        print(classification_report(y_test, y_preds))

    def predict(self, features: pd.DataFrame) -> List[int]:
        """Predecir retrasos para nuevos vuelos."""
        if self._model is None:
            raise Exception("¡El modelo no ha sido entrenado aún!")
        return self._model.predict(features).tolist()

    def get_period_day(self, date: str) -> str:
        date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        morning_min = datetime.strptime("05:00", '%H:%M').time()
        morning_max = datetime.strptime("11:59", '%H:%M').time()
        afternoon_min = datetime.strptime("12:00", '%H:%M').time()
        afternoon_max = datetime.strptime("18:59", '%H:%M').time()
        evening_min = datetime.strptime("19:00", '%H:%M').time()
        evening_max = datetime.strptime("23:59", '%H:%M').time()
        night_min = datetime.strptime("00:00", '%H:%M').time()
        night_max = datetime.strptime("4:59", '%H:%M').time()

        if morning_min < date_time < morning_max:
            return 'mañana'
        elif afternoon_min <= date_time < afternoon_max:
            return 'tarde'
        elif (evening_min <= date_time < evening_max) or (night_min <= date_time < night_max):
            return 'noche'

    def is_high_season(self, fecha: str) -> int:
        fecha_año = int(fecha.split('-')[0])
        fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        ranges = [
            (datetime.strptime('15-Dec', '%d-%b').replace(year=fecha_año), datetime.strptime('31-Dec', '%d-%b').replace(year=fecha_año)),
            (datetime.strptime('1-Jan', '%d-%b').replace(year=fecha_año), datetime.strptime('3-Mar', '%d-%b').replace(year=fecha_año)),
            (datetime.strptime('15-Jul', '%d-%b').replace(year=fecha_año), datetime.strptime('31-Jul', '%d-%b').replace(year=fecha_año)),
            (datetime.strptime('11-Sep', '%d-%b').replace(year=fecha_año), datetime.strptime('30-Sep', '%d-%b').replace(year=fecha_año))
        ]

        for start, end in ranges:
            if start <= fecha <= end:
                return 1
        return 0

    def get_min_diff(self, row) -> float:
        fecha_o = datetime.strptime(row['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(row['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        return (fecha_o - fecha_i).total_seconds() / 60

