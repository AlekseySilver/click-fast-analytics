# ⚡ Click Fast Analytics API Reference Manual

Welcome to the **Click Fast Analytics API Documentation**. This service exposes high-performance analytical endpoints that sit directly in front of a **ClickHouse** columnar database to serve fast multidimensional analytical queries (OLAP) and list pre-configured analytics cubes.

---

## 🏗️ Architecture & Request Flow

The following diagram illustrates the lifecycle of a query submitted to the FastAPI analytical layer, dynamic dispatching, execution on ClickHouse, and results serialization back to the client:

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client / Dashboard
    participant API as FastAPI Service
    participant Engine as ClickHouse Connector (CH)
    database DB as ClickHouse Server

    Client->>API: POST /clickhouse (JSON Payload)
    Note over API: Parses & validates body<br/>against ClickHouseModel
    API->>Engine: ch.query(validated_data)
    Note over Engine: Resolves action method<br/>e.g., q___select()
    Engine->>DB: Executes SQL string
    DB-->>Engine: Returns raw tuple rows
    Engine-->>API: Returns list of rows
    API-->>Client: 200 OK (JSON response data)
```

---

## 🚀 Running & Accessing Interactive Docs

When running the application locally via docker compose or directly, two auto-generated interactive documentation portals are available:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) (Interactive endpoint testing)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) (Clean, structured reference layout)

---

## 🏷️ API Endpoint Directory

| Method | Path | Summary | Tags |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Heartbeat / Health Check | `System` |
| `GET` | `/cubes` | Retrieve Analytics Cube List | `Cubes` |
| `GET` | `/get_cube_axises` | Retrieve Axises for a Specific Cube | `Cubes` |
| `GET` | `/get_cube_measures` | Retrieve Measures for a Specific Cube | `Cubes` |
| `GET` | `/items/{item_id}` | Retrieve Item Info (Placeholder) | `System` |
| `POST` | `/clickhouse` | Execute ClickHouse Analytical Queries | `Analytics & Queries` |
| `POST` | `/cubes/{cube_name}/query` | Query Dynamic OLAP Cube Data | `Cubes` |

---

## 📡 Endpoint Details & Examples

### 1. API Heartbeat / Root
* **Endpoint:** `GET /`
* **Tags:** `System`
* **Description:** Quick health check to verify if the FastAPI server is running and accessible.

#### Curl Example
```bash
curl -X GET http://localhost:8000/
```

#### Successful Response (200 OK)
```json
{
  "message": "Hello, Docker with FastAPI!"
}
```

---

### 2. List Analytical Cubes
* **Endpoint:** `GET /cubes`
* **Tags:** `Cubes`
* **Description:** Returns a list of available analytical cube names and their titles (excluding file extensions) defined under the `./fastapi/cube` directory.

#### Curl Example
```bash
curl -X GET http://localhost:8000/cubes
```

#### Successful Response (200 OK)
```json
[
  {
    "name": "nyc_taxi",
    "title": "nyc taxi"
  }
]
```

---

### 3. Get Item Details (Placeholder)
* **Endpoint:** `GET /items/{item_id}`
* **Tags:** `System`
* **Description:** Retrieve details for a specific item ID.

#### Parameters
* **Path Parameters:**
  * `item_id` (integer, Required): Unique ID of the item. Example: `42`
* **Query Parameters:**
  * `q` (string, Optional): Query string modifier. Example: `fast-olap`

#### Curl Example
```bash
curl -X GET "http://localhost:8000/items/42?q=fast-olap"
```

#### Successful Response (200 OK)
```json
{
  "item_id": 42,
  "q": "fast-olap"
}
```

---

### 4. Execute ClickHouse Analytical Query
* **Endpoint:** `POST /clickhouse`
* **Tags:** `Analytics & Queries`
* **Description:** Executes structured database operations in ClickHouse. The request body is validated against the schema defined below.

#### Request Schema (`ClickHouseModel`)
| Property | Type | Description | Required | Example |
| :--- | :--- | :--- | :--- | :--- |
| `action` | `string` | The command to dispatch. Currently supports: `select`. | **Yes** | `"select"` |
| `query` | `string` | SQL Query to execute. Required for `select`. | No | `"SELECT count(*) FROM nyc_taxi"` |
| `table` | `string` | Target Table name. | No | `"nyc_taxi"` |
| `columns` | `array[string]` | Array of targeted column names. | No | `["trip_id", "pickup_datetime"]` |
| `data` | `array[any]` | Multi-dimensional array of data rows (for future batch inserts). | No | `[[1001, "2026-05-23T11:16:30"]]` |

#### Curl Example (Executing a Select query)
```bash
curl -X POST http://localhost:8000/clickhouse \
     -H "Content-Type: application/json" \
     -d '{
       "action": "select",
       "query": "SELECT count(*), avg(passenger_count) FROM nyc_taxi"
     }'
```

#### Successful Response (200 OK)
```json
[
  [25000, 1.68]
]
```

#### Error Response (200 OK - Backend Exception / Parameter mismatch)
```json
{
  "error": "unknown command"
}
```

---

### 5. Get Cube Axises
* **Endpoint:** `GET /get_cube_axises`
* **Tags:** `Cubes`
* **Description:** Retrieve the list of all defined axises (dimensions) for a specific analytical cube.

#### Parameters
* **Query Parameters:**
  * `cube_name` (string, Required): The name of the cube (without file extension). Example: `"nyc_taxi"`

#### Curl Example
```bash
curl -X GET "http://localhost:8000/get_cube_axises?cube_name=nyc_taxi"
```

#### Successful Response (200 OK)
```json
[
  {
    "name": "trip_id",
    "title": "trip id",
    "type": "number"
  },
  {
    "name": "pickup_datetime",
    "title": "pickup datetime",
    "type": "datetime"
  },
  {
    "name": "passenger_count",
    "title": "passenger count",
    "type": "number"
  },
  {
    "name": "payment_type",
    "title": "payment type",
    "type": "string"
  },
  {
    "name": "pickup_ntaname",
    "title": "pickup ntaname",
    "type": "string"
  },
  {
    "name": "dropoff_ntaname",
    "title": "dropoff ntaname",
    "type": "string"
  },
  {
    "name": "vendor_id",
    "title": "vendor id",
    "type": "number"
  },
  {
    "name": "rate_code_id",
    "title": "rate code id",
    "type": "number"
  }
]
```

#### Error Response (404 Not Found)
```json
{
  "detail": "Cube 'invalid_cube' not found"
}
```

---

### 6. Get Cube Measures
* **Endpoint:** `GET /get_cube_measures`
* **Tags:** `Cubes`
* **Description:** Retrieve the list of all defined measures (metrics) for a specific analytical cube.

#### Parameters
* **Query Parameters:**
  * `cube_name` (string, Required): The name of the cube (without file extension). Example: `"nyc_taxi"`

#### Curl Example
```bash
curl -X GET "http://localhost:8000/get_cube_measures?cube_name=nyc_taxi"
```

#### Successful Response (200 OK)
```json
[
  {
    "name": "trip_id",
    "title": "count",
    "agg": "count"
  },
  {
    "name": "trip_distance",
    "title": "distance",
    "agg": "sum"
  },
  {
    "name": "fare_amount",
    "title": "fare amount",
    "agg": "sum"
  },
  {
    "name": "tip_amount",
    "title": "tip amount",
    "agg": "sum"
  },
  {
    "name": "total_amount",
    "title": "total amount",
    "agg": "sum"
  }
]
```

#### Error Response (404 Not Found)
```json
{
  "detail": "Cube 'invalid_cube' not found"
}
```

---

### 7. Query Dynamic OLAP Cube Data
* **Endpoint:** `POST /cubes/{cube_name}/query`
* **Tags:** `Cubes`
* **Description:** Dynamically generates a ClickHouse SQL SELECT-GROUP-BY query based on the selected dimensions (`rows`) and metrics (`aggs`) and executes it.

#### Parameters
* **Path Parameters:**
  * `cube_name` (string, Required): The name of the cube configuration (e.g. `"nyc_taxi"`).
* **Request Body JSON (`CubeQueryModel`):**
  * `rows` (array[string], Optional): The dimension/axis names to group by.
  * `aggs` (array[string], Optional): The metric/measure names to aggregate.

#### Curl Example
```bash
curl -X POST http://localhost:8000/cubes/nyc_taxi/query \
     -H "Content-Type: application/json" \
     -d '{
       "rows": ["payment_type"],
       "aggs": ["trip_id", "fare_amount"]
     }'
```

#### Successful Response (200 OK)
```json
{
  "query": "SELECT payment_type, count(trip_id) AS trip_id_count, sum(toFloat64OrZero(fare_amount)) AS fare_amount_sum FROM nyc_taxi GROUP BY payment_type",
  "data": [
    ["1", 12500, 185000.5],
    ["2", 11000, 154300.2],
    ["CS", 1500, 2400.0]
  ]
}
```

#### Error Response (404 Not Found)
```json
{
  "detail": "Cube 'invalid_cube' not found"
}
```

---

## 🗃️ Analytical Cube Schema Spec

The analytical service lists and processes cubes (such as `nyc_taxi.json`). Cube specifications follow a structured schema that maps the database source to UI-consumable dimensions (axises) and metrics (measures):

> [!TIP]
> Use these config files to build dynamic interfaces that generate SQL query parameters dynamically based on the measures and axises selected by the user.

```json
{
  "title": "nyc taxi",
  "source": "nyc_taxi",
  "axises": [
    {
      "name": "pickup_datetime",
      "title": "pickup datetime",
      "type": "datetime"
    },
    {
      "name": "passenger_count",
      "title": "passenger count",
      "type": "number"
    }
  ],
  "measures": [
    {
      "name": "trip_id",
      "title": "count",
      "agg": "count"
    },
    {
      "name": "fare_amount",
      "title": "fare amount",
      "agg": "sum"
    }
  ]
}
```
