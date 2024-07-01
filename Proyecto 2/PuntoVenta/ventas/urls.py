from django.urls import path
from . import views
from .views import ExportToXMLView, descargar_xml_clientes,descargar_xml_productos


urlpatterns = [
    path('', views.ventas_view, name='Ventas'),
    path('clientes/', views.clientes_view, name='Clientes'),
    path('add_cliente/', views.add_cliente_view, name='AddCliente'),
    path('edit_cliente/', views.edit_cliente_view, name='EditCliente'),
    path('delete_cliente/', views.delete_cliente_view, name='DeleteCliente'),
    path('productos/', views.productos_view, name='Productos'),
    path('add_producto/', views.add_producto_view, name='AddProducto'),
    path('edit_producto/', views.edit_producto_view, name='EditProducto'),
    path('delete_producto/', views.delete_producto_view, name='DeleteProducto'),
    path('seleccionar_cliente/', views.seleccionar_cliente_view, name='seleccionar_cliente'),
    path('realizar_compra/', views.realizar_compra_view, name='realizar_compra'),    
    path('detalle_factura/<int:factura_id>/', views.detalle_factura_view, name='detalle_factura'),
    path('eliminar_factura/<int:factura_id>/', views.eliminar_factura_view, name='eliminar_factura'),
    path('graficos/', views.graficos_view, name='graficos'),
    path('exportar-xml/', ExportToXMLView.as_view(), name='exportar_xml'),
    path('descargar-xml-clientes/', descargar_xml_clientes, name='descargar_xml_clientes'),
    path('descargar-xml-productos/', descargar_xml_productos, name='descargar_xml_productos'),
]