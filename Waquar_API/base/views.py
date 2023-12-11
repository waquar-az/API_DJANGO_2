from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Q
from rest_framework.views import APIView

from .serializers import AdvocateSerializer,Company,CompanySerializer
# Create your views here.
from .models import Advocate,Company
@api_view(['GET'])
def endpoints(request):
    data=['/advocates','advocates/:username'] 
    return Response(data)

@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
def advocate_list(request):
    if request.method=='GET':
        #data=['waquar','azam','Mname']
        query= request.GET.get('query')
        #print("queryy:",query)
        
        if query==None:
            query= ''
            
        #advocate=Advocate.objects.all()
        advocate=Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        serializer= AdvocateSerializer(advocate,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':       
        advocate=Advocate.objects.create(username=request.data['username'],bio=request.data['bio'])
        serializer= AdvocateSerializer(advocate,many=False)
        return Response(serializer.data)
 
class AdvocateDetail(APIView):
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise JsonResponse('Advocate doesnot exist')
    def get(self, request, username):
        #advocate = Advocate.objects.get(username=username)
        advocate=self.get_object(username) 
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def put(self, request, username):  
        #advocate = Advocate.objects.get(username=username) 
        advocate=self.get_object(username)       
        advocate.username=request.data['username']
        advocate.bio=request.data['bio']
        
        serializer= AdvocateSerializer(advocate,many=False)    
        return Response(serializer.data)
    
    def delete(self, request, username):
        #advocate = Advocate.objects.get(username=username)
        advocate=self.get_object(username)  
        advocate.delete()
        return Response('user was deleted')

@api_view(['GET']) 
def companies_list(request):   
    companies=Company.objects.all()
    serializer=CompanySerializer(companies,many=True)
    return Response(serializer.data)
#######This doesnot work properly so we use Class method------###
# @api_view(['GET','PUT','DELETE'])
# def advocate_details(request,username):
#     if request.method=='GET':
#     #data= username
#         advocate=Advocate.objects.get(username=username)
#         serializer= AdvocateSerializer(advocate,many=False)    
#         return Response(serializer.data)
#     if request.method=='PUT':
#         advocate=Advocate.objects.get(username=username)
#         advocate.username=request.data['username']
#         advocate.bio=request.data['bio']
#         advocate.save()
        
#         serializer= AdvocateSerializer(advocate,many=False)    
#         return Response(serializer.data)
#     if request.method=='DELETE':
#         advocate=Advocate.objects.get(username=username)
#         advocate.delete()
#         #return redirect('/advocates')
#         return Response('user was deleted')  
    