from django.http import HttpResponse


# Create your views here.

def placeholder_view(request):
    return HttpResponse('<h1> places </h1>')
