# test_antipatterns.py
"""
Test file with intentional logging anti-patterns for testing Stage 9
"""

import logging
import json

logger = logging.getLogger(__name__)

def authenticate_user(username, password, email):
    """
    CRITICAL ANTI-PATTERN: Logging sensitive data (password, email)
    """
    logger.info(f"Login attempt: {username}:{password} from {email}")
    
    # Another critical issue
    api_key = "sk-1234567890abcdef"
    logger.debug(f"Using API key: {api_key}")
    
    return True

def process_credit_card(card_number, user):
    """
    CRITICAL ANTI-PATTERN: Logging credit card number
    """
    logger.info(f"Processing payment for {user.name}: {card_number}")
    return True

def batch_process_records(records):
    """
    HIGH ANTI-PATTERN: Logging in hot loop (10,000+ iterations)
    """
    logger.info(f"Starting batch processing of {len(records)} records")
    
    for record in records:
        logger.info(f"Processing record: {record.id}")  # BAD: In loop
        record.process()
    
    logger.info("Batch processing complete")

def recursive_tree_walker(node, depth=0):
    """
    HIGH ANTI-PATTERN: Logging in recursive function
    """
    logger.debug(f"Visiting node: {node.name} at depth {depth}")
    
    for child in node.children:
        recursive_tree_walker(child, depth + 1)  # Recursion with logging

def load_user_data(user_id):
    """
    HIGH ANTI-PATTERN: Silent exception - errors hidden
    """
    try:
        data = fetch_from_db(user_id)
        return json.loads(data)
    except:
        pass  # BAD: No logging!

def save_order(order):
    """
    MEDIUM ANTI-PATTERN: Exception handler without logging
    """
    try:
        db.save(order)
    except Exception:
        # BAD: Caught exception but no logging
        return None
    
    return order.id

def handle_api_request(request):
    """
    LOW ANTI-PATTERN: Using INFO level for error message
    """
    if request.is_invalid():
        logger.info("ERROR: Invalid request received")  # Should be logger.error()
    
    process_request(request)

def process_large_dataset(data):
    """
    MEDIUM ANTI-PATTERN: Logging large objects
    """
    logger.info(f"Processing data: {data}")  # BAD: 'data' might be huge
    
    results = analyze(data)
    logger.debug(f"Results: {results}")  # BAD: Large object
    
    return results

def handle_payment_error(error, request_id):
    """
    LOW ANTI-PATTERN: Missing contextual information
    """
    logger.error("Payment processing failed")  # Should include request_id, user_id, etc.

def log_user_ssn(user):
    """
    CRITICAL ANTI-PATTERN: Logging SSN
    """
    logger.info(f"User SSN: {user.ssn}")  # e.g., "123-45-6789"

def log_jwt_token(token):
    """
    CRITICAL ANTI-PATTERN: Logging JWT token
    """
    logger.debug(f"Auth token: {token}")  # e.g., "eyJhbGc..."

# Good examples for comparison

def authenticate_user_good(username):
    """
    GOOD: No sensitive data logged
    """
    logger.info(f"Login attempt for user: {username}", extra={'success': True})

def batch_process_records_good(records):
    """
    GOOD: Summary logging instead of per-item
    """
    logger.info(f"Processing {len(records)} records")
    
    errors = []
    for record in records:
        try:
            record.process()
        except Exception as e:
            errors.append(record.id)
            logger.error(f"Failed to process record {record.id}: {e}")
    
    logger.info(f"Completed {len(records) - len(errors)}/{len(records)} records")

def load_user_data_good(user_id):
    """
    GOOD: Proper exception logging
    """
    try:
        data = fetch_from_db(user_id)
        return json.loads(data)
    except Exception as e:
        logger.error(f"Failed to load user data: {e}", 
                    extra={'user_id': user_id},
                    exc_info=True)
        raise

def handle_api_request_good(request):
    """
    GOOD: Correct log level and structured context
    """
    if request.is_invalid():
        logger.error("Invalid request received", 
                    extra={'request_id': request.id, 'errors': request.errors})
