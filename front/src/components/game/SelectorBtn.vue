<script setup lang="ts">

const props = defineProps<{
    x: number
}>()
const emit = defineEmits(['put'])
const btnClick = () => {
    emit("put", props.x)
}
</script>
<template>
    <button @click="btnClick">
    </button>
</template>