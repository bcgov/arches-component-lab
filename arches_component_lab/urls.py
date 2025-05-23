from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from arches_component_lab.views.api.relatable_resources import RelatableResourcesView
from arches_component_lab.views.api.concepts import ConceptsView
from arches_component_lab.views.api.widgets import (
    WidgetDataView,
    NodeDataView,
)

urlpatterns = [
    path(
        "arches-component-lab/api/relatable-resources/<slug:graph>/<slug:node_alias>",
        RelatableResourcesView.as_view(),
        name="api-relatable-resources",
    ),
    path(
        "arches-component-lab/api/concepts/<slug:graph>/<slug:node_alias>",
        ConceptsView.as_view(),
        name="api-concepts",
    ),
    path(
        "arches-component-lab/api/widget-data/<slug:graph_slug>/<slug:node_alias>",
        WidgetDataView.as_view(),
        name="api-widget-data",
    ),
    path(
        "arches-component-lab/api/node-data/<slug:graph_slug>/<slug:node_alias>",
        NodeDataView.as_view(),
        name="api-node-data",
    ),
]

# Ensure Arches core urls are superseded by project-level urls
urlpatterns.append(path("", include("arches.urls")))

# Adds URL pattern to serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Only handle i18n routing in active project. This will still handle the routes provided by Arches core and Arches applications,
# but handling i18n routes in multiple places causes application errors.
if settings.ROOT_URLCONF == __name__:
    if settings.SHOW_LANGUAGE_SWITCH is True:
        urlpatterns = i18n_patterns(*urlpatterns)

    urlpatterns.append(path("i18n/", include("django.conf.urls.i18n")))
