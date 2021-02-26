from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from . import utils
from .models import Customer, Wallet
from shippingToken.settings import ADDR_CONTRACT
import math

@login_required(login_url='/login')
def homePage(request):
    if request.method == 'POST':
        pass
    else:
        thisUser= Customer.objects.filter(user=request.user).values()[0]
        
        thisWallet = Wallet.objects.filter(owner = thisUser['id']).values()
        detWall = thisWallet[0]
        #print(detWall['balance'])
        
        return render(request, 'main/home_page.html', {'infoWallet': detWall, 'userInfo':thisUser})


@login_required(login_url='/login')
def adminPage(request):
    if request.method == 'POST':
        pass
    else:
        try:
            #this is procecced if the contract is just runned
            infoWallet = Wallet.objects.all().values()
            print(infoWallet)
            admin = utils.getAdminInfo()
            print("ora siamo qui")
            return render(request, 'main/admin_page.html', {'infoAd':admin, 'list':infoWallet})
        except:
            
            admin = utils.getAdminInfo()
            return render(request, 'main/admin_page.html', {'infoAd':admin})


#reward the user for every produced watt
def checkReward(request):
    #retrieve the watts produced in an hour (0,04)
    dataGet = request.GET

    #retrieve the user
    thisUser = Customer.objects.filter(user=request.user).values()[0]
    use = Customer.objects.get(user=request.user)
    wattRet = thisUser['prodWatt']
    #print('counter', use.counter)
    #print('watt prodotti', use.prodWatt)

    if int(wattRet) >= 4:
        thisWallet = Wallet.objects.filter(owner = thisUser['id']).values()
        wall = Wallet.objects.get(owner=thisUser['id'])
        detWall = thisWallet[0]
        try:
            upB = utils.receiveToken(detWall['address'])
        except:
            wall.state = False
            wall.save()
            return
        
        addr = detWall['address']

        #retrieve the original queryset to use inside data
        use.prodWatt = 0
        use.counter += float(dataGet['neWatt'])
        use.earnedToken += float(upB)
        use.save()
        
        wall.balance += float(upB)
        wall.save()
        
        this = Customer.objects.filter(user=request.user).values()[0]
        data = {'balance': upB, 'address':addr, 'prodWatt': this['prodWatt']}
        
        return JsonResponse(data)
    else:
        #retrieve info of wallet (address)
        thisWallet = Wallet.objects.filter(owner = thisUser['id']).values()
        detWall = thisWallet[0]

	#update field into database
        use.counter+=float(dataGet['neWatt'])
        use.prodWatt+=float(dataGet['neWatt'])
        use.save()
        
        balan = utils.getBalance(detWall['address'])
        
        this = Customer.objects.filter(user=request.user).values()[0]
        data = {'balance': balan, 'address':detWall['address'], 'prodWatt': this['prodWatt']}
        return JsonResponse(data)


def checkWaitWall(request):
    retWall = Wallet.objects.filter(state=False).values()
    if not retWall.exists():
        #print(retWall)
        data = {'check': False}
        return JsonResponse(data)
    else:
        info = {}
        for item in retWall:
            utils.receiveToken(item['address'])
        
        data = {"check": True}
        return JsonResponse(data)

    



def loginC(request):
    if request.method == 'POST':
        form = request.POST
        if form:
            if 'email' not in form: #I check the type of form
                username = form['uname']
                password = form['psw']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('/admin-page')
                    else:
                        return redirect('/')
                else:
                    print("errore")
                    return render(request, "main/login.html")
            
            else:
                username = form['uname']
                email = form['email']
                password = form['psw']
                password2 = form['psw2']

                if password == password2: #CHECK that both passwords match
                    passToCrypt = password
                    user = User.objects.create_user(username=username, email=email, password=password)
                    newUser = Customer.objects.create(user=user)

                    myWallet = utils.createNewWallet(passToCrypt)
                    newWallet = Wallet.objects.create(owner=newUser, balance=myWallet['balance'], privateKey=myWallet['cryptKey'], address=myWallet['address'], state=True)
                    
                    newUser.save()
                    newWallet.save()
                    return render(request, 'main/login.html')
                else:
                    pass
                    #errore
    else:
        return render(request, 'main/login.html', {})


def logOut(request):
    logout(request)
    return redirect('/login')


