from typing import Iterable, Optional, Union
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from TA_Scheduler.models import Account

# Note to teammate: 
# This is a utility class to access the Account database.
# Use the methods below to get accounts:

# createAccount(username, password, authority) --> returns id in database or error
# getAccountByID(id)
# getAllAccounts()
# getInstructors()
class AccountUtil: 

    @staticmethod
    def createAccount(username: str, password: str, authority: int =0) -> Union[int, TypeError]:
        if username == '' or password == '':
            raise TypeError('Username, password, and authority cannot be empty.')
        
        user = User.objects.create(username=username, password=password)
        account = Account.objects.create(user=user, authority=authority)
        return account.id

    @staticmethod
    def getAccountByID(id: int) -> Optional[Account]:
        try:
            account = Account.objects.get(id=id)
            return account
        except Account.DoesNotExist:
            return None

    @staticmethod
    def getAllAccounts() -> Optional[Iterable[Account]]:
        set: QuerySet = Account.objects.all()
        return set if set.exists() else None

    @staticmethod
    def getInstructors() -> Optional[Iterable[Account]]:
        set: QuerySet = Account.objects.filter(authority=1)
        return set if set.exists() else None