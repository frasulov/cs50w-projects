from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
import markdown
import random
from django import forms

# author: Fagan Rasulov
# Github: frasulov

class NewSearchForm(forms.Form):
     search = forms.CharField(label="",widget= forms.TextInput
                           (attrs={'class':'search', 'placeholder':'Search Encyclopedia'}))

class NewAddForm(forms.Form):
     title = forms.CharField(label="",widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Encyclopedia Title'}))
     content = forms.CharField(label="",widget= forms.Textarea(attrs={'class':'form-control', 'placeholder':'Encyclopedia Description'}))

class NewEditForm(forms.Form):
    edit_content = forms.CharField(label="",widget= forms.Textarea(attrs={'class':'form-control'}),initial='value')

def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            res = []
            if search in util.list_entries():
                return wiki(request, search)
            else:
                for entry in util.list_entries():
                    if search in entry:
                        res.append(entry)
                return result(request, res)
        else:
            return render(request, "encyclopedia/index.html",{
                "form":form
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm(),
        "random": random.choice(util.list_entries())
    })

def wiki(request, name):
    if util.get_entry(name) == None:
        content = None
    else:
        content = markdown.markdown(util.get_entry(name))
    return render(request, "encyclopedia/wiki.html",{
        "content": content,
        "name": name,
        "form": NewSearchForm(),
        "random": random.choice(util.list_entries())
    })

def result(request, res):
    return render(request, "encyclopedia/result.html",{
        "form": NewSearchForm(),
        "results": res,
        "random": random.choice(util.list_entries())
    })

def add(request):
    if request.method == "POST":
        form = NewAddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            for entry in util.list_entries():
                if title.lower() in entry.lower():
                    return render(request, "encyclopedia/error.html",{
                        "form": NewSearchForm(),
                        "title": title,
                        "random": random.choice(util.list_entries())
                    }) 
            else:
                util.save_entry(title, content)
                return wiki(request,title)
        else:
            return render(request, "encyclopedia/index.html",{
                "form":form,
                "random": random.choice(util.list_entries())
            })
    return render(request, "encyclopedia/addWiki.html",{
        "addform": NewAddForm(),
        "form": NewSearchForm(),
        "random": random.choice(util.list_entries())
    })

def edit(request, name):
    if request.method == "POST":
        form = NewEditForm(request.POST)
        if form.is_valid():
            edit_content = form.cleaned_data["edit_content"]
            util.save_entry(name, edit_content)
            return wiki(request, name)
        else:
            return index(request)
    return render(request, "encyclopedia/editWiki.html", {
        "form":NewSearchForm(),
        "editform": NewEditForm(initial={'edit_content': util.get_entry(name)}),
        "name":name,
        "random": random.choice(util.list_entries())
    })




