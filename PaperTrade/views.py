# PaperTrade/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Fund, Order, Position, Trade, All_Ticker
from .forms import OrderForm
from django.http import JsonResponse
from Home.yahoo_pull import get_instrument_past_data  # Ensure this function exists and works correctly
from django.utils import timezone
from decimal import Decimal
from django.db import transaction

@login_required
def synth_paper_broker(request):
    user = request.user

    # Get or create Fund
    fund, created = Fund.objects.get_or_create(user=user)

    # Get user's positions
    positions = Position.objects.filter(user=user)

    # Get user's orders
    orders = Order.objects.filter(user=user).order_by('-created_at')

    # Handle Buy/Sell Orders
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():  # Ensure atomicity
                order = form.save(commit=False)
                order.user = user

                # Fetch current stock price using yfinance or a similar service
                ticker_symbol = order.ticker.symbol
                stock_data = get_instrument_past_data(ticker_symbol, period='1d')  # Ensure this returns correct data
                if 'historical_data' in stock_data and stock_data['historical_data']:
                    # Assuming 'Close' is the latest price
                    current_price = Decimal(str(stock_data['historical_data'][-1]['Close']))
                    order.price = current_price
                    order.status = 'EXECUTED'
                    order.save()

                    # Update Fund and Position based on order type
                    if order.order_type == 'BUY':
                        total_cost = Decimal(order.quantity) * order.price
                        if fund.balance >= total_cost:
                            fund.balance -= total_cost
                            fund.save()

                            # Update or create Position
                            position, pos_created = Position.objects.get_or_create(user=user, ticker=order.ticker)
                            total_quantity = Decimal(position.quantity) + Decimal(order.quantity)
                            if total_quantity:
                                position.average_price = ((position.average_price * Decimal(position.quantity)) + (order.price * Decimal(order.quantity))) / total_quantity
                            position.quantity = total_quantity
                            position.current_price = order.price
                            position.save()
                            messages.success(request, f"Bought {order.quantity} shares of {ticker_symbol} at ${order.price}")
                        else:
                            messages.error(request, "Insufficient funds to execute the buy order.")
                            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                return JsonResponse({'status': 'error', 'message': "Insufficient funds to execute the buy order."})
                            return redirect('synth_paper_broker')

                    elif order.order_type == 'SELL':
                        # Check if user has enough shares to sell
                        try:
                            position = Position.objects.get(user=user, ticker=order.ticker)
                            if position.quantity >= order.quantity:
                                position.quantity -= Decimal(order.quantity)
                                position.current_price = order.price
                                # Calculate P&L
                                pnl = (order.price - position.average_price) * Decimal(order.quantity)
                                position.pnl += pnl
                                position.save()

                                # Update Fund
                                total_revenue = Decimal(order.quantity) * order.price
                                fund.balance += total_revenue
                                fund.save()

                                messages.success(request, f"Sold {order.quantity} shares of {ticker_symbol} at ${order.price}")
                            else:
                                messages.error(request, "Insufficient shares to execute the sell order.")
                                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                    return JsonResponse({'status': 'error', 'message': "Insufficient shares to execute the sell order."})
                                return redirect('synth_paper_broker')
                        except Position.DoesNotExist:
                            messages.error(request, "You don't own any shares of this stock.")
                            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                return JsonResponse({'status': 'error', 'message': "You don't own any shares of this stock."})
                            return redirect('synth_paper_broker')

                    # Log the trade
                    Trade.objects.create(
                        order=order,
                        executed_quantity=order.quantity,
                        executed_price=order.price,
                        executed_at=timezone.now()
                    )

                    # For AJAX requests, return a success response
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'status': 'success', 'message': 'Order placed successfully.'})

                    # Redirect to prevent duplicate submissions
                    return redirect('synth_paper_broker')

                else:
                    messages.error(request, "Failed to fetch current stock price.")
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'status': 'error', 'message': "Failed to fetch current stock price."})
                    return redirect('synth_paper_broker')
        else:
            # Form is invalid
            print(form.errors)  # Debugging line to print form errors
            # Collect form errors and send as response
            errors = form.errors.get_json_data()
            # Format errors as a list of messages
            error_messages = []
            for field, field_errors in errors.items():
                for error in field_errors:
                    error_messages.append(f"{field.capitalize()}: {error['message']}")
            # Return errors as a single string
            error_string = "\n".join(error_messages)
            messages.error(request, "Invalid form submission.")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': "Invalid form submission.", 'errors': error_string})
            return redirect('synth_paper_broker')
    else:
        form = OrderForm()

    context = {
        'fund': fund,
        'positions': positions,
        'orders': orders,
        'form': form,
    }
    return render(request, 'PaperTrade/synth_paper_broker.html', context)

@login_required
def get_live_stock_prices(request):
    user = request.user
    watchlist = Position.objects.filter(user=user).select_related('ticker')

    live_prices = {}
    for position in watchlist:
        ticker_symbol = position.ticker.symbol
        stock_data = get_instrument_past_data(ticker_symbol, period='1d')
        if 'historical_data' in stock_data and stock_data['historical_data']:
            current_price = Decimal(str(stock_data['historical_data'][-1]['Close']))
            live_prices[ticker_symbol] = float(current_price)
            # Update position's current price and P&L
            position.current_price = current_price
            position.pnl = (current_price - position.average_price) * Decimal(position.quantity)
            position.save()
        else:
            live_prices[ticker_symbol] = None

    return JsonResponse({'live_prices': live_prices})

@login_required
def get_order_book(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    orders_data = [{
        'ticker': order.ticker.symbol,
        'type': order.order_type,
        'quantity': order.quantity,
        'price': float(order.price),
        'status': order.status,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    } for order in orders]

    return JsonResponse({'orders': orders_data})

@login_required
def get_position_book(request):
    user = request.user
    positions = Position.objects.filter(user=user)
    positions_data = [{
        'ticker': position.ticker.symbol,
        'quantity': position.quantity,
        'average_price': float(position.average_price),
        'current_price': float(position.current_price),
        'pnl': float(position.pnl),
    } for position in positions]

    return JsonResponse({'positions': positions_data})
