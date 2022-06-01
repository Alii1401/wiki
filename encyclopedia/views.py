# from xxlimited import foo
from html import entities
from math import e
from this import d
from time import time
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django import forms
from django.views import View
from . import util
import markdown
from . import urls
import re
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class newpage(View):
    def get (self, request):
        return render(request, "encyclopedia/newpage.html")
    def post(self, request):
        global objct
        objct = request.POST.get('matn')
        mohtva = request.POST.get('content1')
        try:
            with open(f'entries/{objct}.md', 'r', encoding='UTF8') as f:
                f.close()
            
            print('hello')
            return render(request, 'encyclopedia/error.html')
             
        except Exception:

            util.save_entry(objct,mohtva)

            with open(f'entries/{objct}.md', 'r', encoding='UTF8') as f:
                text="{% extends 'encyclopedia/layout.html' %}\n{% block body %}\n"
                a =  f.read()
                text = text + a
                b = "{% endblock %}"
                text = text + b
                html = markdown.markdown(text)
            with open(f'encyclopedia/templates/encyclopedia/{objct}.html', 'w') as f :
                f.write(html)

            return redirect(f'/page/{objct}')

        

slug_list=[]
def page(request, slugtitle):
    
    if slugtitle in slug_list:
        slug_list.remove(slugtitle)
        slug_list.append(slugtitle)
    else:
        slug_list.append(slugtitle)
    return render(request, f'encyclopedia/{slugtitle}.html')


def randpage(request):
    bh = util.list_entries()
    # random.seed(time)
    select = random.choice(bh)
    return render(request, f'encyclopedia/{select}.html')

def edit(request):
    if request.method == 'GET':
        l = slug_list.__len__()
        slug_list[l-1]
        return render (request, 'encyclopedia/edit.html',{
                "mtn_entry" : util.get_entry(slug_list[l-1])
        })
    if request.method == 'POST':
        l = slug_list.__len__()
        objct = slug_list[l-1]
        mohtva = request.POST.get('cntnt')
        util.save_entry(objct,mohtva)

        with open(f'entries/{objct}.md', 'r', encoding='UTF8') as f:
            text="{% extends 'encyclopedia/layout.html' %}\n{% block body %}\n"
            a =  f.read()
            text = text + a
            b = "{% endblock %}"
            text = text + b
            html = markdown.markdown(text)
        with open(f'encyclopedia/templates/encyclopedia/{objct}.html', 'w') as f :
            f.write(html)

        return redirect(f'/page/{objct}')


def search(request):
    word = request.POST.get('q')
    entries_list = []
    entries=util.list_entries()
    for entry in entries:
        # print(entry)
        x = re.search(f'\w+{word}/w+|\w+{word}|{word}/w+|{word}', entry)
        if x:
            entries_list.append(entry)
    
    if entries_list.__len__()<1:
        content = {"masage":'No result found!' }
    else:
        content = {'entries': entries_list}
    
    return render(request, 'encyclopedia/result.html', context=content)

def error(request):
    return render(request,'encyclopedia/index.html')