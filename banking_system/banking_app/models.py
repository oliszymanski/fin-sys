from django.db import models
from django.contrib.auth.models import User

class Account( models.Model ):
    user = models.OneToOneField( User, on_delete=models.CASCADE )
    balance = models.DecimalField( max_digits=10, decimal_places=2, default=0.00 )

    def __str__( self ):
        return f"{ self.user.username }'s Account"

class Transaction( models.Model ):
    account = models.ForeignKey( Account, on_delete=models.CASCADE )
    amount = models.DecimalField( max_digits=10, decimal_places=2 )
    transaction_type = models.CharField( max_length=10 )
    created_at = models.DateTimeField( auto_now_add=True )

    def __str__( self ):
        return f"{ self.transaction_type } of { self.amount } on { self.created_at }"