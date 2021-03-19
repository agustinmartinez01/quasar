from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from Space.models import Satelite
from Space.serializers import (
    SateliteReadSerializer,
    SateliteWriteSerializer,
)
from Space.mediator import ConcreteMediator
# Create your views here.

class SpaceViewSet(viewsets.ModelViewSet):
    """
    VQtoCQirrelevanceRelationViewSet

    ModelViewSet
    for VQtoCQirrelevanceRelation object, Include
        list(), create(), destroy()
    operations
    """
    queryset = Satelite.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_action_classes = {
        'create': SateliteWriteSerializer,
        'update': SateliteWriteSerializer,
        'partial_update': SateliteWriteSerializer,
        'list': SateliteReadSerializer,
        'retrieve': SateliteReadSerializer,
    }
    authentication_classes = []
    permission_classes = ()
    #filter_backends = (filters.DjangoFilterBackend,)
    #filterset_class = SateliteListFilter

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


    def custom_perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                self.custom_perform_create(serializer)
            except Exception:
                return Response({'Data invalid': request.data}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Data invalid': request.data}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data: ':request.data} , status=status.HTTP_201_CREATED)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def custom_perform_update(self, serializer):

        return serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializers = self.get_serializer(instance, data=request.data)
            if serializers.is_valid():
                created_object = self.custom_perform_update(serializers)
                return Response({'Data: ':request.data},status=status.HTTP_200_OK)
            else:
                return Response({'Error: ':'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Error: ':'The instance does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class TopSecret(APIView):

    def update_satelites(self, data):
        try:
            satelite_one = Satelite.objects.get(name=data['satelites'][0]['name'])
            satelite_one._message = data['satelites'][0]['message']
            satelite_one._distance = data['satelites'][0]['distance']
            satelite_one.save()

            satelite_two = Satelite.objects.get(name=data['satelites'][1]['name'])
            satelite_two._message = data['satelites'][1]['message']
            satelite_two._distance = data['satelites'][1]['distance']
            satelite_two.save()

            satelite_three = Satelite.objects.get(name=data['satelites'][2]['name'])
            satelite_three._message = data['satelites'][2]['message']
            satelite_three._distance = data['satelites'][2]['distance']
            satelite_three.save()
            return satelite_one, satelite_two, satelite_three
        except Exception:
            return None, None, None


    def post(self, request, format=None):
        print("data", request.data)
        if 'satelites' in request.data:
            if len(request.data['satelites'])>2:
                satelite_one, satelite_two, satelite_three = self.update_satelites(request.data)
                if satelite_one is not  None and satelite_two is not None and satelite_three is not None:
                    satelites = ConcreteMediator(satelite_one, satelite_two, satelite_three)
                    message = satelites.get_message()
                    position = satelites.get_location()
                    if message != "":
                        return Response({'message: ': message, 'position':position}, status=status.HTTP_200_OK)
                    else:
                        return Response('Fails resolve message: ', status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'Invalid data for satelites: ': request.data}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'At most 3 satellites are needed: ': len(request.data['satelites'])}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Not satelites in body: ': request.data}, status=status.HTTP_400_BAD_REQUEST)





