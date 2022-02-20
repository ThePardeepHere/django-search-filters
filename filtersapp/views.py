from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from datetime import datetime,timedelta

class CustomUserFilterApiView(APIView):

    def get(self,request,*args,**kwargs):
        queryset=User.objects.all()

        #Custom Filters Parameters

        check_active_users=self.request.query_params.get('check_active_users',None)
        check_superusers=self.request.query_params.get('check_superusers',None)
        check_login=self.request.query_params.get('check_login',None)
        check_date_joined=self.request.query_params.get('check_date_joined',None)


        from_date=self.request.query_params.get('from_date',None)
        to_date=self.request.query_params.get('to_date',None)

        if check_active_users: # check if key is not None
            queryset=queryset.filter(is_active=check_active_users)

        if check_superusers: # check if key is not None
            queryset=queryset.filter(is_superuser=check_superusers)

        # Date Filters

        if from_date and to_date: # check if key is not None
            date_format='%d-%m-%Y'
            from_date=datetime.strptime(from_date,date_format) #Convert string into date format
            to_date=datetime.strptime(to_date,date_format)
            to_date=to_date+timedelta(days=1) # add extra day in date search
            queryset=queryset.filter(date_joined__range=[from_date,to_date]) 

        if check_login and ( from_date and to_date ):
            queryset=queryset.filter(last_login__range=[from_date,to_date]) 
        
        if check_date_joined and ( from_date and to_date ):
            queryset=queryset.filter(date_joined__range=[from_date,to_date]) 

        serializer=CustomUserFilterSerializer(queryset,many=True)

        return Response(serializer.data)