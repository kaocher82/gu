from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.conf import settings as django_settings
from . import settings


from . import models

versions = {key: value for (key, value) in
            django_settings.FILEBROWSER_VERSIONS.items()
            if not key.startswith("admin")}
versions = sorted(versions.items(),key=lambda x: x[1]["width"])

def album_list(request):
    albums = models.Album.objects.all()
    return render(request, "gallery/album_list.html",
                  {'albums':albums,})


def album_detail(request, pk):
    album = get_object_or_404(models.Album, pk=pk)
    return render(request, "gallery/album_detail.html",
                  {'album':album,})


def photo_list(request, keyword=None):
    search_string = ""
    list_all = True
    if keyword:
        query = Q(keywords__name__in=[keyword])
        list_all = False
    else:
        query = Q()

    if "search-photos" in request.GET:
        search_string = request.GET["search-photos"]
        search_query = Q(suggested_caption__icontains=search_string) | \
                       Q(photographer__last_name__icontains=search_string) | \
                       Q(photographer__first_names__icontains=search_string) | \
                       Q(keywords__name__in=[search_string])
        query = query & search_query
        list_all = False

    photos = models.Photograph.objects.filter(query).distinct()
    return render(request, "gallery/photo_list.html",
                  {'photos': photos,
                   'keyword': keyword,
                   'search_string': search_string,
                   'list_all': list_all})


def photo_detail(request, pk):
    photo = get_object_or_404(models.Photograph, pk=pk)
    return render(request, "gallery/photo_detail.html",
                  {'photo':photo,
                   'default_copyright': settings.DEFAULT_COPYRIGHT,
                   'versions': versions})


def gallery_front(request):
    featured_photos = models.Photograph.objects.filter(featured=True).\
                         order_by('-modified')[:settings.NUM_FEATURED]
    latest_photos = models.Photograph.objects.filter(featured=False).\
                    order_by('-modified')[:settings.NUM_LATEST]
    latest_albums = models.Album.objects.all().order_by('-modified')\
                    [:settings.NUM_ALBUMS]
    return render(request, "gallery/index.html",
                  {'featured_photos': featured_photos,
                   'latest_photos': latest_photos,
                   'latest_albums': latest_albums})
