from contract_api.domain.models.service import Service
from contract_api.domain.models.service_metadata import ServiceMetadata


class ServiceFactory:

    @staticmethod
    def convert_service_db_model_to_entity_model(service_db):
        if not service_db:
            return None
        return Service(
            org_id=service_db.org_id,
            service_id=service_db.service_id,
            service_path=service_db.service_path,
            ipfs_hash=service_db.ipfs_hash,
            is_curated=service_db.is_curated,
            service_email=service_db.service_email,
            service_metadata=ServiceFactory.convert_service_metadata_db_model_to_entity_model(
                service_db.service_metadata)
        )

    @staticmethod
    def convert_service_metadata_db_model_to_entity_model(service_metadata_db):
        if not service_metadata_db:
            return None
        return ServiceMetadata(
            service_row_id=service_metadata_db.service_row_id,
            org_id=service_metadata_db.org_id,
            service_id=service_metadata_db.service_id,
            display_name=service_metadata_db.display_name,
            description=service_metadata_db.description,
            short_description=service_metadata_db.short_description,
            demo_component_available=service_metadata_db.demo_component_available,
            url=service_metadata_db.url,
            json=service_metadata_db.json,
            model_ipfs_hash=service_metadata_db.model_ipfs_hash,
            encoding=service_metadata_db.encoding,
            type=service_metadata_db.type,
            mpe_address=service_metadata_db.mpe_address,
            assets_url=service_metadata_db.assets_url,
            assets_hash=service_metadata_db.assets_hash,
            service_rating=service_metadata_db.service_rating,
            ranking=service_metadata_db.ranking,
            contributors=service_metadata_db.contributors
        )