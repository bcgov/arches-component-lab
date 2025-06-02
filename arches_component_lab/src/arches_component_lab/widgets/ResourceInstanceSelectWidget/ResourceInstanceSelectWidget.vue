<script setup lang="ts">

import ResourceInstanceSelectWidgetEditor from '@/arches_component_lab/widgets/ResourceInstanceSelectWidget/components/ResourceInstanceSelectWidgetEditor.vue';
import ResourceInstanceSelectWidgetViewer from '@/arches_component_lab/widgets/ResourceInstanceSelectWidget/components/ResourceInstanceSelectWidgetViewer.vue';
import WidgetContainer from '@/arches_component_lab/widgets/WidgetContainer/WidgetContainer.vue'

import type {
    ResourceInstanceReference,
    WidgetMode,
} from '@/arches_component_lab/widgets/types.ts';

const props = withDefaults(
    defineProps<{
        mode: typeof WidgetMode;
        initialValue: ResourceInstanceReference | null | undefined;
        nodeAlias: string;
        graphSlug: string;
        showLabel?: boolean;
    }>(),
    {
        showLabel: true,
    },
);

</script>

<template>
            <ResourceInstanceSelectWidgetEditor
                :initial-value="initialValue"
            />
        </template>
</template>
