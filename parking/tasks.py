from pyzkaccess import ZKAccess
from .models import devices,transactions
import qrcode
import random
import os
import datetime

from datetime import date
from datetime import time
from datetime import timedelta
from datetime import datetime
from django.http import HttpRequest
from django.urls import reverse
from django.test.client import Client
from .views import all_transactions
def my_task():
    try:
        all_ips = devices.objects.values_list("IP", flat=True)
        for ipaddress in all_ips:
            device_data=devices.objects.get(IP=ipaddress)
            device_name=device_data.Device_name
            zk = ZKAccess(f'protocol=TCP,ipaddress={ipaddress},port=4370,timeout=4000,passwd=')
            events = zk.events.poll()
            print(events)
            event_221 = next((event for event in events if event.event_type == 221), None)
            if event_221 is not None:



                # Generate a random number
                random_number = random.randint(1000, 99999999)  # Example range for a 4-digit number

                # Convert the random number to a string
                random_number_str = str(random_number)
                saving_entry_data = transactions(code=random_number,entry_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),entry_point=device_name)
                saving_entry_data.save()
                print("done")

                # Create a QR code instance
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

                # Add data to the QR code
                qr.add_data(random_number_str)
                qr.make(fit=True)
                folder_name = 'qrcodes'
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                file_path = os.path.join(folder_name, f"{random_number}.png")

                # Create an image from the QR code
                qr_img = qr.make_image(fill_color="black", back_color="white")

                # Save the image
                qr_img.save(file_path)

                print(f"Random number: {random_number}")
                print(f"QR code saved as '{file_path}'")


    except Exception as e:
        print(e)
