from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .forms import ScrapedForm
from .models import RecipeURL, Assignment


# Create your views here.
def route_work(request):
    url = find_url()
    if url is None:
        request.session['assignment_id'] = -1
        return HttpResponse('<h1>No URL remaining</h1>')
    assignment = Assignment.objects.create(url=url)
    assignment.save()
    request.session['assignment_id'] = assignment.id

    return redirect('start_work')


def start_work(request):
    if request.method == 'POST':
        return save_work(request)

    assignment_id = request.session['assignment_id']
    assignment = Assignment.objects.get(id=assignment_id)
    url = assignment.url.url
    form = ScrapedForm()
    context = {
        'url': url,
        'scrape_form': form,
    }
    return render(request, 'scrape.html', context)


def save_work(request):
    form = ScrapedForm(request.POST)
    assignment_id = request.session['assignment_id']
    assignment = Assignment.objects.get(id=assignment_id)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.scraped_by_id = assignment_id
        obj.save()
        assignment.finished_at = timezone.now()
        assignment.save()
    return redirect('show_result')


def show_result(request):
    assignment_id = request.session['assignment_id']
    assignment = Assignment.objects.get(id=assignment_id)
    token = 'JOB NOT FINISHED. PLEASE FILL THE FORM AGAIN'
    if assignment.finished_at:
        token = assignment.token

    return render(request, 'success.html', {'token': token})


def find_url():
    url = RecipeURL.objects.annotate(
        num_finished=Count('assignment__finished_at'),
    ).filter(num_finished__lt=3).first()

    return url
