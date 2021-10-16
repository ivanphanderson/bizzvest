from models.models.Company import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

# Create your views here.

def go_to_prev_history_javascript(time_in_ms):
    ret = """
    <script>
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        (
            async function (){
                await sleep( """ + str(time_in_ms) + """);
                window.history.go(-1);
            }
        )();
    </script>
    """
    return ret


def halaman_toko(req:WSGIRequest):
    if (req.GET.get("id") is None):
        ret = HttpResponseRedirect("")
        ret["Location"] += "?id=1"
        return ret

    company_id_str:str = req.GET.get("id")
    if (not company_id_str.isnumeric()):
        ret = HttpResponse("Sorry, the id you're trying to reach is invalid " + go_to_prev_history_javascript(3000))
        ret.status_code = 400
        return ret

    company_id:int = int(company_id_str)

    company_obj_query = Company.objects.filter(id=company_id)
    if (not company_obj_query.exists()):
        ret = HttpResponse("Sorry, the id you're trying to reach is not exist " + go_to_prev_history_javascript(3000))
        ret.status_code = 400
        return ret

    company_obj:Company = company_obj_query[0]


    return render(req, "halaman_toko.html", {
        'company' : company_obj,
        'company_photos': company_obj.companyphoto_set.all()
    })