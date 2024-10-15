# paper_trade/views.py

import requests
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, Position
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.urls import reverse

@login_required
def broker_main(request):
    """
    Display the watchlist with live ticker data.
    """
    api_url = 'http://127.0.0.1:8000/api/v1/market-data-live/home-banner-tickers'
    try:
        response = requests.get(api_url)
        data = response.json()
        stocks = data.get('stocks', [])
    except Exception as e:
        stocks = []
        # Optionally, log the error

    context = {
        'stocks': stocks,
    }
    return render(request, 'paper_trade/paper_broker.html', context)

@login_required
@require_POST
def place_order(request):
    """
    Handle order placement via AJAX.
    """
    user = request.user
    ticker = request.POST.get('ticker')
    order_type = request.POST.get('order_type')
    execution_type = request.POST.get('execution_type')
    price = request.POST.get('price')
    quantity = request.POST.get('quantity')

    # Validate inputs
    if not all([ticker, order_type, execution_type, price, quantity]):
        return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

    try:
        price = Decimal(price)
        quantity = int(quantity)
        if price <= 0 or quantity <= 0:
            raise ValidationError("Price and quantity must be positive.")
    except (ValueError, ValidationError):
        return JsonResponse({'status': 'error', 'message': 'Invalid price or quantity.'})

    funds_needed = price * quantity

    # Create Order
    order = Order.objects.create(
        user=user,
        ticker=ticker,
        order_type=order_type,
        execution_type=execution_type,
        price=price,
        quantity=quantity,
        funds_needed=funds_needed,
    )

    # Mock Order Execution
    # In a real scenario, integrate with a trading API to execute orders
    order.status = 'EXECUTED'
    order.save()

    # Update Positions
    if order_type == 'BUY':
        position, created = Position.objects.get_or_create(user=user, ticker=ticker, defaults={
            'quantity': 0,
            'average_price': price,
            'current_price': price,
        })
        if not created:
            total_cost = (position.average_price * position.quantity) + (price * quantity)
            position.quantity += quantity
            position.average_price = total_cost / position.quantity
        else:
            position.quantity = quantity
        position.current_price = price
    elif order_type == 'SELL':
        try:
            position = Position.objects.get(user=user, ticker=ticker)
            if quantity > position.quantity:
                return JsonResponse({'status': 'error', 'message': 'Insufficient quantity to sell.'})
            position.quantity -= quantity
            if position.quantity == 0:
                position.average_price = Decimal('0.00')
            position.current_price = price
        except Position.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No existing position to sell.'})

    # Calculate P&L
    if order_type == 'BUY':
        position.pnl = (position.current_price - position.average_price) * position.quantity
    elif order_type == 'SELL' and position.quantity > 0:
        position.pnl = (position.current_price - position.average_price) * position.quantity
    elif order_type == 'SELL' and position.quantity == 0:
        position.pnl = Decimal('0.00')

    position.save()

    return JsonResponse({'status': 'success'})

@login_required
def trade_book(request):
    """
    Display the trade book with all orders placed by the user.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'paper_trade/trade_book.html', context)

@login_required
def positions(request):
    """
    Display all current positions of the user.
    """
    positions = Position.objects.filter(user=request.user).order_by('ticker')
    context = {
        'positions': positions,
    }
    return render(request, 'paper_trade/positions.html', context)

@login_required
@require_POST
def exit_position(request):
    """
    Handle exiting a position via AJAX.
    """
    user = request.user
    ticker = request.POST.get('ticker')
    current_price = request.POST.get('current_price')

    if not all([ticker, current_price]):
        return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

    try:
        current_price = Decimal(current_price)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid price format.'})

    try:
        position = Position.objects.get(user=user, ticker=ticker)
        quantity = position.quantity
        if quantity <= 0:
            return JsonResponse({'status': 'error', 'message': 'No position to exit.'})

        # Create SELL Order to exit position
        order = Order.objects.create(
            user=user,
            ticker=ticker,
            order_type='SELL',
            execution_type='MARKET',
            price=current_price,
            quantity=quantity,
            funds_needed=current_price * quantity,
            status='EXECUTED',
        )

        # Update Position
        position.quantity = 0
        position.average_price = Decimal('0.00')
        position.current_price = current_price
        position.pnl = Decimal('0.00')
        position.save()

        return JsonResponse({'status': 'success'})
    except Position.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Position does not exist.'})
