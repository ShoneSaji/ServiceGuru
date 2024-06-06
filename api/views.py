from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response

from rest_framework.decorators import action

from rest_framework import authentication,permissions

from api.serializers import CustomerSerializer,WorkSerializer

from api.models import Customer




class CustomerViewSetView(ModelViewSet):

    serializer_class = CustomerSerializer

    queryset=Customer.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAdminUser]


    def perform_create(self, serializer):
        
        serializer.save(technician=self.request.user)

    @action(method=["post"],detail=True)
    def add_work(self,request,*args,**kwargs):

       # customer_instance=self.get_object()-->id=...

       id=kwargs.get("pk")

       customer_instance=Customer.objects.get(id=id)

       serializer=WorkSerializer(data=request.data)

       if serializer.is_valid():
           
           serializer.save(customer=customer_instance)

           return Response(data=serializer.data)
       
       else:
           
           return Response(data=serializer.errors)

