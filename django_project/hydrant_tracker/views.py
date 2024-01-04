from django.shortcuts import render
from .models import MapPoint
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

def map_view(request):
    points = MapPoint.objects.all()
    return render(request, 'map_template.html', {'points': points})

@require_http_methods(["POST"])
def update_point(request):
    # Add logic to update a point
    # Extract data from request.POST and update the point in the database
    return JsonResponse({"success": True})
