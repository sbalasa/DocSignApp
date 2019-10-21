import os


def get_user_details(user_options):
    document_path = user_options.get("file1", None)
    filename = ""
    if document_path:
        _, filename = os.path.split(document_path)
    signature_type = user_options.get("signature_type1", None)
    signature_algorithm = user_options.get("algorithm1", None)
    file_extension = filename.split(".")[-1]
    return filename, file_extension, signature_type, signature_algorithm


def handle_uploaded_file(f):
    with open(f"./SignMe/static/user_docs/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
