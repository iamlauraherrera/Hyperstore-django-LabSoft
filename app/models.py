from django.db import models
from django.contrib.auth.models import User

# Create your models here.


 #Categoria de los productos
CATEGORY_CHOICE= (
    ('LI', 'Libros'),
    ('RE', 'Revistas'),
    ('DI', 'Diccionarios'),
    ('EN', 'Enciclopedias'),  
    ('NO', 'Novelas'), 
    ('CO', 'Comics')
)
 #Estado del producto
ESTADO= (
    ('NU', 'Nuevo'),
    ('US', 'Usado'),
)

STATE_CHOICES = (
    ('Amazonas','Amazonas'),
    ('Antioquia','Antioquia'),
    ('Arauca','Arauca'),
    ('Atlantico','Atlantico'),
    ('Bogota','Bogota'),
    ('Bolívar','Bolívar'),
    ('Boyaca','Boyaca'),
    ('Caldas','Caldas'),
    ('Caqueta','Caqueta'),
    ('Casanare','Casanare'),
    ('Cauca','Cauca'),
    ('Cesar','Cesar'),
    ('Choco','Choco'),
    ('Cordoba','Cordoba'),
    ('Cundinamarca','Cundinamarca'),
    ('Guainia','Guainia'),
    ('Guaviare','Guaviare'),
    ('Huila','Huila'),
    ('Guajira','Guajira'),
    ('Magdalena','Magdalena'),
    ('Meta','Meta'),
    ('Nariño','Nariño'),
    ('Putumayo','Putumayo'),
    ('Norte de Santander','Norte de Santander'),
    ('Quindío','Quindío'),
    ('Risaralda','Risaralda'),
    ('San Andrés y Providencia','San Andrés y Providencia'),
    ('Santander','Santander'),
    ('Sucre	','Sucre'),
    ('Tolima','Tolima'),
    ('Valle del Cauca','Valle del Cauca'),
    ('Vaupes','Vaupes'),
    ('Vichada','Vichada'),

)

 #Categoria de los pagos
STATUS_CHOICES= (
    ('Aceptada', 'Aceptada'),
    ('Empaque', 'Empaque'),
    ('Enviado', 'Enviado'),
    ('En reparto', 'En reparto'),  
    ('Cancelado', 'Cancelado'), 
    ('Pendiente', 'Pendiente')
)

#Definiendo la clase o atributos del producto
class Product(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    ano_publicacion= models.CharField(max_length=100)
    genero = models.CharField(max_length=100)
    paginas = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100)
    issn = models.CharField(max_length=100)
    idioma = models.CharField(max_length=100)
    fecha_publi = models.CharField(max_length=100)
    estado = models.CharField(choices=ESTADO, max_length=2)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=1000000, decimal_places=3)
    descuento = models.DecimalField(max_digits=1000000, decimal_places=3)
    categoria = models.CharField(choices=CATEGORY_CHOICE, max_length=3)
    imagen_producto = models.ImageField(upload_to = 'product')
    def __str__(self):
        return self.titulo


class Customer(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE) #user
    nombre = models.CharField(max_length=200) #name
    departamento = models.CharField(choices=STATE_CHOICES,max_length=100)  #state
    ciudad = models.CharField(max_length=50) #city
    direccion = models.CharField(max_length=200) #locality
    telefono = models.IntegerField(default=0) #mobile
    codigo_postal = models.IntegerField()   #zipcode
    def _str_(self,):
        return self.nombre


# clase de el carro de compras
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    @property
    def total_cost(self):
        return self.quantity * self.product.descuento
    

class Payment(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True,null=True)
    paid = models.BooleanField(default=False)






class OrderPlaced(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    customer =models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE,default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.descuento
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)