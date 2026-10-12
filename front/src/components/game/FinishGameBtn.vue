<script setup lang="ts">
import type { Link4 } from '../../ts/game';


const props = defineProps<{
    game: Link4
}>()

const emit = defineEmits(['finishGame'])
const btnClick = () => {
    emit("finishGame")
}
</script>

<template>
    <button class="game_finish" @click="btnClick" v-show="props.game.gameData.value?.gameState == 'gameset'">finish the
        game</button>
</template>