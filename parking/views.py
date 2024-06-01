from django.shortcuts import render,redirect
from .models import devices,subscriber,transactions,counting
from datetime import datetime, date
from pyzkaccess import ZKAccess
from .forms import edit_ipform,add_subscriber
from django.contrib import messages
import datetime
from pyzkaccess.tables import User


from datetime import datetime
from django.contrib.auth.decorators import login_required

global ip_address
import accounts

@login_required
def all_devices(request):
    global  ip_address
    #its method to get ip wich entered in input ip to use it to connect conttroller
    if request.method == "GET":
        print(request)
        ip_address = request.GET.get("ip_address")
        device_name=request.GET.get("device_name")





        if ip_address:  # Check if ip_address is not None or empty
            connstr = f'protocol=TCP,ipaddress={ip_address},port=4370,timeout=5000,passwd='
            try:
                #connect the controller and get ip and serial number
                zk = ZKAccess(connstr=connstr)
                print('Device SN:', zk.parameters.serial_number, 'IP:', zk.parameters.ip_address)
                device_serialip=devices(serial=zk.parameters.serial_number,IP=zk.parameters.ip_address,Device_name=device_name)
                #function get all serial number in database
                all_serial=devices.objects.values_list("serial",flat=True)
                #its condetion to not add the same controller twice
                if zk.parameters.serial_number and zk.parameters.ip_address != None and  zk.parameters.serial_number not in all_serial:
                    print(devices.serial)
                    #add ip an serial numer to database

                    device_serialip.save(force_insert=True)
            except Exception as e:
                print(e)

        #get all devices
        all_devices = devices.objects.all()
        context = {"all_devices": all_devices}
        return render(request, "device.html", context)

def edit_ip(request,id):

#get the seleced device id
    device_to_edit=devices.objects.get(id=id)
    global ip_address
    if request.method == "GET":
#get the input data new ip address subnet mask gateway
        Newip_address = request.GET.get("IP")
        subnet=request.GET.get("su_net")
        gate=request.GET.get("gate_way")
#get old ip from database to connect it to edit ip
        device_filter=devices.objects.get(id=id)
        ip_address=device_filter.IP

#defin form
    form=edit_ipform(request.GET,instance=device_to_edit)
#condition if the form valid connect old ip and edit it
    if form.is_valid():
        connstr = f'protocol=TCP,ipaddress={ip_address},port=4370,timeout=5000,passwd='
        try:



            myform = form.save()
            with ZKAccess(connstr=connstr) as zk:
                zk.parameters.gateway_ip_address = gate
                zk.parameters.netmask = subnet
                zk.parameters.ip_address = Newip_address

            messages.success(request, 'Your device was edited successfully!')
            return redirect("/devices")

        except:
            pass

    else:
        form = edit_ipform()

    context = {"form":form}
    return render(request, "edit.html", context)
def destroy(request,id):

    device=devices.objects.get(id=id)
    device.delete()
    messages.success(request, 'Your device was deleted successfully!')
    return redirect("/devices")
# Create your views here.
@login_required
def all_subscriber(request):
    card=None
    start_time=None
    end_time=None
    subscriberid=None
    packege=None
    try:

        if request.method == "GET":
            form = add_subscriber(request.GET)
            if form.is_valid():
                # Save subscriber form data

                # Extract card, start_time, and end_time from the form data
                card = str(form.cleaned_data.get("card"))  # Convert card to string
                start_time = form.cleaned_data.get("valid_from")  # Already a datetime.date object
                end_time = form.cleaned_data.get("valid_to")  # Already a datetime.date object
                subscriberid = str(form.cleaned_data.get("subscriberid"))
                packege=form.cleaned_data.get("packege")

                # Create and save User instance if needed
                all_ips=devices.objects.values_list("IP",flat=True)
                for ipaddress in all_ips:
                    print(ipaddress)

                    zk = ZKAccess(f'protocol=TCP,ipaddress={ipaddress},port=4370,timeout=5000,passwd=')
                    my_user = User(card=card, pin=subscriberid, password='555', start_time=start_time, end_time=end_time, super_authorize=True).with_zk(zk)
                    my_user.save()
                    subscriber_instance = form.save()
                # Handle with_zk() method and zk variable appropriately

        else:
            form = add_subscriber()
    except Exception as e:
        print(e)

    all_subscribers=subscriber.objects.all()
    context={"all_subscribers":all_subscribers,"form":form,"card":card,"start_time":start_time,"end_time":end_time,"packege":packege}
    print(all_subscribers)
    return render(request,"subsciber.html",context)
def delete_subscriber(request,id):
    try:

        delet_subscriber=subscriber.objects.get(id=id)
        card=str(delet_subscriber.card)
        start_time=delet_subscriber.valid_from
        end_time=delet_subscriber.valid_to
        subscriberid=str(delet_subscriber.subscriberid)
        delet_subscriber.delete()
        all_ips = devices.objects.values_list("IP", flat=True)
        for ipaddress in all_ips:
            print(ipaddress)

            zk = ZKAccess(f'protocol=TCP,ipaddress={ipaddress},port=4370,timeout=4000,passwd=')
            my_user = User(card=card, pin=subscriberid, password='555', start_time=start_time, end_time=end_time,
                           super_authorize=True).with_zk(zk)
            my_user.delete()

    except Exception as e :
        print(e)


    #my_user = User(card='123456', pin='123', password='555', super_authorize=True).with_zk(zk)
    messages.success(request, 'Your subscriber was deleted successfully!')
    return redirect("/subscriber")
def edit_subscriber(request,id):
    edit_subscriber=subscriber.objects.get(id=id)

    if request.method=="GET":
        try:

            form = add_subscriber(request.GET, instance=edit_subscriber)
            if form.is_valid():
                myform = form.save()
                card = str(edit_subscriber.card)
                start_time = edit_subscriber.valid_from
                end_time = edit_subscriber.valid_to
                subscriberid = str(edit_subscriber.subscriberid)
                all_ips = devices.objects.values_list("IP", flat=True)
                for ipaddress in all_ips:
                    print(ipaddress)

                    zk = ZKAccess(f'protocol=TCP,ipaddress={ipaddress},port=4370,timeout=4000,passwd=')
                    my_user = User(card=card, pin=subscriberid, password='555', start_time=start_time, end_time=end_time,
                                   super_authorize=True).with_zk(zk)
                    my_user.save()
                return redirect("/subscriber")
        except Exception as e:
            print(e)
    else:
        add_subscriber(instance=edit_subscriber)
    context={"form":form}
    return render(request,"subsciber.html",context)
@login_required
def all_transactions(request):
    all_transactions= transactions.objects.all().order_by('-id')[:5]

    context={"all_transactions":all_transactions}

    return render(request,"parking.html",context)


def Counting(request):
    all_counting = counting.objects.all().order_by('-id')
    context = {"counting": all_counting, "Entrytime": None, "Exitetime": None, "Total_time": None,
               "Cost": None, "user": None}
    if request.method=="GET":
        Code=request.GET.get("code")
        print(Code)
        try:
            user=request.user
            data = transactions.objects.get(code=Code)
            Event_point = data.entry_point
            Entrytime = data.entry_time
            Exitetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Entry_time=datetime.strptime(str(Entrytime),'%Y-%m-%d %H:%M:%S')
            Exite_time=datetime.strptime(str(Exitetime),'%Y-%m-%d %H:%M:%S')
            diff=(Exite_time)-(Entry_time)
            Total_time=diff.total_seconds() / 3600
            Cost=Total_time*5
            context['Entrytime']=Entrytime
            context['Exitetime']=Exitetime
            context['Total_time'] = Total_time
            context['Cost'] = Cost
            context['user'] = user

            #adding houre price and function of approximate time here
            existing_counting = counting.objects.filter(code=Code).first()

            if existing_counting:

               print ("availble")
               messages.warning(request, 'Code already exists, updating existing record.')
            else:
                saving_counting_data=counting(User=user,exite_time=Exite_time,total_time=Total_time,cost=Cost,code=Code,entry_point=Event_point,entry_time=Entry_time)
                saving_counting_data.save()
                print("don")
        except Exception as e:
            print(e)
        






    return render(request,"counting.html",context)
