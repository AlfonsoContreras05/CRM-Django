from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.mail import send_mail
from django.conf import settings

# Función para verificar si el usuario es administrador
def is_admin(user):
    return user.groups.filter(name='Administradores').exists()

@login_required
def home(request):
    return render(request, 'clientes/home.html')


@login_required
@permission_required('clientes.view_cliente', raise_exception=True)
def listar_clientes(request):
    query = request.GET.get('buscar')
    if query:
        # Filtro usando múltiples campos con Q y el operador OR
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query) |
            Q(direccion__icontains=query),
            creado_por=request.user
        )
    else:
        # Si no hay búsqueda, mostrar todos los clientes del usuario
        clientes = Cliente.objects.filter(creado_por=request.user)
    
    return render(request, 'clientes/listar_clientes.html', {'clientes': clientes, 'query': query})

@login_required
@user_passes_test(is_admin)
@permission_required('clientes.add_cliente', raise_exception=True)
def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        notas = request.POST.get('notas')

        # Asegurarse de que todos los campos requeridos están siendo recogidos correctamente
        if nombre and email:
            Cliente.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                notas=notas,
                creado_por=request.user
            )
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('listar_clientes')
        else:
            messages.error(request, 'Faltan datos obligatorios.')
            return render(request, 'clientes/crear_cliente.html')
    return render(request, 'clientes/crear_cliente.html')

@login_required
@user_passes_test(is_admin)
@permission_required('clientes.change_cliente', raise_exception=True)
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id, creado_por=request.user)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')
        cliente.notas = request.POST.get('notas')
        cliente.save()
        messages.success(request, 'Cliente editado exitosamente')
        return redirect('listar_clientes')
    return render(request, 'clientes/editar_cliente.html', {'cliente': cliente})

@login_required
@user_passes_test(is_admin)
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id, creado_por=request.user)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect('listar_clientes')
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})

@login_required
@permission_required('clientes.view_cliente', raise_exception=True)
def dashboard(request):
    # Estadísticas básicas
    total_clientes = Cliente.objects.filter(creado_por=request.user).count()
    clientes_por_estado = Cliente.objects.filter(creado_por=request.user).values('estado').annotate(total=Count('estado'))

    return render(request, 'clientes/dashboard.html', {
        'total_clientes': total_clientes,
        'clientes_por_estado': clientes_por_estado,
    })

# Vista para el registro de nuevos usuarios
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Añadir usuario al grupo de "Usuarios Normales" por defecto
            grupo_usuarios = Group.objects.get(name='Usuarios Normales')
            user.groups.add(grupo_usuarios)
            messages.success(request, 'Registro exitoso. Por favor inicia sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'clientes/registro.html', {'form': form})

# Vista para el inicio de sesión
def inicio_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}')
            return redirect('home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'clientes/inicio_sesion.html', {'form': form})

# Vista para cerrar sesión
@login_required
def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente.')
    return redirect('login')

# Vista para enviar correo al cliente
@login_required
@user_passes_test(is_admin)
@permission_required('clientes.view_cliente', raise_exception=True)
def enviar_correo_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id, creado_por=request.user)

    asunto = "Bienvenido a CRM WizzardTech"
    mensaje = f"Hola {cliente.nombre},\n\nGracias por registrarte en CRM WizzardTech. Estamos felices de tenerte con nosotros."
    destinatario = [cliente.email]

    try:
        send_mail(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,
            destinatario,
            fail_silently=False,
        )
        messages.success(request, f'Correo enviado exitosamente a {cliente.nombre}')
    except Exception as e:
        messages.error(request, f'Error al enviar correo: {str(e)}')

    return redirect('listar_clientes')