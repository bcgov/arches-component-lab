from django.views import View
from arches.app.models.models import Node
from arches.app.models.concept import Concept
from arches.app.utils.response import JSONResponse
from arches.app.utils.betterJSONSerializer import JSONDeserializer
from arches import VERSION as arches_version
from django.db.models import Q


class ConceptsView(View):
    def get(self, request, graph, node_alias):
        node_filter = Q(
            alias=node_alias,
            graph__slug=graph,
            graph__publication__isnull=False,
        )
        if arches_version >= (8, 0):
            node_filter = node_filter & Q(graph__is_active=True)

        node = Node.objects.get(node_filter)

        config = JSONDeserializer().deserialize(node.config.value)
        concept_id = config["rdmCollection"]
        results = Concept().get_e55_domain(concept_id)

        def set_results_keys(results):
            results = [
                result | {"key": result["id"], "label": result["text"]}
                for result in results
            ]
            for result in results:
                if len(result["children"]) > 0:
                    result["children"] = set_results_keys(result["children"])
            return results

        results = set_results_keys(results)

        def count_results(results):
            return len(results) + sum(
                list(map(lambda result: count_results(result["children"]), results))
            )

        total_count = count_results(results)
        data = results

        return JSONResponse(
            {"results": data, "more": False, "total_results": total_count}
        )
