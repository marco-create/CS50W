from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.urls import reverse
from . import util
from markdown2 import Markdown
import re
import random

md = Markdown()

class NewTitleForm(forms.Form):
    add_title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder":"New Entry title."}))
    add_entry = forms.CharField(label="", max_length=300, widget=forms.Textarea(attrs={
                                                        "class":"text-form",
                                                        "placeholder":'''Enter the Markdown content for the page.
#Markdown title
Formatted text'''}))

class EditForm(forms.Form):
    # entry_title = forms.CharField(label="", widget=forms.TextInput())
    entry_text = forms.CharField(label="", widget=forms.Textarea({"class": "text-form"}))

def index(request):
    ''' Return the index page listing all the entries.
    '''
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    ''' Get an entry name. If it exists, the function renders the wiki page with the entry,
        otherwise, it returns a 404 page.
    '''
    is_entry = util.get_entry(entry)
    if is_entry:
        return render(request, "encyclopedia/wiki.html", {
            "entry_title": entry,
            "entry_body": md.convert(is_entry)
        })
    elif is_entry is None:
        return render(request, "encyclopedia/404.html")

def search(request):
    ''' Query field that gets an entry name and tries to retrieve the wiki page of that entry.
        If the query does not exists, it returns a 404, if it exists, it renders the wiki page.
        If the query is a substring of a wiki entry, it lists all the possible entries starting with that letters.
    '''
    found = False
    the_entry = request.GET.get('q')
    if (util.get_entry(the_entry)):
        return render(request, "encyclopedia/wiki.html", {
            "entry_body": md.convert(util.get_entry(the_entry)),
        })
    else:
        words = []
        regexp = re.compile(fr"^{the_entry}", re.IGNORECASE)
        for entry in util.list_entries():
            if regexp.search(entry):
                words.append(entry)
        if len(words) == 0: # if the query does not match any of the entries
            return render(request, "encyclopedia/404.html")
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": words,
                "found": True
            })
            
def newpage(request):
    ''' Create a new entry allowing markdown text.
        If the title entry already exists, then it gives an alert message otherwise,
        a new entry is created and the page is redirected to that new entry.
    '''
    if request.method == "POST":
        form = NewTitleForm(request.POST)
        title = form.data["add_title"]
        if form.is_valid() and title not in util.list_entries():
            new_title = form.cleaned_data["add_title"]
            print(f"{title} will be added")
            util.save_entry(new_title, form.cleaned_data["add_entry"])
            return render(request, "encyclopedia/wiki.html", {
                "entry_body": md.convert(util.get_entry(title)),
            })
        else:   
            # if the entry title already exists come back to original form
            print(f"{title} already exists.")
            messages.info(request, f"{title} already exists.")
            return render(request, "encyclopedia/newpage.html", {
                "title": title,
                "newentry": form
            })

    return render(request, "encyclopedia/newpage.html", {
        "newentry": NewTitleForm()
    })

def randompage(request):
    ''' Return a random wiki page.
    '''
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse("wiki", kwargs={"entry": random_entry}))

def edit(request, entry):
    ''' When clicking on Edit button, the user is redirected to edit page for that particular entry.
        The user can modify the text of the entry using markdown text.
    '''
    if request.method == "POST":
        form = EditForm(request.POST)
        entry_title = entry
        edit_text = form.data["entry_text"]
        if form.is_valid():
            # new_title = form.cleaned_data["entry_title"]
            new_text = form.cleaned_data["entry_text"]
            print(f"{entry} - this is the title")
            print(new_text)
            util.save_entry(entry_title, new_text)
            return render(request, "encyclopedia/wiki.html", {
                "entry_body":md.convert(util.get_entry(entry)),
                "entry_title": entry
            })

    return render(request, "encyclopedia/edit.html", {
        "entry_title": entry,
        "form": EditForm(initial={"entry_title": entry, "entry_text": util.get_entry(entry)})
    })