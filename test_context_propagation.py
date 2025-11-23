"""
Test file for Context Propagation Analysis (Tool 6)
This file demonstrates various context propagation patterns and gaps.
"""

import logging
from flask import Flask, g, request
from fastapi import Depends, Request
from contextvars import ContextVar
import asyncio
from functools import wraps

logger = logging.getLogger(__name__)

# Context variable for request tracking
request_id_var: ContextVar[str] = ContextVar('request_id', default=None)
user_id_var: ContextVar[str] = ContextVar('user_id', default=None)


# ============================================================================
# MISSING CONTEXT PROPAGATION - Tool 6 should detect these gaps
# ============================================================================

class OrderService:
    """Service that DOESN'T propagate context - BAD"""
    
    def create_order(self, user_id, items):
        """Missing request_id parameter - context lost"""
        # ❌ GAP: No request_id parameter
        # ❌ GAP: Logging without correlation ID
        logger.info(f"Creating order for user {user_id}")
        
        # Call to payment service without context
        payment_result = self.process_payment(items)  # ❌ GAP: No request_id passed
        
        # Call to notification without context
        self.send_notification(user_id)  # ❌ GAP: No request_id passed
        
        return {"order_id": "12345"}
    
    def process_payment(self, items):
        """Payment processing without correlation"""
        # ❌ GAP: No request_id in function signature
        # ❌ GAP: Can't trace this back to original request
        logger.info(f"Processing payment for {len(items)} items")
        return {"status": "success"}
    
    def send_notification(self, user_id):
        """Notification without context"""
        # ❌ GAP: No request_id
        logger.info(f"Sending notification to user {user_id}")


class UserService:
    """Another service missing context propagation"""
    
    def get_user(self, user_id):
        """User lookup without correlation"""
        # ❌ GAP: No request_id parameter
        logger.info(f"Fetching user {user_id}")
        return {"id": user_id, "name": "John"}
    
    def update_user(self, user_id, data):
        """Update without context"""
        # ❌ GAP: Missing correlation ID in logs
        logger.info(f"Updating user {user_id}")
        
        # Call to audit log without context
        self.audit_log("user_update", user_id)  # ❌ GAP
        
        return True
    
    def audit_log(self, action, user_id):
        """Audit logging without correlation"""
        # ❌ GAP: Critical audit trail missing request context
        logger.info(f"Audit: {action} by user {user_id}")


# ============================================================================
# BROKEN CONTEXT CHAIN - Context created but lost
# ============================================================================

def api_endpoint_broken(request):
    """API endpoint that creates context but doesn't propagate it"""
    # Create request_id but don't pass it down
    request_id = request.headers.get('X-Request-ID', 'req-12345')
    
    # ❌ GAP: request_id created but not passed to service
    logger.info(f"Request received", extra={'request_id': request_id})
    
    # Lost context here - service call without request_id
    result = process_business_logic()  # ❌ GAP: No request_id argument
    
    return result


def process_business_logic():
    """Business logic that lost the context"""
    # ❌ GAP: No request_id parameter - can't correlate logs
    logger.info("Processing business logic")
    
    # Call database without context
    data = query_database()  # ❌ GAP
    
    # Call external API without context
    response = call_external_api()  # ❌ GAP
    
    return data


def query_database():
    """Database query without correlation"""
    # ❌ GAP: Critical database operation not correlated to request
    logger.info("Executing database query")
    return {"data": "result"}


def call_external_api():
    """External API call without correlation"""
    # ❌ GAP: External service call not correlated
    logger.info("Calling external API")
    return {"status": "ok"}


# ============================================================================
# ASYNC FUNCTIONS WITHOUT CONTEXT
# ============================================================================

async def async_process_order_bad(order_id):
    """Async function without context propagation"""
    # ❌ GAP: No request_id in async function
    logger.info(f"Async processing order {order_id}")
    
    # Background tasks losing context
    await asyncio.gather(
        send_email_async(order_id),  # ❌ GAP
        update_inventory_async(order_id),  # ❌ GAP
        notify_shipping_async(order_id)  # ❌ GAP
    )


async def send_email_async(order_id):
    """Email sending without correlation"""
    # ❌ GAP: Can't trace which request triggered this email
    logger.info(f"Sending email for order {order_id}")
    await asyncio.sleep(0.1)


async def update_inventory_async(order_id):
    """Inventory update without context"""
    # ❌ GAP: Inventory changes not correlated to requests
    logger.info(f"Updating inventory for order {order_id}")
    await asyncio.sleep(0.1)


async def notify_shipping_async(order_id):
    """Shipping notification without context"""
    # ❌ GAP: Shipping logs not correlated
    logger.info(f"Notifying shipping for order {order_id}")
    await asyncio.sleep(0.1)


# ============================================================================
# ERROR HANDLERS WITHOUT CONTEXT
# ============================================================================

def handle_error_bad(error):
    """Error handler that loses context"""
    # ❌ GAP: Critical error logs without request correlation
    logger.error(f"Error occurred: {error}")
    
    # Send to error tracking without context
    send_to_sentry(error)  # ❌ GAP


def send_to_sentry(error):
    """Error tracking without correlation"""
    # ❌ GAP: Can't correlate errors back to requests
    logger.info(f"Sending error to Sentry: {error}")


# ============================================================================
# BACKGROUND JOBS WITHOUT CONTEXT
# ============================================================================

def schedule_background_job_bad(job_type, data):
    """Background job without correlation"""
    # ❌ GAP: Background jobs lose request context
    logger.info(f"Scheduling {job_type} job")
    
    # Job execution without context
    execute_job(job_type, data)  # ❌ GAP


def execute_job(job_type, data):
    """Job execution without correlation"""
    # ❌ GAP: Can't trace job back to triggering request
    logger.info(f"Executing job: {job_type}")


# ============================================================================
# CORRECT EXAMPLES - WITH PROPER CONTEXT PROPAGATION
# ============================================================================

class OrderServiceGood:
    """Service with proper context propagation - GOOD ✓"""
    
    def create_order(self, user_id, items, request_id):
        """✓ GOOD: request_id parameter included"""
        logger.info(f"Creating order for user {user_id}", 
                   extra={'request_id': request_id})
        
        # ✓ GOOD: Context propagated to payment service
        payment_result = self.process_payment(items, request_id)
        
        # ✓ GOOD: Context propagated to notification
        self.send_notification(user_id, request_id)
        
        return {"order_id": "12345", "request_id": request_id}
    
    def process_payment(self, items, request_id):
        """✓ GOOD: Receives and uses request_id"""
        logger.info(f"Processing payment for {len(items)} items",
                   extra={'request_id': request_id})
        return {"status": "success"}
    
    def send_notification(self, user_id, request_id):
        """✓ GOOD: Notification correlated to request"""
        logger.info(f"Sending notification to user {user_id}",
                   extra={'request_id': request_id})


def api_endpoint_good(request):
    """✓ GOOD: API endpoint with proper context propagation"""
    request_id = request.headers.get('X-Request-ID', 'req-12345')
    
    logger.info(f"Request received", extra={'request_id': request_id})
    
    # ✓ GOOD: request_id passed to business logic
    result = process_business_logic_good(request_id)
    
    return result


def process_business_logic_good(request_id):
    """✓ GOOD: Business logic with context"""
    logger.info("Processing business logic", extra={'request_id': request_id})
    
    # ✓ GOOD: Context propagated to database
    data = query_database_good(request_id)
    
    # ✓ GOOD: Context propagated to external API
    response = call_external_api_good(request_id)
    
    return data


def query_database_good(request_id):
    """✓ GOOD: Database query with correlation"""
    logger.info("Executing database query", extra={'request_id': request_id})
    return {"data": "result"}


def call_external_api_good(request_id):
    """✓ GOOD: External API with correlation"""
    logger.info("Calling external API", extra={'request_id': request_id})
    return {"status": "ok"}


# ============================================================================
# FLASK EXAMPLE - Using Flask's 'g' for context
# ============================================================================

app = Flask(__name__)

@app.before_request
def setup_request_context():
    """✓ GOOD: Setup context using Flask's g"""
    g.request_id = request.headers.get('X-Request-ID', 'req-default')
    g.user_id = request.headers.get('X-User-ID', 'user-default')


@app.route('/orders', methods=['POST'])
def create_order_flask():
    """Flask endpoint using g for context"""
    # ✓ GOOD: Access context from g
    logger.info("Creating order", extra={'request_id': g.request_id})
    
    # ✓ GOOD: Pass context to service
    order_service = OrderServiceGood()
    result = order_service.create_order(
        user_id=g.user_id,
        items=request.json.get('items'),
        request_id=g.request_id  # ✓ Context propagated
    )
    
    return result


# ============================================================================
# CONTEXTVARS EXAMPLE - Python 3.7+ approach
# ============================================================================

async def async_process_order_good(order_id):
    """✓ GOOD: Async function with ContextVar"""
    request_id = request_id_var.get()
    
    logger.info(f"Async processing order {order_id}",
               extra={'request_id': request_id})
    
    # ✓ GOOD: Context automatically propagated in async tasks
    await asyncio.gather(
        send_email_async_good(order_id),
        update_inventory_async_good(order_id),
        notify_shipping_async_good(order_id)
    )


async def send_email_async_good(order_id):
    """✓ GOOD: Uses ContextVar for correlation"""
    request_id = request_id_var.get()
    logger.info(f"Sending email for order {order_id}",
               extra={'request_id': request_id})
    await asyncio.sleep(0.1)


async def update_inventory_async_good(order_id):
    """✓ GOOD: Inventory update with context"""
    request_id = request_id_var.get()
    logger.info(f"Updating inventory for order {order_id}",
               extra={'request_id': request_id})
    await asyncio.sleep(0.1)


async def notify_shipping_async_good(order_id):
    """✓ GOOD: Shipping notification with context"""
    request_id = request_id_var.get()
    logger.info(f"Notifying shipping for order {order_id}",
               extra={'request_id': request_id})
    await asyncio.sleep(0.1)


# ============================================================================
# DECORATOR PATTERN - Automatic context injection
# ============================================================================

def with_request_context(func):
    """✓ GOOD: Decorator to automatically inject request context"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_id = request_id_var.get()
        if request_id:
            # Inject request_id into kwargs if not present
            if 'request_id' not in kwargs:
                kwargs['request_id'] = request_id
        return func(*args, **kwargs)
    return wrapper


@with_request_context
def decorated_function(data, request_id=None):
    """✓ GOOD: Function automatically gets request_id from decorator"""
    logger.info(f"Processing data", extra={'request_id': request_id})
    return process_data(data, request_id)


@with_request_context
def process_data(data, request_id=None):
    """✓ GOOD: Context propagated through decorator"""
    logger.info(f"Data processing", extra={'request_id': request_id})
    return {"processed": True}


if __name__ == "__main__":
    print("Context Propagation Test File")
    print("\nExpected Tool 6 Detections:")
    print("- 20+ functions missing request_id parameter")
    print("- 15+ broken context chains (context created but lost)")
    print("- 10+ async functions without context propagation")
    print("- 5+ error handlers without correlation")
    print("- 5+ background jobs without context")
    print("\nExpected Good Examples:")
    print("- 10+ functions with proper request_id propagation")
    print("- Flask 'g' usage detected")
    print("- ContextVar usage detected")
    print("- Decorator pattern detected")
