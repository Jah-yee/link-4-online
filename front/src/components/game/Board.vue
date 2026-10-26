<script setup lang="ts">
import { computed, type Ref } from 'vue';
import { Link4 } from '../../ts/game/';
import BoardSell from './BoardSell.vue';

const props = defineProps<{
    gameData: Ref<Link4.GameData | null>
}>()


const updateEmphasizeBoard = (gameData: Ref<Link4.GameData | null>): boolean[][] => {
    const blankBoard: boolean[][] = [
        new Array(7).fill(false),
        new Array(7).fill(false),
        new Array(7).fill(false),
        new Array(7).fill(false),
        new Array(7).fill(false),
        new Array(7).fill(false),
    ]
    let emphasizeBoard: boolean[][] = structuredClone(blankBoard)
    console.log("updateEmphasizeBoard", emphasizeBoard, gameData.value?.winningLine)
    if (!gameData.value) return blankBoard;
    if (!(gameData.value.winningLine.length > 0)) return blankBoard;
    console.log("updateEmphasize winning_line", gameData.value.winningLine)
    gameData.value.winningLine.forEach((winPattern: Link4.WinPattern) => {
        const currentWinPattern: Link4.WinPattern = JSON.parse(JSON.stringify(winPattern))
        console.log("winning_line forEach", currentWinPattern, currentWinPattern.startPosition)
        let targetEmphasizeSell: [number, number][] = []
        for (let i = 0; i < currentWinPattern.len; i++) {
            let targetPosition: [number, number] = structuredClone(currentWinPattern.startPosition);
            targetPosition[0] = currentWinPattern.startPosition[0] + (currentWinPattern.direction[0] * i);
            targetPosition[1] = currentWinPattern.startPosition[1] + (currentWinPattern.direction[1] * i);
            targetEmphasizeSell.push(targetPosition)
        }
        targetEmphasizeSell.forEach((position) => {
            emphasizeBoard[position[0]][position[1]] = true
        })
    })
    return emphasizeBoard
}

const emphasizeBoard = computed(() => updateEmphasizeBoard(props.gameData))

</script>

<template>
    <div class="game_board">
        <template v-for=",rowIndex in gameData.value?.board">
            <BoardSell v-for="sell, colIndex in gameData.value?.board[Number(rowIndex)]" :key="colIndex" :x="colIndex"
                :y="rowIndex" :data-player="sell" :data-emphasize="emphasizeBoard[Number(rowIndex)][colIndex]" />
        </template>
    </div>
</template>
