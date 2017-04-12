from django.shortcuts import render, redirect
from election.models import Country, Voivodeship, District, Commune, Circuit, Vote, Candidate
from django.shortcuts import get_object_or_404
from .forms import VoteForm
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage

def country(request):
    area=Country.objects.get(name='Polska')
    return render(request, 'country.html', {'area': area})

def voivodeship(request, id):
    area = get_object_or_404(Voivodeship, id=id)
    return render(request, 'voivodeship.html', {'area': area})

def district(request, vid, id):
    area = get_object_or_404(District, id=id)
    return render(request, 'district.html', {'area': area})

def commune(request, vid, did, id):
    area = get_object_or_404(Commune, id=id)
    return render(request, 'commune.html', {'area': area})

def vote_update(request, vid, did, cid, circid, candid):

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    circ = get_object_or_404(Circuit, id=circid)
    cand = get_object_or_404(Candidate, id=candid)
    vote = get_object_or_404(Vote, circuit=circ, candidate=cand)
    form = VoteForm(request.POST or None, instance=vote)
    if form.is_valid():
        vote = form.save(commit=False)
        vote.save()
        return HttpResponseRedirect(request.POST.get('next', '/'))
    return render(request, 'vote_form.html', {'form': form, 'vote':vote, 'next':request.META.get('HTTP_REFERER')})

def search(request):

    if request.method == 'GET':
        query = request.GET.get('q', None)
        try:
            page = int(request.GET.get('p', '1'))
        except:
            page = 1

        if query and page:
            rs = Commune.objects.filter(name__icontains=query)
            paginator = Paginator(rs, 20)
            try:
                result = paginator.page(page)
            except EmptyPage:
                result = paginator.page(paginator.num_pages)
            print(type(result))
            index = result.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 2 if index >= 2 else 0
            end_index = index + 3 if index <= max_index - 3 else max_index
            page_range = paginator.page_range[start_index:end_index]
            return render(request, 'search.html', {'query': query, 'result':result, 'page_range': page_range})

    return render(request, 'search.html')
