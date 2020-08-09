from django.shortcuts import render
from markdown2 import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from random import randint


from . import util


class NewPageForm(forms.Form):
    entry_title = forms.CharField(label="Title")
    entry_body = forms.CharField(label="", widget=forms.Textarea)


class EditPageForm(forms.Form):
    entry_body = forms.CharField(label="", widget=forms.Textarea)


# index page shows the list of encyclopedia entries


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# entry page retrieves markdown text for entry and converts to HTML
# before displaying. If no matching entry is found an error 404 is displayed


def entry(request, entry):
    entry_body = util.get_entry(entry)
    if entry_body is None:
        return render(request, "encyclopedia/error.html", {
            "message": "404 Error: No entry found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry,
            "entry_body": markdown(entry_body)
        })

# search page returns the entry page if entry matches (case sensitive)
# if no exact match a list of search results which match the substring is
# returned


def search(request):
    if (request.method == 'POST'):
        q = request.POST.get('q')
        substring_entries = []
        entries = util.list_entries()
        for entry in entries:
            if q == entry:
                return HttpResponseRedirect(reverse('entry', args=(entry,)))
            elif q in entry:
                substring_entries.append(entry)
        return render(request, "encyclopedia/search_results.html", {
            "substring_entries": substring_entries
        })
    else:
        return HttpResponseRedirect(reverse('index'))


# new_page returns a page with a Django form (defined in class statement at
# top). Form includes a title and a textarea for markdown. This allows a
# new entry to be added to the encyclopedia. If the
# title exactly matches an existing title an error message is returned,
# otherwise the new entry is saved to disk.


def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            entry_body = form.cleaned_data["entry_body"]
            if entry_title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "message": "Title Not Available"
                })
            else:
                util.save_entry(entry_title, entry_body)
                return HttpResponseRedirect(reverse('entry', args=(entry_title,)))
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPageForm()
        })


# edit page provides the existing markup text for an entry to be displayed in
# a textarea of a Django form. The text can be edited and then saved using the
# same title.


def edit_page(request, entry):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            entry_title = entry
            entry_body = form.cleaned_data["entry_body"]
            util.save_entry(entry_title, entry_body)
            return HttpResponseRedirect(reverse('entry', args=(entry_title,)))
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "entry": entry,
                "form": form
            })
    else:
        # this code prepopulates the textarea with the initial value
        form = EditPageForm(initial={'entry_body': util.get_entry(entry)})
        return render(request, "encyclopedia/edit_page.html", {
            "entry": entry,
            "form": form
        })


# Random page enables the user to jump to a randomly selected entry in the
# encyclopedia. randint(a,b) provides a random integer between and including
# the values a and b.


def random(request):
    entries = util.list_entries()
    index = randint(0, (len(entries)-1))
    entry = entries[index]
    return HttpResponseRedirect(reverse('entry', args=(entry,)))
