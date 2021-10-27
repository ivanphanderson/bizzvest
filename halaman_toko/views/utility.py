from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse

from models_app.models import Company


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


def validate_toko_id_by_GET_req(req:WSGIRequest):
    "returns (True, company_obj_query) if valid, or (False, http response object) if is not valid"
    if (req.GET.get("id") is None):
        ret = HttpResponseRedirect("")
        ret["Location"] += "?id=1"
        return (False, ret)

    return validate_toko_id(req.GET.get("id"))


def validate_toko_id(id_str:str):
    "returns (True, company_obj_query) if valid, or (False, http response object) if is not valid"
    company_id_str:str = id_str
    if (not company_id_str.isnumeric()):
        ret = HttpResponse("Sorry, the id you're trying to reach is invalid " + go_to_prev_history_javascript(3000))
        ret.status_code = 400
        return (False, ret)

    company_id:int = int(company_id_str)
    company_obj_query = Company.objects.filter(id=company_id)
    if (not company_obj_query.exists()):
        ret = HttpResponse("Sorry, the id you're trying to reach does not exist " + go_to_prev_history_javascript(3000))
        ret.status_code = 400
        return (False, ret)
    return (True, company_obj_query)