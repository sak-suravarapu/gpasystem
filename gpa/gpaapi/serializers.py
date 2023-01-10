from rest_framework import serializers
from gpaapi.models import PGAccounts
from gpaapi.models import PGTransactions
from gpaapi.models import PGBalance
# The below import for user authentication
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class PGAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model=PGAccounts
        fields=['id','account_number','current_balance','user_id']


class PGTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=PGTransactions
        fields=['id','date','transaction_type','note','amount','account_id']

class PGBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=PGBalance
        fields=['id','account_id','date','balance']
        #lookup_field=''

# The below classes are added for user authentication
User = get_user_model()
class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=('password', )

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username']=user.username
        token['email'] = user.email
        return token

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model=User
        fields = ('username','password','password2')
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password":"Password fields didnt match"}
            )
        return attrs
    
    def create(self,validated_data):
        user = User.objects.create(
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


    


# End of authentication related classes

# The below is the implementation without using ModelSerializer

    # class PGAccountsSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    # account_number = serializers.DecimalField(max_digits=16,decimal_places=0)
    # current_balance = serializers.DecimalField(max_digits=10,decimal_places=2)
    # user_id = serializers.CharField()

    # def create(self,validated_data):
    #     """
    #     #Create and return a new 'Accounts' instance, given the validated data.
    #     """
    #     return PGAccounts.objects.create(**validated_data)

    # def update(self,instance, validated_data):
    #     """
    #     #Update and return an existing 'Accounts' instance, given the validated data
    #     """
    #     instance.account_number=validated_data.get('account_number', instance.account_number)
    #     instance.current_balance=validated_data.get('current_balance', instance.current_balance)
    #     instance.user_id=validated_data.get('user_id', instance.user_id)
    #     instance.save()
    #     return instance


    
 