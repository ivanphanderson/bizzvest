from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import dateformat, timezone

from halaman_toko.authentication_and_authorization import get_logged_in_user_account, get_login_url
from halaman_toko.forms.halaman_toko_add_form import CompanyAddForm
from models.models import Company


class DoesProblemExist():
    def __init__(self):
        pass


class FormErrors():
    def __init__(self, errors):
        dictionary = dict(errors)
        temp = ['proposal',
                'nama_merek',
                'nama_perusahaan',
                'alamat',
                'deskripsi',
                'jumlah_lembar',
                'nilai_lembar_saham',
                'kode_saham',
                'dividen',
                'end_date',
                ]

        self.does_problem_exist = DoesProblemExist()

        for attr_name in temp:
            setattr(self, attr_name, dictionary.get(attr_name, ""))
            setattr(self.does_problem_exist, attr_name, "problem" if (attr_name in dictionary) else "no-problem")


"""
string_character_choices = string.digits + string.ascii_letters
class TemporaryFiles:
    global_dict = {}
    global_queue = deque()

    def __init__(self, data, timeout_in_second=12):
        while (id:=''.join(random.choices(string_character_choices, k=48))) in self.__class__.global_dict:
            pass

        self.data = data
        self.id = id
        self.timeout = datetime.datetime.now() + datetime.timedelta(0, timeout_in_second)
        self.__class__.global_dict[self.id] = self
        self.__class__.global_queue.append(self)

    @classmethod
    def get(cls, key, default=Exception):
        ret = cls.global_dict.get(key, default)
        if isinstance(ret, Exception):
            raise ret("key error")
        return ret


    @classmethod
    def delete_outdated_files(cls):
        if len(cls.global_queue) == 0:
            assert len(cls.global_dict) == 0
            return

        temp = cls.global_queue[-1]
        while (temp.timeout < datetime.datetime.now()):
            if temp.id in cls.global_dict:
                del cls.global_dict[temp.id]
                Company.objects.filter(id=temp.data).delete()
            cls.global_queue.pop()

            if not cls.global_queue:  # if queue is empty, then dict must be empty. Tapi ga berlaku sebaliknya
                assert len(cls.global_dict) == 0
                break

            temp = cls.global_queue[-1]

    @classmethod
    def mark_as_permanent(cls, tempfile_id):
        del cls.global_dict[tempfile_id]

    @classmethod
    def reset_counter(cls, prev_id):
        ret = cls(cls.global_dict[prev_id].data)
        del cls.global_dict[prev_id]
        return ret
"""



def add_toko(req:WSGIRequest):
    # TemporaryFiles.delete_outdated_files()

    validation_state = '1'
    show_invalid_modal = False
    additional_problems = []

    if (get_logged_in_user_account() is None):
        return HttpResponseRedirect(get_login_url())


    if (req.method == 'POST'):

        form = CompanyAddForm(req.POST)
        form.instance.start_date = dateformat.format(timezone.now(), 'Y-m-d')

        temp = get_logged_in_user_account().entrepreneuraccount
        form.instance.pemilik_usaha = temp

        # if ('pemilik_usaha' in req.POST):
        #     return HttpResponse("Illegal attribute: 'pemilik_usaha' ", status=400)

        if ('is_validate_only' not in req.POST):
            additional_problems.append("invalid request error: no 'is_validate_only' property")
            show_invalid_modal = True
        else:
            if (form.is_valid()):
                if (req.POST.get('is_validate_only', '1') == '0'):
                    saved_obj:Company = form.save()

                    redirect_url_target = reverse('halaman_toko:halaman_toko')
                    return HttpResponseRedirect(f"{redirect_url_target}?id={saved_obj.id}")
                elif req.POST['is_validate_only'] == '1':
                    validation_state = '0'
            else:
                show_invalid_modal = True
    else:
        form = CompanyAddForm(None)

    print(dict(form.errors))

    return render(req, "add_toko.html", {
        'form':form,
        'validation_state': validation_state,
        'additional_problems': additional_problems,
        'show_invalid_modal': show_invalid_modal,
        'errors_field_verbose_name': [Company._meta.get_field(field_name).verbose_name
                                      for field_name, errors in form.errors.items()],
        'errors': FormErrors(form.errors),
    })



