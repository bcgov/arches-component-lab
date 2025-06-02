import arches from "arches";

import type { ResourceInstanceReference, CollectionItem } from "@/arches_component_lab/widgets/types.ts";

export const fetchWidgetData = async (graphSlug: string, nodeAlias: string) => {
    const response = await fetch(
        arches.urls.api_widget_data(graphSlug, nodeAlias),
    );

    try {
        const parsed = await response.json();
        if (response.ok) {
            return parsed;
        }
        throw new Error(parsed.message);
    } catch (error) {
        throw new Error((error as Error).message || response.statusText);
    }
};

export const fetchNodeData = async (graphSlug: string, nodeAlias: string) => {
    const response = await fetch(
        arches.urls.api_node_data(graphSlug, nodeAlias),
    );

    try {
        const parsed = await response.json();
        if (response.ok) {
            return parsed;
        }
        throw new Error(parsed.message);
    } catch (error) {
        throw new Error((error as Error).message || response.statusText);
    }
};

export const fetchLists = async (
    nodeAliases: string[] | undefined = undefined,
) => {
    const params = new URLSearchParams();
    nodeAliases?.forEach((alias) => params.append("node_alias", alias));
    const response = await fetch(`${arches.urls.controlled_lists}?${params}`);
    try {
        const parsed = await response.json();
        if (response.ok) {
            return parsed;
        }
        throw new Error(parsed.message);
    } catch (error) {
        throw new Error((error as Error).message || response.statusText);
    }
};

export const fetchRelatableResources = async (
    graphSlug: string,
    nodeAlias: string,
    page: number,
    filterTerm?: string,
    initialValues?: ResourceInstanceReference[] | null | undefined,
) => {
    const params = new URLSearchParams();

    params.append("page", page.toString());
    if (filterTerm) {
        params.append("filter_term", filterTerm);
    }
    initialValues?.forEach((initialValue) =>
        params.append("initialValue", initialValue.resourceId),
    );
    const response = await fetch(
        `${arches.urls.api_relatable_resources(
            graphSlug,
            nodeAlias,
        )}?${params}`,
    );

    const parsed = await response.json();
    if (!response.ok) throw new Error(parsed.message || response.statusText);
    return parsed;
};

/**
 * Get the hierarchy of collection items for the give graph slug and node alias.
 *
 * @todo - Implement for v8, controlled list app
 * @todo - Currently not paging results
 * @param graphSlug
 * @param nodeAlias
 * @param page
 * @param filterTerm
 * @param initialValues
 */
export const fetchConcepts = async (
    graphSlug: string,
    nodeAlias: string,
    page: number,
    filterTerm?: string,
    initialValues?: CollectionItem[] | null | undefined,
) => {
    const params = new URLSearchParams();

    // params.append("page", page.toString());
    if (filterTerm) {
        params.append("filter_term", filterTerm);
    }
    const response = await fetch(
        `${arches.urls.api_concepts(
            graphSlug,
            nodeAlias,
        )}?${params}`,
    );

    const parsed = await response.json();
    if (!response.ok) throw new Error(parsed.message || response.statusText);
    return parsed;
};