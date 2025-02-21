# Point of Sale (POS) System API

This API provides endpoints for managing a Point of Sale system, including products, sales, and sale items. It allows you to:

- Manage product inventory (create, read, update, delete products)
- Process sales transactions
- Track stock levels automatically
- Calculate totals and subtotals
- View sales history

The API is built using Django REST Framework and follows RESTful principles. It includes automatic stock validation and updates, computed fields for pricing, and proper error handling.

Key Features:
- Full CRUD operations for products and sales
- Automatic stock management
- Price calculations
- Input validation
- Detailed error responses


## Base URL
```
http://localhost:8000/api/
```

## Endpoints

### Products

#### List all products
```http
GET /api/products/
```

**Response**
```json
[
    {
        "id": 1,
        "name": "Product Name",
        "price": "99.99",
        "stock": 100
    }
]
```

#### Get single product
```http
GET /api/products/{id}/
```

**Response**
```json
{
    "id": 1,
    "name": "Product Name",
    "price": "99.99",
    "stock": 100
}
```

#### Create product
```http
POST /api/products/
```

**Request Body**
```json
{
    "name": "New Product",
    "price": "99.99",
    "stock": 100
}
```

#### Update product
```http
PUT /api/products/{id}/
PATCH /api/products/{id}/  # For partial updates
```

**Request Body**
```json
{
    "name": "Updated Product",
    "price": "149.99",
    "stock": 200
}
```

#### Delete product
```http
DELETE /api/products/{id}/
```

### Sales

#### List all sales
```http
GET /api/sales/
```

**Response**
```json
[
    {
    "id": 1,
    "date": "2025-02-21T17:01:51.407903Z",
    "items": [
      {
        "product": {
          "id": 1,
          "name": "Product 1",
          "price": "100.00",
          "stock": 10
        },
        "quantity": 4,
        "subtotal": 400.0
      }
    ],
    "total_price": 400.0
    }
]
```

#### Get single sale
```http
GET /api/sales/{id}/
```

#### Create sale
```http
POST /api/sales/
```

**Request Body**
```json
{
    "items": [
        {
            "product": 1,
            "quantity": 3
        },
        {
            "product": 2,
            "quantity": 2
        }
    ]
}
```

#### Update sale
```http
PUT /api/sales/{id}/
PATCH /api/sales/{id}/  # For partial updates
```

#### Delete sale
```http
DELETE /api/sales/{id}/
```

### Sale Items

#### List all sale items
```http
GET /api/saleitems/
```

**Response**
```json
[
    {
        "id": 1,
        "sale": 1,
        "product": 1,
        "quantity": 3,
        "subtotal": "299.97"
    }
]
```

#### Get single sale item
```http
GET /api/saleitems/{id}/
```

#### Create sale item
```http
POST /api/saleitems/
```

**Request Body**
```json
{
    "sale": 1,
    "product": 1,
    "quantity": 3
}
```

#### Update sale item
```http
PUT /api/saleitems/{id}/
PATCH /api/saleitems/{id}/  # For partial updates
```

#### Delete sale item
```http
DELETE /api/saleitems/{id}/
```

## Computed Fields

- `total_price`: Automatically calculated for sales as the sum of all sale items (quantity * product price)
- `subtotal`: Automatically calculated for sale items as (quantity * product price)

## Error Responses

The API will return appropriate HTTP status codes:

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request body
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses will include a message describing the error:

```json
{
    "error": "Error message description"
}
```

## Authentication

[Add authentication details if implemented]

## Rate Limiting

[Add rate limiting details if implemented]

## Future Features

The following features are planned for future releases:

### Authentication and Authorization
- JWT token-based authentication
- Role-based access control (Admin, Manager, Cashier)
- User management endpoints
- Session management

### Enhanced Sales Features
- Support for discounts and promotions
- Tax calculations
- Multiple payment methods
- Receipt generation and printing
- Refund processing

### Inventory Management
- Low stock alerts
- Automatic reordering
- Batch product updates
- Product categories and tags
- Product variants (size, color, etc.)

### Reporting
- Sales analytics dashboard
- Daily/weekly/monthly reports
- Revenue forecasting
- Best-selling products tracking
- Customer purchase history

### Integration Features
- External payment gateway integration
- Barcode scanner support
- Export data to CSV/Excel
- Email notifications
- Third-party accounting software integration

### Performance Optimizations
- Response caching
- Bulk operations
- Pagination improvements
- Search optimization


