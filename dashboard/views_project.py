from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

import logging
import datetime
from .models import Project
from .forms_project import ProjectForm
from users.decorators import superuser_required



logger = logging.getLogger(__name__)

@superuser_required
def project_list(request):
    query = request.GET.get('q', '').strip().lower()

    # Determine boolean value for "is_active" based on query
    is_active_query = {'active': True, 'inactive': False}.get(query, None)

    if query:
        try:
            # Attempt to parse the query as a date
            date_query = datetime.datetime.strptime(query, '%d/%m/%Y').date()
        except ValueError:
            date_query = None

        records_list = Project.objects.filter(
            Q(project_no__icontains=query) |
            Q(purchase_order_no__icontains=query) |
            Q(project_name__icontains=query) |
            Q(client__icontains=query) |
            Q(project_start_date=date_query) |
            Q(project_end_date=date_query) |
            Q(project_budget__icontains=query) |
            (Q(is_active=is_active_query) if is_active_query is not None else Q())
        ).order_by('-created_date')
    else:
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


