from .models import Page
from utilities.logging import SystemLogger
logger = SystemLogger('scenes', __name__)


def delete_page(page_id):
    try:
        page_qs = Page.objects.get(id=int(page_id))
        page_qs.delete()
        return {'type': 'page_deleted', 'msg_type': 'success', 'message': 'Scene has been deleted'}
    except Exception as error:
        logger.log('delete_page','Error deleting Page', str(error), 'ERROR')
        return {'type': 'page_deleted', 'msg_type': 'error', 'message': 'Error deleting page. ' + str(error)}