from tokenize import String
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from CustomerEntry.models import Riders, Riders_Log, MultipleEntries
from graphql_auth import mutations
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from graphql_relay import from_global_id

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
#relay
class EntryNode(DjangoObjectType):
    class Meta:
        model = Riders_Log
        filter_fields = ['customer_name', 'customer_contact']
        interfaces = (graphene.relay.Node, )

#Query
class Query(graphene.ObjectType):
    ridersList = graphene.List(RidersType)
    paginatedEntries =graphene.List(Riders_LogType, limit = graphene.Int(), offset = graphene.Int(), cursor = graphene.String())
    customerEntries = graphene.List(Riders_LogType)
    relatedEnteries = graphene.List(MultipleEntriesType)
    entriesTodaySingle = graphene.List(Riders_LogType)
    entriesTodayMultiple = graphene.List(MultipleEntriesType)
    entry = graphene.relay.Node.Field(EntryNode)
    entries = DjangoFilterConnectionField(EntryNode)

    def resolve_ridersList(root, info):
        return Riders.objects.all()   

    def resolve_customerEntries(root, info ):              
        return Riders_Log.objects.all()        
        
    def resolve_relatedEnteries(root, info):
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
        limit_name = graphene.String()
        last_name = graphene.String()
        username = graphene.String()
        email = graphene.String()
        password1 = graphene.String()
        password2 = graphene.String()
    
    user = graphene.Field(UserType)

    @classmethod 
    def mutate(root, info, id, 
        limit_name, last_name, username, email,
        password1, password2):
        user = User.objects.create(
            limit_name = limit_name,
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
                multiple_log.customer = customer
                multiple_log.Rider = rider_object2
                multiple_log.save()
                
                get_the_riders_log = Riders_Log.objects.get(customer_contact = customer_contact)          
                get_the_riders_log.count.add(multiple_log)

        return CreateRidersLog(riders_log = CreateEntries())

class EditRidersLog(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()
        customerName = graphene.String(required = True)
        customerContact = graphene.String()
        #rider = graphene.String( required = True)
        rider = graphene.Int(name='rider')
        dateCreated = graphene.types.DateTime()    
        
    edit_log = graphene.Field(EntryNode)

    @classmethod 
    def mutate_and_get_payload(cls, root, info, **input):            
       
        id = input.get('id')        
        rider = input.get('rider')
        edit_log = Riders_Log.objects.get(pk = from_global_id(id)[1])
        edit_log.customer_name = input.get('customerName')
        edit_log.customer_contact = input.get('customerContact')
        edit_log.date_created = input.get('dateCreated' )
                
        if rider is not None: 
            rider_object = Riders.objects.get(pk = rider)            
        edit_log.Rider = rider_object     

        edit_log.save()

        return EditRidersLog( edit_log = edit_log )

class DeleteRidersLog(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    delete_log = graphene.Field(EntryNode)    

    @classmethod  
    def mutate_and_get_payload(cls, root, info, **input):  
        id = input.get('id')

        delete_log = Riders_Log.objects.get(pk= from_global_id(id)[1])        
        delete_log.delete()        

        #return DeleteRidersLog( delete_log = delete_log )
class RelayMutation(graphene.AbstractType):
    edit_riders_log2 = EditRidersLog.Field()

class Mutation(AuthMutation, RelayMutation, graphene.ObjectType):
    addRiders = AddRiders.Field()
    createUser = CreateUser.Field()
    createRidersLog = CreateRidersLog.Field()
    editRidersLog = EditRidersLog.Field()
    deleteRidersLog = DeleteRidersLog.Field()


schema = graphene.Schema(query=Query, mutation = Mutation)