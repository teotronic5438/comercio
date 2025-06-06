# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Remitos
from .forms import RemitoForm

def listar_remitos(request):
    remitos = Remitos.objects.filter(aprobado=False)
    return render(request, 'listar.html', {'remitos': remitos, 'show_navbar': True})

def listar_remitos_hitorial(request):
    remitos = Remitos.objects.filter(aprobado=True)
    return render(request, 'listar_historial.html', {'remitos': remitos, 'show_navbar': True})

def crear_remito(request):
    if request.method == 'POST':
        form = RemitoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingresos')
    else:
        form = RemitoForm()
    return render(request, 'formulario.html', {'form': form, 'show_navbar': True})

def editar_remito(request, pk):
    remito = get_object_or_404(Remitos, pk=pk)
    if request.method == 'POST':
        form = RemitoForm(request.POST, instance=remito)
        if form.is_valid():
            form.save()
            return redirect('ingresos')
    else:
        form = RemitoForm(instance=remito)
    return render(request, 'formulario.html', {'form': form, 'show_navbar': True})

def aprobar_remito(request, pk):
    remito = get_object_or_404(Remitos, pk=pk)
    
    if remito.aprobado == False:
        remito.aprobado = True
        remito.save()
        return redirect('ingresos')
    else:
        return redirect('ingresos')


def eliminar_remito(request, pk):
    remito = get_object_or_404(Remitos, pk=pk)
    if request.method == 'POST':
        remito.delete()
        return redirect('ingresos')
    return render(request, 'confirmar_eliminar.html', {'remito': remito, 'show_navbar': True})
