from datetime import datetime

from django.contrib.auth import get_user_model

from db.models import Order, Ticket

from django.db import transaction


def create_order(tickets: list, username: str, date: datetime = None) -> list:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()
        for item in tickets:
            Ticket.objects.create(
                movie_session_id=item["movie_session"],
                order=order,
                row=item["row"],
                seat=item["seat"]
            )
        return order


def get_orders(username: str = None) -> list:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
