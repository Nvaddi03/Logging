# Sample E-Commerce Application

A microservices-based e-commerce platform for testing logging gap analysis.

## Services

- **User Service** (Python/Flask) - Port 5001
  - Handles user authentication and profile management
  - File: `user_service.py`
  - Intentional logging gaps: DELETE operations, database transactions, token generation
  
- **Order Service** (Python/FastAPI) - Port 8001  
  - Handles order processing and management
  - File: `order_service.py`
  - Intentional logging gaps: Database transactions, inventory updates, payment records, refund processing
  
- **Payment Service** (Node.js/Express) - Port 3001
  - Handles payment processing and transaction management
  - File: `payment_service.js`
  - Intentional logging gaps: External API calls, webhooks, database operations
  
- **Inventory Service** (Java/Spring Boot) - Port 8080
  - Handles inventory management and stock tracking
  - File: `InventoryController.java`
  - Intentional logging gaps: Stock reservations, bulk operations, low stock checks

## Expected Logging Gaps

This test repository contains **intentional logging gaps** to validate the analysis tool:

### Critical Gaps (High Priority)
1. **Financial Operations**: Payment processing, refunds (NO logging)
2. **Inventory Changes**: Stock reservations, releases (NO logging)
3. **Data Deletion**: User/order deletion (NO audit trail)
4. **External API Calls**: Payment gateway calls (NO request/response logging)

### Important Gaps (Medium Priority)
1. **Database Transactions**: CRUD operations missing logging
2. **Authentication**: Token generation, password validation
3. **Webhooks**: Incoming webhook events not logged
4. **Error Handling**: Some exception handlers missing logging

### Minor Gaps (Low Priority)
1. **GET Endpoints**: Some read operations without logging
2. **Validation**: Input validation failures not logged
3. **Status Changes**: Some state transitions without logging

## Setup

```bash
# Python services
pip install -r requirements.txt

# Node.js service
npm install

# Java service
mvn clean install
```

## Testing

Push this repository to GitHub and analyze with the Logging Gap Analysis tool to verify:
- ✅ Multi-language detection (Python, JavaScript, Java)
- ✅ Framework detection (Flask, FastAPI, Express, Spring Boot)
- ✅ Cross-language code parsing
- ✅ Database transaction detection
- ✅ External API call detection
- ✅ Logging gap identification (should find 40+ gaps)
- ✅ Report generation with severity levels
- ✅ Diagram generation showing service architecture
