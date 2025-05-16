from arches.app.utils.betterJSONSerializer import JSONDeserializer, JSONSerializer
from django.views.generic import View

from arches import __version__ as arches_version
from arches.app.models import models
from arches.app.utils.response import JSONResponse
from arches.app.datatypes.datatypes import DataTypeFactory


class WidgetDataView(View):
    def get(self, request, graph_slug, node_alias):
        if arches_version < "8":
            card_x_node_x_widget = (
                models.CardXNodeXWidget.objects.filter(
                    node__graph__slug=graph_slug,
                    node__alias=node_alias,
                )
                .select_related("node")
                .get()
            )
        elif arches_version >= "8":
            card_x_node_x_widget = (
                models.CardXNodeXWidget.objects.filter(
                    node__graph__slug=graph_slug,
                    node__alias=node_alias,
                    node__source_identifier_id__isnull=True,
                )
                .select_related("node")
                .get()
            )

        card_x_node_x_widget_dict = JSONDeserializer().deserialize(
            JSONSerializer().serialize(card_x_node_x_widget)
        )

        datatype = DataTypeFactory().get_instance(card_x_node_x_widget.node.datatype)
        # When dropping support for v7.6, try/except can be removed
        try:
            card_x_node_x_widget_dict["config"]["defaultValue"] = (
                datatype.get_interchange_value(
                    card_x_node_x_widget_dict["config"].get("defaultValue", None)
                )
            )
        except AttributeError:
            # Handle the case where the datatype does not have a get_interchange_value method
            pass

        return JSONResponse(card_x_node_x_widget_dict)


class NodeDataView(View):
    def get(self, request, graph_slug, node_alias):
        node = (
            models.Node.objects.get(
                graph__slug=graph_slug,
                alias=node_alias,
                source_identifier_id__isnull=True,
            )
            if getattr(models.Node, "source_identifier_id", False)
            else models.Node.objects.get(
                graph__slug=graph_slug,
                alias=node_alias,
            )
        )

        return JSONResponse(node)
