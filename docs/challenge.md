Parte I: Modelado y Pruebas
Desarrollo del modelo de predicción:

Se creó la clase DelayModel en model.py, que se encarga de cargar datos, preprocesar las características, entrenar un modelo y realizar predicciones sobre si un vuelo tendrá retraso.
Se implementaron métodos como:
load_data: para cargar datos desde un archivo CSV.
preprocess: para preparar los datos para el entrenamiento y la predicción.
fit: para entrenar el modelo utilizando XGBoost.
predict: para realizar predicciones sobre nuevos datos.
Métodos auxiliares para obtener características específicas, como get_period_day y is_high_season.
Pruebas unitarias:

Se creó un conjunto de pruebas utilizando unittest en test_model.py para asegurar que el modelo funcione correctamente.
Se implementaron pruebas para verificar la correcta preprocesamiento de datos, el entrenamiento del modelo y las predicciones.
Parte II: API con FastAPI
Creación de la API:

Se implementó una API RESTful utilizando FastAPI en api.py.
Se definieron dos endpoints:
GET /health: para verificar el estado de la API.
POST /predict: para recibir datos sobre un vuelo y devolver una predicción de retraso.
Se utilizó Pydantic para validar y estructurar los datos de entrada.
Integración del modelo en la API:

La API carga el modelo de predicción y utiliza el método predict del DelayModel para generar respuestas basadas en las solicitudes de los usuarios.
Parte III: Despliegue de la API
Despliegue en Google Cloud Platform (GCP):

Se configuró el entorno de GCP y se utilizó Google Cloud Run para desplegar la API.
Se configuraron los archivos Dockerfile y requirements.txt para crear la imagen del contenedor que contiene la API y sus dependencias.
Se solucionaron problemas relacionados con la configuración del contenedor y el puerto definido para asegurar que la API se inicie correctamente.
Verificación del despliegue:

Se probó la API para asegurarse de que respondiera correctamente y fuera accesible a través de la URL proporcionada.
Parte IV: Implementación de CI/CD
Configuración de GitHub Actions:

Se creó un directorio .github en el repositorio para almacenar los flujos de trabajo de CI/CD.
Se copiaron y configuraron los archivos ci.yml y cd.yml para automatizar el proceso de integración y despliegue continuo.
Se definieron los pasos necesarios para construir, probar y desplegar la API automáticamente al hacer push en el repositorio.
Configuración de secretos en GitHub:

Se añadieron los secretos DOCKER_USERNAME y DOCKER_PASSWORD en el repositorio de GitHub para permitir la autenticación en Docker Hub durante los procesos de CI/CD.