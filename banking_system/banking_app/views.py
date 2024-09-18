from django.shortcuts import render, redirect
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, UserLoginForm




def index( request ):
    return render( request, 'index.html' )



def register( request ):

    if ( request.method == 'POST' ):
        form = UserRegisterForm( request.POST )
        
        if ( form.is_valid() ):
            user = form.save()
            login( request, user )

            return redirect( 'index' )

    else:
        form = UserRegisterForm()
    
    return render( request, 'register.html', { 'form' : form } )



def user_login( request ):

    if ( request.method == 'POST' ):
        form = UserLoginForm( data=request.POST )

        if ( form.is_valid() ):
            username = form.cleaned_data[ 'username' ]
            password = form.cleaned_data[ 'password' ]
            user = authenticate( request, username=username, password=password )
            
            if ( user is not None ):
                login( request, user )
                return redirect( 'index' )
    
    else:
        form = UserLoginForm()
    
    return render( request, 'login.html', { 'form' : form } )




@login_required
def account_details( request ):
    account_details_dict = {}

    account = Account.objects.get( user=request.user )
    transactions = Transaction.objects.filter( account=account )

    account_details_dict['account'] = account
    account_details_dict['transactions'] = transactions

    return render( request, 'account_details.html', account_details_dict )



@login_required
def deposit( request ):

    if ( request.method == 'POST' ):
        amount = request.POST.get( 'amount' )
        account = Account.objects.get( user=request.user )
        account.balance += float( amount )
        account.save()

        # saving transaction into a log
        Transaction.objects.create( account=account, amount=amount, transaction_type='deposit' )
        
        return redirect( 'account_details' )

    return render( request, 'deposit.html' )


@login_required
def withdraw( request ):

    if ( request.method == 'POST' ):
        amount = request.POST.get( 'amount' )
        account = Account.objects.get( user=request.user )

        if ( account.balance > float( amount ) ):
            account.balance -= float( amount )
            account.save()
            Transaction.objects.create( account=account, amount=amount, transaction_type='withdrawal' )
        
        else:
            return render( request, 'withdraw.html', { 'error':'Insifficient funds' } )

    return render( request, 'withdraw.html' )