from django.contrib import admin #llamar nuestros modelos
from ventas.models import Cliente, Producto

#agregar modelos a la pagina de admin
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'telefono', 'direccion')
    search_fields = ['nombre'] #buscador solamente por nombre
    readonly_fields = ('created','updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
#
admin.site.register(Cliente, ClienteAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'stock')
    search_fields = ['descripcion'] #buscador solamente por nombre
    readonly_fields = ('created','updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
#
admin.site.register(Producto, ProductoAdmin)

# Register your models here.
