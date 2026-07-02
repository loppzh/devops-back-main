import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Item

@method_decorator(csrf_exempt, name='dispatch')
class ItemListView(View):
    def get(self, request):
        items = list(Item.objects.all().values('id', 'name'))
        return JsonResponse(items, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        item = Item.objects.create(name=data.get('name'))
        return JsonResponse({'id': item.id, 'name': item.name}, status=201)