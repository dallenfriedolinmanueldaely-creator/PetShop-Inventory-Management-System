from .models import Product
from .constants import LOW_STOCK_THRESHOLD


def stock_alerts(request):
    if not request.user.is_authenticated:
        return {
            'low_stock_count': 0,
            'out_of_stock_count': 0,
        }

    try:
        low_stock_count = Product.objects.filter(
            stock__gt=0, stock__lte=LOW_STOCK_THRESHOLD
        ).count()
        out_of_stock_count = Product.objects.filter(stock=0).count()
    except Exception:
        low_stock_count = 0
        out_of_stock_count = 0

    return {
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
    }
