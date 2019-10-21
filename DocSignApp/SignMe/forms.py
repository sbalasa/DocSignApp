from django import forms


signature_choices = (("PAdES", "PAdES"), ("CAdES", "CAdES"), ("XAdES", "XAdES"))


algorithmn_choices = (
    ("RSASHA1", "RSASHA1"),
    ("RSAMD5", "RSAMD5"),
    ("RSASHA256", "RSASHA256"),
    ("RSASHA512", "RSASHA512"),
    ("MD5", "MD5"),
    ("SHA1", "SHA1"),
    ("SHA256", "SHA256"),
    ("SHA512", "SHA512"),
)


class FileForm(forms.Form):
    file1 = forms.FilePathField(label="Choose a file to sign: ", path="/home/santee/DocSignApp/SignMe/static/")


class SignatureForm(forms.Form):
    signature_type1 = forms.ChoiceField(label="Choose a signature type: ", choices=signature_choices)


class AlgorithmForm(forms.Form):
    algorithm1 = forms.ChoiceField(label="Choose a signing algorithm: ", choices=algorithmn_choices)


class FileUploadForm(forms.Form):
    upload_file1 = forms.FileField(label="Sign your own document: ")
