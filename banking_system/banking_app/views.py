from django.shortcuts import render, redirect
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required

def index( request ):
    return render( request, 'index.html' )



@login_required
def account_details( request ):
    account_details_dict = {}

    account = Account.objects.get( user=request.user )
    transactions = Transaction.objects.filter( account=account )

    account_details_dict['account'] = account
    account_details_dict['transactions'] = transactions

    return render( request, 'banking_app/account_details.html', account_details_dict )



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

    return render( request, 'banking_app/deposit.html' )


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
            return render( request, 'banking_app/withdraw.html', { 'error':'Insifficient funds' } )

    return render( request, 'banking_app/withdraw.html' )