from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from dataclasses import dataclass
from dataclasses import asdict
from database import get_db_connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from models import TopProduct, TopCTR
from statistics import get_stats


app = FastAPI()

@app.get("/recommendations/{adv}/{modelo}")
def get_recommendations(adv: str, modelo: str, start_date: datetime = None, end_date: datetime = None):
    try:
        # Obtener una conexión a la base de datos
        with get_db_connection() as db:
            if modelo == "TopCTR":
                query = db.query(TopCTR).filter(TopCTR.advertiser_id == adv)
            elif modelo == "TopProduct":
                query = db.query(TopProduct).filter(TopProduct.advertiser_id == adv)
            else:
                raise HTTPException(status_code=400, detail="Invalid model")

            if start_date and end_date:
                if modelo == "TopCTR":
                    query = query.filter(TopCTR.date.between(start_date, end_date))
                elif modelo == "TopProduct":
                    query = query.filter(TopProduct.date.between(start_date, end_date))
            elif start_date:
                if modelo == "TopCTR":
                    query = query.filter(TopCTR.date >= start_date)
                elif modelo == "TopProduct":
                    query = query.filter(TopProduct.date >= start_date)
            elif end_date:
                if modelo == "TopCTR":
                    query = query.filter(TopCTR.date <= end_date)
                elif modelo == "TopProduct":
                    query = query.filter(TopProduct.date <= end_date)

            recommendations = query.limit(20).all()

            if not recommendations:
                raise HTTPException(status_code=404, detail="No recommendations found")

            return recommendations

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/stats/")
async def get_stats_route(advertiser_id: str):
    # Llamamos a la función get_stats para obtener las estadísticas basadas en el advertiser_id
    stats = get_stats(advertiser_id)
    return stats

@app.get("/history/{adv}")
def get_history(adv: str):
    try:
        seven_days_ago = datetime.now() - timedelta(days=7)

        with get_db_connection() as db:
            top_product_recommendations = db.query(TopProduct).filter(TopProduct.advertiser_id == adv, TopProduct.date >= seven_days_ago).all()
            top_ctr_recommendations = db.query(TopCTR).filter(TopCTR.advertiser_id == adv, TopCTR.date >= seven_days_ago).all()

            recommendations = top_product_recommendations + top_ctr_recommendations

            if not recommendations:
                raise HTTPException(status_code=404, detail="No recommendations found")

            return recommendations
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
