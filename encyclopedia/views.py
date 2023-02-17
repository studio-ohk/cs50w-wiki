import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from markdown2 import Markdown

from . import util


markdowner = Markdown()

class CreateNewPage(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    title.widget.attrs.update({'class': 'form-control'})
    content.widget.attrs.update({'class': 'form-control'})

class EditPage(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

    content.widget.attrs.update({'class': 'form-control'})

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),

    })

def entry(request, title):

    # make input and entries lowercase for comparing
    titleLower = title.lower()
    entries = util.list_entries()
    entriesLower = [entry.lower() for entry in entries]

    if titleLower in entriesLower:
        # if there is matching entry, render pages accordingly
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdowner.convert(util.get_entry(title)),
        })

        # if it doesn't show error message
    else:
        return render(request, "encyclopedia/errorMessage.html", {
            "message": "message: entry does not exist"
        })

def edit(request, title):

    # populate form with old data
    if request.method == "GET":
        entry = util.get_entry(title)

        form = EditPage(initial={'content':entry})
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": entry,
            "form": form
        })

    # if request method is POST
    else:
        edit_form = EditPage(request.POST)
        if edit_form.is_valid():
            content = edit_form.cleaned_data['content']
            # save edited content
            util.save_entry(title, content)

            # redirect to edited version of entry page
            return render(request,"encyclopedia/entry.html", {
                "title": title,
                "entry": markdowner.convert(util.get_entry(title)),
                "form": edit_form
            })

def create(request):

    #print request method and data to check status
    print('The request method is:', request.method)
    print('The POST data is:', request.POST)

    if request.method == "POST":
        # existing entries to compare with user input data
        entries = util.list_entries()
        entriesLower = [entry.lower() for entry in entries]

        # save user input data
        form = CreateNewPage(request.POST)
        # if form is valid and entry does not exist append entries
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            # make input lowercase
            titleLower = title.lower()

            # if entry does not already exist save input data and show new entry's page
            if not titleLower in entriesLower:
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": markdowner.convert(util.get_entry(title))
                })

            else:
                # if entry exist already show error message
                return render(request, "encyclopedia/errorMessage.html", {
                    "message": f"error: \"{title}\" is existing entry."
                })

        # if form is not valid show create page with typed form data
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    # get form
    return render(request,"encyclopedia/create.html", {
        "form": CreateNewPage()
    })

def random_entry(request):

    entries = util.list_entries()
    print(entries)

    title = random.choice(entries)
    print(title)
    entry = markdowner.convert(util.get_entry(title))


    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })


def search(request):

    # if user submits search query
    if request.method == "POST":
        #required informations for comparing
        query = request.POST["q"].lower()
        entries = util.list_entries()
        entriesLower = [entry.lower() for entry in entries]
        matchingEntries = [entry for entry in entriesLower if query in entry]

        # if submitted query matches with existing entries show it.
        if query in entriesLower:
            return render(request,"encyclopedia/entry.html", {
                "title": query,
                "entry": markdowner.convert(util.get_entry(query))
            })

        # if substring of query matches with existing entries show it.
        elif matchingEntries:
            return render(request,"encyclopedia/matchingSearch.html", {
                "entries": matchingEntries
            })

        # if query does not match, show message
        else:
            return render(request, "encyclopedia/errorMessage.html", {
                "message": f"message: \"{query}\" does not exist"
            })
