from .models import ResourceCost
from .models_resource_cost import ResourceCost
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms_resource_cost import ResourceCostForm
from django.contrib import messages
from users.decorators import superuser_required

@superuser_required
def resource_cost_list(request):
    resources = ResourceCost.objects.all().order_by('-last_modification_date')
    return render(request, 'resource_cost/resource_cost_list.html', {'resources': resources})

@superuser_required
def create_resource_cost(request):
    if request.method == 'POST':
        form = ResourceCostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource cost created successfully.")
            return redirect('resource_cost_list')  # Redirect to the resource cost listing page
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