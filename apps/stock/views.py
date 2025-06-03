from django.shortcuts import render,HttpResponse
from .models import Stock

# Create your views here.
def stock(request):
    productos = Stock.objects.all()
    # return HttpResponse("<h1>Stock</h1>")
    return render(request, 'stock.html', {'productos': productos})
