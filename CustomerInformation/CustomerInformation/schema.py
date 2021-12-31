import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from CustomerEntry.models import Riders, Riders_Log, MultipleEntries

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

    def resolve_ridersList(root, info):
        return Riders.objects.all()

    def resolve_customerEntries(root, info):
        return Riders_Log.objects.all()
        
    def resolve_relatedEntries(root, info):
        return MultipleEntries.objects.select_related("customer").all()


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
                Riders_Log.objects.create(
                    customer_name = customer_name,
                    customer_contact = customer_contact,
                    Rider = rider, 
                    discount_amount = discount_amount, 
                    date_created = date_created
                )
            else:
                MultipleEntries.objects.create(
                    customer = customer_name,
                    customer_contact = customer_contact,
                    Rider = rider,
                    discount_amount = discount_amount,
                    date_created = date_created,
                )

        return CreateRidersLog(riders_log = CreateEntries())
        
class Mutation(graphene.ObjectType):
    addRiders = AddRiders.Field()
    createUser = CreateUser.Field()
    createRidersLog = CreateRidersLog.Field()

schema = graphene.Schema(query=Query, mutation = Mutation)