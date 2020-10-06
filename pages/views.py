from django.shortcuts import render

def about(request):
    return render(request, 'pages/about.html')

def delivery(request):
    return render(request, 'pages/delivery.html')
