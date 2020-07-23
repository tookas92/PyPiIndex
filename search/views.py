from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

# Create your views here.


class SearchView(View):

    def get(self, request):
        ctx = 'test'
        return render(request, 'index.html', context={"obj": ctx})
