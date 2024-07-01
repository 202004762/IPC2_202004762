import os
from django.shortcuts import render, redirect
from .models import Cliente, Producto
from .forms import AddClienteForm, EditarClienteForm, AddProductoForm, EditProductoForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Factura, DetalleFactura
from django.db import transaction
import matplotlib
from django.db.models import Sum , Count
from django.conf import settings
from django.template import loader

# libreria Matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO

#xml
from django.http import HttpResponse
from django.core.serializers import serialize
import xml.etree.ElementTree as ET
from django.views import View
# Create your views here.

def ventas_view(request):
    num_ventas = 156
    context = {
        'num_ventas': num_ventas
    }
    return render(request, 'ventas.html', context)

def clientes_view(request):
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()

    context = {
        'clientes': clientes,
        'form_personal': form_personal,
        'form_editar': form_editar
    }
    return render(request, 'clientes.html', context)

#agregar cliente desde form
def add_cliente_view(request): 
    #print("Guardar cliente")
    if request.POST:
        form = AddClienteForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request, "Error al Guardar")
                return redirect('Clientes')


    return redirect('Clientes')

#editar formulario
def edit_cliente_view(request): 
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarClienteForm(
            request.POST, request.FILES, instance= cliente)
        if form.is_valid:
            form.save()
    return redirect('Clientes')


#eliminar cliente de formulario
def delete_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        cliente.delete()
        
    return redirect('Clientes')

def productos_view(request):
    """
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()
    """
    productos = Producto.objects.all()
    form_add = AddProductoForm()
    form_editar_producto = EditProductoForm()

    context = {
        'productos': productos,
        'form_add': form_add,
        'form_editar_producto': form_editar_producto
        
    }
    return render(request, 'productos.html', context)


#agregar producto desde form
def add_producto_view(request): 
    #print("Guardar Producto")
    if request.POST:
        form = AddProductoForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request, "Error al Guardar el Producto")
                return redirect('Productos')
        return redirect('Productos')
    
#editar formulario
def edit_producto_view(request): 
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_editar'))
        form = EditProductoForm(
            request.POST, request.FILES, instance= producto)
        if form.is_valid:
            form.save()
    return redirect('Productos')

def delete_producto_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_eliminar'))
        if producto.imagen:
            # Eliminar la imagen asociada al producto si existe
            if os.path.exists(producto.imagen.path):
                os.remove(producto.imagen.path)
        # Eliminar el producto
        producto.delete() 

    return redirect('Productos')

def seleccionar_cliente_view(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        
        request.session['cliente_id'] = cliente_id
    return redirect('Productos') 


@transaction.atomic
def realizar_compra_view(request):
    if request.method == 'POST':
        cliente_id = request.session.get('cliente_id')
        
        if cliente_id is None:
            messages.error(request, "Cliente no seleccionado.")
            return redirect('Clientes')

        productos_ids = request.POST.getlist('productos[]')

        try:
            with transaction.atomic():
                factura = Factura.objects.create(cliente_id=cliente_id)

                total_factura = 0
                for producto_id in productos_ids:
                    producto = Producto.objects.get(pk=producto_id)
                    if producto.stock > 0:
                        producto.stock -= 1
                        producto.save()

                        detalle = DetalleFactura.objects.create(
                            factura=factura,
                            producto=producto,
                            cantidad=1,
                            precio_unitario=producto.precio,
                            subtotal=producto.precio
                        )

                        total_factura += detalle.subtotal

                factura.total = total_factura
                factura.save()

                messages.success(request, "Compra realizada con éxito.")

        except Exception as e:
            messages.error(request, f"Error al realizar la compra: {str(e)}")

    return redirect('Productos')


def ventas_view(request):
    facturas = Factura.objects.all()
    return render(request, 'ventas.html', {'facturas': facturas})


def detalle_factura_view(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id)
    detalles_factura = DetalleFactura.objects.filter(factura=factura)

    context = {
        'factura': factura,
        'detalles_factura': detalles_factura,
    }

    return render(request, 'detalle_factura.html', context)


def eliminar_factura_view(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id)

    factura.delete()
    return redirect('Ventas')


def graficos_view(request):
    # Gráfico de productos más vendidos
    productos_mas_vendidos = Producto.objects.annotate(total_vendido=Sum('detallefactura__cantidad')).order_by('-total_vendido')[:10]

    productos_mas_vendidos = [p for p in productos_mas_vendidos if p.total_vendido is not None]

    nombres_productos = [p.nombre for p in productos_mas_vendidos]
    cantidades_vendidas = [p.total_vendido for p in productos_mas_vendidos]

    plt.figure(figsize=(10, 6))
    plt.bar(nombres_productos, cantidades_vendidas)
    plt.title('Productos más vendidos')
    plt.xlabel('Productos')
    plt.ylabel('Cantidad vendida')
    
    image_stream_productos = BytesIO()
    plt.savefig(image_stream_productos, format="png")
    plt.close()
    image_stream_productos.seek(0)

    # Gráfico de clientes con más compras
    clientes_mas_repiten = Cliente.objects.annotate(num_compras=Count('factura')).order_by('-num_compras')[:10]

    nombres_clientes = [cliente.nombre for cliente in clientes_mas_repiten]
    num_compras = [cliente.num_compras for cliente in clientes_mas_repiten]

    plt.figure(figsize=(10, 6))
    plt.bar(nombres_clientes, num_compras)
    plt.title('Clientes con más compras')
    plt.xlabel('Clientes')
    plt.ylabel('Número de compras')
    
    image_stream_clientes = BytesIO()
    plt.savefig(image_stream_clientes, format="png")
    plt.close()
    image_stream_clientes.seek(0)

    context = {
        'image_url_productos': get_image_url(image_stream_productos, 'grafico_productos.png'),
        'image_url_clientes': get_image_url(image_stream_clientes, 'grafico_clientes.png'),
    }

    return render(request, 'graficos.html', context)


def get_image_url(image_stream, filename):
    # Guardar la imagen en el sistema de archivos
    image_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(image_path, 'wb') as f:
        f.write(image_stream.read())

    # Proporcionar una URL para acceder a la imagen
    image_url = os.path.join(settings.MEDIA_URL, filename)
    return image_url

def export_to_xml(request):
    # Obtén los datos que deseas exportar
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    facturas = Factura.objects.all()
    detalles_factura = DetalleFactura.objects.all()

    # Serializa los datos a XML
    clientes_xml = serialize('xml', clientes)
    productos_xml = serialize('xml', productos)
    facturas_xml = serialize('xml', facturas)
    detalles_factura_xml = serialize('xml', detalles_factura)

    # Combina los datos en un archivo XML
    xml_content = f"""
    <data>
        {clientes_xml}
        {productos_xml}
        {facturas_xml}
        {detalles_factura_xml}
    </data>
    """

    # Devuelve los datos como respuesta HTTP
    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=data.xml'
    return response


class ExportToXMLView(View):
    def get(self, request, *args, **kwargs):
        # Obtener datos de clientes y productos
        clientes = Cliente.objects.all()
        productos = Producto.objects.all()

        # Crear el elemento raíz del XML
        root = ET.Element("data")

        # Crear elementos para clientes
        clientes_element = ET.SubElement(root, "clientes")
        for cliente in clientes:
            cliente_element = ET.SubElement(clientes_element, "cliente")
            ET.SubElement(cliente_element, "nit").text = str(cliente.nit)
            ET.SubElement(cliente_element, "nombre").text = cliente.nombre
            ET.SubElement(cliente_element, "telefono").text = cliente.telefono
            ET.SubElement(cliente_element, "direccion").text = cliente.direccion

        # Crear elementos para productos
        productos_element = ET.SubElement(root, "productos")
        for producto in productos:
            producto_element = ET.SubElement(productos_element, "producto")
            ET.SubElement(producto_element, "nombre").text = producto.nombre
            ET.SubElement(producto_element, "descripcion").text = producto.descripcion
            ET.SubElement(producto_element, "precio").text = str(producto.precio)
            ET.SubElement(producto_element, "stock").text = str(producto.stock)

        # Crear el árbol XML y escribirlo en la respuesta HTTP
        tree = ET.ElementTree(root)
        response = HttpResponse(content_type="application/xml")
        response["Content-Disposition"] = 'attachment; filename="datos.xml"'
        tree.write(response)

        return response
    
def descargar_xml_clientes(request):
    # Obtén la lista de clientes desde tu base de datos (puedes ajustar esto según tu modelo)
    clientes = Cliente.objects.all()

    # Crea un objeto XML
    root = ET.Element("clientes")
    for cliente in clientes:
        cliente_element = ET.SubElement(root, "cliente")
        ET.SubElement(cliente_element, "id").text = str(cliente.id)
        ET.SubElement(cliente_element, "nit").text = cliente.nit
        ET.SubElement(cliente_element, "nombre").text = cliente.nombre
        ET.SubElement(cliente_element, "telefono").text = cliente.telefono
        ET.SubElement(cliente_element, "direccion").text = cliente.direccion

    xml_data = ET.tostring(root, encoding="utf-8")
    response = HttpResponse(xml_data, content_type="application/xml")
    response["Content-Disposition"] = 'attachment; filename="clientes.xml"'
    return response

def descargar_xml_productos(request):
    # Obtén la lista de productos desde tu base de datos (ajusta esto según tu modelo)
    productos = Producto.objects.all()

    # Crea un objeto XML
    root = ET.Element("productos")
    for producto in productos:
        producto_element = ET.SubElement(root, "producto")
        ET.SubElement(producto_element, "id").text = str(producto.id)
        ET.SubElement(producto_element, "nombre").text = producto.nombre
        ET.SubElement(producto_element, "descripcion").text = producto.descripcion
        ET.SubElement(producto_element, "precio").text = str(producto.precio)
        ET.SubElement(producto_element, "stock").text = str(producto.stock)

    xml_data = ET.tostring(root, encoding="utf-8")
    response = HttpResponse(xml_data, content_type="application/xml")
    response["Content-Disposition"] = 'attachment; filename="productos.xml"'
    return response