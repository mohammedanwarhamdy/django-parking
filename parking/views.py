from django.shortcuts import render,redirect
from .models import devices
from pyzkaccess import ZKAccess
from .forms import edit_ipform
from django.contrib import messages

global ip_address



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

            with ZKAccess(connstr=connstr) as zk:
                zk.parameters.gateway_ip_address = gate
                zk.parameters.netmask = subnet
                zk.parameters.ip_address = Newip_address

            myform = form.save()

            return redirect("/")

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
    return redirect("/")
# Create your views here.
