from django.shortcuts import render,HttpResponse
from .models import Stock
from .models import Deposito
# Create your views here.
def stock(request):
    productos = Stock.objects.all()
    # return HttpResponse("<h1>Stock</h1>")
    return render(request, 'stock.html', {'productos': productos})

def stock_deposito(request):
    depositos = Deposito.objects.all()
    # return HttpResponse("<h1>Deposito</h1>")
    return render(request, 'deposito.html', {'depositos': depositos})