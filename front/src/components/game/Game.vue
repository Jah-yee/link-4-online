<script setup lang="ts">
import Board from './Board.vue';
import Selector from './Selector.vue';
import { Link4 } from '../../ts/game/index.ts';
import GameMessage from './GameMessage.vue';
import FinishGameBtn from './FinishGameBtn.vue';

const props = defineProps<{
    game: Link4
}>()


const backRoom = () => {
    props.game.finishGame.value = {}
}

</script>

<template>
    <div class="game">
        <FinishGameBtn @finishGame="backRoom" :game="game" />
        <Selector :game="game" />
        <GameMessage :gameData="game.gameData" />
        <Board :gameData="game.gameData" />
    </div>
</template>
