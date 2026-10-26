<script setup lang="ts">
import SelectorBtn from './SelectorBtn.vue';
import type { Link4 } from '../../ts/game/index.ts';

const props = defineProps<{
    game: Link4
}>()

const gamePut = (x: number) => {
    console.log("gamePut", x)
    props.game.lastPut.value = { x: x };
}
</script>

<template>
    <div class="game_selector">
        <ul>
            <li v-for=",index in new Array(7)" :key="index">
                <SelectorBtn :x="index" @put="gamePut" :data-player="game.gameData.value?.playerNum" />
            </li>
        </ul>
    </div>
</template>
