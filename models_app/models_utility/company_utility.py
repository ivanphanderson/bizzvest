from models_app.models import Company


def recalculate_img_index(company_obj:Company, zero_based_index_update_start_pos:int=0):
    """mengupdate semua CompanyPhoto.img_index sesuai yang seharusnya
    CompanyPhoto akan diurutkan berdasarkan img_index saat ini. Kemudian seluruh CompanyPhoto yang berada pada
    index >= zero_based_index_update_start_pos (zero-based index), akan diupdate img-index nya.
    """

    company_photos = list(company_obj.companyphoto_set.all().order_by('img_index'))
    temp = zero_based_index_update_start_pos + 1  # karena img_index bukan zero based, melainkan one-based

    for i in range(zero_based_index_update_start_pos, len(company_photos)):
        company_photos[i].img_index = temp
        company_photos[i].save()
        temp += 1

    return company_photos


def recalculate_img_index_from_list(list_of_company_photo, zero_based_index_update_start_pos:int=0):
    "mirip seperti recalculate_img_index, tapi kini parameternya menerima list of CompanyPhoto"

    company_photos = list_of_company_photo
    temp = zero_based_index_update_start_pos + 1  # karena img_index bukan zero based, melainkan one-based

    for i in range(zero_based_index_update_start_pos, len(company_photos)):
        company_photos[i].img_index = temp
        company_photos[i].save()
        temp += 1

    return company_photos