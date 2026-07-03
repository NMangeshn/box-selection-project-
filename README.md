# AI-Assisted Box Selection System

This is a small Django and Django REST Framework project for recommending a shipping box for an ecommerce order.

The code is intentionally simple and easy to explain in an interview.

## Features

- Product management
- Shipping box management
- Order creation with order items
- Admin panel for all models
- API endpoint to recommend the lowest-cost suitable box
- Input validation
- Unit tests for API and recommendation logic
- SQLite database

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite

## Recommendation Logic

The recommendation is based on three simple checks:

1. The total order weight must be less than or equal to the box max weight.
2. The largest product in the order must fit inside the box dimensions.
3. The total product volume must be less than or equal to the box volume.

From all suitable boxes, the system returns the box with the lowest cost. If two boxes have the same cost, the smaller box is selected.

This is a simple practical approach, not a complex 3D packing algorithm.

## Project Structure

```text
box_selection_project/
  manage.py
  requirements.txt
  README.md
  AI_USAGE.md
  TEST_OUTPUT.md
  box_selection_project/
    settings.py
    urls.py
    wsgi.py
    asgi.py
  shipping/
    admin.py
    apps.py
    models.py
    serializers.py
    services.py
    views.py
    urls.py
    tests.py
    migrations/
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Run migrations:

python manage.py migrate

This creates the SQLite database (db.sqlite3) in the project root directory.

Create an admin user:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

API root:

```text
http://127.0.0.1:8000/api/
```

## API Endpoints

### Products

```text
GET    /api/products/
POST   /api/products/
GET    /api/products/<id>/
PUT    /api/products/<id>/
PATCH  /api/products/<id>/
DELETE /api/products/<id>/
```

Example product request:

```json
{
  "name": "Laptop",
  "length": "30",
  "width": "20",
  "height": "5",
  "weight": "2"
}
```

### Boxes

```text
GET    /api/boxes/
POST   /api/boxes/
GET    /api/boxes/<id>/
PUT    /api/boxes/<id>/
PATCH  /api/boxes/<id>/
DELETE /api/boxes/<id>/
```

Example box request:

```json
{
  "name": "Small Box",
  "inner_length": "20.00",
  "inner_width": "15.00",
  "inner_height": "10.00",
  "max_weight": "5.00",
  "cost": "25.00",
  "is_active": true
}
```

### Orders

```text
GET    /api/orders/
POST   /api/orders/
GET    /api/orders/<id>/
PUT    /api/orders/<id>/
PATCH  /api/orders/<id>/
DELETE /api/orders/<id>/
```

Example order request:

```json
{
  "customer_name": "Mangesh",
  "items": [
    {
      "product": 1,
      "quantity": 2
    }
  ]
}
```

### Recommend Box

```text
GET /api/orders/<id>/recommend-box/
```

Example success response:

```json
{
  "box": {
    "id": 1,
    "name": "Small Box",
    "inner_length": "20.00",
    "inner_width": "15.00",
    "inner_height": "10.00",
    "max_weight": "5.00",
    "cost": "25.00",
    "is_active": true
  },
  "total_weight": "1.00",
  "total_product_volume": "1280.00"
}
```

Example error response:

```json
{
  "detail": "No suitable box found for this order."
}
```

## Validations

- Product dimensions must be greater than 0.
- Product weight must be greater than 0.
- Box dimensions must be greater than 0.
- Box max weight must be greater than 0.
- Box cost cannot be negative.
- Order must have at least one item.
- Order item quantity must be greater than 0.
- Inactive boxes are ignored during recommendation.

## Running Tests

```bash
python manage.py test
```


