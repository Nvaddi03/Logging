"""
Test file for Service Dependency Detection (Tool 5)
This file contains various service calls that should be detected by the analyzer.
"""

import requests
import json
import asyncio
import aiohttp
from typing import Dict, Any, List
import grpc
import websockets


# ============================================================================
# HTTP REST API Calls
# ============================================================================

class UserServiceClient:
    """REST API client for user service"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_user(self, user_id: int) -> Dict:
        """Get user by ID - should be logged"""
        # SERVICE DEPENDENCY: HTTP GET to user service
        response = requests.get(f"{self.base_url}/api/users/{user_id}")
        response.raise_for_status()
        return response.json()
    
    def create_user(self, user_data: Dict) -> Dict:
        """Create new user - should be logged"""
        # SERVICE DEPENDENCY: HTTP POST to user service
        response = requests.post(
            f"{self.base_url}/api/users",
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        return response.json()
    
    def update_user(self, user_id: int, updates: Dict) -> Dict:
        """Update user - should be logged"""
        # SERVICE DEPENDENCY: HTTP PUT to user service
        response = requests.put(
            f"{self.base_url}/api/users/{user_id}",
            json=updates
        )
        return response.json()
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user - should be logged"""
        # SERVICE DEPENDENCY: HTTP DELETE to user service
        response = requests.delete(f"{self.base_url}/api/users/{user_id}")
        return response.status_code == 204
    
    def search_users(self, query: str) -> List[Dict]:
        """Search users - should be logged"""
        # SERVICE DEPENDENCY: HTTP GET with query parameters
        response = self.session.get(
            f"{self.base_url}/api/users/search",
            params={'q': query, 'limit': 10}
        )
        return response.json()


# ============================================================================
# External Third-Party API Calls
# ============================================================================

class PaymentGateway:
    """Payment gateway integration"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.gateway_url = "https://api.stripe.com/v1"
    
    def process_payment(self, amount: float, currency: str, card_token: str) -> Dict:
        """Process payment via Stripe - should be logged"""
        # SERVICE DEPENDENCY: External payment service
        response = requests.post(
            f"{self.gateway_url}/charges",
            data={
                'amount': int(amount * 100),
                'currency': currency,
                'source': card_token
            },
            auth=(self.api_key, '')
        )
        return response.json()
    
    def create_customer(self, email: str, name: str) -> Dict:
        """Create customer in Stripe - should be logged"""
        # SERVICE DEPENDENCY: External payment service
        response = requests.post(
            f"{self.gateway_url}/customers",
            data={'email': email, 'name': name},
            auth=(self.api_key, '')
        )
        return response.json()
    
    def refund_payment(self, charge_id: str) -> Dict:
        """Refund payment - should be logged"""
        # SERVICE DEPENDENCY: External payment service
        response = requests.post(
            f"{self.gateway_url}/refunds",
            data={'charge': charge_id},
            auth=(self.api_key, '')
        )
        return response.json()


class EmailService:
    """Email service integration (SendGrid)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sendgrid.com/v3"
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email via SendGrid - should be logged"""
        # SERVICE DEPENDENCY: External email service
        response = requests.post(
            f"{self.base_url}/mail/send",
            json={
                'personalizations': [{'to': [{'email': to}]}],
                'from': {'email': 'noreply@example.com'},
                'subject': subject,
                'content': [{'type': 'text/plain', 'value': body}]
            },
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
        )
        return response.status_code == 202


class SMSService:
    """SMS service integration (Twilio)"""
    
    def send_sms(self, phone: str, message: str) -> Dict:
        """Send SMS via Twilio - should be logged"""
        # SERVICE DEPENDENCY: External SMS service
        response = requests.post(
            "https://api.twilio.com/2010-04-01/Accounts/AC123/Messages.json",
            data={
                'To': phone,
                'From': '+1234567890',
                'Body': message
            },
            auth=('AC123', 'auth_token')
        )
        return response.json()


# ============================================================================
# Async HTTP Calls
# ============================================================================

class AsyncAPIClient:
    """Async HTTP client using aiohttp"""
    
    async def fetch_user_async(self, user_id: int) -> Dict:
        """Async user fetch - should be logged"""
        # SERVICE DEPENDENCY: Async HTTP GET
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://api.example.com/users/{user_id}") as response:
                return await response.json()
    
    async def batch_fetch_users(self, user_ids: List[int]) -> List[Dict]:
        """Batch async fetches - should be logged"""
        # SERVICE DEPENDENCY: Multiple async HTTP calls
        async with aiohttp.ClientSession() as session:
            tasks = []
            for user_id in user_ids:
                tasks.append(session.get(f"http://api.example.com/users/{user_id}"))
            
            responses = await asyncio.gather(*tasks)
            results = []
            for response in responses:
                results.append(await response.json())
            
            return results
    
    async def post_analytics(self, event_data: Dict) -> bool:
        """Async analytics post - should be logged"""
        # SERVICE DEPENDENCY: Async HTTP POST
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://analytics.example.com/events",
                json=event_data
            ) as response:
                return response.status == 200


# ============================================================================
# GraphQL API Calls
# ============================================================================

class GraphQLClient:
    """GraphQL API client"""
    
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
    
    def query_user(self, user_id: int) -> Dict:
        """GraphQL query - should be logged"""
        # SERVICE DEPENDENCY: GraphQL query
        query = """
        query GetUser($userId: ID!) {
            user(id: $userId) {
                id
                name
                email
                posts {
                    id
                    title
                }
            }
        }
        """
        
        response = requests.post(
            self.endpoint,
            json={
                'query': query,
                'variables': {'userId': user_id}
            }
        )
        return response.json()
    
    def create_post(self, title: str, content: str, author_id: int) -> Dict:
        """GraphQL mutation - should be logged"""
        # SERVICE DEPENDENCY: GraphQL mutation
        mutation = """
        mutation CreatePost($title: String!, $content: String!, $authorId: ID!) {
            createPost(title: $title, content: $content, authorId: $authorId) {
                id
                title
                createdAt
            }
        }
        """
        
        response = requests.post(
            self.endpoint,
            json={
                'query': mutation,
                'variables': {
                    'title': title,
                    'content': content,
                    'authorId': author_id
                }
            }
        )
        return response.json()


# ============================================================================
# gRPC Service Calls
# ============================================================================

class GRPCUserClient:
    """gRPC client for user service"""
    
    def __init__(self, host: str, port: int):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        # Note: In real code, would import generated stubs
    
    def get_user_grpc(self, user_id: int) -> Dict:
        """Get user via gRPC - should be logged"""
        # SERVICE DEPENDENCY: gRPC call
        # In real code: stub = user_pb2_grpc.UserServiceStub(self.channel)
        # request = user_pb2.GetUserRequest(user_id=user_id)
        # response = stub.GetUser(request)
        return {'id': user_id, 'name': 'John Doe'}
    
    def stream_user_events(self, user_id: int):
        """Stream events via gRPC - should be logged"""
        # SERVICE DEPENDENCY: gRPC streaming
        # In real code: stub = user_pb2_grpc.UserServiceStub(self.channel)
        # for event in stub.StreamEvents(request):
        #     yield event
        pass


# ============================================================================
# WebSocket Connections
# ============================================================================

class WebSocketClient:
    """WebSocket client for real-time updates"""
    
    async def connect_and_listen(self, ws_url: str):
        """Connect to WebSocket - should be logged"""
        # SERVICE DEPENDENCY: WebSocket connection
        async with websockets.connect(ws_url) as websocket:
            await websocket.send(json.dumps({'action': 'subscribe', 'channel': 'updates'}))
            
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
    
    async def send_message(self, ws_url: str, message: Dict):
        """Send WebSocket message - should be logged"""
        # SERVICE DEPENDENCY: WebSocket send
        async with websockets.connect(ws_url) as websocket:
            await websocket.send(json.dumps(message))


# ============================================================================
# Message Queue / Pub-Sub
# ============================================================================

class MessageQueueClient:
    """Message queue client (e.g., RabbitMQ, AWS SQS)"""
    
    def publish_message(self, queue_name: str, message: Dict) -> bool:
        """Publish to queue - should be logged"""
        # SERVICE DEPENDENCY: Message queue publish
        response = requests.post(
            f"http://rabbitmq.example.com/api/exchanges/%2F/amq.default/publish",
            json={
                'routing_key': queue_name,
                'payload': json.dumps(message),
                'properties': {}
            }
        )
        return response.status_code == 200
    
    def consume_messages(self, queue_name: str) -> List[Dict]:
        """Consume from queue - should be logged"""
        # SERVICE DEPENDENCY: Message queue consume
        response = requests.get(
            f"http://rabbitmq.example.com/api/queues/%2F/{queue_name}/get",
            json={'count': 10, 'ackmode': 'ack_requeue_false'}
        )
        return response.json()


class KafkaProducer:
    """Kafka producer client"""
    
    def send_event(self, topic: str, event: Dict) -> bool:
        """Send event to Kafka - should be logged"""
        # SERVICE DEPENDENCY: Kafka publish
        # In real code: from kafka import KafkaProducer
        # producer.send(topic, value=json.dumps(event).encode('utf-8'))
        return True


# ============================================================================
# Cloud Service APIs (AWS, Azure, GCP)
# ============================================================================

class AWSServices:
    """AWS service integrations"""
    
    def upload_to_s3(self, bucket: str, key: str, data: bytes) -> bool:
        """Upload to S3 - should be logged"""
        # SERVICE DEPENDENCY: AWS S3 API
        response = requests.put(
            f"https://{bucket}.s3.amazonaws.com/{key}",
            data=data,
            headers={'Content-Type': 'application/octet-stream'}
        )
        return response.status_code == 200
    
    def send_sns_notification(self, topic_arn: str, message: str) -> Dict:
        """Send SNS notification - should be logged"""
        # SERVICE DEPENDENCY: AWS SNS API
        response = requests.post(
            "https://sns.us-east-1.amazonaws.com/",
            data={
                'Action': 'Publish',
                'TopicArn': topic_arn,
                'Message': message
            }
        )
        return response.json()
    
    def invoke_lambda(self, function_name: str, payload: Dict) -> Dict:
        """Invoke Lambda function - should be logged"""
        # SERVICE DEPENDENCY: AWS Lambda API
        response = requests.post(
            f"https://lambda.us-east-1.amazonaws.com/2015-03-31/functions/{function_name}/invocations",
            json=payload
        )
        return response.json()


class AzureServices:
    """Azure service integrations"""
    
    def store_blob(self, container: str, blob_name: str, data: bytes) -> bool:
        """Store blob in Azure - should be logged"""
        # SERVICE DEPENDENCY: Azure Blob Storage
        response = requests.put(
            f"https://storageaccount.blob.core.windows.net/{container}/{blob_name}",
            data=data,
            headers={'x-ms-blob-type': 'BlockBlob'}
        )
        return response.status_code == 201


# ============================================================================
# Database HTTP APIs (Firebase, MongoDB Atlas)
# ============================================================================

class FirebaseClient:
    """Firebase Realtime Database client"""
    
    def __init__(self, project_id: str):
        self.base_url = f"https://{project_id}.firebaseio.com"
    
    def write_data(self, path: str, data: Dict) -> Dict:
        """Write to Firebase - should be logged"""
        # SERVICE DEPENDENCY: Firebase API
        response = requests.put(
            f"{self.base_url}/{path}.json",
            json=data
        )
        return response.json()
    
    def read_data(self, path: str) -> Dict:
        """Read from Firebase - should be logged"""
        # SERVICE DEPENDENCY: Firebase API
        response = requests.get(f"{self.base_url}/{path}.json")
        return response.json()


class MongoDBAtlasClient:
    """MongoDB Atlas Data API client"""
    
    def find_documents(self, collection: str, filter_query: Dict) -> List[Dict]:
        """Find documents via Atlas API - should be logged"""
        # SERVICE DEPENDENCY: MongoDB Atlas Data API
        response = requests.post(
            "https://data.mongodb-api.com/app/data-abc/endpoint/data/v1/action/find",
            json={
                'collection': collection,
                'database': 'mydb',
                'filter': filter_query
            },
            headers={'api-key': 'your-api-key'}
        )
        return response.json().get('documents', [])


# ============================================================================
# Multi-Service Orchestration
# ============================================================================

class OrderService:
    """Order service that calls multiple dependencies"""
    
    def __init__(self):
        self.user_client = UserServiceClient("http://user-service:8001")
        self.payment_gateway = PaymentGateway("sk_test_123")
        self.email_service = EmailService("SG.123")
        self.sms_service = SMSService()
    
    def create_order(self, user_id: int, items: List[Dict], total: float) -> Dict:
        """Create order - orchestrates multiple service calls"""
        # SERVICE DEPENDENCY 1: Get user details
        user = self.user_client.get_user(user_id)
        
        # SERVICE DEPENDENCY 2: Process payment
        payment_result = self.payment_gateway.process_payment(
            amount=total,
            currency='USD',
            card_token=user.get('payment_token')
        )
        
        if payment_result.get('status') == 'succeeded':
            # SERVICE DEPENDENCY 3: Send confirmation email
            self.email_service.send_email(
                to=user.get('email'),
                subject='Order Confirmation',
                body=f'Your order has been confirmed. Total: ${total}'
            )
            
            # SERVICE DEPENDENCY 4: Send SMS notification
            self.sms_service.send_sms(
                phone=user.get('phone'),
                message=f'Order confirmed! Total: ${total}'
            )
        
        return {
            'order_id': '12345',
            'status': 'confirmed',
            'user': user,
            'payment': payment_result
        }


if __name__ == "__main__":
    print("This file contains service dependencies for testing Tool 5: Service Dependency Detection")
    print("\nExpected Detections:")
    print("- 10+ HTTP REST API calls (GET, POST, PUT, DELETE)")
    print("- 5+ External API integrations (Stripe, SendGrid, Twilio)")
    print("- 3+ Async HTTP calls (aiohttp)")
    print("- 2+ GraphQL operations")
    print("- 2+ gRPC calls")
    print("- 2+ WebSocket connections")
    print("- 3+ Message queue operations")
    print("- 5+ Cloud service APIs (AWS S3, SNS, Lambda, Azure)")
    print("- 2+ Database HTTP APIs (Firebase, MongoDB Atlas)")
    print("- Multi-service orchestration example")
