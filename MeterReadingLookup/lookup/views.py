import traceback

from django.shortcuts import render, redirect
from .models import RegisterReadings,ParsedData
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UploadFileForm
from lookup.management.commands import parse_file


#@login_required(login_url='/login/')
def index(request):
    return render(request, 'lookup/index.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'lookup/login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_name = uploaded_file.name
            decoded_file = uploaded_file.read().decode('utf-8').split('\n')
            # get the file contents and file name to be parsed and stored in the data base
            try:
                parse_file.Command().file_parser(file_name=file_name, file_content=decoded_file)
            except Exception as e:
                return render(request, 'lookup/upload_status.html', {'file_name': file_name,
                                                                     'status': "failure", 'failure_msg': e.__class__.__name__})

            return render(request, 'lookup/upload_status.html', {'file_name': file_name,
                                                                 'status': "success"})
    else:
        form = UploadFileForm()
    return render(request, 'lookup/upload.html', {'form': form})


def flowfile_list(request):
    # To Display the list of all the unique files uploaded/ parsed into database
    files = RegisterReadings.objects.values_list('mpan__file_name', flat=True).distinct()
    return render(request, 'lookup/flowfile_list.html', {'files': files})


def flowfile_detail(request, file_name):
    # To display the meter reading details from each flow file and search
    MPAN_query = request.GET.get('MPAN_search')
    serialno_query = request.GET.get('serialno_search')

    if file_name == "all":
        # To view readings from all flow files available at once and search
        file_readings = RegisterReadings.objects.all()
    else:
        # To view readings from a specific flow file and search in the same
        file_readings = RegisterReadings.objects.filter(mpan__file_name=file_name)

    if MPAN_query:
        file_readings = file_readings.filter(mpan__MPAN_Core__startswith=MPAN_query)

    elif serialno_query:
        file_readings = file_readings.filter(mpan__serial_number__startswith=serialno_query)

    return render(request, 'lookup/flowfile_readings.html', {'file_readings': file_readings, 'file_name': file_name})
