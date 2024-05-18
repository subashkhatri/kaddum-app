from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms_project import ProjectForm
from .models import Project
from django.contrib import messages
from .forms_project import ProjectForm
import logging
from django.core.paginator import Paginator
from users.decorators import superuser_required



logger = logging.getLogger(__name__)

@superuser_required
def project_list(request):
    records_list = Project.objects.order_by('-created_date')
    paginator = Paginator(records_list, 15)  # Show 10 records per page.
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    return render(request, 'project/project_list.html', {'records': projects})

@superuser_required
def project_create(request):
    form_action = reverse('project_create')
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request, 'Project created successfully.')
          return redirect('project_list')
    else:
        form = ProjectForm()
        return render(request, 'project/project_create.html', {'form': form, 'form_action': form_action})

@superuser_required
def project_update(request, project_no):
    form_action = reverse('project_update', args=[project_no])
    record = get_object_or_404(Project, pk=project_no)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=record)
        if form.is_valid():
          form.save()
          messages.success(request, 'Project updated successfully.')
          return redirect('project_list')
    else:
        form = ProjectForm(instance=record)
        return render(request, 'project/project_update.html', {'form': form, 'record': record, 'form_action': form_action})

@superuser_required
def project_delete(request, project_no):
    record = get_object_or_404(Project, pk=project_no)

    if request.method == 'POST':
        record.delete()
        messages.success(request, "Project deleted successfully.")
        return redirect('project_list')

    return render(request, 'project/project_delete_confirm.html', {'record': record})


