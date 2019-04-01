from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        name = args[0].request.data.get("name", "")
        restaurant = args[0].request.data.get("restaurant", "")
        if not name and not restaurant:
            return Response(
                data={
                    "message": "Both name and restaurant are required to add a dish"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
