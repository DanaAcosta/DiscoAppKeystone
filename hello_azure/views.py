from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/index.html')

def update(request): #Esto es lo que agregamos
    print('Request for update page received')
    return render(request, 'hello_azure/update.html')

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
        name = request.POST.get('name')
        
        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            print("Request for hello page received with name=%s" % name)
            context = {'name': name }
            return render(request, 'hello_azure/hello.html', context)
    else:
        return redirect('index')