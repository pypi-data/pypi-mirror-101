from django.views.generic import View,CreateView,ListView,DetailView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse,reverse_lazy
from django.db.models import Q, F, Func
from django.db.models import Count, Subquery
from django.db.models.expressions import RawSQL
from django.db.models.query import QuerySet
from django.db.models.functions import Trim
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from .models import ActivityReason, Activity, ActivityHistory, Actor, ActorHistory, OldDevice
from .forms import  ActorForm, ActorFilterForm
from .filters import ActorFilter
from .tables import ActorTable

from dcim.models import Device, DeviceRole

from netbox.views import generic


#from extras.models import ChangeLoggedModel
#from rq import Worker #verificar se a para usar
#logger = logging.getLogger("rq.worker") #verificar se da para usar

'''
Version 2 : PlugConectividadeapp
'''

#view for input information on the device for get,
#input method post activity, its send to view ActivityCreateView
class ListConectividadeView(PermissionRequiredMixin,View):
    permission_required = 'conectividadeapp.view_activity'
    """
    List all reg in the database.
    """

    #tratar

    def get(self, request):

        rg = Activity.objects.all().order_by('-id')[:5]
        ls = Device.objects.order_by('-id')[:10]
        dr = DeviceRole.objects.all()

        quantity = len(ls)#verifica se tem device instalado

        if quantity == 0 : #se não tem manda false
            quant=False
        else:
            quant=True


        context = {
            'registro': rg,
            'devicerole': dr,
            'ls': ls,
            'quant':quant,
        }

        return render(request, 'conectividadeapp/listagem.html', context)

    def post(self, request):


        rg = Activity.objects.all().order_by('-id')[:5]
        dv = Device.objects.all()
        ls = Device.objects.order_by('-id')[:30]
        dr = DeviceRole.objects.all()
        actors= Actor.objects.all()

        quantity = len(ls)#verifica se tem device instalado

        if quantity == 0 : #se não tem device cadastrado nada false
            quant=False
        else:
            quant=True

        #analisar se é a melhor maneira
        if request.POST['deviceid'] :
            deviceid  = request.POST['deviceid']

        else:
            return redirect('plugins:conectividadeapp:list')


        if request.POST['op'] :

            op = request.POST['op']


            if op == "1" :

                activity_reason = ActivityReason.objects.filter(type="INSTALL")

            else :
                activity_reason = ActivityReason.objects.filter(type="REMOVE")

        else:
            #print("erro op")
            return redirect('plugins:conectividadeapp:list')


        #testes e revisar!
        # try get object for post
        try:
            device_obj =get_object_or_404(Device.objects.filter(id=deviceid)) # cria instancia do device
        #erro
        except MultiValueDictKeyError :

            return redirect('plugins:conectividadeapp:list')

        else:

            if deviceid :
                device_obj = Device.objects.get(id=deviceid) # cria instancia do device

                context = {
                        'registro': rg,
                        'devicerole': dr,
                        'ls': ls,
                        'op': op,
                        'deviceid':deviceid,
                        'device_obj':device_obj,
                        'actors':actors,
                        'quant':quant,
                        'activity_reason':activity_reason,


                    }
                return render(request, 'conectividadeapp/listagem.html', context)
            else:

                return redirect('plugins:conectividadeapp:list')



        # Context dictionary for rendering
        context = {
                    'registro': rg,
                    'devicerole': dr,
                    'ls': ls,
                    'op': op,
                    'actors': actors,
                    'quant': quant,
                    'activity_reason': activity_reason,
                }

        return render(request, 'conectividadeapp/listagem.html', context)

#view to save activity and olddevice.
# Save  automaticy olddevice made in activity.
# its dependency to save activity.
class ActivityCreateView(PermissionRequiredMixin,View):
    permission_required = 'conectividadeapp.add_activity'
    def get(self, request):


        return render(request, 'conectividadeapp/activity_op.html')


    def post(self, request):

        data = {}

        op = request.POST['op']

        # opção de remoção ou instalação para um determinado device
        #removal or installation option for a given device
        if op=="1" or op == "0":


            data['registro'] = Activity.objects.all().order_by('-id')[:5]

            deviceobj=request.POST['device_obj_id']
            actorlist=request.POST.getlist('actorss')
            reasonobj=request.POST['reason']
            #fks:
            dev_ob = Device.objects.get(id=deviceobj)
            res_ob = ActivityReason.objects.get(id=reasonobj)
            #onetoone
            gravadevice = OldDevice.objects.create(
                    name = request.POST['device_name'],
                    ipv4 = request.POST['ip'],
                    ipv6 = request.POST['ipv6'],
                    site = request.POST['site'],
                    rack = request.POST['rack']
                    )
            res_old =OldDevice.objects.get(id=gravadevice.pk)

            activity_op = Activity.objects.create(device= dev_ob,olddevice=res_old,reason=res_ob,when=request.POST['year_month_day'],description=request.POST['description'])

            for k in actorlist: #add list
                activity_op.actor.add(k)

            activity_op.is_active=False
            activity_op.save_without_historical_record()


            atv=Activity.objects.last()
            data['id_activit'] = atv.pk

            return render(request, 'conectividadeapp/activity_success.html', data)


        # imput multiple devices /insere varios devices para uma atividade
        if op=="3" or op == "4":

            devices_multlist=request.POST.getlist('devices_mult')
            tam=len(devices_multlist)

            data['registro'] = Activity.objects.all().order_by('-id')[:tam]


            for j in devices_multlist:


                actorlist=request.POST.getlist('actorss')
                reasonobj=request.POST['reason']


                #fks/ create to objects device and activity reason:
                dev_ob = Device.objects.get(id=j)
                res_ob = ActivityReason.objects.get(id=reasonobj)

                # tratamento de atributos do objeto selecionado / object attributes processing for olddevice:

                if dev_ob.name == None :
                    dev_ob.name = ""
                if dev_ob.primary_ip4 == None :
                    dev_ob.primary_ip4 = None
                if dev_ob.primary_ip6 == None :
                    dev_ob.primary_ip6 = None
                if dev_ob.site == None :
                    dev_ob.site = ""

                if dev_ob.rack == None :
                    rack = None
                else :
                    rack = dev_ob.rack.name

                #onetoone
                gravadevice = OldDevice.objects.create(
                        name = dev_ob.name,
                        ipv4 = dev_ob.primary_ip4,
                        ipv6 = dev_ob.primary_ip6,
                        site = dev_ob.site,
                        rack = rack
                        )
                res_old =OldDevice.objects.get(id=gravadevice.pk)

                if op == "3": #entra aqui se for atividade de instalação/into install activity
                    type = 'INSTALL'
                else: #entra aqui se for atividade de remoção / into remove activity
                    type = 'REMOVE'

                activity_op = Activity.objects.create(device= dev_ob,olddevice=res_old,reason=res_ob,when=request.POST['year_month_day'],description=request.POST['description'])

                for k in actorlist: # adiciona lista de atores /add  actores list
                    activity_op.actor.add(k)

                activity_op.is_active=False #mecanismo de status da atividade, tratado no signals django
                activity_op.save_without_historical_record() #save is active / salvo atributo "is_active"


            #get id in object for demonstration in template/ pega objeto para demotrar no template
            atv=Activity.objects.last()
            data['id_activit'] = atv.pk

            return render(request, 'conectividadeapp/activity_success.html', data)

'''
Activity Filter Views
'''

# All activities
# Activity List Views

class ActivityopListView(PermissionRequiredMixin, View):
    permission_required = 'conectividadeapp.view_activity'
    def get(self, request):


        return render(request, 'conectividadeapp/activity_op.html')

class ActivityListView(PermissionRequiredMixin, View):
    permission_required = 'conectividadeapp.view_activity'
    def get(self, request, type):



        # Current year
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        current_day = datetime.date.today().day

        # Template to be rendered
        template_name = 'conectividadeapp/activity_list.html'

        # Search and Filters setup
        r = request.GET

        search = None
        year_month_day_researched = None
        year_month_researched = None
        year_researched = None

        first_activity = Activity.objects.all().order_by('when').first()

        if 'btn-search-research' in r:
            if r.get('search') is not None:
                search = r.get('search')

                activity_list = (
                    Activity.objects.filter(reason__type__icontains=search)
                    | Activity.objects.filter(actor__name__icontains=search)
                    | Activity.objects.filter(description__icontains=search)
                ).order_by('-when')

        elif 'btn-year-month-day-research' in r:
            if r.get('year_month_day') is not None:
                year_month_day_researched = datetime.datetime.strptime(r.get('year_month_day'), '%Y-%m-%d')

                activity_list = Activity.objects.filter(
                    when__year=year_month_day_researched.year,
                    when__month=year_month_day_researched.month,
                    when__day=year_month_day_researched.day,
                ).order_by('-when')

        elif 'btn-year-month-research' in r:
            if r.get('year_month') is not None:
                year_month_researched = datetime.datetime.strptime(r.get('year_month'), '%Y-%m')

                activity_list = Activity.objects.filter(
                    when__year=year_month_researched.year,
                    when__month=year_month_researched.month,
                ).order_by('-when')

        elif 'btn-year-research' in r:
            if r.get('year') is not None:
                year_researched = datetime.datetime.strptime(r.get('year'), '%Y')

                activity_list = Activity.objects.filter(
                    when__year=year_researched.year,
                ).order_by('-when')

        else:
            activity_list = Activity.objects.all().order_by('-when')

        if type == 'INSTALL' or type == 'REMOVE':
            activity_list = activity_list.filter(reason__type=type)
            type_activity=type


        # Limits listing of only active activities
        activity_list = activity_list.filter(_active=True)

        # Quantity of activities after the filter
        quantity = len(activity_list)

        #device role to filter/papeis para filtro com papeis
        dr = DeviceRole.objects.all()

        # Context dictionary for rendering
        context = {
            'current_year': current_year,
            'current_month': current_month,
            'current_day': current_day,
            'activity_list': activity_list,
            'quantity': quantity,
            'first_activity': first_activity,
            'year_month_researched': year_month_researched,
            'year_month_day_researched': year_month_day_researched,
            'year_researched': year_researched,
            'type_activity': type_activity,
            'dr' : dr,
        }

        return render(request, template_name, context)

'''
Role device filter made in activity_list
'''

class ActivityListRoleView(LoginRequiredMixin, View):

    def post(self, request):


        #pegando valores via post
        activitys_list=request.POST.getlist('activitys_list')

        print("----")
        print(activitys_list)
        type_activity = request.POST['type_activity']
        role = request.POST['role']
        filter1 = request.POST['filter1']
        op = request.POST['op']




        #Transformando em objetos
        #rolelist2= Device.objects.filter(pk__in=rolelist) #lista de devices de acordo com obj
        activitys_list_objects= Activity.objects.filter(pk__in=activitys_list)#lista de atividades

        if role !="0" :
            dr_role = DeviceRole.objects.get(slug=role)
            print(dr_role)
            list_obj= dr_role.devices.all() #lista de devices com o papel selecionado

        else:
            list_obj= None
            dr_role=None



        print(list_obj)
        lista_all=[]
        lista_all_role=[]


        dr= DeviceRole.objects.all()
        activitys_list1=[]
        activitys_list2=[]
        activitys_list3=[]
        activitys_list4=[]

        #quantity
        lista=0 #geral

        template_name = 'conectividadeapp/activity_list_role.html'

        #op == 1   : filtro de um papel especifico

        if op == "1" : #apenas 1 papel

            for activity in activitys_list_objects :

                if activity.device.device_role.slug == role  :
                    lista=lista+ 1  #quantidade
                    print("*")
                    activitys_list1.append(activity.id)

            activitys_list1_obj= Activity.objects.filter(pk__in=activitys_list1)#cria objetos



        #op == 2   : filtro papeis de conectividdade

        elif op == "2" :


            #Quantiry for grup/quantidade por grupos de papeis
            lista_ap=0
            lista_sw=0
            lista_tr=0
            lista_mo=0

            list_conectivity_ap = ["wireless-controller","wireless-access-point","injetor-poe"]
            list_conectivity_sw = ["router","switch-access","switch-distribution","switch-core","switch-chassi"]
            list_transceiver = ["transceiver","transceiver-sfp-lx","transceiver-sfp-sx","transceiver-sfp-tx","transceiver-sfp-plus-lr","transceiver-sfp-plus-sr","transceiver-xfp-lr","transceiver-xfp-sr"]
            list_modulos = ["module-5120-5500","module-9500"]

            for activity in activitys_list_objects :

                if activity.device.device_role.slug in list_conectivity_ap :
                    lista_ap=lista_ap + 1  #quantidade
                    print("*2")
                    activitys_list1.append(activity.id)
                if activity.device.device_role.slug in list_conectivity_sw  :
                    lista_sw=lista_sw + 1  #quantidade
                    activitys_list2.append(activity.id)
                    print("*2")
                if activity.device.device_role.slug in list_transceiver  :
                    lista3_tr=lista_tr + 1  #quantidade
                    activitys_list3.append(activity.id)
                    print("*2")
                if activity.device.device_role.slug in list_modulos  :
                    lista_mo=lista_mo + 1  #quantidade
                    activitys_list4.append(activity.id)
                    print("*2")

            lista=lista_ap+lista_sw+lista_tr+lista_mo  #quantidade geral
            activitys_list1_obj= Activity.objects.filter(pk__in=activitys_list1)#cria objetos ap
            activitys_list2_obj= Activity.objects.filter(pk__in=activitys_list2)#cria objetos sw
            activitys_list3_obj= Activity.objects.filter(pk__in=activitys_list3)#cria objetos tran
            activitys_list4_obj= Activity.objects.filter(pk__in=activitys_list4)#cria objetos  mod
            quantity = lista

            context = {

            'type_activity': type_activity,
            'dr_role': dr_role,
            'role':role,
            'quantity':quantity,
            'activitys_list_objects':activitys_list_objects,
            'list_obj':list_obj,
            'lista':lista,
            'lista_all': lista_all,
            'lista_all_role':lista_all_role,
            'filter1': filter1,
            'op':op,
            'lista_ap':lista_ap,
            'lista_sw':lista_sw,
            'lista_tr':lista_tr,
            'lista_mo':lista_mo,
            'list_modulos':list_modulos,
            'list_transceiver':list_transceiver,
            'list_conectivity_sw':list_conectivity_sw,
            'list_conectivity_ap':list_conectivity_ap,
            'activitys_list1_obj':activitys_list1_obj,
            'activitys_list2_obj':activitys_list2_obj,
            'activitys_list3_obj':activitys_list3_obj,
            'activitys_list4_obj':activitys_list4_obj,

            }

            return render(request, template_name, context)

        #op == 10   : filtro geral todos papeis
        elif op == "10" :
            print("*3")

            role_list = request.POST.getlist('roles_mult')
            print(role_list)
            role_list_slug = []
            role_list_obj = DeviceRole.objects.filter(pk__in=role_list)
            print(role_list_obj)

            print("-------------------------")
            print(activitys_list_objects)

            lista=0


            for activity_role in role_list_obj :

                lista_all_role.append(activity_role.slug)
                print(lista_all_role)


                for activity in activitys_list_objects :
                    if  activity.device.device_role.slug == activity_role.slug  :
                            print(activity)

                            #print(activity_role.slug)
                            #print("=")

                            #print(activity.device.device_role.slug)
                            lista=lista+ 1  #quantidade
                            activitys_list1.append(activity.id) #pega id para construir obj

                            print("*")

            activitys_list1_obj = Activity.objects.filter(pk__in=activitys_list1)#cria objetos atividades

            quantity = lista
            print( lista_all_role )

            context = {

            'dr_role': dr_role,
            'role':role,

            'activitys_list_objects':activitys_list_objects,
            'list_obj':list_obj,
            'lista_all': lista_all,
            'lista_all_role':lista_all_role,

            'type_activity': type_activity,
            'filter1': filter1,
            'op':op,
            'lista':lista,
            'quantity':quantity,
            'activitys_list1_obj':activitys_list1_obj,
            }

            return render(request, template_name, context)
        else:

            for activity_role in dr :

                for activity in activitys_list_objects :

                    if activity.device.device_role.slug == activity_role.slug  :
                        lista=lista+ 1  #quantidade
                        activitys_list3.append(activity.id) #pega id para construir obj
                        print("*")


                lista_all.append(lista) #add quantidade do role 1 na posição X de activity
                lista_all_role.append(activity_role.slug) #add papel/role 1 na posição X de activity

                print(lista_all_role ) #
                print("lista:")
                print(lista)
                print("lista all:")
                print(lista_all)
                lista=0

            activitys_list3_obj= Activity.objects.filter(pk__in=activitys_list3)#cria objetos

        print("all----")
        print(lista_all)
        print("----")

        #list_obj_activitys=activitys_list2.devices.all() #lista de devices com as atividades
        #records = (list_obj | list_obj_activitys).distinct()


        # Template to be rendered
        #template_name = 'conectividadeapp/list_activity_quant_role.html'
        print(type_activity)


        # Quantity of activities after the filter dr_role
        quantity = lista

        print(filter1)
        print(activitys_list1_obj)

        # Context dictionary for rendering
        # 'rolelist2': rolelist2,
        context = {

            'dr_role': dr_role,
            'role':role,

            'activitys_list_objects':activitys_list_objects,
            'list_obj':list_obj,
            'lista_all': lista_all,
            'lista_all_role':lista_all_role,
            'type_activity': type_activity,
            'filter1': filter1,
            'op':op,
            'lista':lista,
            'quantity':quantity,
            'activitys_list1_obj':activitys_list1_obj,
        }

        return render(request, template_name, context)



'''

Multiple Role filter

'''
class ListActivityListRoleView(LoginRequiredMixin,View):

    def post(self, request):

        object_list = DeviceRole.objects.all()
        template_name = 'conectividadeapp/list_role_device.html'

        #pegando valores via post

        activitys_list=request.POST.getlist('activitys_list')
        activitys_list_objects= Activity.objects.filter(pk__in=activitys_list)
        print("----")
        print(activitys_list)
        type_activity = request.POST['type_activity']
        role = request.POST['role']
        filter1 = request.POST['filter1']


        context = {

            'type_activity': type_activity,
            'role': role,
            'filter1': filter1,
            'activitys_list': activitys_list,
            'object_list': object_list,
            'activity_list' : activitys_list_objects,

        }



        return render(request, template_name, context)

'''
Activity details (DetailView) and update
'''

#detalhes da atividade
class ActivityDetailsView(PermissionRequiredMixin,DetailView):
    permission_required = 'conectividadeapp.view_activity'
    model = Activity
    template_name = 'conectividadeapp/activity_details.html'

#update atividade (ActivityUpdateView)
#class ActivityUpdateView(PermissionRequiredMixin,LoginRequiredMixin,View):

class ActivityUpdateView(LoginRequiredMixin,View):
    permission_required = 'conectividadeapp.change_activity'
    def get(self, request, atv):
        return redirect('plugins:conectividadeapp:activity_op_list')



    def post(self, request, atv):
        if request.POST['status'] :
            status =  request.POST['status']


            if status == "True" :
                activity = Activity.objects.get(pk=atv)
                activity.deactivate()

            else :
                activity = Activity.objects.get(pk=atv)
                activity.activate()

        else:

            return redirect('plugins:conectividadeapp:list')


        activity= get_object_or_404(Activity.objects.filter(id = atv))

        return render(request, 'conectividadeapp/activity_details.html', {
            'activity' : activity
        } )

'''
 Device history

'''

class DeviceHistoryView(PermissionRequiredMixin,View):
    permission_required = 'conectividadeapp.view_activity'
    def get(self, request, pk):
        device = get_object_or_404(Device.objects.filter(id=pk))
        o = Device.objects.get(id=pk)    # pega o objeto da atividade
        activitys = o.activity_set.all()
        return render(request, 'conectividadeapp/device_history.html',  {
            'device': device,
            'activitys': activitys,
        })

    def post(self, request):

        actors=Actor.objects.all()


         #analisar se é a melhor maneira
        if request.POST['device_obj_id'] :
            deviceid  = request.POST['device_obj_id']
            device_obj = Device.objects.get(id=deviceid) # cria instancia do device

        else:
            print("erro device_obj_id")
            return redirect('plugins:conectividadeapp:list')


        if request.POST['op'] :

            op = request.POST['op']


            if op == "1" :

                activity_reason = ActivityReason.objects.filter(type="INSTALL")

            else :
                activity_reason = ActivityReason.objects.filter(type="REMOVE")

        else:
            print("erro op")
            return redirect('plugins:conectividadeapp:list')

        context = {
                        'op': op,
                        'actors': actors,
                        'activity_reason': activity_reason,
                        'device_obj':device_obj
                    }

        return render(request, 'conectividadeapp/activity_form_device.html', context)


'''
    Multiple Device
'''


class SelectMultipleView(LoginRequiredMixin,View):


    def post(self, request): #metodo para achamada form


        device_obj= True
        actors= Actor.objects.all()


        if request.POST.getlist('devices_mult') :

            devices_mult=request.POST.getlist('devices_mult')

            quantity = len(devices_mult)#verifica quantos tem na lista

            #print(devices_mult)
            #print(quantity)
            #print("----")

            if quantity == 1 or quantity == 2  :
                #print("a")
                #print(devices_mult)
                #print(quantity)
                return redirect('plugins:conectividadeapp:searchdevice')

            else :
                # se mais de um device é selecionado ok!
                del devices_mult[0] #deleta o primeiro elemento (elemento de controle)
                #cria os objetos

                #https://docs.djangoproject.com/en/dev/topics/db/queries/#the-pk-lookup-shortcut

                #obj = Device.objects.in_bulk(devices_mult, field_name='pk')
                obj = Device.objects.filter(pk__in=devices_mult)
        else :


            return redirect('plugins:conectividadeapp:searchdevice')


        if request.POST['op'] :

            op = request.POST['op']

            if op == "3" :

                activity_reason  = ActivityReason.objects.filter(type="INSTALL")

            else :

                activity_reason = ActivityReason.objects.filter(type="REMOVE")

        else :

            #print("c")

            return redirect('plugins:conectividadeapp:searchdevice')



        return render(request, 'conectividadeapp/activity_form_select_multipledevice.html', {

                'devices_mult':devices_mult,
                'obj':obj,
                'device_obj':device_obj,
                'activity_reason':activity_reason,
                'op':op,
                'actors':actors,
            }
            )

'''
CRUD actor
'''

class ActorView(PermissionRequiredMixin,View):
    permission_required = 'conectividadeapp.view_actor'
    def get(self, request, pk):
        actor = get_object_or_404(Actor.objects.filter(id=pk))
        o=Actor.objects.get(id=pk) #pega o objeto da atividade
        activitys=o.activity_set.all()
        history_list = ActorHistory.objects.filter(id=actor.id).order_by('-history_date')[:5]

        return render(request, 'conectividadeapp/actor.html',  {
            'actor': actor,
            'activitys': activitys,
            'history_list': history_list,
        })

class CreateActor(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = 'conectividadeapp.add_actor'
    model = Actor
    queryset = Actor.objects.all()
    model_form =  ActorForm
    template_name = 'conectividadeapp/actor_edit.html'
    default_return_url = 'plugins:conectividadeapp:actor_list'

class EditActor(LoginRequiredMixin,CreateActor):
    permission_required = 'conectividadeapp.change_actor'

class ActorListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = 'conectividadeapp.view_actor'
    queryset = Actor.objects.all()
    filterset = ActorFilter
    filterset_form = ActorFilterForm
    table = ActorTable
    template_name = 'conectividadeapp/actor_list.html'

class DeleteActor(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = 'conectividadeapp.delete_actor'
    queryset = Actor.objects.all()
    model = Actor
    default_return_url = 'plugins:conectividadeapp:actor_list'

class BulkDeleteActor(PermissionRequiredMixin, generic.BulkDeleteView):
    permission_required = 'conectividadeapp.delete_actor'
    queryset = Actor.objects.filter()
    table = ActorTable
    default_return_url = 'plugins:conectividadeapp:actor_list'

'''
Search Devices Views
'''
class ListDeviceView(LoginRequiredMixin,ListView):
    permission_required = 'conectividadeapp.view_activity'
    model = Device
    template_name = 'conectividadeapp/searchdevice.html'

class ListDeviceWithFieldsEmpty(LoginRequiredMixin,ListView):
    model = Device
    template_name = 'conectividadeapp/device_with_fields_empty.html'
    permission_required = 'conectividadeapp.view_activity'

    def get_queryset(self):
        object_list = {}

        devices = Device.objects.annotate(trim_serial=Func(F('serial'), function='TRIM'),
            trim_asset_tag=Func(F('asset_tag'), function='TRIM')).filter(

            Q(serial__in = RawSQL('''select d.serial from dcim_device d
       	 		                   group by d.serial
                                   having count(d.serial) > %s''',('1'))) |
            Q(trim_serial = '') | Q(serial__isnull = True) |
            Q(trim_asset_tag = '') | Q(asset_tag__isnull = True)

        ).order_by('serial')

        for device in devices:
            if device.serial in object_list :
                object_list[device.serial].append(device)
            else:
                object_list[device.serial] = [device]


        return object_list

class SearchDeviceView(PermissionRequiredMixin,ListView):
    permission_required = 'conectividadeapp.view_activity'
    model = Device
    template_name = 'conectividadeapp/searchdeviceresult.html'

    def get_queryset(self):

        query = self.request.GET.get('q')
        object_list = Device.objects.filter(
            Q(asset_tag__icontains=query)
            | Q(name__icontains=query)
        )
        return object_list



class ActorsHistoryListView(PermissionRequiredMixin, View):
    permission_required = 'conectividadeapp.view_actor'
    '''
    View list of general history of modifications of instances of the Actor class
    '''
    def get(self, request):

        history_list = ActorHistory.objects.all().order_by('-history_date')

        template_name = 'conectividadeapp/actors_history_list.html'

        context = {
            'history_list': history_list,
        }

        return render(request, template_name, context)

class ActorHistoryListView(PermissionRequiredMixin, View):
    permission_required = 'conectividadeapp.view_actor'
    '''
    View list of general history of modifications of one instance of the Actor class
    '''
    def get(self, request, pk):

        history_list = ActorHistory.objects.filter(id=pk).order_by('-history_date')
        actor = Actor.objects.get(id=pk)

        template_name = 'conectividadeapp/actor_history_list.html'

        context = {
            'history_list': history_list,
            'actor': actor,
        }

        return render(request, template_name, context)

class ActivitiesHistoryListView(PermissionRequiredMixin, View):
    permission_required = 'conectividadeapp.view_activity'
    '''
    View list of general history of modifications of instances of the Activity class
    '''
    def get(self, request):

        history_list = ActivityHistory.objects.all().order_by('-history_date')

        template_name = 'conectividadeapp/activities_history_list.html'

        context = {
            'history_list': history_list,
        }

        return render(request, template_name, context)

class ActivityHistoryListView(PermissionRequiredMixin, View):
    permission_required = 'conectividadeapp.view_activity'
    '''
    View list of general history of modifications of one instance of the Activity class
    '''
    def get(self, request, pk):

        history_list = ActivityHistory.objects.filter(id=pk).order_by('-history_date')
        activity = Activity.objects.get(id=pk)

        template_name = 'conectividadeapp/activity_history_list.html'

        context = {
            'history_list': history_list,
            'activity': activity,
        }

        return render(request, template_name, context)
