import logging

from cryptography import x509
from cryptography.x509.oid import NameOID


def _get_cert_cn(pem_data):
    """ 
    Return the CN of the certificate given in pem_data. 
    Internal usage by check_hostname
    """

    cert = x509.load_pem_x509_certificate(pem_data)
    cn = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    return cn


def check_hostname(pemchain, claims):
    """ 
    Verify that the system hostname matches the signing certificate's CN.
    Return true if the name matches. False otherwise.
    Exception on error. 
    """

    cert_cn = _get_cert_cn(pemchain[0])
    hostname = claims["systeminfo"]["hostname"]
    return cert_cn == hostname


def check_request_param(expected_value, claims, param):
    """ 
    Verify that the request parameter is present in the signed response.
    expected_value: the value we put in the request.
    claims: dictionary with the claims
    param: the name of the parameter in the request.
    Return true or false. Exception on error. 
    """
    signed_param = claims["requestdata"][param]
    return signed_param == expected_value

