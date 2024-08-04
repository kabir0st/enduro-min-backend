import hashlib
import hmac
import json

import requests
from core.settings.environments import (FONEPAY_KEY, FONEPAY_MERCHANT_CODE,
                                        FONEPAY_PASSWORD, FONEPAY_USERNAME)
from core.tasks import write_log_file


def generate_fonepay_qr(fonepay_obj):
    if len(FONEPAY_USERNAME) < 2 or len(FONEPAY_PASSWORD) < 2 or len(
            FONEPAY_MERCHANT_CODE) < 2:
        raise Exception('Fonepay creds are not set in setting.')
    url = ('https://merchantapi.fonepay.com/api/merchant/'
           'merchantDetailsForThirdParty/thirdPartyDynamicQrDownload')
    data = {
        'amount': float(fonepay_obj.amount),
        'remarks1': f"{fonepay_obj.invoice_number}",
        'remarks2': str("Himalayan Trail Running Pvt. Ltd."),
        'prn': f'{fonepay_obj.invoice_number} Payment {fonepay_obj.id}',
        'merchantCode': int(FONEPAY_MERCHANT_CODE),
        'dataValidation': "",
        'username': FONEPAY_USERNAME,
        'password': FONEPAY_PASSWORD
    }
    to_be_hash = (f'{data["amount"]},{data["prn"]},{data["merchantCode"]},'
                  f'{data["remarks1"]},{data["remarks2"]}')
    key = FONEPAY_KEY
    byte_key = bytes(key, 'UTF-8')
    hashed = hmac.new(byte_key, to_be_hash.encode(), hashlib.sha256)
    data['dataValidation'] = str(hashed.hexdigest())
    res = requests.post(url=url, json=data)
    res = res.json()
    if res['success']:
        fonepay_obj.qr_status = 'requested'
        fonepay_obj.last_response_from_fonepay = json.dumps(res)
        fonepay_obj.save()
        res['fonepay_payment_id'] = fonepay_obj.id
        return (res)
    else:
        fonepay_obj.qr_status = 'failed'
        fonepay_obj.last_response_from_fonepay = str(res.text)
        fonepay_obj.save()
        write_log_file('payments/fonepay/', f"{fonepay_obj.id}: {res}", True)
        return {'status': False, 'msg': res.text}


def verify_qr(fonepay_obj):
    if len(FONEPAY_USERNAME) < 2 or len(FONEPAY_PASSWORD) < 2 or len(
            FONEPAY_MERCHANT_CODE) < 2:
        raise Exception('Fonepay creds are not set in setting.')
    url = ('https://merchantapi.fonepay.com/api/merchant/'
           'merchantDetailsForThirdParty/thirdPartyDynamicQrGetStatus')
    data = {
        'prn': f'{fonepay_obj.invoice_number} Payment {fonepay_obj.id}',
        'merchantCode': int(FONEPAY_MERCHANT_CODE),
        'dataValidation': "",
        'username': FONEPAY_USERNAME,
        'password': FONEPAY_PASSWORD
    }
    to_be_hash = f'{data["prn"]},{data["merchantCode"]}'
    key = FONEPAY_KEY
    byte_key = bytes(key, 'UTF-8')
    hashed = hmac.new(byte_key, to_be_hash.encode(), hashlib.sha256)
    data['dataValidation'] = str(hashed.hexdigest())
    res = requests.post(url=url, json=data)
    res = res.json()
    if res['paymentStatus'] == "success":
        fonepay_obj.is_verified_from_server = True
        fonepay_obj.trace_id = res['fonepayTraceId']
        fonepay_obj.last_response_from_fonepay = json.dumps(res)
        fonepay_obj.save()
        res['status'] = True
        return res
    else:
        write_log_file('payments/fonepay/', f"{fonepay_obj.id}: {res.text}",
                       True)
        return {'status': False, 'msg': res.text}
