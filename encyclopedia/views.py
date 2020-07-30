from django.shortcuts import render
from markdown2 import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms


from . import util


class NewPageForm(forms.Form):
    entry_title = forms.CharField(label="Title")
    entry_body = forms.CharField(widget=forms.Textarea)


# index page shows the list of encyclopedia entries


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# entry page retrieves markdown text for entry and converts to HTML
# before displaying if no matching entry is found an error 404 is displayed


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
