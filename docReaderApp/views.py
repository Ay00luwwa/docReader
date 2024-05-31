from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import UploadFileForm
from openpyxl import load_workbook
import pandas as pd

def upload_files(request): #upload file view
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            summary = generate_summary('uploaded_file.xlsx')
            send_summary_email(summary)
            return HttpResponse("File has been successgully uploaded, you will receive a summary email soon")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('uploaded_file.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def generate_summary(file_path): #summary generation
    wb = load_workbook(filename=file_path, read_only=True)
    ws = wb.active
    data = ws.values

    columns = next(data)[0:]
    df = pd.DataFrame(data, columns=columns)
    
    summary = df.groupby(['Date', 'ACCNO', 'Cust State', 'Cust Pin', 'DPD']).size().reset_index(name='Count')
    return summary

def send_summary_email(summary):
    subject = 'Python Assignment - Ijidakinro Ayooluwa'
    body = summary.to_string(index=False)
    send_mail(subject, body, 'bloga.blog2.1@gmail.com', ['tech@themedius.ai', 'hr@themedius.ai', 'ijidakinroayooluwa@gmail.com'])
            