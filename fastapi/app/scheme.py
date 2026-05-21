from pydantic import BaseModel, Field
from typing import List, Optional

class ClickHouseModel(BaseModel):
	action: str
	query: str | None = Field(default=None)
	table: str | None = Field(default=None)
	columns: List[str] | None = Field(default=None)
	data: List | None = Field(default=None)

