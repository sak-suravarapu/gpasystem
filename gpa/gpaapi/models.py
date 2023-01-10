from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PGAccounts(models.Model):
    account_number=models.DecimalField(unique=True,decimal_places=0,max_digits=16)
    current_balance=models.DecimalField(decimal_places=2,max_digits=10)
    #user_id=models.IntegerField()
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    #models.UniqueConstraint()
    def __str__(self) -> str:
        return str(self.account_number).zfill(16)

class PGTransactions(models.Model):
    date=models.DateTimeField('transaction date')
    transaction_type=models.TextField(max_length=6)
    note=models.TextField()
    amount=models.DecimalField(decimal_places=2,max_digits=10)
    account_id=models.ForeignKey(PGAccounts,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return '%s %s %s %s' %(self.account_id, self.transaction_type, self.note, str(self.amount))

class PGBalance(models.Model):
    date=models.DateField('balance_date')
    balance=models.DecimalField(decimal_places=2,max_digits=10)
    account_id=models.ForeignKey(PGAccounts,on_delete=models.CASCADE)
    class Meta:
        constraints =[
            models.UniqueConstraint(
                fields=['account_id','date'],
                name='balancedateconstraint'
            )
        ]
    