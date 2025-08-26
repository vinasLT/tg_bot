from aiogram.utils.i18n import gettext as _
from rpc_client.gen.python.carfax.v1 import carfax_pb2


def serialize_carfax(carfax: carfax_pb2.Carfax):
    return _('🦊 CarFax:\n'
             '🚘 VIN: {vin}\n'
             '📊 Status: {status}\n').format(vin=carfax.vin,
                                            status= 'Paid' if carfax.is_paid else 'Unpaid')
