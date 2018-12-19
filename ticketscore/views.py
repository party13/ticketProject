
from django.shortcuts import redirect
from django.shortcuts import render
import os



def redirect_index(request):
    return redirect('index_page', permanent=True)