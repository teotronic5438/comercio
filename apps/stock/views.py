from django.shortcuts import render,HttpResponse
from .models import StockProductos
from .models import Depositos
# Create your views here.
def stock(request):
    productos = StockProductos.objects.all()
    # return HttpResponse("<h1>Stock</h1>")
    return render(request, 'stock.html', {'productos': productos})

def stock_deposito(request):
    depositos = Depositos.objects.all()
    # return HttpResponse("<h1>Deposito</h1>")
    return render(request, 'deposito.html', {'depositos': depositos})