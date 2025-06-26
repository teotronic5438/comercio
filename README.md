# 🧠 Enigma ERP - Backend

Este es el backend del sistema Enigma, un ERP modular desarrollado con Django y Django REST Framework. Gestiona productos, equipos, remitos, órdenes de reparación, logística y stock.

## Estructura del Proyecto

    comercio/
    │
    ├── apps/ # Contiene las aplicaciones divididas por etapas
    │   ├── core/       # Funcionalidades base o comunes
    │   ├── usuarios/   # Etapa 1: Roles y usuarios
    │   ├── ingresos/   # Etapa 2: Remitos y productos ingresados
    │   ├── stock/      # Etapa 3: Stock de productos
    │   ├── ordenes/    # Etapa 4: Órdenes, estados y equipos
    │   └── despachos/  # Etapa 5: Pallets y DetallePallets
    │
    ├── seting/ # Configuración principal de Django (settings, urls, wsgi)
    │   ├── init.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── templates/      # Template's globales al proyecto
    │      ├── includes/
    │      │      ├── footer.html
    │      │      ├── header.html
    │      │      └── navbar.html
    │      ├── base.html
    │      └── dashboard.html
    │
    ├── templates/ # Templates globales al proyecto
    │
    ├── manage.py # Script principal para administrar el proyecto
    │
    └── requirements.txt # Dependencias del proyecto


### 🔧 0. PRUEBA CON AUTENTICACION

Primero debemos borrar todas las migraciones hechas

    rm usuarios/migrations/.py
    rm ingresos/migrations/.py
    rm ordenes/migrations/.py
    rm stock/migrations/.py
    rm despachos/migrations/.py

Segundo: Primera migracion debe ser usuarios

    python manage.py makemigrations usuarios    # devuelve la creacion de tabla usuarios y roles

Tercero: Resto de  migraciones

    python manage.py makemigrations     # devuelve la creacion de las otras tablas.

Cuarto: Aplicamos migrate

    python manage.py migrate

Cinco: Si no esta, debe tener las bases de datos.

Verificar que este copiada la base

### 🔧 1. Entorno Virtual

✅ Crear entorno virtual

    python -m venv env

✅ Activarlo

En Windows:

    .\env\Scripts\activate

En Linux/macOS:

    source env/bin/activate

✅ Desactivarlo

    deactivate

### 📦 2. Pip: congelar e instalar dependencias

✅ Generar lista de paquetes

    pip freeze > requirements.txt

✅ Instalar desde requirements.txt

    pip install -r requirements.txt

### 🚀 3. Comandos comunes de Django

✅ Ejecutar servidor

    python manage.py runserver

✅ Crear migraciones a partir de modelos

    python3 manage.py makemigrations

✅ Aplicar migraciones (crear las tablas en la BD)

    python3 manage.py migrate

✅ Entrar al shell interactivo

    python manage.py shell

Ejemplo básico para probar modelos en el shell:

    from apps.usuarios.models import Usuario  # o como se llame tu modelo
    Usuario.objects.all()         # Ver todos los registros
    Usuario.objects.create(nombre='Elías', email='ej@correo.com')  # Crear uno

### 🛠️ 4. Crear proyecto Django

✅ Crear un proyecto nuevo (estructura normal)

    django-admin startproject config

Esto crea:

    config/
    ├── manage.py
    └── config/
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        ├── asgi.py
        └── wsgi.py

### 📁 5. Crear proyecto DENTRO de una carpeta ya creada

✅ Si ya tenés una carpeta vacía (ej: seting) y querés que el proyecto se llame config:

    cd seting
    django-admin startproject config .

El . al final indica que los archivos deben crearse en el directorio actual, no anidar otro más.

### 🧩 6. Crear apps Django

✅ Crear app normalmente

    python manage.py startapp core

Esto genera la carpeta core/ en el mismo nivel que manage.py.

### 📦 7. Crear apps DENTRO de una carpeta apps/

Paso a paso:

1) Crear la carpeta apps si no existe:

    mkdir apps

2) Crear la app dentro de apps:

    django-admin startapp usuarios apps/usuarios

Esto genera:

    apps/
    └── usuarios/
        ├── admin.py
        ├── apps.py
        ├── models.py
        ├── views.py
        └── ...

✅ Luego agregás 'apps.usuarios' o 'usuarios' (según tu estructura) a INSTALLED_APPS en settings.py.

### 📦 8. Crear superusuario

    python manage.py createsuperuser

Seguir las indicaciones y guardar losd atos

🧠 Resumen final:

    | Acción                                     | Comando                                        |
    | ------------------------------------------ | ---------------------------------------------- |
    | Crear entorno virtual                      | `python -m venv venv`                          |
    | Activar entorno                            | `venv\Scripts\activate` (Windows)              |
    | Desactivar entorno                         | `deactivate`                                   |
    | Guardar dependencias                       | `pip freeze > requirements.txt`                |
    | Instalar desde archivo                     | `pip install -r requirements.txt`              |
    | Crear proyecto nuevo                       | `django-admin startproject config`             |
    | Crear proyecto dentro de carpeta existente | `django-admin startproject config .`           |
    | Crear app                                  | `python manage.py startapp core`               |
    | Crear app dentro de carpeta `apps/`        | `django-admin startapp usuarios apps/usuarios` |
    | Correr servidor                            | `python manage.py runserver`                   |
    | Crear migraciones                          | `python manage.py makemigrations`              |
    | Aplicar migraciones                        | `python manage.py migrate`                     |
    | Entrar al shell                            | `python manage.py shell`                       |



### Flujo de trabajo

    python manage.py runserver
    ↓
    manage.py → settings.py
    ↓
    settings.py → ROOT_URLCONF = 'seting.urls'
    ↓
    seting/urls.py → path('', include('apps.core.urls'))
    ↓
    apps/core/urls.py → path('dashboard/', dashboard)
    ↓
    apps/core/views.py → def dashboard()
    ↓
    return render(template.html)