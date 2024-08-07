from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, ProtectedError
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
        records_list = Project.objects.filter(
            Q(project_no__icontains=query) |
            Q(project_name__icontains=query) |
            Q(client__icontains=query) |
            Q(purchase_order_no__icontains=query) |
            Q(project_budget__icontains=query) |
            (Q(is_active=is_active_query) if is_active_query is not None else Q())
        ).order_by('-project_no')
    else:
        records_list = Project.objects.order_by('-project_no')

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
            messages.error(request, 'Failed to create a Project. Please check the errors below.')
    else:
        form = ProjectForm()

    return render(request, 'project/project_create.html', {'form': form, 'form_action': form_action})

@superuser_required
def project_update(request, project_no):
    record = get_object_or_404(Project, pk=project_no)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=record)
        if form.is_valid():
          form.save()
          messages.success(request, 'Project updated successfully.')
          return redirect('project_list')
        else:
            messages.error(request, 'Failed to create a Project. Please check the errors below.')
    else:
        form = ProjectForm(instance=record)

    form_action = reverse('project_update', args=[project_no])
    return render(request, 'project/project_update.html', {'form': form, 'record': record, 'form_action': form_action})



@superuser_required
def project_delete(request, project_no):
    record = get_object_or_404(Project, pk=project_no)

    if request.method == 'POST':
        try:
            record.delete()
            messages.success(request, "Project deleted successfully.")
            return redirect('project_list')
        except ProtectedError as e:
            # Extracting information from the ProtectedError
            message = f"Cannot delete this project because '{record}' is referenced by other records. Please set the project status to inactive."
            messages.error(request, message)
            return redirect('project_list')  # Redirect to the list or some error page

    return render(request, 'project/project_delete_confirm.html', {'record': record})
