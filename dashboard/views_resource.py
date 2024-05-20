from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms_resource_cost import ResourceCostForm
from .models_resource_cost import ResourceCost
from users.decorators import superuser_required
import datetime


@superuser_required
def resource_cost_list(request):
    query = request.GET.get('q', '').strip().lower()
    if query:
        try:
            # Attempt to parse the query as a date
            date_query = datetime.datetime.strptime(query, '%d/%m/%Y').date()
        except ValueError:
            date_query = None

        resources = ResourceCost.objects.filter(
            Q(item_type__icontains=query) |
            Q(item_name__icontains=query) |
            Q(item_id__icontains=query) |
            Q(item_location__icontains=query) |
            Q(unit_of_measure__icontains=query) |
            Q(mobilisation_desc__icontains=query) |
            Q(item_rate__icontains=query) |
            (Q(created_date__date=date_query) | Q(last_modification_date__date=date_query) if date_query else Q())
        ).order_by('-created_date')
    else:
        resources = ResourceCost.objects.all().order_by('-last_modification_date')

    paginator = Paginator(resources, 15)  # Show 10 records per page.
    page_number = request.GET.get('page')
    resources_list  = paginator.get_page(page_number)
    return render(request, 'resource_cost/resource_cost_list.html', {'resources': resources_list})

@superuser_required
def create_resource_cost(request):
    if request.method == 'POST':
        form = ResourceCostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource cost created successfully.")
            return redirect('resource_cost_list')  # Redirect to the resource cost listing page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResourceCostForm()

    return render(request, 'resource_cost/resource_cost_create.html', {'form': form})

@superuser_required
def edit_resource_cost(request, resource_id):
    resource = get_object_or_404(ResourceCost, pk=resource_id)
    if request.method == 'POST':
        form = ResourceCostForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource_cost_list')
    else:
        form = ResourceCostForm(instance=resource)

    return render(request, 'resource_cost/edit_resource_cost.html', {
        'form': form,
        'resource': resource
    })

@superuser_required
def delete_resource_cost(request, resource_id):
    resource = get_object_or_404(ResourceCost, pk=resource_id)

    if request.method == 'POST':
        resource.delete()
        messages.success(request, "Resource cost deleted successfully.")
        return redirect('resource_cost_list')

    return render(request, 'resource_cost/resource_delete_confirm.html', {'resource': resource})