from django.shortcuts import render, redirect

def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Usuario y contraseña hardcodeados (solo para probar)
        if username == 'admin' and password == '1234':
            request.session['usuario'] = username  # guardamos el usuario en sesión
            return redirect('Dashboard')
        else:
            error = 'Usuario o contraseña incorrectos'

    return render(request, 'core/login.html', {'show_navbar': False, 'error': error})

def dashboard(request):
    if 'usuario' not in request.session:
        return redirect('Login')  # si no hay usuario en sesión, lo redirigimos al login

    return render(request, 'dashboard.html', {'show_navbar': True})

def logout(request):
    request.session.flush()  # eliminamos todos los datos de la sesión
    return redirect('Login')
