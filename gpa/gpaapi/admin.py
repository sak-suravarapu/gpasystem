from django.contrib import admin
from .models import PGAccounts
from .models import PGTransactions
from .models import PGBalance
# Register your models here.
admin.site.register(PGAccounts)
admin.site.register(PGTransactions)
admin.site.register(PGBalance)

