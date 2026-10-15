from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def placeholder(request, title):
    """Temporary page so every menu/footer link works until its real step is built."""
    return render(request, "placeholder.html", {"page_title": title})


def search(request):
    return render(request, "search.html", {"q": request.GET.get("q", "").strip()})
