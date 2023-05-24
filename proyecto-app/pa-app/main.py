# Importamos las clases y funciones necesarias
from fastapi import FastAPI, HTTPException, APIRouter
from datetime import datetime, timedelta
from database import get_db_connection
from sqlalchemy.exc import SQLAlchemyError
from models import TopProduct, TopCTR
from statistics import get_stats

# Creamos una instancia de la aplicación FastAPI
app = FastAPI()

# Definimos los endpoints de la API según las especificaciones proporcionadas

# Lógica para obtener las recomendaciones del día para el ADV y Modelo especificados
# y devolver la respuesta en formato JSON

@app.get("/recommendations/{adv}/{modelo}")
def get_recommendations(adv: str, modelo: str, start_date: datetime = None, end_date: datetime = None):
    try:
        with get_db_connection() as db:
            if modelo == "TopCTR":
                # Filtrar por modelo TopCTR y anuncio
                query = db.query(TopCTR).filter(TopCTR.advertiser_id == adv)
            elif modelo == "TopProduct":
                # Filtrar por modelo TopProduct y anuncio
                query = db.query(TopProduct).filter(TopProduct.advertiser_id == adv)
            else:
                raise HTTPException(status_code=400, detail="Invalid model")

            # Filtrar por rango de fechas si se proporcionan los parámetros start_date y end_date
            if start_date and end_date:
                if modelo == "TopCTR":
                    query = query.filter(TopCTR.date.between(start_date, end_date))  # Filtrar por rango de fechas
                elif modelo == "TopProduct":
                    query = query.filter(TopProduct.date.between(start_date, end_date))  # Filtrar por rango de fechas
            elif start_date:
                if modelo == "TopCTR":
                    query = query.filter(TopCTR.date >= start_date)  # Filtrar fechas igual o posteriores a start_date
                elif modelo == "TopProduct":
                    query = query.filter(TopProduct.date >= start_date)  # Filtrar fechas igual o posteriores a start_date
            elif end_date:
                if modelo == "TopCTR":
                    query = query.filter(TopCTR.date <= end_date)  # Filtrar fechas igual o anteriores a end_date
                elif modelo == "TopProduct":
                    query = query.filter(TopProduct.date <= end_date)  # Filtrar fechas igual o anteriores a end_date

            # Limitar a un máximo de 20 resultados
            recommendations = query.limit(20).all()
            
            # Si no se encuentran recomendaciones, se lanza una excepción HTTP con el código 404 
            # y el detalle "No recommendations found".
            if not recommendations:
                raise HTTPException(status_code=404, detail="No recommendations found")

            
            return recommendations
    # En caso de producirse un error en la comunicación con la base de datos
    # se lanza una excepción HTTP con el código 500 y el detalle "Database error".
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


# Lógica para obtener las estadísticas sobre las recomendaciones y devolver la respuesta en formato JSON

@app.get("/stats/")
def get_stats(advertiser_id: str):
    stats = get_stats(advertiser_id)
    return stats

#  Lógica para obtener el historial de los ultimos 7 días para un adv específico

@app.get("/history/{adv}")
def get_history(adv: str):
    try:
        # Obtener la fecha de hace 7 días
        seven_days_ago = datetime.now() - timedelta(days=7)

        with get_db_connection() as db:
            # Obtener las recomendaciones de TopProduct y TopCTR para el advertiser especificado en los últimos 7 días
            top_product_recommendations = db.query(TopProduct).filter(TopProduct.advertiser_id == adv, TopProduct.date >= seven_days_ago).all()
            top_ctr_recommendations = db.query(TopCTR).filter(TopCTR.advertiser_id == adv, TopCTR.date >= seven_days_ago).all()

            # Combinar las recomendaciones de ambos modelos en una lista única
            recommendations = top_product_recommendations + top_ctr_recommendations

            # Si no se encuentran recomendaciones, se lanza una excepción HTTP con el código 404 
            # y el detalle "No recommendations found".
            if not recommendations:
                raise HTTPException(status_code=404, detail="No recommendations found")

            return recommendations
    # En caso de producirse un error en la comunicación con la base de datos
    # se lanza una excepción HTTP con el código 500 y el detalle "Database error".
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
