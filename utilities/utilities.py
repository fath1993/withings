import jdatetime


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_json(method, request, result, message):
    body = {
        'method': method,
        'request': request,
        'result': result,
        'message': message
    }
    return body


def date_string_to_date_format(date_in_string):
    try:
        date_list = str(date_in_string).replace('/', ' ').replace(':', ' ').split()
        date_shamsi = jdatetime.datetime(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]),
                                         hour=int(date_list[3]), minute=int(date_list[4]))
        return date_shamsi
    except Exception as e:
        print(str(e))
        return None