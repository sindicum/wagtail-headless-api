from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from .views import CustomPagesAPIViewSet, TagsAPIViewSet


api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('pages', CustomPagesAPIViewSet)
api_router.register_endpoint('tags', TagsAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)

 