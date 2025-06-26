# apps/despachos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.views import View
from apps.ordenes.models import Ordenes, Estados, Destinos
from django.db.models import Q, Count # <-- Importamos Count directamente aquí también
from django.urls import reverse
from apps.despachos.models import Pallet, DetallePallet
from collections import defaultdict
from django.db import models # <-- ¡IMPORTACIÓN CRUCIAL AÑADIDA!

# --- CLASE-BASADA EN VISTA BASE (Para reutilizar lógica común de filtrado y búsqueda en vistas de visualización de pallets) ---
class BaseOrdenesDespachoView(View):
    template_name = 'despachos/ordenes_despacho_base.html'
    destino_base_nombre = None
    titulo_pagina = "Órdenes Palletizadas"

    def get_queryset(self):
        estado_palletizado_obj = Estados.objects.filter(nombre_estado__iexact='palletizado').first()
        estado_despachado_pallet_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first()
        destino_obj = Destinos.objects.filter(nombre_destino__iexact=self.destino_base_nombre).first()

        if not estado_palletizado_obj:
            messages.error(self.request, "El estado 'Palletizado' no está configurado en la base de datos (modelo Estados). Por favor, créalo en el panel de administración.")
            return Ordenes.objects.none()

        if not destino_obj:
            messages.error(self.request, f"El destino '{self.destino_base_nombre}' no está configurado en la base de datos (modelo Destinos). Por favor, créalo en el panel de administración.")
            return Ordenes.objects.none()

        # Filtrar órdenes que están en estado 'Palletizado' y en el destino base,
        # y cuyo PALLET NO esté en estado 'Despachado'.
        queryset = Ordenes.objects.filter(
            estado_id=estado_palletizado_obj,
            destino=destino_obj,
            detalle_pallet__pallet__isnull=False # Asegura que la orden esté en un pallet
        )

        if estado_despachado_pallet_obj:
            queryset = queryset.exclude(detalle_pallet__pallet__estado_pallet=estado_despachado_pallet_obj)

        queryset = queryset.select_related(
            'destino', 'equipo_id', 'equipo_id__producto_id', 'estado_id',
            'detalle_pallet', 'detalle_pallet__pallet', 'detalle_pallet__pallet__estado_pallet'
        ).order_by('detalle_pallet__pallet__nro_pallet', 'fecha_creacion')

        return queryset

    def get_context_data(self, request, queryset, mensaje_busqueda=None):
        pallets_agrupados = defaultdict(lambda: {
            'id': None,
            'nro_pallet': 'N/A',
            'destino': 'N/A',
            'fecha_creacion': None,
            'estado_pallet': 'N/A',
            'ordenes': []
        })

        for orden in queryset:
            equipo_obj = orden.equipo_id
            producto_obj = equipo_obj.producto_id if equipo_obj else None

            producto_modelo = producto_obj.modelo if producto_obj and hasattr(producto_obj, 'modelo') else 'N/A'
            producto_marca = producto_obj.marca if producto_obj and hasattr(producto_obj, 'marca') else 'N/A'

            nombre_destino = orden.destino.nombre_destino if orden.destino else 'Sin asignar'
            nombre_estado = orden.estado_id.nombre_estado if orden.estado_id else 'Sin estado'

            if hasattr(orden, 'detalle_pallet') and orden.detalle_pallet and orden.detalle_pallet.pallet:
                pallet_obj = orden.detalle_pallet.pallet
                pallet_id = pallet_obj.id
                pallet_info = {
                    'id': pallet_obj.id,
                    'nro_pallet': pallet_obj.nro_pallet,
                    'destino': pallet_obj.destino.nombre_destino if pallet_obj.destino else 'N/A',
                    'fecha_creacion': pallet_obj.fecha_creacion,
                    'estado_pallet': pallet_obj.estado_pallet.nombre_estado if pallet_obj.estado_pallet else 'N/A',
                }

                if pallets_agrupados[pallet_id]['id'] is None:
                    pallets_agrupados[pallet_id].update(pallet_info)

                pallets_agrupados[pallet_id]['ordenes'].append({
                    'id': orden.id,
                    'numero_serie': equipo_obj.numero_serie if equipo_obj else 'N/A',
                    'modelo': producto_modelo,
                    'marca': producto_marca,
                    'fecha_creacion': orden.fecha_creacion,
                    'estado': nombre_estado,
                    'destino': nombre_destino,
                    'falla_detectada': orden.falla_detectada,
                    'reparacion': orden.reparacion,
                    'fecha_revision': orden.fecha_revision,
                })

        lista_pallets = sorted(list(pallets_agrupados.values()), key=lambda p: p['nro_pallet'] if p['nro_pallet'] != 'N/A' else '')

        context = {
            'pallets_activos': lista_pallets,
            'mensaje_busqueda': mensaje_busqueda,
            'query_actual': request.GET.get('q', ''),
            'titulo_pagina': self.titulo_pagina,
            'destinos_disponibles': Destinos.objects.all().order_by('nombre_destino'),
            'estados_disponibles': Estados.objects.all().order_by('nombre_estado'),
            'mostrar_boton_armar_pallet': False,
            'max_items_pallet': 15,
            'despachar_pallet_url': reverse('despachos:despachar_pallet'),
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


# --- VISTA PARA ÓRDENES REVISADAS (PUNTO DE PARTIDA PARA LA ASIGNACIÓN DE DESTINO Y PALLETIZADO) ---
class OrdenesRevisadasView(View):
    template_name = 'despachos/revisadas.html'

    def get(self, request, *args, **kwargs):
        estado_revisado_obj = Estados.objects.filter(nombre_estado__iexact='revisado').first()

        if not estado_revisado_obj:
            messages.error(request, "El estado 'Revisado' no está configurado en la base de datos (modelo Estados). Por favor, créalo en el panel de administración.")
            return render(request, self.template_name, {
                'ordenes': [],
                'error_estado': "Estado 'Revisado' no encontrado.",
                'query_actual': request.GET.get('q', ''),
                'filtro_destino_seleccionado': request.GET.get('filtro_destino', 'todos'),
                'destinos_para_filtro': Destinos.objects.all().order_by('nombre_destino'),
                'destinos_para_despacho': Destinos.objects.all().order_by('nombre_destino'),
                'mostrar_boton_despacho': False,
                'titulo_pagina': 'Órdenes Revisadas',
            })

        ordenes_queryset = Ordenes.objects.filter(estado_id=estado_revisado_obj).select_related(
            'destino', 'equipo_id', 'equipo_id__producto_id', 'estado_id'
        ).order_by('-fecha_creacion')

        query = request.GET.get('q', '')
        filtro_destino_param = request.GET.get('filtro_destino', 'todos')

        if filtro_destino_param and filtro_destino_param != 'todos':
            destino_obj_filtro = Destinos.objects.filter(nombre_destino__iexact=filtro_destino_param).first()
            if destino_obj_filtro:
                ordenes_queryset = ordenes_queryset.filter(destino=destino_obj_filtro)
            else:
                messages.warning(request, f"El destino '{filtro_destino_param}' no es un filtro válido o no existe en la base de datos.")

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
                nombre_estado = orden.estado_id.nombre_estado if orden.estado_id else 'Sin estado'

                datos_ordenes.append({
                    'id': orden.id,
                    'equipo_id': orden.equipo_id,
                    'numero_serie': equipo_obj.numero_serie if equipo_obj else 'N/A',
                    'modelo': producto_modelo,
                    'marca': producto_marca,
                    'fecha_creacion': orden.fecha_creacion,
                    'estado': nombre_estado,
                    'destino': nombre_destino,
                    'falla_detectada': orden.falla_detectada,
                    'reparacion': orden.reparacion,
                    'fecha_revision': orden.fecha_revision,
                })

        destinos_para_despacho = Destinos.objects.all().order_by('nombre_destino')

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


# --- CLASE-BASADA EN VISTA PARA PROCESAR EL CAMBIO DE ESTADO/DESTINO (desde Revisadas) ---
class ProcesarDespachoOrdenesView(View):
    def post(self, request, *args, **kwargs):
        ordenes_ids = request.POST.getlist('orden_ids')
        destino_id = request.POST.get('destino_id_despacho')
        MAX_ITEMS_PER_PALLET = 15 # Definimos el límite aquí

        if not ordenes_ids:
            messages.error(request, "No se seleccionó ninguna orden para palletizar.")
            return redirect('despachos:ordenes_revisadas')

        # Si se seleccionan más órdenes de la cuenta, informamos al usuario, pero la lógica de 15 por pallet
        # se manejará internamente si se seleccionan más de 15.
        if len(ordenes_ids) > MAX_ITEMS_PER_PALLET:
            messages.warning(request, f"Se seleccionaron {len(ordenes_ids)} órdenes. Se distribuirán en pallets de hasta {MAX_ITEMS_PER_PALLET} ítems cada uno.")

        if not destino_id:
            messages.error(request, "No se seleccionó ningún destino para el pallet.")
            return redirect('despachos:ordenes_revisadas')

        try:
            destino_obj = get_object_or_404(Destinos, id=destino_id)
            estado_palletizado_obj = get_object_or_404(Estados, nombre_estado__iexact='palletizado')
            estado_revisado_obj = get_object_or_404(Estados, nombre_estado__iexact='revisado')
            estado_despachado_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first() # Necesario para excluir pallets despachados

            current_pallet = None # Pallet actual en el que se están agregando órdenes
            updated_count = 0
            pallets_creados_o_actualizados = set() # Para llevar un registro de los pallets afectados

            for orden_id in ordenes_ids:
                try:
                    orden = Ordenes.objects.get(id=orden_id)

                    if orden.estado_id != estado_revisado_obj:
                        messages.warning(request, f"La orden con ID {orden_id} no está en estado 'Revisado' y no pudo ser palletizada. Su estado actual es: {orden.estado_id.nombre_estado}.")
                        continue

                    # Buscar un pallet "activo" (no despachado) para este destino
                    # que tenga menos de MAX_ITEMS_PER_PALLET órdenes.
                    # Excluir pallets que estén en estado 'despachado'
                    active_pallets_for_destination_qs = Pallet.objects.filter(
                        destino=destino_obj
                    ).annotate(
                        item_count=Count('detalles') # Usa Count directamente si ya está importado
                    ).filter(
                        item_count__lt=MAX_ITEMS_PER_PALLET # Que tenga menos de 15 ítems
                    ).order_by('fecha_creacion') # Priorizamos el más antiguo con espacio

                    if estado_despachado_obj:
                        active_pallets_for_destination_qs = active_pallets_for_destination_qs.exclude(
                            estado_pallet=estado_despachado_obj
                        )

                    active_pallet_with_space = active_pallets_for_destination_qs.first()


                    if not current_pallet or current_pallet.detalles.count() >= MAX_ITEMS_PER_PALLET:
                        # Si no hay pallet actual, o el actual está lleno, buscamos uno existente o creamos uno nuevo.
                        if active_pallet_with_space:
                            current_pallet = active_pallet_with_space
                        else:
                            # Si no se encuentra un pallet activo con espacio, crear uno nuevo
                            last_pallet = Pallet.objects.order_by('-id').first()
                            next_pallet_number = 1
                            if last_pallet and last_pallet.nro_pallet and last_pallet.nro_pallet.isdigit():
                                next_pallet_number = int(last_pallet.nro_pallet) + 1
                            generated_nro_pallet = str(next_pallet_number).zfill(4)

                            current_pallet = Pallet.objects.create(
                                destino=destino_obj,
                                fecha_creacion=now(),
                                nro_pallet=generated_nro_pallet,
                                usuario_id=request.user if request.user.is_authenticated else None,
                                estado_pallet=estado_palletizado_obj,
                            )
                            messages.info(request, f"Se ha creado un nuevo pallet: Nro. {current_pallet.nro_pallet} para el destino '{destino_obj.nombre_destino}'.")

                    # 2. Crear DetallePallet para la orden actual en el current_pallet
                    DetallePallet.objects.create(
                        pallet=current_pallet,
                        orden_id=orden,
                        modelo=orden.equipo_id.producto_id.modelo if orden.equipo_id and orden.equipo_id.producto_id else 'N/A',
                        serial=orden.equipo_id.numero_serie if orden.equipo_id else 'N/A',
                        cantidad=1,
                    )

                    # 3. Actualizar el estado de la Orden a 'Palletizado'
                    orden.estado_id = estado_palletizado_obj
                    orden.destino = destino_obj # Aseguramos que la orden tenga el destino del pallet
                    orden.save()
                    updated_count += 1
                    pallets_creados_o_actualizados.add(current_pallet.id) # Registramos el pallet afectado

                except Ordenes.DoesNotExist:
                    messages.warning(request, f"La orden con ID {orden_id} no existe y no pudo ser procesada.")
                except Exception as e:
                    messages.error(request, f"Error al procesar orden {orden_id} para pallet: {e}")

            if updated_count > 0:
                messages.success(request, f"{updated_count} órdenes fueron distribuidas en {len(pallets_creados_o_actualizados)} pallet(s) para destino '{destino_obj.nombre_destino}'.")
            else:
                messages.info(request, "No se procesó ninguna orden para palletizar. Asegúrate de que estén en estado 'Revisado'.")

            return redirect('despachos:ordenes_revisadas')

        except Destinos.DoesNotExist:
            messages.error(request, "El destino de pallet seleccionado no es válido. Asegúrate de que exista en tu base de datos.")
            return redirect('despachos:ordenes_revisadas')
        except Estados.DoesNotExist as e:
            messages.error(request, f"Uno de los estados requeridos no está configurado en la base de datos: {e}. Por favor, créalos en el panel de administración de Django.")
            return redirect('despachos:ordenes_revisadas')
        except Exception as e:
            messages.error(request, f"Ocurrió un error general al procesar el pallet: {e}")
            return redirect('despachos:ordenes_revisadas')


# --- VISTA PARA PROCESAR EL DESPACHO DE UN PALLET COMPLETO ---
class ProcesarDespachoPalletView(View):
    def post(self, request, *args, **kwargs):
        pallet_id = request.POST.get('pallet_id_a_despachar')
        if not pallet_id:
            messages.error(request, "No se recibió el ID del pallet a despachar.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            pallet = get_object_or_404(Pallet, id=pallet_id)

            estado_despachado_pallet_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first()
            if not estado_despachado_pallet_obj:
                messages.error(request, "El estado 'Despachado' para pallets no está configurado en la base de datos (modelo Estados). Por favor, créalo.")
                return redirect(request.META.get('HTTP_REFERER', '/'))

            estado_despachado_orden_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first()
            if not estado_despachado_orden_obj:
                messages.warning(request, "El estado 'Despachado' para órdenes no está configurado. Las órdenes no cambiarán de estado.")

            # Actualizar el estado del Pallet
            pallet.estado_pallet = estado_despachado_pallet_obj
            pallet.fecha_despacho = now()
            pallet.usuario_id = request.user if request.user.is_authenticated else None # Asigna el usuario que despacha
            pallet.save()

            # Actualizar el estado de TODAS las órdenes dentro de este Pallet
            ordenes_actualizadas_count = 0
            for detalle_pallet in pallet.detalles.all():
                orden = detalle_pallet.orden_id
                if orden and estado_despachado_orden_obj:
                    orden.estado_id = estado_despachado_orden_obj
                    orden.save()
                    ordenes_actualizadas_count += 1

            messages.success(request, f"Pallet {pallet.nro_pallet} despachado exitosamente. Se actualizaron {ordenes_actualizadas_count} órdenes.")

        except Pallet.DoesNotExist:
            messages.error(request, f"El pallet con ID {pallet_id} no existe.")
        except Estados.DoesNotExist:
            messages.error(request, "Error: Uno o ambos estados ('Despachado' para pallet u orden) no encontrados en la base de datos.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al despachar el pallet: {e}")

        return redirect(request.META.get('HTTP_REFERER', '/'))


# --- VISTAS PARA ÓRDENES CON ESTADO REVISADO Y UN DESTINO ESPECÍFICO (CON HISTORIAL) ---
class OrdenesNuevasView(BaseOrdenesDespachoView):
    destino_base_nombre = 'nuevo'
    titulo_pagina = 'Órdenes Nuevas Palletizadas'

    def get_context_data(self, request, queryset, mensaje_busqueda=None):
        context = super().get_context_data(request, queryset, mensaje_busqueda) # Obtiene los pallets_activos

        # --- LÓGICA PARA EL HISTORIAL DE PALLETS DESPACHADOS DE ESTE DESTINO ---
        estado_despachado_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first()
        destino_obj = Destinos.objects.filter(nombre_destino__iexact=self.destino_base_nombre).first()

        pallets_despachados = []
        if estado_despachado_obj and destino_obj:
            despachados_queryset = Pallet.objects.filter(
                estado_pallet=estado_despachado_obj,
                destino=destino_obj
            ).select_related(
                'destino', 'estado_pallet', 'usuario_id', 'remito_salida'
            ).prefetch_related(
                'detalles__orden_id__equipo_id__producto_id',
                'detalles__orden_id__estado_id',
                'detalles__orden_id__destino'
            ).order_by('-fecha_despacho')

            for pallet in despachados_queryset:
                ordenes_en_pallet = []
                for detalle_pallet in pallet.detalles.all():
                    orden = detalle_pallet.orden_id
                    if orden:
                        ordenes_en_pallet.append({
                            'id': orden.id,
                            'numero_serie': orden.equipo_id.numero_serie if orden.equipo_id else 'N/A',
                            'modelo': orden.equipo_id.producto_id.modelo if orden.equipo_id and orden.equipo_id.producto_id else 'N/A',
                            'marca': orden.equipo_id.producto_id.marca if orden.equipo_id and orden.equipo_id.producto_id else 'N/A',
                            'estado': orden.estado_id.nombre_estado if orden.estado_id else 'N/A',
                        })

                pallets_despachados.append({
                    'id': pallet.id,
                    'nro_pallet': pallet.nro_pallet,
                    'destino': pallet.destino.nombre_destino if pallet.destino else 'N/A',
                    'fecha_creacion': pallet.fecha_creacion,
                    'fecha_despacho': pallet.fecha_despacho,
                    'estado_pallet': pallet.estado_pallet.nombre_estado,
                    'usuario_despacho': pallet.usuario_id.username if pallet.usuario_id else 'N/A',
                    'remito_salida': pallet.remito_salida.nro_remito if pallet.remito_salida else 'N/A',
                    'cantidad_ordenes': len(ordenes_en_pallet),
                    'ordenes': ordenes_en_pallet,
                })

        context['pallets_despachados'] = pallets_despachados
        context['titulo_historial'] = f"Historial de Pallets Despachados a {self.destino_base_nombre.capitalize()}"
        # --- FIN LÓGICA HISTORIAL ---

        return context

class OrdenesAveriadasView(OrdenesNuevasView):
    destino_base_nombre = 'averia'
    titulo_pagina = 'Órdenes Averiadas Palletizadas'

class OrdenesDestruidasView(OrdenesNuevasView):
    destino_base_nombre = 'destruccion'
    titulo_pagina = 'Órdenes de Destrucción Palletizadas'