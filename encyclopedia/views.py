from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

from . import util


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
        "entry": util.get_entry(title),
        })

        # if it doesn't show error message
    else:
        return render(request, "encyclopedia/errorMessage.html", {
        "message": "message: entry does not exist"
        })


def search(request):

    # if user submits search query
    if request.method == "POST":
        query = request.POST["q"].lower()
        entries = util.list_entries()
        entriesLower = [entry.lower() for entry in entries]
        matchingEntries = [entry for entry in entriesLower if query in entry]

        # if submitted query matches with existing entries show it.
        if query in entriesLower:
            return render(request,"encyclopedia/entry.html", {
            "title": query,
            "entry": util.get_entry(query)
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
