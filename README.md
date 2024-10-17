# Django Real-Time Notification App

This project is a basic Django application that implements real-time notifications using Django Channels and WebSockets. It allows clients to connect via WebSockets and receive real-time updates when a notification is created.

## Features

- Real-time notifications using WebSockets.
- Clients can subscribe to notifications via WebSocket connections.
- Notifications are broadcasted to all connected clients when created.
- Utilizes Django Channels and Redis as the message broker.

## Requirements

To run this project, you'll need the following installed:

- Python 3.8+
- Django 4.x+
- Django Channels 4.x+
- Redis server (for channel layers) (For production)
- Daphne (ASGI server)

## Installation

1.  Clone the repository to your local machine:

    ```bash
    git clone https://github.com/davidinmichael/notification_app.git
    cd notification_app

    ```

2.  Set up a virtual environment and activate it:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4.  Set up Redis for your channel layers. Make sure you have Redis running and configured in your settings (For production):

        ```python
        # In settings.py
        CHANNEL_LAYERS = {
            "default": {
                "BACKEND": "channels_redis.core.RedisChannelLayer",
                "CONFIG": {
                    "hosts": [("127.0.0.1", 6379)],
                },
            },
        }
        ```
        # in Development

        ```python
        CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }

    }

        ````

5.  Apply the database migrations:

    ```bash
    python manage.py migrate
    ```

6.  Run the Redis server: (Ignore if not using redis)

    If Redis is installed on your local machine, you can run it using:

    ```bash
    redis-server
    ```

## Running the Application

To run the application:

1. Start the Django development server with Daphne:

   ```bash
   daphne -b 127.0.0.1 -p 8000 notification_app.asgi:application
   ```

   or add the daphne in installed apps and run the server as usuall -

   ```bash
   python manage.py runserver
   ```

2. Navigate to the WebSocket client and connect to:

   ```
   ws://127.0.0.1:8000/ws/notifications/
   ```

3. To test notifications, you can create a notification via the API. Here's an example using Postman or cURL:

   **GET** to `http://127.0.0.1:8000/`:

   ```bash
   curl -X POST http://127.0.0.1:8000/ \
   -H 'Content-Type: application/json' \
   -d '{"message": "New notification created!"}'
   ```

4. Any connected WebSocket clients will immediately receive the notification message in real-time.

## File Structure

- `asgi.py`: Configures Django to work with ASGI and Channels.
- `routing.py`: Defines the WebSocket URL routing.
- `consumers.py`: Contains the `NotificationConsumer` which handles WebSocket connections and sending notifications.
- `views.py`: Defines API endpoints for creating notifications.

## Example Consumer Code

Here’s a quick overview of the core WebSocket logic in `NotificationConsumer`:

```python
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "notifications", self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "notifications", self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        await self.channel_layer.group_send(
            "notifications",
            {
                "type": "send_notification",
                "message": message,
            }
        )

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))
```
