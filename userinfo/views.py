from django.shortcuts import render,redirect
from .models import User_address
from django.contrib import messages
from .models import User_address
# Create your views here.

def addAddress(request):
    current_user_id = request.user.id
    if request.method=='POST':
        full_name = request.POST['full_name']
        mobile_number = request.POST['mobile_number']
        pincode = request.POST['pin_code']
        streetAddress = request.POST['streetAddress']
        landmark = request.POST['landmark']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country'] 
        if current_user_id is not None:
            user_address = User_address.objects.create(fullName=full_name,mobileNumber=mobile_number,pincode=pincode,streetAddress=streetAddress,landmark=landmark,city=city,state=state,country=country,user_id=current_user_id)
            print("------------------address saved")
            return redirect('login_signup:addresses')
        else:
            messages.info(request,'Please Login first')
            return redirect('order:addAddress')
    else:
        return render(request,'addAddress.html')


def deleteAddress(request):
    if request.method=='POST':
        address_id = request.POST['address_id']
        print("=============address deleted========userinfo=======",address_id)
        deleteObject = User_address.objects.all().filter(id = address_id)
        deleteObject.delete()
        return redirect('login_signup:addresses')
    else:
        print("==================requet is get====================")


def test(request):
    if request.method=='POST':
        print("request is post=-===============================")
    else:
        print("request is get------------------------------------")