from app.repositories.base import BaseRepository
from app.models.threat_indicator import ThreatIndicator
from app.schemas.security import ThreatIndicatorCreate, ThreatIndicatorUpdate


class ThreatIndicatorRepository(BaseRepository[ThreatIndicator, ThreatIndicatorCreate, ThreatIndicatorUpdate]):
    pass


threat_indicator_repository = ThreatIndicatorRepository(ThreatIndicator)
