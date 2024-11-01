from abc import ABC, abstractmethod

class CatalogEnricher(ABC):

    @abstractmethod
    def enrich_from_image(self, image_url, additional_context):
        pass