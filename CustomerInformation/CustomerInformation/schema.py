from math import fabs
from pyexpat import model
from tabnanny import check
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

""""class MultipleEntryNode(DjangoObjectType):
    class Meta:
        model = MultipleEntries
        filter_fields = ['customer_contact', 'customer']
        interfaces = ( graphene.relay.Node, )"""

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
    #multiples = graphene.relay.Node.Field(MultipleEntryNode)
    #multiplesNode = DjangoFilterConnectionField(MultipleEntryNode)

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

class EditMultiple(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        date_created = graphene.types.DateTime(required = True)
        rider = graphene.Int(name="rider", required = True)
    
    multiple = graphene.Field(MultipleEntriesType)
    
    @classmethod
    def mutate(root, info, id, date_created, rider):
        multiple = MultipleEntries.objects.get(pk = id)
        
        if rider is not None:
            riders = Riders.objects.get(pk = rider)            
        multiple.Rider = riders
        multiple.date_created = date_created
        multiple.save()
        return EditMultiple(multiple = multiple)

        
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

class CreateRidersLog(relay.ClientIDMutation):
    
    class Input:
        id = graphene.ID()
        customer_name = graphene.String()
        customer_contact = graphene.String( required = True)
        rider = graphene.Int(name="rider", required = True)
        discount_amount = graphene.String()
        date_created = graphene.types.DateTime(required = True)
    
    riders_log = graphene.Field(EntryNode)    
    multiple_log = graphene.Field(MultipleEntriesType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):                
        print(input)         
        customer_contact = input.get('customer_contact')
        customer_name = input.get('customer_name')
        discount_amount = input.get('discount_amount')
        date_created = input.get('date_created')
        rider = input.get('rider')

        check_for_contact = Riders_Log.objects.filter(customer_contact = customer_contact).exists()
        #global riders_log
        if check_for_contact == False:                        
            riders_log = Riders_Log.objects.create(
                customer_name = customer_name,
                customer_contact = customer_contact,                    
                discount_amount = discount_amount, 
                date_created = date_created
            )
            
            if input.get('rider') is not None:
                rider_object = Riders.objects.get(pk = rider)
            riders_log.Rider = rider_object
            riders_log.save()
            return CreateRidersLog(  riders_log = riders_log) 
        if check_for_contact == True :            
            multiple_log = MultipleEntries.objects.create(                    
                customer_contact = customer_contact,
                discount_amount = discount_amount,
                date_created = date_created,
            )            

            if input.get('rider') is not None:
                rider_object2 = Riders.objects.get(pk = rider)
            customer = Riders_Log.objects.get(customer_contact = customer_contact)                
            multiple_log.customer = customer
            multiple_log.Rider = rider_object2
            multiple_log.save()
            
            get_the_riders_log = Riders_Log.objects.get(customer_contact = customer_contact)          
            get_the_riders_log.count.add(multiple_log)            

            return CreateRidersLog(multiple_log = multiple_log) 

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

        delete_log = Riders_Log.objects.get(pk = from_global_id(id)[1])        
        print("delete log:",delete_log)
        delete_log.delete()        

        return DeleteRidersLog( delete_log = delete_log )

class BulkDeleteLog(relay.ClientIDMutation):
    class Input:
        id = graphene.List(graphene.ID)

    bulk_delete_log = graphene.List(EntryNode)    

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):            
        id = input.get('id')        
        check_global = []

        #convert ids to int type
        for ids in id:            
            convert_ids = from_global_id(ids)[1]            
            check_global.append(convert_ids)        

        deleted_users = []
        for ids in Riders_Log.objects.filter(pk__in = check_global):
            ids.delete()    
            deleted_users.append(ids)    
 
        return BulkDeleteLog(bulk_delete_log = deleted_users)

class RelayMutation(graphene.AbstractType):
    edit_riders_log2 = EditRidersLog.Field()
    deleteRidersLog2 = DeleteRidersLog.Field()
    createRidersLog2 = CreateRidersLog.Field()
    bulk_delete_log = BulkDeleteLog.Field()

class Mutation(AuthMutation, RelayMutation, graphene.ObjectType):
    addRiders = AddRiders.Field()
    createUser = CreateUser.Field()    
    editRidersLog = EditRidersLog.Field()
    deleteRidersLog = DeleteRidersLog.Field()
    edit_multiple = EditMultiple.Field()

schema = graphene.Schema(query=Query, mutation = Mutation)