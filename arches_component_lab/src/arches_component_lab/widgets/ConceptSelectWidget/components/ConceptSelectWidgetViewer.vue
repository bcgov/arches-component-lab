<script setup lang="ts">
import arches from 'arches';
import type { ConceptItem } from '@/arches_component_lab/widgets/types.ts';

const props = defineProps<{
    value?: typeof ConceptItem | null | undefined;
}>();
</script>
<template>
    <div
        :key="props.value.key"
    >
        <a
            :href="`${arches.urls.resource_editor}${props.value.key}`"
        >
            {{ props.value.label }}
        </a>
    </div>
</template>
