import traceback
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from Space.models import Satelite
from Space.mediator import ConcreteMediator
from Space.serializers import (
    SateliteReadSerializer,
    SateliteWriteSerializer,
)


class SpaceViewSet(viewsets.ModelViewSet):
    """
        SpaceViewSet

        ModelViewSet for SpaceViewSet object, Include list(), create(), update() and retrieve() operations
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
        satelites = Satelite.objects.all()
        if satelites.count()<=2:

            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                try:
                    self.custom_perform_create(serializer)
                except Exception:
                    return Response({'Data invalid': request.data}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'Data invalid': request.data}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'data: ':request.data} , status=status.HTTP_201_CREATED)
        else:
            return Response({'satellite limit exceeded': request.data}, status=status.HTTP_400_BAD_REQUEST)

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
    """
        TopSecret

        APIView for TopSecret object, Include post() operations
    """
    def update_satelites(self, data):
        try:
            satelite_one = Satelite.objects.get(name=data['satelites'][0]['name'])
            satelite_one.set_distance(data['satelites'][0]['distance'])
            satelite_one.set_message(data['satelites'][0]['message'])
            satelite_one.save()

            satelite_two = Satelite.objects.get(name=data['satelites'][1]['name'])
            satelite_two.set_distance(data['satelites'][1]['distance'])
            satelite_two.set_message(data['satelites'][1]['message'])
            satelite_two.save()

            satelite_three = Satelite.objects.get(name=data['satelites'][2]['name'])
            satelite_three.set_distance(data['satelites'][2]['distance'])
            satelite_three.set_message(data['satelites'][2]['message'])
            satelite_three.save()
            return satelite_one, satelite_two, satelite_three
        except Exception:
            print(traceback.format_exc())
            return None, None, None

    def post(self, request, format=None):
        """
           :param request:
           :param format:10
           :return: message and positions
        """
        if 'satelites' in request.data:
            if len(request.data['satelites'])>2:
                satelite_one, satelite_two, satelite_three = self.update_satelites(request.data)
                if satelite_one is not  None and satelite_two is not None and satelite_three is not None:
                    satelites = ConcreteMediator(satelite_one, satelite_two, satelite_three)
                    message = satelites.get_message()
                    lat, lon = satelites.get_location()
                    if message is not None:
                        return Response({'message: ': message, 'position':{'lat:':lat, 'lon':lon}}, status=status.HTTP_200_OK)
                    else:
                        return Response('Fails resolve message: ', status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'Invalid data for satelites: ': request.data}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'At most 3 satellites are needed: ': len(request.data['satelites'])}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Not satelites in body: ': request.data}, status=status.HTTP_400_BAD_REQUEST)



class TopSecretSplit(APIView):
    """
        TopSecretSplit

        APIView for TopSecretSplit object, Include post() and get() operations
    """
    def post(self, request, format=None):
        try:
            satelite = Satelite.objects.get(name=request.data['name'])
            satelite.set_message(request.data['message'])
            satelite.set_distance(request.data['distance'])
            satelite.save()
            return Response({'satelite':satelite.get_name(), 'distance':satelite.get_distance()}, status=status.HTTP_200_OK)
        except Exception:
            print(traceback.format_exc())
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        try:
            satelite = Satelite.objects.get(name=request.META['PATH_INFO'][21:])
            satelites = Satelite.objects.all().order_by('id')
            list_satelites = (list(satelites))
            concrete_space = ConcreteMediator(list_satelites[0], list_satelites[1], list_satelites[2])
            message = concrete_space.get_message()
            lat, lon = concrete_space.get_location()
            return Response({'message': message, 'position': str(lat)+" - "+str(lon)}, status=status.HTTP_200_OK)
        except Exception:
            print(traceback.format_exc())
            return Response(status=status.HTTP_404_NOT_FOUND)


