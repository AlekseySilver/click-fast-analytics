from pydantic import BaseModel, Field
from typing import List, Any

class ClickHouseModel(BaseModel):
	action: str = Field(
		...,
		description="The action type to perform. Currently supported: 'select'.",
		examples=["select"]
	)
	query: str | None = Field(
		default=None,
		description="The SQL query to execute. Required when action is 'select'.",
		examples=["SELECT count(*) FROM nyc_taxi"]
	)
	table: str | None = Field(
		default=None,
		description="The target ClickHouse table name for operations.",
		examples=["nyc_taxi"]
	)
	columns: List[str] | None = Field(
		default=None,
		description="List of column names for query mapping or schemas.",
		examples=[["trip_id", "pickup_datetime"]]
	)
	data: List[Any] | None = Field(
		default=None,
		description="Nested array of data rows, e.g. for batch inserts.",
		examples=[[[1, "value"]]]
	)

	model_config = {
		"json_schema_extra": {
			"example": {
				"action": "select",
				"query": "SELECT count(*) FROM nyc_taxi"
			}
		}
	}


class AxisModel(BaseModel):
	name: str = Field(
		...,
		description="Technical database column name representing the axis.",
		examples=["pickup_datetime"]
	)
	title: str = Field(
		...,
		description="Display title for dashboard representation.",
		examples=["pickup datetime"]
	)
	type: str = Field(
		...,
		description="Data type of the axis (e.g., number, datetime, string).",
		examples=["datetime"]
	)

	model_config = {
		"json_schema_extra": {
			"example": {
				"name": "pickup_datetime",
				"title": "pickup datetime",
				"type": "datetime"
			}
		}
	}


class MeasureModel(BaseModel):
	name: str = Field(
		...,
		description="Technical database column name representing the metric to aggregate.",
		examples=["trip_distance"]
	)
	title: str = Field(
		...,
		description="Display title for dashboard representation.",
		examples=["distance"]
	)
	agg: str = Field(
		...,
		description="Aggregation function to apply (e.g. sum, count, avg).",
		examples=["sum"]
	)

	model_config = {
		"json_schema_extra": {
			"example": {
				"name": "trip_distance",
				"title": "distance",
				"agg": "sum"
			}
		}
	}


class CubeQueryModel(BaseModel):
	rows: List[str] = Field(
		default=[],
		description="List of axis (dimension) names to group by.",
		examples=[["payment_type", "passenger_count"]]
	)
	aggs: List[str] = Field(
		default=[],
		description="List of measure (metric) names to aggregate.",
		examples=[["trip_id", "fare_amount"]]
	)

	model_config = {
		"json_schema_extra": {
			"example": {
				"rows": ["payment_type"],
				"aggs": ["trip_id", "fare_amount"]
			}
		}
	}


