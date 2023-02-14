from django.shortcuts import render
from markdown2 import Markdown
from . import util
from random import choice
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewEntry(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(label="Content", widget = forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def view_entry(request, entry):
    if entry not in util.list_entries():
        return render(request, "encyclopedia/error.html")

    content = Markdown()
    content = content.convert(util.get_entry(entry))
    title = entry

    return render(request, f"encyclopedia/entry.html", 
    {
        'content': content,
        'title': title
    })


def new_entry(request):
    if request.method == "POST":
        EntryForm = NewEntry(request.POST)
        if EntryForm.is_valid():
            title = EntryForm.cleaned_data["title"]
            content = EntryForm.cleaned_data["content"]
            
            if title.upper() not in [x.upper() for x in util.list_entries()]:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry_view", args=[title]))
            
            else:
                return render(request, "encyclopedia/new_entry.html",
                {
                    "newEntryForm" : EntryForm,
                    "Error": "Error: entry already exists!"
                })
        else:
            return render(request, "encyclopedia/new_entry.html",
                {
                    "newEntryForm" : EntryForm,
                    "Error": "Invalid Form"
                })  

    return render(request, "encyclopedia/new_entry.html",
    {
        "newEntryForm" : NewEntry()
    })

def edit(request, entry):
    if request.method == "POST":
        EntryForm = NewEntry(request.POST)
        if EntryForm.is_valid():
            title = EntryForm.cleaned_data["title"]
            content = EntryForm.cleaned_data["content"]
            if title not in util.list_entries():
                util.remove_entry(entry)
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry_view", args=[title]))
        else:
            return render(request, "encyclopedia/edit.html", {
                    "editEntryForm" : EntryForm,
                    "Error": "Invalid Form"
            })  

    EntryForm = NewEntry()
    entry_title = entry
    EntryForm["title"].initial = entry_title
    EntryForm["content"].initial = util.get_entry(entry)
    return render(request, "encyclopedia/edit.html", {
        "editEntryForm": EntryForm
    })

def search(request):
    search_request = request.GET['q']
    entries = util.list_entries()
    search_results = []

    for entry in entries:
        if search_request.strip().upper() == entry.upper():
            return HttpResponseRedirect(reverse("entry_view", args=[entry]))
        elif search_request.strip().upper() in entry.upper():
            search_results.append(entry)
        
    
    return render(request, "encyclopedia/search.html", {
        'search_results' : search_results
    })


def random_page(request):
    return HttpResponseRedirect(reverse("entry_view", args=[choice(util.list_entries())]))


def remove(request, entry):
    util.remove_entry(entry)
    return HttpResponseRedirect(reverse("index"))
    