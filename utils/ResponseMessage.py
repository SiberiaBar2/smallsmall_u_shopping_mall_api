import json
from django.http import HttpResponse, JsonResponse

class MenuResponse():
    @staticmethod
    def success(data):
        result = {"status": 1000, "data": data}
        result = HttpResponse(json.dumps(result), content_type='application/json')
        return result

    @staticmethod
    def failed(data):
        result = {"status": 1001, "data": data}
        result = HttpResponse(json.dumps(result), content_type='application/json')
        return result

    @staticmethod
    def other(data):
        result = {"status": 1002, "data": data}
        result = HttpResponse(json.dumps(result), content_type='application/json')
        return result

class GoodsResponse():
    @staticmethod
    def success(data):
        result = {"status": 2000, "data": data}
        result = HttpResponse(json.dumps(result), content_type='application/json')
        return result

    @staticmethod
    def failed(data):
        result = {"status": 2001, "data": data}
        result = HttpResponse(json.dumps(result), content_type='application/json')
        return result

    @staticmethod
    def other(data):
        result = {"status": 2002, "data": data}
        result = HttpResponse(json.dumps(result), content_type='application/json')
        return result

class CartResponse():
    @staticmethod
    def success(data):
        result = {"status": 3000, "data": data}
        result = HttpResponse(json.dumps(result), content_type='application/json')
        return result

    @staticmethod
    def failed(data):
        result = {"status": 3001, "data": data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data):
        result = {"status": 3002, "data": data}
        return JsonResponse(result, safe=False)

class UserResponse():
    @staticmethod
    def success(data):
        result = {"status": 4000, "data": data}
        result = JsonResponse(result)
        return result

    @staticmethod
    def failed(data):
        result = {"status": 4001, "data": data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data):
        result = {"status": 4002, "data": data}
        return JsonResponse(result, safe=False)

class CommentResponse():
    @staticmethod
    def success(data):
        result = {"status": 5000, "data": data}
        result = JsonResponse(result, safe=False)
        return result

    @staticmethod
    def failed(data):
        result = {"status": 5001, "data": data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data):
        result = {"status": 5002, "data": data}
        return JsonResponse(result, safe=False)

class AdddressResponse():
    @staticmethod
    def success(data):
        result = {"status": 6000, "data": data}
        result = JsonResponse(result, safe=False)
        return result

    @staticmethod
    def failed(data):
        result = {"status": 6001, "data": data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data):
        result = {"status": 6002, "data": data}
        return JsonResponse(result, safe=False)