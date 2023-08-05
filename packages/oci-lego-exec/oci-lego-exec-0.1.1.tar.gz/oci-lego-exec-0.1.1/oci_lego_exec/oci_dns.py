import logging

from oci import config
from oci.dns import DnsClient
from oci.dns.models import RecordDetails, UpdateRRSetDetails
from oci.exceptions import ServiceError
from os import path, environ

from oci_lego_exec.utils import zone_names, cleanup

LOG = logging.getLogger(name=__name__)


class OciDns:
    """
    Encapsulates all communication with the OCI API.
    """
    def __init__(self):
        self.client = self._get_oci_dns_client()

    def add_txt_record(self, record_name, record_content, ttl):
        zone_name = self._find_zone_name(record_name)
        cleaned_record_name = cleanup(record_name)
        try:
            LOG.debug('Update TXT record with data: %s', record_content)
            update_rr_set_details = UpdateRRSetDetails(
                items=[
                    RecordDetails(
                        domain=cleaned_record_name,
                        rdata=record_content,
                        rtype='TXT',
                        ttl=ttl
                    )
                ]
            )
            self.client.update_rr_set(zone_name_or_id=zone_name,
                                      domain=cleaned_record_name, rtype='TXT',
                                      update_rr_set_details=update_rr_set_details)
        except ServiceError as e:
            LOG.warning('Error updating TXT record %s using the OCI API: %s', record_name, e)
            raise Exception(e)

    def del_txt_record(self, record_name):
        zone_name = self._find_zone_name(record_name)
        cleaned_record_name = cleanup(record_name)
        rr_set = self.client.get_rr_set(zone_name_or_id=zone_name, domain=cleaned_record_name, rtype='TXT')

        try:
            if rr_set.data.items:
                LOG.debug('Removing TXT record with data: %s', rr_set.data.items)
                self.client.delete_rr_set(zone_name_or_id=zone_name, domain=cleaned_record_name, rtype='TXT')
        except Exception as e:
            LOG.warning('Error deleting TXT record %s using the OCI API: %s', rr_set.data.items, e)

    @staticmethod
    def _get_oci_dns_client():
        oci_config_file = path.join(path.expanduser("~"), ".oci", "config")
        oci_config_profile = 'DEFAULT'

        if "OCI_CONFIG_PROFILE" in environ:
            oci_config_profile = environ.get("OCI_CONFIG_PROFILE")

        oci_config = config.from_file(file_location=oci_config_file, profile_name=oci_config_profile)

        return DnsClient(oci_config)

    def _find_zone_name(self, domain_name):
        domain_name_guesses = zone_names(domain_name)
        for domain in domain_name_guesses:
            try:
                self.client.get_zone(zone_name_or_id=domain)
                return domain
            except ServiceError as e:
                if e.status == 404:
                    pass

        raise ValueError('Cannot find zone for domain name {}'.format(domain_name))
