from django.shortcuts import render
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


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
