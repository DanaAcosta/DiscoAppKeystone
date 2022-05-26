from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


import csv
from .forms import CsvModelForm
from .models import Csv

import pyrebase
config= {
  "apiKey": "AIzaSyC4Wop3qYzyJJyR6nES3V3_4ouh8XIxcFU",
  "authDomain": "discoapp-e8634.firebaseapp.com",
  "databaseURL": "https://discoapp-e8634-default-rtdb.firebaseio.com",
  "projectId": "discoapp-e8634",
  "storageBucket": "discoapp-e8634.appspot.com",
  "messagingSenderId": "1044386622635",
  "appId": "1:1044386622635:web:b52bd41e52dc3147289bee",
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

# Use the application default credentials
# Creamos la conexión a la base de datos si no existe
if not firebase_admin._apps:
    # Es necesario configurar cred con la ruta del archivo json
    cred = credentials.Certificate("C:\Apps\discoapp-e8634-firebase-adminsdk-i64d2-9fe03f1fb7.json")
    # Inicializamos app
    firebase_admin.initialize_app(cred)

# Base de datos
db = firestore.client()


def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/index.html')

def update(request): #Esto es lo que agregamos
    print('Request for update page received')
    return render(request, 'hello_azure/update.html')

def up(request): #Esto es lo que agregamos
    print('Request for upload page received')
    return render(request, 'hello_azure/up.html')

def verify(request):
    day = database.get().val()
    return render(request, 'hello_azure/verify.html', {"prod":list(day.items())})

def home(request):
    print('Request for home page received')
    return render(request, 'hello_azure/hello.html')

#@csrf_exempt
# Para cargar los datos en la base de datos
def upload(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated = False)
        doc_ref = db.collection(u'products')

        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i == 0:
                    pass
                else:
                    row = "".join(row)
                    row = row.replace(";", " ")
                    row = row.split()
                    print(row)
                    if not row:
                        pass
                    else:
                        try:
                            int(row[1])
                        except ValueError:
                            print("Price is no numeric")
                            obj.delete()
                            return render(request, 'hello_azure/opss.html')
                        except IndexError:
                            print("Product or Price does not exist")
                            obj.delete()
                            return render(request, 'hello_azure/opss.html')
                        else:
                            doc_ref.document(row[0]+row[1]).set({
                                u'name': row[0],
                                u'price': int(row[1]),
                            })

            obj.activated = True
            obj.save()
            obj.delete()

        return render(request, 'hello_azure/succesful.html', {'form': form})
    return render(request, 'hello_azure/up.html', {'form': form})

@csrf_exempt
def hello(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pw = request.POST.get('password')
        
        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            print("Request for hello page received with name=%s" % name)
            context = {'username': name }

            emails = []
            psswrds = []
            users_ref = db.collection(u'Users')
            docs = users_ref.stream()

            # Consultamos los ususarios y contraseñas en la base de datos
            for doc in docs:
                dictionary = doc.to_dict()
                #print(f'{doc.id} => {doc.to_dict()}')
                emails.append(dictionary.get("email"))
                psswrds.append(dictionary.get("password"))
            #print(emails,psswrds) 

            # Verificamos si el ussuario y contraseña coinciden con alguno en la base de datos
            for i in range (0,len(emails)):
                print(emails[i],psswrds[i])
                print(name, pw)
                if name == emails[i] and pw == psswrds[i]:
                    return render(request, 'hello_azure/hello.html', context)
            return redirect('index')
    else:
        return redirect('index')

@csrf_exempt
def add(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name1')
        product_price = request.POST.get('product_price1')
        
        if product_name is None or product_name == '' or product_price is None or product_price == '':
            print("Request to add received with no name or blank name -- redirecting")
            return redirect('update')
        else:
            print("Request to add received with name=%s" % product_name)
            doc_ref = db.collection(u'products')
            doc_ref.document(product_name+str(product_price)).set({
                                u'name': product_name,
                                u'price': product_price,
                            })
            return render(request, 'hello_azure/succesful.html')

@csrf_exempt
def modify(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name2')
        product_price = request.POST.get('product_price2')
        
        if product_name is None or product_name == '' or product_price is None or product_price == '':
            print("Request to modify received with no name or blank name -- redirecting")
            return redirect('update')
        else:
            print("Request to modify received with name=%s" % product_name)
            doc_ref = db.collection(u'products')
            docs = doc_ref.stream()

            for doc in docs:
                dictionary = doc.to_dict()
                p_name = dictionary.get("name")
                if p_name == product_name:
                    doc_ref.document(doc.id).set({
                                        u'name': product_name,
                                        u'price': product_price,
                                    })
            return render(request, 'hello_azure/succesful.html')

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name3')
        
        if product_name is None or product_name == '':
            print("Request to delete received with no name or blank name -- redirecting")
            return redirect('update')
        else:
            print("Request to delete received with name=%s" % product_name)
            doc_ref = db.collection(u'products')
            docs = doc_ref.stream()

            for doc in docs:
                dictionary = doc.to_dict()
                p_name = dictionary.get("name")
                if p_name == product_name:
                    doc_ref.document(doc.id).delete()
                    return render(request, 'hello_azure/succesful.html')
            return render(request, 'hello_azure/notfound.html')