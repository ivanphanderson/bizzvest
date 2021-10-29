from io import BytesIO
from itertools import permutations
from random import randint, choices, choice, sample, shuffle
from unittest import mock
from unittest.mock import Mock

from PIL import Image
from django.core.files.images import ImageFile
from django.test import Client, TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.core.files import File as django_file
from models_app.models import *
from halaman_toko.views import *
from halaman_toko.forms import *
from models_app.models_utility import *
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile

# Create your tests here.



def mock_image_field(nama="gambar asal asalan.jpg"):
    return SimpleUploadedFile(name=nama, content=open('test.jpg', 'rb').read(),
                              content_type='image/jpeg')


def mock_pdf_field(nama="pdf asal asalan.pdf"):
    return SimpleUploadedFile(name=nama, content=open('test.pdf', 'rb').read(),
                              content_type='application/pdf')



class UserAccountTest(TestCase):
    def test_run(self) -> None:
        mock_should_fail_1 = mock_image_field()
        mock_should_fail_2 = mock_pdf_field(nama="asd.jpg")
        mock_should_fail_3 = mock_pdf_field(nama="bsd")
        mock_should_run_well_1 = mock_pdf_field(nama="csd.pdf")
        mock_should_run_well_2 = mock_pdf_field(nama="dsd.PDF")
        mock_should_run_well_3 = mock_pdf_field(nama="esd.PdF")

        validate_pdf_file_extension(mock_should_run_well_1)
        validate_pdf_file_extension(mock_should_run_well_2)
        validate_pdf_file_extension(mock_should_run_well_3)

        self.assertRaises(ValidationError, validate_pdf_file_extension, mock_should_fail_1)
        self.assertRaises(ValidationError, validate_pdf_file_extension, mock_should_fail_2)
        self.assertRaises(ValidationError, validate_pdf_file_extension, mock_should_fail_3)
