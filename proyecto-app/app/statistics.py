from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database import SessionLocal
from models import TopProduct, TopCTR

def get_stats(advertiser_id: str):
    session = SessionLocal()
    try:
        # Consulta para obtener el número de impresiones del modelo TopProduct
        impressions = session.query(TopProduct).filter_by(advertiser_id=advertiser_id).count()

        # Consulta para obtener el número de clics del modelo TopCTR
        clicks = session.query(func.sum(TopCTR.ctr)).filter_by(advertiser_id=advertiser_id).scalar()

        # Consulta para obtener la cantidad de advertisers
        num_advertisers = session.query(func.count(TopProduct.advertiser_id.distinct())).scalar()

        # Crear un diccionario con los datos obtenidos
        stats = {
            'advertiser_id': advertiser_id,
            'impressions': impressions,
            'clicks': clicks,
            'num_advertisers': num_advertisers
        }
        return stats
    finally:
        session.close()
