from django.shortcuts import render
from django.shortcuts import render, redirect

from .models import *

import re
# Create your views here.
def index(request):

    return render(request,'mips/index.html')