from itertools import permutations

from django.test import Client, TestCase
from models_app.models import *
from halaman_toko.views import *
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile

# Create your tests here.



def mock_image_field(nama="gambar asal asalan.jpg"):
    return SimpleUploadedFile(name=nama, content=open('test.jpg', 'rb').read(),
                              content_type='image/jpeg')
    # return mock.MagicMock(spec=django_file, name=nama)

    # image = Image.new('RGBA', size=(50,50), color=(256,0,0))
    # image_file = BytesIO()
    # image.save(image_file, 'PNG')  # or whatever format you prefer
    # return ImageFile(image_file)



class UserAccountPhoneNumberTest(TestCase):
    def test_phone_number_1(self) -> None:

        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", user_model=User,
                               full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="asdfg")
        temp_acc.photo_profile = mock_image_field()

        def f():
            temp_acc.full_clean()
            temp_acc.save()
        self.assertRaises(ValidationError, f)  # harusnya ada Validation Error karena phone_number


    def test_phone_number_2(self) -> None:
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", user_model=User,
                               full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="1234567890")
        temp_acc.photo_profile = mock_image_field()

        def f():
            temp_acc.full_clean()
            temp_acc.save()
        self.assertRaises(ValidationError, f)  # harusnya ada Validation Error karena phone_number tidak dimulai dari 0


    def test_phone_number_3(self) -> None:
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="08138911")
        temp_acc.photo_profile = mock_image_field()
        def f():
            temp_acc.full_clean()
            temp_acc.save()
        self.assertRaises(ValidationError, f)  # harusnya ada Validation Error karena TOTAL minimal 9 digit


    def test_phone_number_4(self) -> None:

        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", user_model=User,
                               full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="0813891144674643")
        temp_acc.photo_profile = mock_image_field()

        def f():
            temp_acc.full_clean()
            temp_acc.save()
        # harusnya ada Validation Error karena TOTAL digit pada phone_number maksimal 15 digit
        self.assertRaises(ValidationError, f)


    def test_phone_number_5(self) -> None:

        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", user_model=User,
                               full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="0813891a674643")
        temp_acc.photo_profile = mock_image_field()
        def f():
            temp_acc.full_clean()
            temp_acc.save()
        # harusnya ada Validation Error karena ada huruf pada digit
        self.assertRaises(ValidationError, f)


    def test_phone_number_6(self) -> None:
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", user_model=User,
                               full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="081389136746434")
        temp_acc.photo_profile = mock_image_field()
        temp_acc.full_clean()
        temp_acc.save()
        temp_acc.delete()


    def test_phone_number_7(self) -> None:
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", user_model=User,
                               full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="081389136")
        temp_acc.photo_profile = mock_image_field()
        temp_acc.full_clean()
        temp_acc.save()
        temp_acc.delete()


class UserAccountTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", user_model=User,
                               full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="08128845191")
        temp_acc.photo_profile = mock_image_field()
        temp_acc.save()
        self.id = temp_acc.id


    def initial_test(self):
        temp = UserAccount.objects.filter(id=self.id).first()
        self.assertIsNot(temp, None)
        self.assertFalse(temp.is_investor)
        self.assertFalse(hasattr(temp, 'investoraccount'))
        self.assertFalse(temp.is_entrepreneur)
        self.assertFalse(hasattr(temp, 'entrepreneuraccount'))


    def investor_test_false(self, temp:UserAccount):
        temp.is_investor = False
        self.assertFalse(temp.is_investor)
        self.assertTrue(
            not hasattr(temp, 'investoraccount') or temp.investoraccount is None
        )
        self.assertEqual(InvestorAccount.objects.all().count(), 0)


    def investor_test_true(self, temp:UserAccount):
        temp.is_investor = True
        self.assertTrue(temp.is_investor)
        ttemp = temp.investoraccount
        self.assertIsNotNone(temp.investoraccount)
        self.assertEqual(InvestorAccount.objects.all().count(), 1)


    def test_investor(self):
        self.initial_test()
        temp = UserAccount.objects.filter(id=self.id).first()

        for i in range(5):
            self.investor_test_false(temp)
            self.investor_test_true(temp)


    def entrepreneur_test_false(self, temp:UserAccount):
        temp.is_entrepreneur = False
        self.assertFalse(temp.is_entrepreneur)
        self.assertTrue(
            not hasattr(temp, 'entrepreneuraccount') or temp.entrepreneuraccount is None
        )
        self.assertEqual(EntrepreneurAccount.objects.all().count(), 0)


    def entrepreneur_test_true(self, temp:UserAccount):
        temp.is_entrepreneur = True
        self.assertTrue(temp.is_entrepreneur)
        ttemp = temp.entrepreneuraccount
        self.assertIsNotNone(temp.entrepreneuraccount)
        self.assertEqual(EntrepreneurAccount.objects.all().count(), 1)


    def test_entrepreneur(self):
        self.initial_test()
        temp = UserAccount.objects.filter(id=self.id).first()

        for i in range(5):
            self.entrepreneur_test_false(temp)
            self.entrepreneur_test_true(temp)


    def test_both_investor_entrepreneur(self):
        self.initial_test()
        temp = UserAccount.objects.filter(id=self.id).first()

        def f_00():
            self.entrepreneur_test_false(temp)
            self.investor_test_false(temp)

        def f_01():
            self.entrepreneur_test_false(temp)
            self.investor_test_true(temp)

        def f_10():
            self.entrepreneur_test_true(temp)
            self.investor_test_false(temp)

        def f_11():
            self.entrepreneur_test_true(temp)
            self.investor_test_true(temp)

        functions = [f_00, f_01, f_10, f_11]
        permutate = permutations(functions)

        for perm in permutate:
            for func in perm:
                func()
        f_00()  # reset its state


class EntrepreneurInvestorAccountTest(TestCase):
    def test_run(self) -> None:
        self.client = Client()
        temp_acc = UserAccount(username="shjkrk", email="shjkrk@localhost", user_model=User,
                               full_name="sujhek kheruk",
                               deskripsi_diri="Aku tidak punya deskripsi", alamat="apakah aku punya rumah",
                               phone_number="08128845191")
        temp_acc.photo_profile = mock_image_field()
        temp_acc.save()
        self.id = temp_acc.id

        temp_inv = InvestorAccount(account=temp_acc)
        temp_inv.save()

        temp_entr = EntrepreneurAccount(account=temp_acc)
        temp_entr.save()

        self.assertEqual(temp_entr.account.id, temp_acc.id)
        self.assertEqual(temp_inv.account.id, temp_acc.id)
