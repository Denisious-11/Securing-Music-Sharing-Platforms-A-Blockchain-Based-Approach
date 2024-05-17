from django.shortcuts import render
from .models import *
import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db.models import Count
import re
import os
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
from blockchain import *
from datetime import date
from datetime import datetime


# Create your views here.

@never_cache
def show_index(request):
    return render(request, "index.html", {})


@never_cache
def logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    return render(request,'index.html')

def register(request):
	username=request.POST.get("username")
	password=request.POST.get("password")
	user_type=request.POST.get("u_type")
	mobile=request.POST.get("mobile")
	p_address=request.POST.get("p_address")

	print(username,password,user_type,mobile,p_address)

	if not verify_adr(p_address):
		return HttpResponse("<script>alert('Public Key does not belong to blockchain');window.location.href='/show_index/';</script>")
	else:
		if user_type=="Select":
			return HttpResponse("<script>alert('Please Select UserType');window.location.href='/show_index/'</script>")

		else:
			obj10=Requests.objects.filter(mobile=mobile,username=username,password=password,p_address=p_address,user_type=user_type)
			co=obj10.count()
			if co==1:
				return HttpResponse("<script>alert('Request is in Pending list');window.location.href='/show_index/'</script>")

			else:
				obj1=Requests(mobile=mobile,username=username,password=password,p_address=p_address,user_type=user_type)
				obj1.save()
				return HttpResponse("<script>alert('Request sent, Wait For Approval');window.location.href='/show_index/'</script>")




def check_login(request):
	username = request.POST.get("username")
	password = request.POST.get("password")

	print(username)
	print(password)

	if username == 'admin' and password == 'admin':
		request.session["uid"] = "admin"
		return HttpResponse("<script>alert('Admin Login Successful');window.location.href='/show_home_admin/'</script>")
	
	# if username=="agent" and password=="agent":
	# 	request.session["uid"] = "agent"
	# 	return HttpResponse("<script>alert('Agent Login Successful');window.location.href='/show_home_agent/'</script>")
	
	else:
		obj1=Artists.objects.filter(username=username,password=password)
		c1=obj1.count()
		if c1==1:
			ob=Artists.objects.get(username=username,password=password)
			request.session["uid"] = ob.u_id
			request.session["username"]=ob.username
			return HttpResponse("<script>alert('Artist Login Successful');window.location.href='/show_home_artist/'</script>")

		else:
			obj2=Users.objects.filter(username=username,password=password)
			c2=obj2.count()
			if c2==1:
				ob9=Users.objects.get(username=username,password=password)
				request.session["uid"] = ob9.u_id
				request.session["username"]=ob9.username
				return HttpResponse("<script>alert('User Login Successful');window.location.href='/show_home_user/'</script>")
			else:
				return HttpResponse("<script>alert('Invalid');window.location.href='/show_index/'</script>")


@never_cache
###############ADMIN START
def show_home_admin(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		return render(request,'home_admin.html') 
	else:
		return render(request,'index.html')

@never_cache
def show_request_admin(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		req_list=Requests.objects.all()

		return render(request,'view_request_admin.html',{'req': req_list}) 
	else:
		return render(request,'index.html')


def approve(request):
	r_id=request.POST.get('r_id')
	username=request.POST.get('username')
	password=request.POST.get('password')
	mobile=request.POST.get('mobile')
	user_type=request.POST.get('user_type')
	p_address=request.POST.get('p_address')

	if user_type=="Artist":
		obj1=Artists(mobile=mobile,username=username,password=password,p_address=p_address)
		obj1.save()
		obj2=Artists.objects.get(mobile=mobile,username=username,password=password,p_address=p_address)
		user_id=obj2.u_id
		print("User id : ",user_id)
		#Adding to blockchain
		add_artist1(user_id,username,password,mobile,p_address)

		obj3=Requests.objects.get(r_id=int(r_id))
		obj3.delete()
		return HttpResponse("<script>alert('Approved Successfully');window.location.href='/show_request_admin/'</script>")
	
	else:
		obj1=Users(mobile=mobile,username=username,password=password,p_address=p_address)
		obj1.save()
		obj2=Users.objects.get(mobile=mobile,username=username,password=password,p_address=p_address)
		user_id=obj2.u_id
		print("User id : ",user_id)
		#Adding to blockchain
		add_user1(user_id,username,password,mobile,p_address)

		obj3=Requests.objects.get(r_id=int(r_id))
		obj3.delete()
		return HttpResponse("<script>alert('Approved Successfully');window.location.href='/show_request_admin/'</script>")

def reject(request):
	r_id=request.POST.get('r_id')
	obj1=Requests.objects.get(r_id=int(r_id))
	obj1.delete()
	return HttpResponse("<script>alert('Rejected');window.location.href='/show_request_admin/'</script>")


@never_cache
def display_view_artists(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		obj=get_artists()
		# obj=Farmers.objects.all()
		return render(request,'view_artists_admin.html',{'obj':obj}) 
	else:
		return render(request,'index.html')

@never_cache
def display_view_users(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		obj=get_users()
		# obj=Customers.objects.all()
		return render(request,'view_users_admin.html',{'obj':obj}) 
	else:
		return render(request,'index.html')



@never_cache
def show_home_artist(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		return render(request,'home_artist.html') 
	else:
		return render(request,'index.html')

@never_cache
def show_home_user(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		return render(request,'home_user.html') 
	else:
		return render(request,'index.html')


from web3 import Web3
import web3
from ipfs import upload as up1

@never_cache
def upload_music_artist(request):
	if 'uid' in request.session:
		return render(request,'artist_upload_music.html') 
	else:
		return render(request,'index.html')

@never_cache
def view_my_list_artist(request):
	if 'uid' in request.session:
		#print(request.session['uid'])
		username=request.session["username"]
		blocks=Musics.objects.filter(author=username)
		return render(request,'my_list_artist.html',{'mdetails':blocks}) 
	else:
		return render(request,'index.html')

def upload_music(request):
	private_key=request.POST.get('private_key')

	file1 = request.FILES["f_upload"]

	file_name=file1.name
	print("file_name : ",file_name)

	username=request.session["username"]

	obj1=Artists.objects.get(username=username)
	public_key=obj1.p_address

	verify_result=verify_key(public_key,private_key,1)
	if(verify_result=="No"):
		return HttpResponse("<script>alert('Key Error');window.location.href='/upload_music_artist/'</script>")
	else:
		fs = FileSystemStorage("cm_app/static/rough_audio/")
		fs.save(file_name, file1)

		#file storing to IPFS
		hash_value=up1("cm_app/static/rough_audio/"+str(file_name))
		print("Hash value :::: > ",hash_value)

		if Musics.objects.filter(hash_value=hash_value).exists():
			return HttpResponse("<script>alert('Sorry! Copyright Detected');window.location.href='/upload_music_artist/'</script>")

		else:

			fs = FileSystemStorage("cm_app/static/audio/")
			fs.save(file_name, file1)

			obj1=Files(title=file_name,author=username)
			obj1.save()


			now = datetime.now()
			time = now.strftime("%H:%M:%S")
			print("Current Time =", time)

			today = date.today()
			current_date = today.strftime("%d/%m/%Y")
			print("date =",current_date)

			obj3=Files.objects.get(title=file_name,author=username)
			my_m_id=obj3.m_id
			print("m_id : ",my_m_id)

			obj4=Musics(m_id=my_m_id,title=file_name,author=username,date=current_date,time=time,hash_value=hash_value)
			obj4.save()

			add_music1(my_m_id,file_name,username,current_date,time,hash_value)

			# get_musics()
			return HttpResponse("<script>alert('Uploaded Successfully');window.location.href='/view_my_list_artist/'</script>")


@never_cache
def artist_view_transactions(request):
	if 'uid' in request.session:
		username=request.session["username"]
		blocks=Transactionss.objects.filter(receiver_name=username)
		return render(request,'show_transactions_artist.html',{'t_details':blocks}) 
	else:
		return render(request,'index.html')

@never_cache
def display_music_user(request):
	if 'uid' in request.session:
		blocks11=Musics.objects.all()
		return render(request,'music_list_user.html',{'sdetails':blocks11}) 
	else:
		return render(request,'index.html')


def check_download(request):
	username=request.session["username"]
	m_id=request.POST.get("m_id")
	title=request.POST.get("title")
	hash_value=request.POST.get("hash_value")
	author=request.POST.get("author")

	print("my_title : ",title)
	print("id : ",m_id)
	print("my_hash_value : ",hash_value)

	obj1=Transactionss.objects.filter(sender_name=username,title=title)
	c=obj1.count()
	if c==1:
		res=download(hash_value,title)
		return res

		#return HttpResponse("<script>alert('Downloaded Successfully');window.location.href='/display_music_user/'</script>")

		#call download function
	else:
		return render(request,"payment.html",{"title":title,"hash_value":hash_value,"author":author,"username":username})

def download(hash_value,title):
	try:
		print("Title : ", title)
		file1_path = 'cm_app/static/audio/'+title
		print(os.path.exists(file1_path))
		print(file1_path)

		if os.path.exists(file1_path):
		    with open(file1_path, 'rb') as fh:
		        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
		        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file1_path)
		        return response
		raise HttpResponse("<script>alert('File does not exists, You may want to check IPFS using hash');window.location.href='/display_music_user/'</script>")
	except Exception as ex:
	    print("Exception: ",ex)
	    print("--")
	    
	    return HttpResponse("<script>alert('File does not exists, You may want to check IPFS using hash');window.location.href='/display_music_user/'</script>")



def do_payment(request):
	m_id=request.GET.get("m_id")
	title=request.GET.get("title")
	price=request.GET.get("price")
	private_key=request.GET.get("p_key")
	author=request.GET.get("author")
	username=request.GET.get("username")
	hash_value=request.GET.get("hash_value")

	obj11=Artists.objects.get(username=author)
	receiver_public_key=obj11.p_address
	print(receiver_public_key)

	obj12=Users.objects.get(username=username)
	sender_public_key=obj12.p_address

	print("^"*20)

	print(sender_public_key)
	print(private_key)
	verify_result=verify_key(sender_public_key,private_key,1)
	if(verify_result=="No"):
		return HttpResponse("Key Error")
	else:

		t_hash=transfer(sender_public_key,receiver_public_key,private_key,price,username,author,title)

		obj21=Transactionss(title=title,sender_name=username,receiver_name=author,sender_address=sender_public_key,receiver_address=receiver_public_key,amount=price,transaction_hash=t_hash)
		obj21.save()
		obj22=Transactionss.objects.get(title=title,sender_name=username,receiver_name=author,sender_address=sender_public_key,receiver_address=receiver_public_key,amount=price,transaction_hash=t_hash)
		get_id=obj22.t_id
		print("Get_id : ",get_id)

		add_transaction_to_table(get_id,title,username,author,sender_public_key,receiver_public_key,price,t_hash)
		get_transactions()

		download(hash_value,title)
		return HttpResponse("Payment Successful")


@never_cache
def user_view_transactions(request):
	if 'uid' in request.session:
		username=request.session["username"]
		blocks=Transactionss.objects.filter(sender_name=username)
		return render(request,'show_transactions_user.html',{'t_details':blocks}) 
	else:
		return render(request,'index.html')