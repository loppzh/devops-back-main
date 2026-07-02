import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Item

@method_decorator(csrf_exempt, name='dispatch')
class ItemListView(View):
    def get(self, request):
        items = list(Item.objects.all().values('id', 'name', 'date'))
        return JsonResponse(items, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        item = Item.objects.create(
            name=data.get('name'),
            date=data.get('date')
        )
        return JsonResponse({'id': item.id, 'name': item.name, 'date': item.date}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class ItemDetailView(View):
    def put(self, request, item_id):
        data = json.loads(request.body)
        try:
            item = Item.objects.get(id=item_id)
            item.name = data.get('name', item.name)
            item.date = data.get('date', item.date)
            item.save()
            return JsonResponse({'id': item.id, 'name': item.name, 'date': item.date})
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            return JsonResponse({'message': 'Deleted successfully'}, status=204)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)