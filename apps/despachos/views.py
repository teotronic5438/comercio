# apps/despachos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now 
from django.views import View 
from apps.ordenes.models import Ordenes, Estados, Destinos
from django.db.models import Q 

# Asegúrate de que tus modelos se llamen 'Pallet' y 'DetallePallet'.
# Si están en otra app (ej. apps/almacen/models.py), ajusta la importación.
from apps.despachos.models import Pallet, DetallePallet 


# --- CLASE-BASADA EN VISTA BASE (Para reutilizar lógica común de filtrado y búsqueda) ---
class BaseOrdenesDespachoView(View):
    template_name = 'despachos/ordenes_despacho_base.html' 
    destino_base_nombre = None 
    titulo_pagina = "Órdenes" 

    def get_queryset(self):
        estados_map = {estado.nombre_estado.lower(): estado for estado in Estados.objects.all()}
        destinos_map = {destino.nombre_destino.lower(): destino for destino in Destinos.objects.all()}

        # Siempre buscamos órdenes que están en estado 'Revisado'
        # y que tienen un destino específico (Nuevo, Averia, Destruccion)
        estado_revisado_obj = estados_map.get('revisado') # Se busca el objeto Estado 'Revisado'
        destino_obj = destinos_map.get(self.destino_base_nombre) # Se busca el objeto Destino según la subclase

        print(f"DEBUG: En {self.__class__.__name__}")
        print(f"DEBUG: Estado base buscado: 'revisado', Objeto: {estado_revisado_obj.id if estado_revisado_obj else 'N/A'}")
        print(f"DEBUG: Destino base buscado: '{self.destino_base_nombre}', Objeto: {destino_obj.id if destino_obj else 'N/A'}")

        if not estado_revisado_obj:
            messages.error(self.request, "El estado 'Revisado' no está configurado en la base de datos.")
            print(f"DEBUG: ERROR - Estado 'Revisado' no encontrado.")
            return Ordenes.objects.none()
        
        if not destino_obj:
            messages.error(self.request, f"El destino '{self.destino_base_nombre}' no está configurado en la base de datos.")
            print(f"DEBUG: ERROR - Destino '{self.destino_base_nombre}' no encontrado.")
            return Ordenes.objects.none()

        # Filtro principal: estado 'Revisado' Y el destino_base_nombre específico
        queryset = Ordenes.objects.filter(
            estado_id=estado_revisado_obj, 
            destino=destino_obj
        ).select_related(
            'destino', 'equipo_id', 'equipo_id__producto_id', 'estado_id'
        ).order_by('-fecha_creacion')
        
        print(f"DEBUG: Queryset resultante (antes de búsqueda si aplica): {queryset.count()} órdenes")

        return queryset

    def get_context_data(self, request, queryset, mensaje_busqueda=None):
        datos_ordenes = []
        for orden in queryset:
            equipo_obj = orden.equipo_id
            producto_obj = equipo_obj.producto_id if equipo_obj else None
            
            producto_modelo = producto_obj.modelo if producto_obj and hasattr(producto_obj, 'modelo') else 'N/A'
            producto_marca = producto_obj.marca if producto_obj and hasattr(producto_obj, 'marca') else 'N/A'
            
            nombre_destino = orden.destino.nombre_destino if orden.destino else 'Sin asignar'
            
            datos_ordenes.append({
                'id': orden.id,
                'equipo_id': orden.equipo_id, 
                'numero_serie': equipo_obj.numero_serie if equipo_obj else 'N/A', 
                'modelo': producto_modelo,
                'marca': producto_marca,
                'fecha_creacion': orden.fecha_creacion,
                'estado': orden.estado_id.nombre_estado,
                'destino': nombre_destino,
                'falla_detectada': orden.falla_detectada,
                'reparacion': orden.reparacion,
                'fecha_revision': orden.fecha_revision,
            })
        
        print(f"DEBUG: Número de órdenes para mostrar en el template (datos_ordenes): {len(datos_ordenes)}")

        destinos_disponibles = Destinos.objects.all().order_by('nombre_destino')
        estados_disponibles = Estados.objects.all().order_by('nombre_estado')

        context = {
            'ordenes': datos_ordenes,
            'mensaje_busqueda': mensaje_busqueda,
            'query_actual': request.GET.get('q', ''),
            'titulo_pagina': self.titulo_pagina, 
            'destinos_disponibles': destinos_disponibles, 
            'estados_disponibles': estados_disponibles, 
            'mostrar_boton_armar_pallet': bool(datos_ordenes), 
            'max_items_pallet': 15, 
        }
        return context

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset() 
        query = request.GET.get('q', '')
        mensaje_busqueda = None

        if query:
            q_objects = Q(id__icontains=query) | Q(equipo_id__numero_serie__icontains=query)
            queryset = queryset.filter(q_objects)
            
            if not queryset.exists():
                mensaje_busqueda = f"No se encontraron órdenes con el ID/Número de Serie '{query}'."
        
        context = self.get_context_data(request, queryset, mensaje_busqueda)
        return render(request, self.template_name, context)


# --- VISTA PARA ÓRDENES REVISADAS (PUNTO DE PARTIDA PARA EL DESPACHO INICIAL) ---
class OrdenesRevisadasView(View):
    template_name = 'despachos/revisadas.html' 
    
    def get(self, request, *args, **kwargs):
        estados_map = {estado.nombre_estado.lower(): estado for estado in Estados.objects.all()}
        destinos_map = {destino.nombre_destino.lower(): destino for destino in Destinos.objects.all()}
        
        query = request.GET.get('q', '') 
        filtro_destino_param = request.GET.get('filtro_destino', 'todos') 

        estado_revisado_obj = estados_map.get('revisado')

        if not estado_revisado_obj:
            messages.error(request, "El estado 'Revisado' no está configurado en la base de datos. Por favor, créalo.")
            return render(request, self.template_name, {
                'ordenes': [], 
                'error_estado': "Estado 'Revisado' no encontrado.",
                'query_actual': query,
                'filtro_destino_seleccionado': filtro_destino_param,
                'destinos_para_filtro': Destinos.objects.all().order_by('nombre_destino'), 
                'destinos_para_despacho': Destinos.objects.all().order_by('nombre_destino'), # Incluye todos los destinos disponibles para despacho
                'mostrar_boton_despacho': False, 
                'titulo_pagina': 'Órdenes Revisadas',
            })

        ordenes_queryset = Ordenes.objects.filter(estado_id=estado_revisado_obj).select_related(
            'destino', 'equipo_id', 'equipo_id__producto_id', 'estado_id'
        ).order_by('-fecha_creacion')

        # Si se filtra por destino en la vista de Revisadas
        if filtro_destino_param and filtro_destino_param != 'todos':
            destino_obj_filtro = destinos_map.get(filtro_destino_param) # Busca el destino por el nombre exacto
            if destino_obj_filtro:
                ordenes_queryset = ordenes_queryset.filter(destino=destino_obj_filtro)
            else:
                messages.warning(request, f"El destino '{filtro_destino_param}' no es un filtro válido.")

        mensaje_busqueda = None
        if query:
            q_objects = Q(id__icontains=query) | Q(equipo_id__numero_serie__icontains=query)
            ordenes_queryset = ordenes_queryset.filter(q_objects)
            
            if not ordenes_queryset.exists():
                mensaje_busqueda = f"No se encontraron órdenes con el ID/Número de Serie '{query}'."
        
        datos_ordenes = []
        if ordenes_queryset.exists():
            for orden in ordenes_queryset:
                equipo_obj = orden.equipo_id
                producto_obj = equipo_obj.producto_id if equipo_obj else None
                
                producto_modelo = producto_obj.modelo if producto_obj and hasattr(producto_obj, 'modelo') else 'N/A'
                producto_marca = producto_obj.marca if producto_obj and hasattr(producto_obj, 'marca') else 'N/A'
                
                nombre_destino = orden.destino.nombre_destino if orden.destino else 'Sin asignar'
                
                datos_ordenes.append({
                    'id': orden.id,
                    'equipo_id': orden.equipo_id, 
                    'numero_serie': equipo_obj.numero_serie if equipo_obj else 'N/A', 
                    'modelo': producto_modelo,
                    'marca': producto_marca,
                    'fecha_creacion': orden.fecha_creacion,
                    'estado': orden.estado_id.nombre_estado,
                    'destino': nombre_destino,
                    'falla_detectada': orden.falla_detectada,
                    'reparacion': orden.reparacion,
                    'fecha_revision': orden.fecha_revision,
                })
        
        destinos_para_despacho = Destinos.objects.all().order_by('nombre_destino') # Todos los destinos disponibles para el dropdown de despacho

        context = {
            'ordenes': datos_ordenes,
            'mensaje_busqueda': mensaje_busqueda,
            'query_actual': query,
            'filtro_destino_seleccionado': filtro_destino_param,
            'destinos_para_filtro': Destinos.objects.all().order_by('nombre_destino'), 
            'destinos_para_despacho': destinos_para_despacho, 
            'mostrar_boton_despacho': bool(datos_ordenes), 
            'titulo_pagina': 'Órdenes Revisadas', 
        }
        return render(request, self.template_name, context)

# --- VISTAS PARA ÓRDENES CON ESTADO REVISADO Y UN DESTINO ESPECÍFICO (PARA EL ARMADO DE PALLETS) ---

class OrdenesNuevasView(BaseOrdenesDespachoView):
    template_name = 'despachos/ordenes_nuevas.html' 
    destino_base_nombre = 'nuevo' 
    titulo_pagina = 'Órdenes Nuevas para Despacho'

class OrdenesAveriadasView(BaseOrdenesDespachoView):
    template_name = 'despachos/ordenes_averiadas.html'
    destino_base_nombre = 'averia' 
    titulo_pagina = 'Órdenes Averiadas para Despacho'

class OrdenesDestruidasView(BaseOrdenesDespachoView):
    template_name = 'despachos/ordenes_destruidas.html'
    destino_base_nombre = 'destruccion' 
    titulo_pagina = 'Órdenes de Destrucción para Despacho'


# --- CLASE-BASADA EN VISTA PARA PROCESAR EL CAMBIO DE ESTADO/DESTINO (desde Revisadas) ---
class ProcesarDespachoOrdenesView(View):
    def post(self, request, *args, **kwargs):
        ordenes_ids = request.POST.getlist('orden_ids')
        destino_id = request.POST.get('destino_id_despacho') 
        
        return_url_name = request.POST.get('return_url_name', 'despachos:ordenes_revisadas') 

        if not ordenes_ids:
            messages.error(request, "No se seleccionó ninguna orden para despachar.")
            return redirect(return_url_name)
        
        if not destino_id:
            messages.error(request, "No se seleccionó ningún destino de despacho.")
            return redirect(return_url_name)

        try:
            destino_obj = get_object_or_404(Destinos, id=destino_id) 
            
            # El estado de las órdenes que se despachan SIEMPRE será 'Revisado'
            # Es el DESTINO lo que cambia.
            estado_revisado_obj = get_object_or_404(Estados, nombre_estado__iexact='revisado')
            
            updated_count = 0
            for orden_id in ordenes_ids:
                try:
                    orden = Ordenes.objects.get(id=orden_id)
                    # Solo actualiza si el destino actual es diferente, y asegúrate de mantener el estado 'Revisado'
                    if orden.destino != destino_obj:
                        orden.destino = destino_obj
                        orden.estado_id = estado_revisado_obj # Mantiene el estado en 'Revisado'
                        orden.save()
                        updated_count += 1
                except Ordenes.DoesNotExist:
                    messages.warning(request, f"La orden con ID {orden_id} no existe y no pudo ser procesada.")
            
            messages.success(request, f"{updated_count} órdenes enviadas exitosamente a {destino_obj.nombre_destino}.")
            
            # Redirigimos a la vista de Revisadas con el filtro aplicado al destino al que se envió
            filtro_destino_param_redirect = destino_obj.nombre_destino.lower() 
            return redirect(f"{return_url_name}?filtro_destino={filtro_destino_param_redirect}")

        except Destinos.DoesNotExist: 
            messages.error(request, "El destino de despacho seleccionado no es válido.")
            return redirect(return_url_name)
        except Estados.DoesNotExist: 
            messages.error(request, "El estado 'Revisado' no está configurado en la base de datos. Por favor, créalo.")
            return redirect(return_url_name)
        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar las órdenes: {e}")
            return redirect(return_url_name)