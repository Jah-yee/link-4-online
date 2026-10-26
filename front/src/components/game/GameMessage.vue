<script setup lang="ts">
import { computed, nextTick, onMounted, type Ref } from 'vue';
import type { Link4 } from '../../ts/game';


const props = defineProps<{
    gameData: Ref<Link4.GameData | null>
}>()

const setMessage = (gameData: Link4.GameData): string => {
    if (gameData.gameState == "gameset") {
        if (gameData.winningLine.length == 0) return "引き分け";
        const startPosition = gameData.winningLine[0].startPosition
        const winPlayer = gameData.board[startPosition[0]][startPosition[1]]
        if (winPlayer == gameData.playerNum) {
            return "you win"
        } else {
            return "you loss"
        }
    } else {
        if (gameData?.yourTurn) {
            return "your turn"
        } else {
            return "opponent turn"
        }
    }
}

let message = computed(() => {
    if (props.gameData.value) {
        return setMessage(props.gameData.value)
    }
})

onMounted(() => {
    nextTick()
    if (props.gameData.value) {
        setMessage(props.gameData.value)
    }
})



</script>

<template>
    <p class="game_message">{{ message }}</p>
</template>