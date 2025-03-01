from .models import Page, PageSection
from utilities.logging import SystemLogger
from django.urls import reverse

logger = SystemLogger('scenes', __name__)


def delete_page(page_id):
    try:
        page_qs = Page.objects.get(id=int(page_id))
        page_qs.delete()
        return {'type': 'page_deleted', 'msg_type': 'success', 'message': 'Scene has been deleted'}
    except Exception as error:
        logger.log('delete_page','Error deleting Page', str(error), 'ERROR')
        return {'type': 'page_deleted', 'msg_type': 'error', 'message': 'Error deleting page. ' + str(error)}
    

def delete_section(section_id):
    try:
        section_qs = PageSection.objects.get(id=int(section_id))
        page_id = section_qs.page.id
        return_url = reverse('tiles:detail', kwargs={'page_id': page_id})
        section_qs.delete()
        return {'type': 'section_deleted', 'msg_type': 'success', 'message': 'Section has been deleted', 'return_url': return_url}
    except Exception as error:
        logger.log('delete_section','Error deleting Section', str(error), 'ERROR')
        return {'type': 'section_deleted', 'msg_type': 'error', 'message': 'Error deleting section. ' + str(error)}