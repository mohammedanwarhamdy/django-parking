import math
from django.contrib.auth import login, authenticate
from accounts .forms import SignUpForm
from django.shortcuts import render,redirect
from .models import devices,subscriber,transactions,counting,counting_settings
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from pyzkaccess import ZKAccess
from .forms import edit_ipform,add_subscriber,FilterForm,counting_settings_form
from django.contrib import messages
import datetime
from pyzkaccess.tables import User
from django.db.models import Sum
import math
from datetime import datetime
from django.contrib.auth.decorators import login_required

global ip_address
import accounts

@login_required
def all_devices(request):
    if request.user.is_staff:
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
    else:
        return redirect('/')
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
    Name=None
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
                Name=str(form.cleaned_data.get("name"))
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
    context={"all_subscribers":all_subscribers,"form":form,"card":card,"start_time":start_time,"end_time":end_time,"packege":packege,"subscriberid":subscriberid,"Name":Name}
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
    if request.user.is_staff:
        all_counting = counting.objects.all().order_by('-id')
    else:
        all_counting = counting.objects.filter(User=request.user)

    context = {
        "counting": all_counting,
        "Entrytime": None,
        "Exitetime": None,
        "Total_time": None,
        "Cost": None,
        "user": None
    }

    if request.method == "GET":
        Code = request.GET.get("code")
        print(Code)
        try:
            user = request.user
            data = transactions.objects.get(code=Code)
            Event_point = data.entry_point
            Entrytime = data.entry_time
            Exitetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Entry_time = datetime.strptime(str(Entrytime), '%Y-%m-%d %H:%M:%S')
            Exite_time = datetime.strptime(str(Exitetime), '%Y-%m-%d %H:%M:%S')

            # Calculate total time in minutes
            total_duration = (Exite_time - Entry_time).total_seconds() / 60  # convert to minutes

            # Retrieve the counting settings
            settings_instance = counting_settings.objects.first()

            if total_duration < settings_instance.period_of_allowing:
                total_cost = 0
            else:
                total_cost = 0
                remaining_duration = total_duration

                # First Period Cost Calculation
                if remaining_duration <= settings_instance.first_period_duration:
                    total_cost += settings_instance.first_period_duration_cost
                    remaining_duration = 0
                else:
                    total_cost += settings_instance.first_period_duration_cost
                    remaining_duration -= settings_instance.first_period_duration

                # Second Period Cost Calculation
                if remaining_duration > 0:
                    if remaining_duration <= settings_instance.second_period_duration:
                        total_cost +=  settings_instance.second_period_duration_cost
                        remaining_duration = 0
                    else:
                        total_cost += settings_instance.second_period_duration_cost
                        remaining_duration -= settings_instance.second_period_duration

                # Rest Period Cost Calculation
                if remaining_duration > 0:
                    total_cost += (
                            math.ceil(remaining_duration / 60)) * settings_instance.rest_period_duration_cost_perhoure  # convert minutes to hours

                # Night Mode Handling
                if settings_instance.enable_night_mode:
                    night_start = datetime.combine(Entry_time.date(), settings_instance.n_starttime)
                    night_end = datetime.combine(Exite_time.date(), settings_instance.n_endtime)

                    if night_start > night_end:
                        night_end += timedelta(days=1)  # handle overnight night mode

                    before_night_duration = max((night_start - Entry_time).total_seconds() / 60, 0)
                    after_night_duration = max((Exite_time - night_end).total_seconds() / 60, 0)
                    night_duration = max(total_duration - before_night_duration - after_night_duration, 0)
                    if night_duration <settings_instance.min_period_tocost:
                        settings_instance = counting_settings.objects.first()

                        if total_duration < settings_instance.period_of_allowing:
                            total_cost = 0
                        else:
                            total_cost = 0
                            remaining_duration = total_duration

                            # First Period Cost Calculation
                            if remaining_duration <= settings_instance.first_period_duration:
                                total_cost += settings_instance.first_period_duration_cost
                                remaining_duration = 0
                            else:
                                total_cost += settings_instance.first_period_duration_cost
                                remaining_duration -= settings_instance.first_period_duration

                            # Second Period Cost Calculation
                            if remaining_duration > 0:
                                if remaining_duration <= settings_instance.second_period_duration:
                                    total_cost += settings_instance.second_period_duration_cost
                                    remaining_duration = 0
                                else:
                                    total_cost += settings_instance.second_period_duration_cost
                                    remaining_duration -= settings_instance.second_period_duration

                            # Rest Period Cost Calculation
                            if remaining_duration > 0:
                                total_cost += (
                                                  math.ceil(
                                                      remaining_duration / 60)) * settings_instance.rest_period_duration_cost_perhoure  # convert minutes to hours

                    else:
                        sum_of_befor_and_after=before_night_duration+after_night_duration
                        total_duration=sum_of_befor_and_after
                        if total_duration < settings_instance.period_of_allowing:
                            total_cost = 0
                        else:
                            total_cost = 0
                            remaining_duration = total_duration

                            # First Period Cost Calculation
                            if remaining_duration <= settings_instance.first_period_duration:
                                total_cost += settings_instance.first_period_duration_cost
                                remaining_duration = 0
                            else:
                                total_cost += settings_instance.first_period_duration_cost
                                remaining_duration -= settings_instance.first_period_duration

                            # Second Period Cost Calculation
                            if remaining_duration > 0:
                                if remaining_duration <= settings_instance.second_period_duration:
                                    total_cost += settings_instance.second_period_duration_cost
                                    remaining_duration = 0
                                else:
                                    total_cost += settings_instance.second_period_duration_cost
                                    remaining_duration -= settings_instance.second_period_duration

                            # Rest Period Cost Calculation
                            if remaining_duration > 0:
                                total_cost += (
                                                  math.ceil(
                                                      remaining_duration / 60)) * settings_instance.rest_period_duration_cost_perhoure

                                total_cost += settings_instance.night_modeCost  # convert minutes to hours

            context.update({
                "Entrytime": Entrytime,
                "Exitetime": Exitetime,
                "Total_time": total_duration,
                "Cost": total_cost,
                "user": user
            })

        except transactions.DoesNotExist:
            print(f"No transaction found with code {Code}")

    return render(request, "counting.html", context)
def reports(request):
    if request.user.is_staff:
        form = FilterForm(request.GET)
        combined_filtered_data = counting.objects.none()
        total_sum = None

        if form.is_valid():
            user = form.cleaned_data.get('user')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            if user is None:
                filtered_data = counting.objects.filter(creatrd_at__range=(start_date, end_date))
                filtered_data_test = subscriber.objects.filter(creatrd_at__range=(start_date, end_date))
            else:
                filtered_data = counting.objects.filter(User_id=user, creatrd_at__range=(start_date, end_date))
                filtered_data_test = subscriber.objects.filter(User_id=user, creatrd_at__range=(start_date, end_date))

            # Aggregate total cost from counting and sum of packege_cost from subscriber's packages
            counting_sum = filtered_data.aggregate(total=Sum("cost"))
            subscriber_sum = filtered_data_test.aggregate(total=Sum("packege__packege_cost"))  # Sum packege_cost

            # Calculate total sum if both are not None
            if counting_sum['total'] is not None and subscriber_sum['total'] is not None:
                total_sum = counting_sum['total'] + subscriber_sum['total']
            elif counting_sum['total'] is not None:
                total_sum = counting_sum['total']
            elif subscriber_sum['total'] is not None:
                total_sum = subscriber_sum['total']

            combined_filtered_data = list(filtered_data) + list(filtered_data_test)
            combined_filtered_data.sort(key=lambda x: x.creatrd_at)

            context = {"form": form, "combined_filtered_data": combined_filtered_data, "total_sum": total_sum}
            return render(request, "reports.html", context)

    else:
        form = FilterForm(request.GET)
        combined_filtered_data = counting.objects.none()
        total_sum = None

        if form.is_valid():
            user = request.user
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            filtered_data = counting.objects.filter(User=user, creatrd_at__range=(start_date, end_date))
            filtered_data_test = subscriber.objects.filter(User=user, creatrd_at__range=(start_date, end_date))

            # Aggregate total cost from counting and sum of packege_cost from subscriber's packages
            counting_sum = filtered_data.aggregate(total=Sum("cost"))
            subscriber_sum = filtered_data_test.aggregate(total=Sum("packege__packege_cost"))  # Sum packege_cost

            # Calculate total sum if both are not None
            if counting_sum['total'] is not None and subscriber_sum['total'] is not None:
                total_sum = counting_sum['total'] + subscriber_sum['total']
            elif counting_sum['total'] is not None:
                total_sum = counting_sum['total']
            elif subscriber_sum['total'] is not None:
                total_sum = subscriber_sum['total']

            combined_filtered_data = list(filtered_data) + list(filtered_data_test)
            combined_filtered_data.sort(key=lambda x: x.creatrd_at)

            context = {"form": form, "combined_filtered_data": combined_filtered_data, "total_sum": total_sum}
            return render(request, "reports.html", context)

        # If no valid form or other conditions met, return an empty context to render the form
    context = {"form": form, "combined_filtered_data": combined_filtered_data}
    return render(request, "reports.html", context)



def Counting_settings(request):
    if request.user.is_staff:
        settings_instance, created = counting_settings.objects.get_or_create(pk=1)

        # If the form is submitted (POST request), process the data
        if request.method == 'POST':
            form = counting_settings_form(request.POST, instance=settings_instance)
            if form.is_valid():
                form.save()
                  # Replace with the URL to redirect after successful form submission
        else:
            # If it's a GET request, populate the form with existing data
            form = counting_settings_form(instance=settings_instance)
        context={'form': form}
        return render(request,"settings.html",context)
    else:
        return redirect("/")
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})