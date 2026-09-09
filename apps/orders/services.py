import logging
from firebase_admin import messaging

logger = logging.getLogger(__name__)

def send_order_status_notification(user, order):
    """Sends FCM push notification to the user when their order status changes."""
    if not user or not getattr(user, 'device_token', None):
        return

    # Clean status string for user display (e.g. IN_PROGRESS -> In Progress)
    formatted_status = order.status.replace("_", " ").title()

    title = "Order Status Updated"
    body = f"Your order #{order.id} status is now {formatted_status}."

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data={
            "order_id": str(order.id),
            "status": str(order.status),
            "type": "ORDER_STATUS_UPDATE",
        },
        token=user.device_token,
    )

    try:
        response = messaging.send(message)
        logger.info(f"Notification sent for order {order.id}: {response}")
    except Exception as e:
        # Prevent notification failures from crashing the API request
        logger.error(f"Failed to send FCM notification for order {order.id}: {e}")