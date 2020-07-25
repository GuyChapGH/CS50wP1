from django.shortcuts import render
from markdown2 import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse


from . import util
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
