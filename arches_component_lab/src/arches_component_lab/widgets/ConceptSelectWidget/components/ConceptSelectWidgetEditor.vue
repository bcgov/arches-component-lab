<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';

import { useGettext } from 'vue3-gettext';
import { FormField } from '@primevue/forms';

import Message from 'primevue/message';
import TreeSelect from 'primevue/treeselect';

import { fetchConcepts } from '@/arches_component_lab/widgets/api.ts';

import type { MultiSelectFilterEvent } from 'primevue/multiselect';
import type { FormFieldResolverOptions } from '@primevue/forms';
import type { VirtualScrollerLazyEvent } from 'primevue/virtualscroller';

import type {
    CollectionItem,
} from '@/arches_component_lab/widgets/types.ts';

const props = defineProps<{
    initialValue: typeof CollectionItem | null | undefined;
    graphSlug: string;
    nodeAlias: string;
}>();

const { $gettext } = useGettext();

const itemSize = 36; // in future iteration this should be declared in the CardXNodeXWidget config

const options = ref<CollectionItem[]>([]);
const isLoading = ref(false);
const conceptsPage = ref(0);
const conceptsTotalCount = ref(0);
const fetchError = ref<string | null>(null);

const conceptsCurrentCount = computed(() => options.value.length);

onMounted(async () => {
    await getOptions(1);
});

function clearOptions() {
    options.value = props.initialValue || null;
}

function onFilter(event: MultiSelectFilterEvent) {
    clearOptions();
    getOptions(1, event.value);
}

async function getOptions(page: number, filterTerm?: string) {
    try {
        isLoading.value = true;

        const conceptData = await fetchConcepts(
            props.graphSlug,
            props.nodeAlias,
        );


        // We're not paging yet
        // if (resourceData.current_page == 1) {
            options.value = conceptData.results;
        // } else {
        //     options.value = [...options.value, ...references];
        // }


        // Not paging yet
        conceptsPage.value = 1;
        conceptsTotalCount.value = 1;
        // resourceResultsPage.value = resourceData.current_page;
        conceptsTotalCount.value = conceptData.total_results;
    } catch (error) {
        fetchError.value = (error as Error).message;
    } finally {
        isLoading.value = false;
    }
}

async function onLazyLoadResources(event?: VirtualScrollerLazyEvent) {
    if (isLoading.value) {
        return;
    }

    if (
        // if we have already fetched all the resources
        conceptsTotalCount.value > 0 &&
        conceptsCurrentCount.value >= conceptsTotalCount.value
    ) {
        return;
    }

    if (
        // if the user has NOT scrolled to the end of the list
        event &&
        event.last < conceptsCurrentCount.value - 1
    ) {
        return;
    }

    if (
        // if the dropdown is opened and we already have data
        !event &&
        conceptsCurrentCount.value > 0
    ) {
        return;
    }

    await getOptions((conceptsPage.value || 0) + 1);
}

function getOption(value: string): CollectionItem | undefined {
    const option = options.value.find((option) => option.id == value);
    return option;
}

function resolver(e: FormFieldResolverOptions) {
    validate(e);

    let value = e.value;

    if (!Array.isArray(value)) {
        value = [value];
    }

    return {
        values: {
            [props.nodeAlias]: options.value.filter((option) => {
                return value?.includes(option.id);
            }),
        },
    };
}

function validate(e: FormFieldResolverOptions) {
    console.log('validate', e);
}
</script>

<template>
    <Message
        v-if="fetchError"
        severity="error"
    >
        {{ fetchError }}
    </Message>
    <FormField
        v-else
        v-slot="$field"
        :name="props.nodeAlias"
        :initial-value="
            props.initialValue?.id
        "
        :resolver="resolver"
    >
        <TreeSelect
            option-label="text"
            option-value="id"
            :filter="true"
            :filter-placeholder="$gettext('Filter Concepts')"
            :fluid="true"
            :loading="isLoading"
            :options="options"
            :placeholder="$gettext('Select Concept')"
            :reset-filter-on-hide="true"
            :virtual-scroller-options="{
                itemSize: itemSize,
                lazy: true,
                loading: isLoading,
                onLazyLoad: onLazyLoadResources,
            }"
            @filter="onFilter"
            @before-show="getOptions(1)"
        >
        </TreeSelect>
        <Message
            v-for="error in $field.errors"
            :key="error.message"
            severity="error"
            size="small"
        >
            {{ error.message }}
        </Message>
    </FormField>
</template>

<style scoped>
</style>
