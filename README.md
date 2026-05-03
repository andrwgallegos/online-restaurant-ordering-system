# Online Restaurant Ordering System API

FastAPI backend for an online restaurant ordering system, built for ITSC-3155 Software Engineering (Group Project Part 3).

**Team Members:** Andrew G, Dalia F, Xanaan S

## Tech Stack

- **FastAPI** for the HTTP layer
- **SQLAlchemy** ORM
- **MySQL** as the production database (SQLite available as a development fallback)
- **Pydantic v2** for request/response validation
- **pytest** for unit tests

## Project Structure

```
api/
├── controllers/      # Business logic and database operations
├── dependencies/     # Database connection and configuration
├── models/           # SQLAlchemy ORM models (one file per table)
├── routers/          # FastAPI routes (one file per resource)
├── schemas/          # Pydantic request/response schemas
├── tests/            # pytest unit tests
├── main.py           # FastAPI application entry point
└── seed.py           # Sample data loader for demos
```

## Quick Start

### 1. Create a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r api/requirements.txt
```

### 3. Set up MySQL

Create a database called `restaurant_ordering_system`:

```sql
CREATE DATABASE restaurant_ordering_system;
```

By default the API connects with:

| Setting     | Default                        | Override env var |
|-------------|--------------------------------|------------------|
| DB engine   | `mysql`                        | `DB_ENGINE`      |
| Host        | `localhost`                    | `DB_HOST`        |
| Port        | `3306`                         | `DB_PORT`        |
| Database    | `restaurant_ordering_system`   | `DB_NAME`        |
| User        | `root`                         | `DB_USER`        |
| Password    | `password123`                  | `DB_PASSWORD`    |

If your credentials differ, either set environment variables or edit `api/dependencies/config.py`.

#### Optional: SQLite fallback

For quick local development without MySQL set:
```bash
export DB_ENGINE=sqlite   # macOS / Linux
set DB_ENGINE=sqlite      # Windows cmd
```

### 4. Load sample data

```bash
python -m api.seed
```

This drops and recreates all tables and inserts demo customers, menu items, orders, payments, and reviews.

### 5. Run the server

```bash
uvicorn api.main:app --reload
```

The API is now available at `http://127.0.0.1:8000` and the interactive docs at `http://127.0.0.1:8000/docs`.

## Running Tests

```bash
pytest api/tests
```

Tests use a temporary SQLite database (configured in `api/tests/conftest.py`) so they run without requiring MySQL.

## Key Endpoints

### Customer-facing

| Method | Path                                         | Description |
|--------|----------------------------------------------|-------------|
| GET    | `/menu-items/`                               | Browse menu, optional `?category=` and `?available_only=` filters |
| POST   | `/checkout/`                                 | Guest checkout: creates customer, order, items, optional payment in one call |
| GET    | `/orders/tracking/{tracking_number}`         | Track order status by tracking number |
| POST   | `/checkout/{order_id}/apply-promotion`       | Apply a promo code to an existing order |
| POST   | `/reviews/`                                  | Submit a rating and review for a dish |

### Staff-facing

| Method | Path                                         | Description |
|--------|----------------------------------------------|-------------|
| GET    | `/reports/low-stock?threshold=10`            | Resources at or below stock threshold |
| GET    | `/reports/orders/{order_id}/insufficient-resources` | Detect ingredient shortages for an order |
| GET    | `/reports/revenue/daily?date=YYYY-MM-DD`     | Total completed-payment revenue and order count for a date |
| GET    | `/reports/orders/range?start_date=...&end_date=...` | Orders placed in a date range |
| GET    | `/reports/dishes/review-summary`             | Review counts and average ratings per dish |
| Full CRUD | `/menu-items/`, `/promotions/`, `/orders/`, `/resources/`, `/recipes/` | Standard create/read/update/delete |

## Documentation

See the `docs/` folder for the User Manual and Technical Document.
