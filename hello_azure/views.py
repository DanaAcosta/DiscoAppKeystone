from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Use the application default credentials
# Creamos la conexión a la base de datos si no existe
if not firebase_admin._apps:
    # Es necesario configurar cred con la ruta del archivo json
    cred = credentials.Certificate("C:\Apps\DiscoAppKeystone\hello_azure\discoapp-e8634-firebase-adminsdk-i64d2-fbcdf05c38.json")
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

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        name = request.POST.get('filename')
        
        if name is None or name == '':
            print("File not found")
            return redirect('update')
        else:
            print("Filename found=%s" % name)
            context = {'filename': name }
            return render(request, 'hello_azure/hello.html', context)
    else:
        return redirect('update')

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