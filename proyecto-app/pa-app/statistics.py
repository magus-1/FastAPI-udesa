from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database import SessionLocal
from models import TopProduct, TopCTR, Stats

def get_stats(advertiser_id: str):
    session = SessionLocal()
    try:
        # Consulta para obtener el número de impresiones del modelo TopProduct
        impressions = session.query(TopProduct).filter_by(advertiser_id=advertiser_id).count()

        # Consulta para obtener el número de clics del modelo TopCTR
        clicks = session.query(TopCTR).filter_by(advertiser_id=advertiser_id).sum(TopCTR.ctr)

        # Consulta para obtener la cantidad de advertisers
        num_advertisers = session.query(func.count(TopProduct.advertiser_id.distinct())).scalar()

        # Consulta para obtener los advertisers que más varían sus recomendaciones por día
        varying_advertisers = session.query(TopProduct.advertiser_id, func.count(TopProduct.date)).group_by(TopProduct.advertiser_id).order_by(func.count(TopProduct.date).desc()).all()

        # Consulta para obtener las estadísticas de coincidencia entre ambos modelos para los diferentes advertisers
        matching_stats = session.query(TopProduct.advertiser_id, func.count().label('matching_count')).join(TopCTR, TopProduct.advertiser_id == TopCTR.advertiser_id).filter(TopProduct.product_id == TopCTR.product_id).group_by(TopProduct.advertiser_id).all()

        # Crear una instancia de Stats con los datos obtenidos
        stats = Stats(advertiser_id=advertiser_id, impressions=impressions, clicks=clicks, num_advertisers=num_advertisers, varying_advertisers=varying_advertisers, matching_stats=matching_stats)
        return stats
    finally:
        session.close()
