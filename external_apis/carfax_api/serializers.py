from external_apis.carfax_api.types import Carfax
from aiogram.utils.i18n import gettext as _

def serialize_carfax(carfax: Carfax):
    return _('🦊 CarFax:\n'
             '🚘 VIN: {vin}\n'
             '📊 Status: {status}\n').format(vin=carfax.vin,
                                            status= 'Paid' if carfax.is_paid else 'Unpaid')
