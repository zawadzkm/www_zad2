from django.shortcuts import render, redirect
from election.models import Country, Voivodeship, District, Commune, Circuit, Vote, Candidate
from django.shortcuts import get_object_or_404
from .forms import VoteForm
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse

def country(request):
    area=Country.objects.get(name='Polska')
    return render(request, 'country.html', {'area': area})

def voivodeship(request, vno):
    area = get_object_or_404(Voivodeship, no=vno)
    return render(request, 'voivodeship.html', {'area': area})

def district(request, vno, dno):
    area = get_object_or_404(District, no=dno)
    return render(request, 'district.html', {'area': area})

def commune(request, vno, dno, ccode):
    area = get_object_or_404(Commune, code=ccode)
    return render(request, 'commune.html', {'area': area})

def vote_update(request, vno, dno, ccode, circid, candid):
    if request.user.is_anonymous:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    circ = get_object_or_404(Circuit, id=circid)
    cand = get_object_or_404(Candidate, id=candid)
    vote = get_object_or_404(Vote, circuit=circ, candidate=cand)
    if request.method == 'POST':
        form = VoteForm(request.POST or None, instance=vote)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.save()
            return HttpResponseRedirect(reverse('commune', args=[circ.commune.district.voivodeship.no, circ.commune.district.no, circ.commune.code]))
    else:
        form = VoteForm(instance=vote)

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

            index = result.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 2 if index >= 2 else 0
            end_index = index + 3 if index <= max_index - 3 else max_index
            page_range = paginator.page_range[start_index:end_index]
            return render(request, 'search.html', {'query': query, 'result':result, 'page_range': page_range})

    return render(request, 'search.html')
