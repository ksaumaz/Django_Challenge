from .models import User, IOU
from .serializers import IOUSerializer, UserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view


@swagger_auto_schema(method="post", operation_description="Return selected users with their IOU details", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'users': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of user\'s names', items=openapi.Items(type=openapi.TYPE_STRING)),
        }))
		
@swagger_auto_schema(method="get", operation_description="Return all users with their IOU details")
@api_view(['GET', 'POST'])
def user_list(request):
	if request.method == 'GET':
		users = User.objects.all().order_by('name')
		serializer = UserSerializer(users, many=True)
		for user in serializer.data:
			user.update(getUser(user["name"]))
		return JsonResponse({"users":serializer.data}, safe=False)
	elif request.method == 'POST':
		try:
			data=request.data.get('users')

			if data is None:
				raise Exception("No users specified")

			data = [name.title() for name in data]

			users = User.objects.filter(name__in=data)
			serializer = UserSerializer(users, many=True)
			for user in serializer.data:
				user.update(getUser(user["name"]))
			return JsonResponse({"users":serializer.data}, safe=False)
		except Exception as e:
			print("Exception: " + str(e))
			return JsonResponse({"error": "Invalid data format should be { 'users' :['name', 'name'] } "}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="post", operation_description="Create user", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user': openapi.Schema(type=openapi.TYPE_STRING, description='User\'s name'),
        }))
@api_view(['POST'])
def create_user(request):
	try:
		name = request.data.get('user')
		#Check if user is present
		if name is None:
			return JsonResponse({"error": "Invalid data, format should be { user: 'name'}"}, status=status.HTTP_400_BAD_REQUEST)
		#Name to title case
		name = name.title()
		data = {"name": name}
		serializer = UserSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(getUser(name), status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		print("Exception: " + str(e))
		return JsonResponse({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="post", operation_description="Create IOU", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'lender': openapi.Schema(type=openapi.TYPE_STRING, description='Lender\'s name'),
			'borrower': openapi.Schema(type=openapi.TYPE_STRING, description='Borrower\'s name'),
			'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount'),
        }))
@api_view(['POST'])
def create_IOU(request):
	try:
		lender = request.data.get('lender')
		borrower = request.data.get('borrower')
		amount = request.data.get('amount')
		#Check if all fields are present
		if lender is None or borrower is None or amount is None:
			return JsonResponse({"error": "Invalid data, format should be { lender: 'name', borrower: 'name', amount: 'amount'}"}, status=status.HTTP_400_BAD_REQUEST)

		#Title case the names
		lender = lender.title()
		borrower = borrower.title()

		#Check if lender and borrower are the same
		if lender == borrower:
			return JsonResponse({"error": "Invalid data, lender and borrower cannot be the same"}, status=status.HTTP_400_BAD_REQUEST)

		#Check if lender and borrower exist
		try:
			lender = User.objects.get(name=lender)
			borrower = User.objects.get(name=borrower)
		except Exception as e:
			print("Exception: " + str(e))
			return JsonResponse({"error": "Invalid data, lender and borrower must exist"}, status=status.HTTP_400_BAD_REQUEST)

		data = {"lender": lender, "borrower": borrower, "amount": amount}
		serializer = IOUSerializer(data=data)
		if serializer.is_valid():
			serializer.save()

			users = User.objects.filter(name__in=[lender.name, borrower.name]).order_by('name')
			serializer = UserSerializer(users, many=True)
			for user in serializer.data:
				user.update(getUser(user["name"]))
			return JsonResponse({"users":serializer.data}, safe=False, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		print("Exception: " + str(e))
		return JsonResponse({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

def getUser(name):
	try:
		#Name to title case
		name = name.title()
		user = User.objects.get(name=name)
		lender = IOU.objects.filter(lender=user)
		borrower = IOU.objects.filter(borrower=user)
		#Calculate the total amount owed to the user
		total = 0
		owed_by = {}

		#group IOUs by lender
		for iou in lender:
			total += iou.amount
			if iou.borrower.name in owed_by:
				owed_by[iou.borrower.name] += iou.amount
			else:
				owed_by[iou.borrower.name] = iou.amount

		#group IOUs by borrower
		owes = {}
		for iou in borrower:
			total -= iou.amount
			if iou.lender.name in owes:
				owes[iou.lender.name] += iou.amount
			else:
				owes[iou.lender.name] = iou.amount

		return {"name":user.name, "owes":owes, "owed_by":owed_by, "balance":total}
	except Exception as e:
		print("Exception: " + str(e))
		return None