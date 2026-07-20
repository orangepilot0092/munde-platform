from fastapi import APIRouter, HTTPException, Request
from src.core.connectors.open_meteo import OpenMeteoConnector
from src.core.connectors.mock_reservoir import MockReservoirConnector
from src.core.connectors.imd_connector import IMDWeatherConnector
from src.core.connectors.data_gov_connector import DataGovInConnector
from src.core.connectors.osm_connector import OSMOverpassConnector
from src.core.connectors.gr_maharashtra_connector import GRMaharashtraConnector
from src.core.limiter import limiter

router = APIRouter(prefix="/connectors", tags=["Data Connectors"])

# Unified handler: all connectors now use LiveConnectorBase.fetch()
CONNECTORS = {
    "open_meteo_pune": lambda r: OpenMeteoConnector().fetch(),
    "mock_reservoirs": lambda r: MockReservoirConnector().fetch(),
    "imd_weather": lambda r: IMDWeatherConnector().fetch(
        district=r.query_params.get("district", "Pune")
    ),
    "data_gov_in": lambda r: DataGovInConnector().fetch(
        resource_id=r.query_params.get(
            "resource_id", "8b68ae56-84cf-4728-a0a6-1be11028dea7"
        ),
        limit=int(r.query_params.get("limit", 10)),
    ),
    "osm_overpass": lambda r: OSMOverpassConnector().fetch(
        query_type=r.query_params.get("type", "hospitals")
    ),
    "gr_maharashtra": lambda r: GRMaharashtraConnector().fetch(
        department=r.query_params.get("department"),
        limit=int(r.query_params.get("limit", 10)),
    ),
}


@router.post("/run/{connector_id}")
@limiter.limit("3/minute")
def run_connector(request: Request, connector_id: str):
    handler = CONNECTORS.get(connector_id)
    if not handler:
        raise HTTPException(
            status_code=404,
            detail=f"Connector '{connector_id}' not found. Available: {list(CONNECTORS.keys())}",
        )
    return handler(request)
