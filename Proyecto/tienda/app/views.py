from urllib import request
from django.http import  JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist
from . forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q 
import razorpay
from django.conf import settings

# Create your views here.

def home (request):
    return render(request,"app/home.html")
    
def about (request):
    return render(request,"app/about.html")
    
def contact (request):
    return render(request,"app/contact.html")


#clase de la categoria, que permiite mostrar los productos

class CategoryView(View):
    def get (self, request,val):
        product = Product.objects.filter(categoria=val)
        title = Product.objects.filter(categoria=val).values('titulo')
        return render(request,"app/category.html",locals())


#clase de la categoria de los productos  
class CategoryTitle(View):
    def get (self, request,val):
        product = Product.objects.filter(titulo=val)
        title = Product.objects.filter(categoria=product[0].categoria).values('titulo')
        return render(request,"app/category.html",locals())



# clase de detalles del producto
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q (user=request.user))
        return render(request,"app/productdetail.html",locals())


#clase de registro 
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "El usuario ha sido registrado con exito")
        else:
            messages.warning(request,"Datos incorrectos")
        return render(request, 'app/customerregistration.html', locals())


#clase del perfil del usuario   con la informacion que se desea agregar
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usuario = request.user
            nombre = form.cleaned_data['nombre'] 
            departamento = form.cleaned_data['departamento']  
            ciudad = form.cleaned_data['ciudad'] 
            direccion = form.cleaned_data['direccion'] 
            telefono = form.cleaned_data['telefono'] 
            codigo_postal = form.cleaned_data['codigo_postal']
            reg = Customer(usuario=usuario,nombre=nombre,departamento=departamento,ciudad=ciudad,direccion=direccion,telefono=telefono,codigo_postal=codigo_postal)
            reg.save()
            messages.success(request,"Perfil, guardado con exito")
        else:
            messages.warning(request,"Error al guardar los datos")
        return render(request, 'app/profile.html',locals())

#permite mostrar la informacion que se tiene agregad del usuario   
def address(request):
    add = Customer.objects.filter(usuario=request.user)
    return render(request, 'app/address.html', locals())

#permite actualizar los datos que se tienen del usuario, con base en los datos anteriores que se tienen 
class updateAddress(View):
    def get(self,request,pk):
        add= Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add )
        return render(request, 'app/updateAddress.html', locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)    
        if form.is_valid():   #permite agregar nuevos valores 
            add = Customer.objects.get(pk=pk)
            #usuario = request.user
            add.nombre = form.cleaned_data['nombre'] 
            add.departamento = form.cleaned_data['departamento']  
            add.ciudad = form.cleaned_data['ciudad'] 
            add.direccion = form.cleaned_data['direccion'] 
            add.telefono = form.cleaned_data['telefono'] 
            add.codigo_postal = form.cleaned_data['codigo_postal']
            add.save(   )
            messages.success(request,"Perfil, guardado con exito")
        else:
            messages.warning(request,"Error al guardar los datos")
        return redirect("address")



def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    cleaned_product_id = int(product_id.split('/')[0])
    product = get_object_or_404(Product, id=cleaned_product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0 
    for p in cart:
         value = p.quantity * p.product.descuento
         amount =amount + value 
    totalamount = amount+12
    amount =totalamount-12
    
    return render(request, 'app/addtocart.html',locals())

def show_wishlist(request):
    user = request.user
    product = Wishlist.objects.filter(user=user)
    return render(request, "app/wishlist.html", {'product': product})








class checkout(View):
    def get(self, request):
        user=request.user
        add=Customer.objects.filter(usuario=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p  in cart_items:
            value= p.quantity * p.product.descuento
            famount = famount + value
        totalamount = famount +12
        razoramount = int(totalamount * 100 )
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data ={"amount": razoramount, "currency": "INR","receipt": "order_rcptid_11"}
        payment_response= client.order.create(data=data)
        print(payment_response)
        #{'id': 'order_MwEEMUx8cHfxqi', 'entity': 'order', 'amount': 51200, 'amount_paid': 0, 'amount_due': 51200, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1699064148}
        order_id= payment_response['id']
        order_status = payment_response['status']
        if order_status =='created':
            payment = Payment(
                user=user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status=order_status
            )
            payment.save ()



        return render(request, 'app/checkout.html', locals())





def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer = Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id=payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for  c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")

        
def orders (request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())

#permite incrementar la cantidad de productos por carro agregados
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']  
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0
        for p in cart:
            value = p.quantity * p.product.descuento
            amount += value

        totalamount = amount + 12

        data = {
            'quantity': c.quantity,
            'amount': amount,  
            'totalamount': totalamount,
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']  
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.descuento
            amount += value

        totalamount = amount + 12

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']  
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.descuento
            amount += value

        totalamount = amount + 12

        data = {
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        wishlist, created = Wishlist.objects.get_or_create(user=user, product=product)

        if created:
            data = {
                'mensaje': 'Agregado correctamente a la lista de deseos'
            }
        else:
            data = {
                'mensaje': 'Ya está en la lista de deseos'
            }

        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user

        try:
            wishlist = Wishlist.objects.get(user=user, product=product)
            wishlist.delete()
            data = {
                'mensaje': 'Eliminado correctamente de la lista de deseos'
            }
        except Wishlist.DoesNotExist:
            data = {
                'mensaje': 'No estaba en la lista de deseos'
            }

        return JsonResponse(data)
    

def search (request):
    query = request.GET['search']
    product =  Product.objects.filter(Q(titulo__icontains=query))
    return render(request, "app/search.html", locals())






    