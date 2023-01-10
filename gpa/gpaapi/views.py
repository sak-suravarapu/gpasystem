from django.http import Http404
from django.http import HttpResponse
from django.db import transaction
from datetime import datetime

#rest framework specific libraries

from rest_framework import generics, filters
from rest_framework import mixins
from rest_framework import request

from decimal import Decimal

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
# The below import for authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User


#libraries from the app
from gpaapi.models import PGAccounts
from gpaapi.models import PGTransactions
from gpaapi.models import PGBalance
from gpaapi.serializers import PGAccountsSerializer
from gpaapi.serializers import PGTransactionsSerializer
from gpaapi.serializers import PGBalanceSerializer
from gpaapi.serializers import UserSerializer
from gpaapi.serializers import MyTokenObtainPairSerializer, RegisterSerializers

# Create your views here.

class PGAccountsList(generics.ListCreateAPIView):
    """
    List all accounts or create a new account
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset=PGAccounts.objects.all()
    serializer_class=PGAccountsSerializer

class PGAccountsDetail(APIView):
    """
    Retrieve, update or delete an account
    """
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return PGAccounts.objects.get(pk=pk)
        except PGAccounts.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        account = self.get_object(pk)
        serializer = PGAccountsSerializer(account)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        account=self.get_object(pk)
        serializer=PGAccountsSerializer(account,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        account=self.get_object(pk)
        account.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

class PGTransactionsList(APIView):

    """
    List all transactions or create a new transaction
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,format=None):
        accounts = PGTransactions.objects.all()
        serializer = PGTransactionsSerializer(accounts, many=True)
        return Response(serializer.data)
    
    @transaction.atomic
    def post(self,request2,format=None):
        serializer = PGTransactionsSerializer(data=request2.data)
        if serializer.is_valid():
            # variables to hold the values
            
            acctid=request2.data['account_id']
            trantype=request2.data['transaction_type']
            tranamt=request2.data['amount']

            self1=PGAccountsDetail()
            account=self1.get_object(pk=acctid)
            
            curr_bal=account.current_balance
            member=PGAccounts.objects.get(pk=account.account_number)
            member.account_number=account.account_number
            member.user_id=account.user_id
            if trantype == 'DEBIT':    
                member.current_balance = curr_bal-Decimal(tranamt)                
            elif trantype == 'CREDIT':
                member.current_balance = curr_bal+Decimal(tranamt)
            dt=datetime.strptime(request2.data['date'],"%Y-%m-%dT%H:%M:%SZ").date()
            
            try:
                balance=PGBalance.objects.get(account_id=acctid,date=dt)
                """
                There is an existing entry for the date and account id - Hence, just need to update the balance
                """
                balance.account_id=member
                balance.date=dt
                """
                We want the balance to reflect the most current balance
                """
                bal = member.current_balance
                curr_bal=member.current_balance
                """
                """
                balance.balance=bal
                #balance.balance
            except PGBalance.DoesNotExist:
                try:
                    balance=PGBalance.objects.get(account_id=acctid)
                    # curr_bal=balance.balance                    
                    """
                    There is an entry for the account, hence, we need to determine the most recent entry for the account and then use that as current balance to update
                    using member.account_number as it requires to be an instance of PGAccounts
                    """
                    #balance=PGBalance()
                    balance = PGBalance(date=dt,balance=curr_bal,account_id=member)
                    

                    # if trantype == 'DEBIT':
                    #     balance=PGBalance(date=dt,balance=curr_bal-Decimal(tranamt),account=acctid)
                    # elif trantype =='CREDIT':
                    #     balance=PGBalance(date=dt,balance=curr_bal+Decimal(tranamt),account=acctid)                 
                except PGBalance.DoesNotExist:
                    """
                    There is no entry for the account itself, hence the current balance will be the first entry into PGBalance model
                    """
                    balance = PGBalance(date=dt,balance=curr_bal,account_id=member)
                    #balance=PGBalance(date=dt,balance=curr_bal,account_id=member.account_number)
        
            serializer.save()
            member.save()
            balance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PGBalanceList(generics.ListCreateAPIView):
    """
    List all balances
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset=PGBalance.objects.all()
    serializer_class=PGBalanceSerializer

class PGBalanceDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    List the account balance on a date
    """
    queryset=PGBalance.objects.all()
    serializer_class=PGBalanceSerializer

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def balance_detail(request, account_id, date, format=None):
        
        try:
            queryset=PGBalance.objects.get(account_id=account_id,date=date)
        except PGBalance.DoesNotExist:
            return Response(None,status=status.HTTP_404_NOT_FOUND)
        serializer = PGBalanceSerializer(queryset)
        if serializer.is_valid():
            return Response(serializer.data)
        
class PGTransactionsDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    queryset=PGTransactions.objects.all()
    serializer_class=PGTransactionsSerializer
    """
    Retrieve, update or delete an transaction
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request,*args,**kwargs)
        
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.delete(request,*args,**kwargs)

# The below view is to handle user authentication

# class UserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes=(AllowAny,)
    serializer_class=RegisterSerializers

@api_view(['GET'])
def getRoutes(request):
    routes=[
        '/token',
        '/register/',
        '/token/refresh/'
    ]
    return Response(routes)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulations {request.user}, your API was able to respond to the GET request"
        return Response({'response':data},status=status.HTTP_200_OK)
    elif request.method == "POST":
        text = request.POST.get('text')
        data = f"Congratulations {request.user}, your API was able to respond to the request with text: {text}"
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({},status.HTTP_400_BAD_REQUEST)

#End of user authentication related section

# class PGTransactionsList(mixins.ListModelMixin,
#                      mixins.CreateModelMixin,
#                      generics.GenericAPIView):
#     """
#     List all accounts or create a new account
#     """
#     queryset=PGTransactions.objects.all()
#     serializer_class=PGTransactionsSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         #Do an inquiry of account with the same id
#         account=PGAccountsDetail.get_object(pk)
#         #Update the account balance with the amount of transaction
#         return self.create(request,*args,**kwargs)

# class PGAccountsDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Retrieve, update or delete an account
#     """
#     queryset=PGAccounts.objects.all()
#     serializer_class=PGAccountsSerializer

# class PGTransactionsList(generics.ListCreateAPIView):
#     """
#     List all transactions or create a new transaction
#     """ 
#     queryset=PGTransactions.objects.all()
#     serializer_class=PGTransactionsSerializer


# class PGTransactionsDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Retrieve, update or delete a transaction
#     """
#     queryset=PGTransactions.objects.all()
#     queryset1=PGAccounts.objects.all()

#     serializer_class=PGTransactionsSerializer



#django libraries
#from django.shortcuts import render
#from django.http import HttpResponse, JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#from django.http import Http404

# The below imports are used for mixins based views
#from rest_framework import mixins

#The below imports are used for class based views

#from rest_framework.parsers import JSONParser
#from rest_framework import status
#from rest_framework.decorators import APIView
#from rest_framework.response import Response

#The below import is used for function based view and not for class based view.
#from rest_framework.decorators import api_view



# The below implementation of views using Mixins. We can take this a step further using REST framework Generic Views.

# class PGAccountsList(mixins.ListModelMixin,
#                      mixins.CreateModelMixin,
#                      generics.GenericAPIView):
#     """
#     List all accounts or create a new account
#     """
#     queryset=PGAccounts.objects.all()
#     serializer_class=PGAccountsSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class PGAccountsDetail(mixins.RetrieveModelMixin,
#                        mixins.UpdateModelMixin,
#                        mixins.DestroyModelMixin,
#                        generics.GenericAPIView):
#     """
#     Retrieve, update or delete an account
#     """
#     queryset=PGAccounts.objects.all()
#     serializer_class=PGAccountsSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request,*args,**kwargs)
        
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)

#     def delete(self,request,*args,**kwargs):
#         return self.delete(request,*args,**kwargs)




# The below is the implementation of views using class based views. We can take it a step further using the Mixins which are buts of common behavior implemented by REST franework

# class PGAccountsList(APIView):
#     """
#     List all accounts or create a new account
#     """
#     def get(self,request,format=None):
#         accounts = PGAccounts.objects.all()
#         serializer = PGAccountsSerializer(accounts, many=True)
#         return Response(serializer.data)
    
#     def post(self,request,format=None):
#         serializer = PGAccountsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PGAccountsDetail(APIView):
#     """
#     Retrieve, update or delete an account
#     """
#     def get_object(self, pk):
#         try:
#             return PGAccounts.objects.get(pk=pk)
#         except PGAccounts.DoesNotExist:
#             raise Http404

#     def get(self,request,pk,format=None):
#         account = self.get_object(pk)
#         serializer = PGAccountsSerializer(account)
#         return Response(serializer.data)

#     def put(self,request,pk,format=None):
#         account=self.get_object(pk)
#         serializer=PGAccountsSerializer(account,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk,format=None):
#         account=self.get_object(pk)
#         account.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)



# The below is the implementation of views using function based views. If we want to keep our code DRY, we need to implement class based views. 

# @api_view(['GET','POST'])
# def pgaccounts_list(request, format=None):
#     """
#     List all accounts or create a new account
#     """
#     if request.method == 'GET':
#         accounts = PGAccounts.objects.all()
#         serializer = PGAccountsSerializer(accounts, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = PGAccountsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def pgaccounts_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete an account
#     """
#     try:
#         account=PGAccounts.objects.get(pk=pk)
#     except PGAccounts.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = PGAccountsSerializer(account)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer=PGAccountsSerializer(account,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         account.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)



# The below is the implementation of views from scratch without using much of the django rest framework magic

# @csrf_exempt
# def pgaccounts_list(request):
#     """
#     List all accounts or create a new account
#     """
#     if request.method == 'GET':
#         pgaccounts=PGAccounts.objects.all()
#         serializer=PGAccountsSerializer(pgaccounts,many=True)
#         return JsonResponse(serializer.data, safe=False)
    
#     elif request.method =='POST':
#         data = JSONParser().parse(request)
#         serializer=PGAccountsSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# def pgaccounts_detail(request, pk):
#     """
#     Retrieve, Update or Delete an Account
#     """
#     try:
#         account=PGAccounts.objects.get(pk=pk)
#     except PGAccounts.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = PGAccountsSerializer(account)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data=JSONParser().parse(request)
#         serializer=PGAccountsSerializer(account,data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors,status=400)

#     elif request.method == 'DELETE':
#         account.delete()
#         return HttpResponse(status=204)


