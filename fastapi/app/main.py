from fastapi import FastAPI, Body, Path as FastAPIPath, Query, HTTPException
from contextlib import asynccontextmanager
from clickhouse import CH
from scheme import ClickHouseModel, AxisModel, MeasureModel, CubeQueryModel
from json import loads
from datetime import datetime
from pathlib import Path
from typing import Any

ch = CH()

@asynccontextmanager
async def lifespan(app: FastAPI):
	ch.connect()
	yield
	ch.close()

app = FastAPI(
	lifespan=lifespan,
	title="Click Fast Analytics API",
	description="""
# ⚡ Click Fast Analytics API

Use the interactive Swagger UI below to test queries in real time.
""",
	version="1.0.0"
)


@app.get("/", tags=["System"], summary="Read API Root / Heartbeat")
def read_root():
	"""
	Check the API status and obtain a basic welcome message confirming the service is online.
	"""
	return {"message": "Hello, Docker with FastAPI!"}


@app.get("/cubes", tags=["Cubes"], summary="List Analytical Cubes", response_model=list[dict[str, str]])
def list_cubes():
	"""
	Retrieve a list of all analytical cubes available on the server with their names and titles.
	
	Cubes define multi-dimensional schemas mapping ClickHouse columns to axises (dimensions) and measures (metrics).
	"""
	# Try local sibling cube directory (Docker layout) first, then fallback to parent-level sibling (local environment layout)
	cube_dir = Path(__file__).resolve().parent / "cube"
	if not cube_dir.exists():
		cube_dir = Path(__file__).resolve().parent.parent / "cube"
	
	if not cube_dir.exists():
		return []
	
	cubes = []
	for f in cube_dir.iterdir():
		if f.is_file() and f.suffix == ".json":
			try:
				with open(f, "r", encoding="utf-8") as file:
					cube_data = loads(file.read())
				cubes.append({
					"name": f.stem,
					"title": cube_data.get("title", f.stem)
				})
			except Exception:
				# Graceful fallback in case of JSON parse errors
				cubes.append({
					"name": f.stem,
					"title": f.stem
				})
	return cubes



@app.post("/clickhouse", tags=["Analytics & Queries"], summary="Execute ClickHouse Query", response_model=Any)
def clickhouse_query(query: ClickHouseModel):
	data = query.model_dump(exclude_unset=True) if hasattr(query, "model_dump") else query.dict(exclude_unset=True)
	return ch.query(data)


@app.get("/get_cube_axises", tags=["Cubes"], summary="Get Cube Axises", response_model=list[AxisModel])
def get_cube_axises(
	cube_name: str = Query(..., description="The name of the cube (without file extension)", example="nyc_taxi")
):
	"""
	Retrieve the list of all defined axises (dimensions) for a specific analytical cube.
	
	Axises define structural properties by which data can be grouped or filtered, mapping database columns to dimensions.
	"""
	# Try local sibling cube directory (Docker layout) first, then fallback to parent-level sibling (local environment layout)
	cube_dir = Path(__file__).resolve().parent / "cube"
	if not cube_dir.exists():
		cube_dir = Path(__file__).resolve().parent.parent / "cube"
		
	cube_file = cube_dir / f"{cube_name}.json"
	if not cube_file.exists():
		raise HTTPException(status_code=404, detail=f"Cube '{cube_name}' not found")
		
	try:
		with open(cube_file, "r", encoding="utf-8") as file:
			cube_data = loads(file.read())
		return cube_data.get("axises", [])
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to read cube metadata: {str(e)}")


@app.get("/get_cube_measures", tags=["Cubes"], summary="Get Cube Measures", response_model=list[MeasureModel])
def get_cube_measures(
	cube_name: str = Query(..., description="The name of the cube (without file extension)", example="nyc_taxi")
):
	"""
	Retrieve the list of all defined measures (metrics) for a specific analytical cube.
	
	Measures define numeric metrics that can be aggregated, such as sums, counts, and averages.
	"""
	# Try local sibling cube directory (Docker layout) first, then fallback to parent-level sibling (local environment layout)
	cube_dir = Path(__file__).resolve().parent / "cube"
	if not cube_dir.exists():
		cube_dir = Path(__file__).resolve().parent.parent / "cube"
		
	cube_file = cube_dir / f"{cube_name}.json"
	if not cube_file.exists():
		raise HTTPException(status_code=404, detail=f"Cube '{cube_name}' not found")
		
	try:
		with open(cube_file, "r", encoding="utf-8") as file:
			cube_data = loads(file.read())
		return cube_data.get("measures", [])
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to read cube metadata: {str(e)}")


@app.post("/cubes/{cube_name}/query", tags=["Cubes"], summary="Query Cube Data", response_model=Any)
def query_cube(
	query: CubeQueryModel,
	cube_name: str = FastAPIPath(..., description="The name of the cube (without file extension)", example="nyc_taxi")
):
	"""
	Execute a dynamic OLAP analytical query against a specific cube definition.
	
	Generates a dynamic SQL SELECT-GROUP-BY query in ClickHouse based on the requested axes (`rows`) and measures (`aggs`).
	"""
	# Try local sibling cube directory (Docker layout) first, then fallback to parent-level sibling (local environment layout)
	cube_dir = Path(__file__).resolve().parent / "cube"
	if not cube_dir.exists():
		cube_dir = Path(__file__).resolve().parent.parent / "cube"
		
	cube_file = cube_dir / f"{cube_name}.json"
	if not cube_file.exists():
		raise HTTPException(status_code=404, detail=f"Cube '{cube_name}' not found")
		
	try:
		with open(cube_file, "r", encoding="utf-8") as file:
			cube_data = loads(file.read())
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to read cube metadata: {str(e)}")
		
	source_table = cube_data.get("source")
	if not source_table:
		raise HTTPException(status_code=400, detail="Cube configuration has no 'source' table defined")
		
	# Map aggs (measures) to ClickHouse expressions
	measures_map = {m["name"]: m for m in cube_data.get("measures", [])}
	
	select_parts = []
	# 1. Add rows (axises) to SELECT
	for r in query.rows:
		select_parts.append(r)
		
	# 2. Add aggs (measures) to SELECT with safe type casting (since NYC Taxi has some string-based measures)
	for a in query.aggs:
		if a in measures_map:
			m = measures_map[a]
			agg_func = m.get("agg", "sum")
			col_name = m.get("name")
			
			if agg_func == "count":
				select_parts.append(f"count({col_name}) AS {col_name}_count")
			else:
				select_parts.append(f"{agg_func}(toFloat64OrZero({col_name})) AS {col_name}_{agg_func}")
		else:
			# If measure is not defined in metadata, fallback to a simple sum with safety cast
			select_parts.append(f"sum(toFloat64OrZero({a})) AS {a}_sum")
			
	if not select_parts:
		raise HTTPException(status_code=400, detail="Query must request at least one row (axis) or agg (measure)")
		
	sql_query = f"SELECT {', '.join(select_parts)} FROM {source_table}"
	
	if query.rows:
		sql_query += f" GROUP BY {', '.join(query.rows)}"
		
	try:
		ch_result = ch.query({"action": "select", "query": sql_query})
		return {
			"query": sql_query,
			"data": ch_result
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Database execution failed: {str(e)}")




