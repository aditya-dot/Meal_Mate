from django.shortcuts import render,HttpResponse
from. models import Customer,Restaurant,Menu_Item,Cart

def index(request):
    return render(request,'foodapp/index.html')

def open_signin(request):
    return render(request,'foodapp/signin.html')

def open_signup(request):
    return render(request,'foodapp/signup.html')

# Registration page------------------
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        
        try:
            Customer.objects.get(username = username)
            return HttpResponse("Dublicate not allow") 
        except:
            Customer.objects.create(
                username = username,
                password = password,
                email = email,
                mobile = mobile,
                address = address,
            )
    return render(request,'foodapp/signin.html')

# Loging page--------------------
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    try:
        Customer.objects.get(username = username, password = password)
        if username == 'admin':
            return render(request,'foodapp/admin_home.html')
            
        else:
            restaurant_list = Restaurant.objects.all()
            return render(request,'foodapp/customer_home.html',{"r_list" : restaurant_list ,"username":username})
        
    except Customer.DoesNotExist:
        return render(request,'foodapp/fail.html')
        
# Restaurent---------------

def open_add_restaurant(request):
    return render(request,'foodapp/add_restaurant.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('url')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
    try:     
        Restaurant.objects.get(name = name)
        return HttpResponse("Dublicate user not allow") 
    except:
        Restaurant.objects.create(
            name = name,
            url = url,
            cuisine = cuisine,
            rating = rating
        )
    return render(request,'foodapp/admin_home.html')

def open_show_restaurant(request):
    restaurant_list = Restaurant.objects.all()
    return render(request,'foodapp/show_restaurant.html',{"r_list" : restaurant_list})

def open_update_restaurant(request,r_id):
    restaurant = Restaurant.objects.get(id = r_id)
    return render(request,'foodapp/update_restaurant.html',{"restaurant_data" : restaurant})

# Update Restureant---------------------

def update_restaurant(request,r_id):
    update_data = Restaurant.objects.get(id = r_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('url')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        update_data.name = name
        update_data.url = url
        update_data.cuisine = cuisine
        update_data.rating = rating
        update_data.save()
    restaurant_list = Restaurant.objects.all()
    return render(request,'foodapp/show_restaurant.html',{"r_list" : restaurant_list})

def delete_restaurant(request,r_id):
    delete_data = Restaurant.objects.get(id = r_id)
    delete_data.delete()
    restaurant_list = Restaurant.objects.all()
    return render(request,'foodapp/show_restaurant.html',{"r_list" : restaurant_list})

def open_update_menu(request,r_id):
    menu = Restaurant.objects.get(id = r_id)
    itemList = menu.items.all()
    return render(request,"foodapp/update_menu.html",{"menu_data":menu,"itemList":itemList})

def update_menu(request,r_id):
    restaurant = Restaurant.objects.get(id = r_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('is_veg') == 'on'
        picture = request.POST.get('picture')
      
        Menu_Item.objects.create(
            restaurant = restaurant,
            name = name,
            description = description,
            price = price,
            vegeterian = vegeterian,
            picture = picture
        )
    itemList = Menu_Item.objects.filter(restaurant=restaurant)    
    return render(request,"foodapp/update_menu.html",{'menu_data': restaurant,'itemList': itemList})
            
def view_menu(request,r_id,username):
    menu = Restaurant.objects.get(id = r_id)
    itemList = menu.items.all()
    return render(request,"foodapp/customer_menu.html",{"menu_data":menu,"itemList":itemList,"username":username})


def add_to_cart(request,item_id,username):
    item = Menu_Item.objects.get(id = item_id)
    customer = Customer.objects.get(username = username)
    cart,created = Cart.objects.get_or_create(customer = customer)
    cart.items.add(item)
    return HttpResponse("Added to Cart ")

def show_cart(request,username):
    customer = Customer.objects.get(username = username)
    cart = Cart.objects.filter(customer = customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0
    
    return render(request,'foodapp/cart.html',{"items":items,"total_price":total_price,"username":username})

def checkout(request,username):
    return HttpResponse("Data Passed ")