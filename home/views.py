from django.shortcuts import render,HttpResponse
from home.models import Contact
from django.contrib import messages
import base64
import os
from io import BytesIO
from PIL import Image
import subprocess
from django.http import HttpResponse
import openpyxl
import home.templates.Final as p
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import openpyxl

def view_attendance(request):
    # Define the path to the Excel file
    excel_file_name = 'Attendance.xlsx'  # Update the filename as per your requirement
    excel_file_path = os.path.join('templates', excel_file_name)

    # Check if the Excel file exists
    if os.path.exists(excel_file_path):
        # Open the Excel file
        wb = openpyxl.load_workbook(excel_file_path)
        ws = wb.active

        # Extract the date from the filename
        date_from_filename = excel_file_name.split('-')[-1].split('.')[0]

        # Get all data from the Excel sheet
        data = []
        for row in ws.iter_rows(values_only=True):
            data.append(row)

        # Render the template with the data and date
        return render(request, 'view_attendance.html', {'data': data, 'date': date_from_filename})
    else:
        # Return an error message if the file does not exist
        return render(request, 'view_attendance.html', {'error': 'Attendance file not found'})
    
def run_face_recognition_view(request):
    # Construct the full path to the image file
    image_path = os.path.join(os.path.dirname(__file__), 'templates', 'check', 'photo_1.jpg')

    # Check if the image file exists
    if os.path.exists(image_path):
        # Run face recognition on the image
        p.run_face_recognition(image_path)
        return HttpResponse("Face recognition process initiated and completed. You can check for your attendance.")
    else:
        return HttpResponse("Image file not found.")


# def run_face_recognition(image_data):
#     # Construct the full path to the Python script
#     script_path = os.path.join(os.path.dirname(__file__), 'templates', 'Final.py')

#     # Check if the script file exists
#     if not os.path.exists(script_path):
#         print("Error: Python script file not found.")
#         return

    # Run the Python script with the image data
    try:
        result = subprocess.run(['python', script_path, image_data], capture_output=True, check=True)
        print("Python script executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error running Python script:", e)



    
def index(request):
    context = {
        "variable":"This is sent"
    }
    messages.success(request,"Please Click Upload to upload the photo")
    return render(request, 'index.html',context)
def index2(request):
    context = {
        "variable":"This is sent"
    }
    return render(request, 'index2.html',context)
    #return HttpResponse("This is Homepage") #Use Template instead of HttpResponse 
def about(request):
    return render(request, 'about.html')
    #return HttpResponse("This is Aboutpage") #Use Template instead of HttpResponse
def services(request):
    return render(request, 'services.html')
    #return HttpResponse("This is servicespage") #Use Template instead of HttpResponse
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email =request.POST.get('email')
        password =request.POST.get('password')
        contact = Contact(name = name,email = email,password = password)
        contact.save()
        messages.success(request, "Form updated..."+str(Contact.objects.all()[0].name))
    return render(request, 'contact.html')
    #return HttpResponse("This is contactpage") #Use Template instead of HttpResponse
    #
    # Contact.objects.filter(name="Aj",email="xyz").first() / .last() [Contact.objects.all().first() / .last()] .create()
    # ins.save()
    # VARIABLEA_a = Contact.objects.get(name="Aj") IF WE KNOW ONLY ONE DATA PRESENT
def upload_photo_page(request):
    if request.method == 'POST':
        # Retrieve the data URL of the photo from the request
        data_url = request.POST.get('photo_data')

        if data_url:
            try:
                # Extract the base64-encoded image data from the data URL
                encoded_image_data = data_url.split(",")[1]

                # Decode the base64-encoded image data to bytes
                decoded_image_data = base64.b64decode(encoded_image_data)

                # Create a BytesIO object to simulate a file-like object
                photo = BytesIO(decoded_image_data)

                # Define the path to the "check" folder in the templates directory
                check_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'check')

                # Create the "check" folder if it doesn't exist
                if not os.path.exists(check_folder_path):
                    os.makedirs(check_folder_path)

                # Write the uploaded photo to a file in the "check" folder
                with open(os.path.join(check_folder_path, "photo_1.jpg"), 'wb+') as destination:
                    destination.write(decoded_image_data)

                # Return a success message
                return render(request, 'upload_photo.html', {'message': 'Photo uploaded successfully'})

            except Exception as e:
                # Handle any errors that occur during image processing
                return render(request, 'upload_photo.html', {'message': 'Failed to process image: ' + str(e)})
        else:
            # Handle case where no data URL is provided
            return render(request, 'upload_photo.html', {'message': 'No photo data received'})
    else:
        # Handle case where request method is not POST
        return render(request, 'upload_photo.html', {'message': ''})
