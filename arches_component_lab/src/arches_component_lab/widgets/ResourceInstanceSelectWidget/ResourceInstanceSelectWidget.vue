<script setup lang="ts">

import ResourceInstanceSelectWidgetEditor from '@/arches_component_lab/widgets/ResourceInstanceSelectWidget/components/ResourceInstanceSelectWidgetEditor.vue';
import ResourceInstanceSelectWidgetViewer from '@/arches_component_lab/widgets/ResourceInstanceSelectWidget/components/ResourceInstanceSelectWidgetViewer.vue';
import WidgetContainer from '@/arches_component_lab/widgets/WidgetContainer/WidgetContainer.vue'

import type {
    ResourceInstanceReference,
    WidgetMode,
} from '@/arches_component_lab/widgets/types.ts';

import { ref } from 'vue';
import type {  Ref } from 'vue';

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

const currentValue: Ref<ResourceInstanceReference> = ref();
function getCurrentValue()
{
    return currentValue.value;
}
defineExpose({getCurrentValue})
</script>

<template>
    <WidgetContainer
        :mode=props.mode
        :initial-value=props.initialValue
        :node-alias=props.nodeAlias
        :graph-slug=props.graphSlug
        :show-label=props.showLabel
    >
        <template v-slot:editWidget>
            <ResourceInstanceSelectWidgetEditor
                v-model="currentValue"
                :initial-value="initialValue"
                :node-alias="nodeAlias"
                :graph-slug="graphSlug"
            />
        </template>
        <template v-slot:viewWidget>
            <ResourceInstanceSelectWidgetViewer
                v-model="currentValue"
                :value="initialValue" />
        </template>
    </WidgetContainer>
</template>
