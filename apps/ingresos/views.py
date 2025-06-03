# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Remito
from .forms import RemitoForm

def listar_remitos(request):
    remitos = Remito.objects.all()
    return render(request, 'remitos/listar.html', {'remitos': remitos})

def crear_remito(request):
    if request.method == 'POST':
        form = RemitoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_remitos')
    else:
        form = RemitoForm()
    return render(request, 'remitos/formulario.html', {'form': form})

def editar_remito(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    if request.method == 'POST':
        form = RemitoForm(request.POST, instance=remito)
        if form.is_valid():
            form.save()
            return redirect('listar_remitos')
    else:
        form = RemitoForm(instance=remito)
    return render(request, 'remitos/formulario.html', {'form': form})

def eliminar_remito(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    if request.method == 'POST':
        remito.delete()
        return redirect('listar_remitos')
    return render(request, 'remitos/confirmar_eliminar.html', {'remito': remito})
