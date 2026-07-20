from typing import Any
from pydantic import BaseModel, Field
from src.core.connectors.base import BaseConnector


class ReservoirRecord(BaseModel):
    reservoir_name: str
    district: str
    water_level_tmc: float = Field(ge=0)  # Rule: Cannot be negative
    capacity_tmc: float = Field(gt=0)  # Rule: Must be greater than 0


class MockReservoirConnector(BaseConnector):
    def __init__(self):
        super().__init__(
            connector_id="mock_reservoirs", source_url="https://mock.gov.in/reservoirs"
        )
        self.schema = ReservoirRecord  # Attach the Pydantic schema

    def fetch(self, **kwargs) -> Any:
        # Simulating a government API that returns some bad data
        return [
            {
                "reservoir_name": "Ujani",
                "district": "Solapur",
                "water_level_tmc": 80.5,
                "capacity_tmc": 118,
            },
            {
                "reservoir_name": "Koyna",
                "district": "Satara",
                "water_level_tmc": 90.0,
                "capacity_tmc": 105,
            },
            # INVALID: Negative water level
            {
                "reservoir_name": "Bhama Askhed",
                "district": "Pune",
                "water_level_tmc": -5.0,
                "capacity_tmc": 10,
            },
            # INVALID: Missing required 'district' field
            {
                "reservoir_name": "Khadakwasla",
                "water_level_tmc": 20.0,
                "capacity_tmc": 35,
            },
        ]

    def validate(self, data: Any) -> bool:
        return isinstance(data, list)

    def get_transformations(self) -> dict:
        return {"action": "mock_reservoir_fetch", "format": "json"}
