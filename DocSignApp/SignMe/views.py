import os
import shutil


from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

from .forms import FileForm, SignatureForm, AlgorithmForm, FileUploadForm
from .utils import get_user_details, handle_uploaded_file


LICENSE_DNS_NAME = "testserverbit.com"
PORT = "8080"
CONNECTOR_PATH = "/opt/bit4id/connector"
DOCUMENT_FILENAME = ""
SIGNATURE_TYPE = ""


def index(request):
    return render(request, "welcome.html")


@csrf_exempt
def get_file(request):
    if request.method == "POST":
        file_form = FileForm(request.POST)
        signature_form = SignatureForm(request.POST)
        algorithm_form = AlgorithmForm(request.POST)
    else:
        file_form = FileForm()
        signature_form = SignatureForm()
        algorithm_form = AlgorithmForm()
    return render(
        request,
        "file.html",
        {"file_form": file_form, "signature_form": signature_form, "algorithm_form": algorithm_form},
    )


@csrf_exempt
def sign_file(request):
    if request.method == "POST":
        (filename, file_extension, signature_type, signature_algorithm) = get_user_details(request.POST.dict())
        global DOCUMENT_FILENAME
        DOCUMENT_FILENAME = filename
        global SIGNATURE_TYPE
        SIGNATURE_TYPE = signature_type
        if signature_type == "CAdES":
            DOCUMENT_FILENAME = "".join([DOCUMENT_FILENAME, ".p7m"])
        if file_extension != "xml" and signature_type == "XAdES":
            return render(request, "error.html", {"error_msg": "Cannot sign non XML files with XAdES signature type"})
        if file_extension != "pdf" and signature_type == "PAdES":
            return render(request, "error.html", {"error_msg": "Cannot sign non PDF files with PAdES signature type"})
        if file_extension != "xml" and any(i for i in ["MD5", "SHA1", "SHA256", "SHA512"] if i == signature_algorithm):
            return render(request, "error.html", {"error_msg": f"Cannot sign non XML files with {signature_algorithm}"})
        if file_extension == "xml" and any(
            i for i in ["RSASHA1", "RSAMD5", "RSASHA256", "RSASHA512"] if i == signature_algorithm
        ):
            return render(request, "error.html", {"error_msg": f"Cannot sign XML files with {signature_algorithm}"})
    return render(
        request,
        "file_upload.html",
        {
            "document_path": f"http://{LICENSE_DNS_NAME}:{PORT}/static/{filename}",
            "filename": filename,
            "signatureType": signature_type,
            "signatureAlgorithm": signature_algorithm,
        },
    )


@csrf_exempt
def uploaded(request):
    if request.method == "POST":
        shutil.copy(
            f"{CONNECTOR_PATH}/var/test_output/webapptest/test.pdf",
            f"./SignMe/static/signed/signed-{SIGNATURE_TYPE}-{DOCUMENT_FILENAME}",
        )
    return render(
        request,
        "success.html",
        {"path": f"http://{LICENSE_DNS_NAME}:{PORT}/static/signed/signed-{SIGNATURE_TYPE}-{DOCUMENT_FILENAME}"},
    )


@csrf_exempt
def file_upload(request):
    if request.method == "POST" and request.FILES.get("uploaded_file", None):
        (_, _, signature_type, signature_algorithm) = get_user_details(request.POST.dict())
        uploaded_file = request.FILES["uploaded_file"]
        handle_uploaded_file(uploaded_file)
        filename = uploaded_file.name
        file_extension = filename.split(".")[-1]
        global DOCUMENT_FILENAME
        DOCUMENT_FILENAME = filename
        global SIGNATURE_TYPE
        SIGNATURE_TYPE = signature_type
        if signature_type == "CAdES":
            DOCUMENT_FILENAME = "".join([DOCUMENT_FILENAME, ".p7m"])
        if file_extension != "xml" and signature_type == "XAdES":
            return render(request, "error.html", {"error_msg": "Cannot sign non XML files with XAdES signature type"})
        if file_extension != "pdf" and signature_type == "PAdES":
            return render(request, "error.html", {"error_msg": "Cannot sign non PDF files with PAdES signature type"})
        if file_extension != "xml" and any(i for i in ["MD5", "SHA1", "SHA256", "SHA512"] if i == signature_algorithm):
            return render(request, "error.html", {"error_msg": f"Cannot sign non XML files with {signature_algorithm}"})
        if file_extension == "xml" and any(
            i for i in ["RSASHA1", "RSAMD5", "RSASHA256", "RSASHA512"] if i == signature_algorithm
        ):
            return render(request, "error.html", {"error_msg": f"Cannot sign XML files with {signature_algorithm}"})
        return render(
            request,
            "file_upload.html",
            {
                "document_path": f"http://{LICENSE_DNS_NAME}:{PORT}/static/user_docs/{filename}",
                "filename": filename,
                "signatureType": signature_type,
                "signatureAlgorithm": signature_algorithm,
            },
        )
    else:
        upload_form = FileUploadForm()
        signature_form = SignatureForm()
        algorithm_form = AlgorithmForm()
    return render(
        request,
        "upload.html",
        {"upload_form": upload_form, "signature_form": signature_form, "algorithm_form": algorithm_form},
    )
