import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from CustomerEntry.models import Riders, Riders_Log, MultipleEntries
from graphql_auth import mutations

from datetime import datetime

today = datetime.now().date()  

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        
class RidersType(DjangoObjectType):
    class Meta:
        model = Riders
        
class Riders_LogType(DjangoObjectType):
    class Meta:
        model = Riders_Log

class MultipleEntriesType(DjangoObjectType):
    class Meta:
        model = MultipleEntries

#Query
class Query(graphene.ObjectType):
    ridersList = graphene.List(RidersType)
    customerEntries = graphene.List(Riders_LogType)
    relatedEnteries = graphene.List(MultipleEntriesType)
    entriesTodaySingle = graphene.List(Riders_LogType)
    entriesTodayMultiple = graphene.List(MultipleEntriesType)

    def resolve_ridersList(root, info):
        return Riders.objects.all()

    def resolve_customerEntries(root, info):
        return Riders_Log.objects.all()
        
    def resolve_relatedEntries(root, info):
        return MultipleEntries.objects.select_related("customer").all()

    def resolve_entriesTodaySingle(root, info):
        return Riders_Log.objects.filter( date_created__date = today)

    def resolve_entriesTodayMultiple(root, info):
        return MultipleEntries.objects.filter(date_created__date = today)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()

###Mutation
class AddRiders(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        rider_name = graphene.String()
        rider_Number = graphene.String()

    riders = graphene.Field(RidersType)

    @classmethod
    def mutate(root, info, id, rider_name, rider_Number):
        riders = Riders.objects.create(
            rider_name = rider_name,
            rider_Number = rider_Number,
        )

        return AddRiders(riders = riders)

class CreateUser(graphene.Mutation):
    class Arguements:
        id = graphene.ID()
        first_name = graphene.String()
        last_name = graphene.String()
        username = graphene.String()
        email = graphene.String()
        password1 = graphene.String()
        password2 = graphene.String()
    
    user = graphene.Field(UserType)

    @classmethod
    def mutate(root, info, id, 
        first_name, last_name, username, email,
        password1, password2):
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            password1 = password1,
            password2 = password2,
        )
        return CreateUser(user = user)

class CreateRidersLog(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        customer_name = graphene.String()
        customer_contact = graphene.String()
        rider = graphene.Int(name="rider")
        discount_amount = graphene.Int()
        date_created = graphene.types.DateTime()
    
    riders_log = graphene.Field(Riders_LogType)

    @classmethod
    def mutate(root, info, id, customer_name, 
        customer_contact, rider, discount_amount,
        date_created):

        def CreateEntries():
            check_for_contact = Riders_Log.objects.filter(customer_contact = customer_contact).exists()
            if check_for_contact == False:
                log = Riders_Log.objects.create(
                    customer_name = customer_name,
                    customer_contact = customer_contact,                    
                    discount_amount = discount_amount, 
                    date_created = date_created
                )
                
                if rider is not None:
                    rider_object = Riders.objects.get(pk = rider)
                log.Rider = rider_object
                log.save()

            else:
                multiple_log = MultipleEntries.objects.create(                    
                    customer_contact = customer_contact,                    
                    discount_amount = discount_amount,
                    date_created = date_created,
                )

                if rider is not None:
                    rider_object2 = Riders.objects.get(pk = rider)
                customer = Riders_Log.objects.get(customer_contact = customer_contact)
                print(customer)
                multiple_log.customer = customer
                multiple_log.Rider = rider_object2
                multiple_log.save()

        return CreateRidersLog(riders_log = CreateEntries())
        
class Mutation(AuthMutation, graphene.ObjectType):
    addRiders = AddRiders.Field()
    createUser = CreateUser.Field()
    createRidersLog = CreateRidersLog.Field()

schema = graphene.Schema(query=Query, mutation = Mutation)