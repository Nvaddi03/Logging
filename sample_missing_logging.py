"""
Sample Python application with intentionally missing logging.

This file demonstrates common scenarios where logging should exist but is missing.
Use this as test input for the Logging Gap Detection Agent.

This file has the following logging gaps:
1. Missing error logging in exception handlers
2. Missing logging for critical business operations
3. Missing context propagation
4. Missing structured logging
5. Missing logging in database operations
6. Missing logging in API calls
7. Missing logging for authentication/authorization
8. Missing performance metrics logging
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class UserService:
    """User management service - MISSING CRITICAL LOGGING"""
    
    def __init__(self, db_connection_string: str):
        self.db_connection = db_connection_string
        # GAP: No logging for service initialization
    
    def create_user(self, username: str, email: str, password: str) -> Dict:
        """
        Create a new user account.
        GAP: Missing logging for user creation (critical business operation)
        """
        try:
            # GAP: No logging before database operation
            user = {
                "id": self._generate_user_id(),
                "username": username,
                "email": email,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Simulate database insert
            self._save_to_database(user)
            
            # GAP: No logging for successful user creation
            return user
            
        except Exception as e:
            # GAP: CRITICAL - Exception caught but not logged!
            return {"error": "Failed to create user"}
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate user credentials.
        GAP: Missing security logging for authentication attempts
        """
        # GAP: No logging for authentication attempt
        user = self._find_user_by_username(username)
        
        if not user:
            # GAP: Failed login attempt not logged (security issue!)
            return None
        
        if self._verify_password(password, user.get("password_hash")):
            # GAP: Successful login not logged
            return user
        else:
            # GAP: Failed authentication not logged (security issue!)
            return None
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete user account.
        GAP: Missing logging for user deletion (critical operation)
        """
        try:
            # GAP: No logging before deleting user data
            self._delete_from_database(user_id)
            # GAP: No logging after deletion
            return True
        except Exception:
            # GAP: Exception caught and swallowed without logging!
            return False
    
    def _generate_user_id(self) -> str:
        """Generate unique user ID"""
        return f"user_{datetime.utcnow().timestamp()}"
    
    def _save_to_database(self, user: Dict):
        """Save user to database - GAP: No database operation logging"""
        pass
    
    def _find_user_by_username(self, username: str) -> Optional[Dict]:
        """Find user by username - GAP: No query logging"""
        return None
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password - GAP: No security logging"""
        return False
    
    def _delete_from_database(self, user_id: str):
        """Delete from database - GAP: No deletion logging"""
        pass


class PaymentProcessor:
    """Payment processing service - MISSING TRANSACTION LOGGING"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        # GAP: No logging for payment service initialization
    
    def process_payment(self, user_id: str, amount: float, currency: str) -> Dict:
        """
        Process payment transaction.
        GAP: Missing logging for financial transactions (CRITICAL!)
        """
        # GAP: No logging before payment processing starts
        
        if amount <= 0:
            # GAP: Invalid amount not logged
            return {"success": False, "error": "Invalid amount"}
        
        try:
            # GAP: No logging for external API call
            response = self._call_payment_gateway({
                "user_id": user_id,
                "amount": amount,
                "currency": currency
            })
            
            if response.get("status") == "success":
                # GAP: Successful payment not logged (CRITICAL!)
                return {"success": True, "transaction_id": response.get("id")}
            else:
                # GAP: Failed payment not logged
                return {"success": False, "error": response.get("error")}
                
        except Exception as e:
            # GAP: Payment processing exception not logged (CRITICAL!)
            return {"success": False, "error": "Payment processing failed"}
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict:
        """
        Refund a payment.
        GAP: Missing logging for refund operations (CRITICAL!)
        """
        try:
            # GAP: No logging before refund processing
            response = self._call_payment_gateway({
                "transaction_id": transaction_id,
                "amount": amount,
                "operation": "refund"
            })
            
            # GAP: No logging for refund result
            return response
            
        except Exception:
            # GAP: Refund exception not logged!
            return {"success": False}
    
    def _call_payment_gateway(self, data: Dict) -> Dict:
        """Call external payment gateway - GAP: No API call logging"""
        return {"status": "success", "id": "txn_123"}


class DataAnalyzer:
    """Data analysis service - MISSING PERFORMANCE LOGGING"""
    
    def analyze_large_dataset(self, dataset: List[Dict]) -> Dict:
        """
        Analyze large dataset.
        GAP: Missing performance metrics logging
        """
        # GAP: No logging for analysis start
        # GAP: No logging for dataset size
        
        results = []
        for item in dataset:
            try:
                # GAP: No logging for processing errors
                processed = self._process_item(item)
                results.append(processed)
            except Exception:
                # GAP: Processing error silently ignored!
                continue
        
        # GAP: No logging for analysis completion
        # GAP: No performance metrics (time, memory, etc.)
        return {"total_processed": len(results)}
    
    def _process_item(self, item: Dict) -> Dict:
        """Process single item - GAP: No progress logging"""
        return item


class APIClient:
    """External API client - MISSING REQUEST/RESPONSE LOGGING"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        # GAP: No initialization logging
    
    def get_user_data(self, user_id: str) -> Optional[Dict]:
        """
        Fetch user data from external API.
        GAP: Missing logging for external API calls
        """
        try:
            # GAP: No logging before API call
            url = f"{self.base_url}/users/{user_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                # GAP: Successful API call not logged
                return response.json()
            elif response.status_code == 404:
                # GAP: 404 error not logged
                return None
            else:
                # GAP: API error not logged
                return None
                
        except requests.Timeout:
            # GAP: Timeout exception not logged!
            return None
        except requests.RequestException:
            # GAP: Network error not logged!
            return None
    
    def post_data(self, endpoint: str, data: Dict) -> bool:
        """
        Post data to external API.
        GAP: Missing request/response logging
        """
        try:
            # GAP: No logging of request payload
            url = f"{self.base_url}{endpoint}"
            response = requests.post(url, json=data, timeout=self.timeout)
            
            # GAP: No logging of response status
            return response.status_code == 200
            
        except Exception:
            # GAP: Exception not logged!
            return False


class DatabaseManager:
    """Database operations - MISSING TRANSACTION LOGGING"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        # GAP: No database connection logging
    
    def execute_query(self, query: str, params: Dict = None) -> List[Dict]:
        """
        Execute database query.
        GAP: Missing query execution logging
        """
        # GAP: No logging of SQL query
        # GAP: No logging of query parameters
        
        try:
            # Simulate query execution
            results = self._run_query(query, params)
            # GAP: No logging of query results count
            return results
        except Exception:
            # GAP: Database error not logged!
            return []
    
    def begin_transaction(self):
        """
        Begin database transaction.
        GAP: Missing transaction start logging
        """
        pass
    
    def commit_transaction(self):
        """
        Commit database transaction.
        GAP: Missing transaction commit logging
        """
        pass
    
    def rollback_transaction(self):
        """
        Rollback database transaction.
        GAP: Missing transaction rollback logging (CRITICAL!)
        """
        pass
    
    def _run_query(self, query: str, params: Dict) -> List[Dict]:
        """Execute query - GAP: No execution logging"""
        return []


class CacheManager:
    """Cache operations - MISSING CACHE HIT/MISS LOGGING"""
    
    def __init__(self):
        self.cache = {}
        # GAP: No cache initialization logging
    
    def get(self, key: str) -> Optional[any]:
        """
        Get value from cache.
        GAP: Missing cache hit/miss logging (important for performance monitoring)
        """
        if key in self.cache:
            # GAP: Cache hit not logged
            return self.cache[key]
        else:
            # GAP: Cache miss not logged
            return None
    
    def set(self, key: str, value: any, ttl: int = 300):
        """
        Set value in cache.
        GAP: Missing cache write logging
        """
        # GAP: No logging for cache write
        self.cache[key] = value
    
    def delete(self, key: str):
        """
        Delete from cache.
        GAP: Missing cache deletion logging
        """
        # GAP: No logging for cache deletion
        if key in self.cache:
            del self.cache[key]


class MessageQueue:
    """Message queue operations - MISSING MESSAGE PROCESSING LOGGING"""
    
    def publish_message(self, queue_name: str, message: Dict) -> bool:
        """
        Publish message to queue.
        GAP: Missing message publishing logging
        """
        try:
            # GAP: No logging before publishing
            self._send_to_queue(queue_name, message)
            # GAP: No logging after successful publish
            return True
        except Exception:
            # GAP: Publish failure not logged!
            return False
    
    def consume_message(self, queue_name: str) -> Optional[Dict]:
        """
        Consume message from queue.
        GAP: Missing message consumption logging
        """
        try:
            # GAP: No logging for message retrieval
            message = self._receive_from_queue(queue_name)
            # GAP: No logging of message content
            return message
        except Exception:
            # GAP: Consumption error not logged!
            return None
    
    def _send_to_queue(self, queue_name: str, message: Dict):
        """Send to queue - GAP: No operation logging"""
        pass
    
    def _receive_from_queue(self, queue_name: str) -> Dict:
        """Receive from queue - GAP: No operation logging"""
        return {}


# Main execution block - MISSING STARTUP LOGGING
if __name__ == "__main__":
    # GAP: No application startup logging
    
    # Initialize services without logging
    user_service = UserService("postgresql://localhost/users")
    payment_processor = PaymentProcessor("api_key_12345")
    api_client = APIClient("https://api.example.com")
    
    # GAP: No logging for service initialization
    
    # Perform operations without proper logging
    user = user_service.create_user("john_doe", "john@example.com", "password123")
    payment_result = payment_processor.process_payment("user_123", 99.99, "USD")
    
    # GAP: No logging for operation results
    # GAP: No application shutdown logging
