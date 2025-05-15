from app.repositories.base import BaseRepository
from app.models.uba_login_anomaly import UBALoginAnomalyAlert
from app.schemas.uba import UBALoginAnomalyAlertCreate, UBALoginAnomalyAlertUpdate


class UBALoginAnomalyRepository(BaseRepository[UBALoginAnomalyAlert, UBALoginAnomalyAlertCreate, UBALoginAnomalyAlertUpdate]):
    pass


uba_login_anomaly_repository = UBALoginAnomalyRepository(UBALoginAnomalyAlert)
