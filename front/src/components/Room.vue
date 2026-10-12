<script setup lang="ts">
import { useRoute } from 'vue-router';
import { qs } from '../ts/util';
import { Room } from '../ts/room';
import { computed, nextTick, onMounted, watch } from 'vue';
import Game from './game/Game.vue';
import { canJoinRoom } from '../ts/home.ts';
import { Link4 } from '../ts/game/index.ts';

const route = useRoute()
const room = new Room(Number(route.params.roomId));

const copyRoomId = () => {
    const sleep = async (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))
    const targetElementSelector = "#copyRoomIdMessage"
    navigator.clipboard.writeText(String(room.id))
        .then(async () => {
            console.log("succesfully copy room id ", room.id)
            const copyRoomIdMessage = qs(targetElementSelector)
            if (!copyRoomIdMessage) return;
            copyRoomIdMessage.innerText = "succesfully copy room id "
            await sleep(3000)
            copyRoomIdMessage.innerText = ""
        })
        .catch(async (e) => {
            console.error("faild copy room id", e)
            const copyRoomIdMessage = qs(targetElementSelector)
            if (!copyRoomIdMessage) return;
            copyRoomIdMessage.innerText = "faild copy room id"
            await sleep(3000)
            copyRoomIdMessage.innerText = ""
        })
}

const updateReadyCheckBox = () => {
    const checkbox = qs("#readyStartGame")
    if (checkbox instanceof HTMLInputElement) {
        checkbox.checked = room.readyStartGame.value
    }
}

(() => {
    onMounted(async () => {
        await nextTick()
        // init bandle
        room.join()
        console.log("canGameJoinRoom", (await canJoinRoom(room.id)))
        qs("#exitRoom")?.addEventListener("click", () => room.exit())
        qs("#gameStart")?.addEventListener("click", () => room.gameStart())
        qs(".copyImage")?.addEventListener("click", () => copyRoomId())
        qs("#readyStartGame")?.addEventListener("input", (e) => {
            if (e.target instanceof HTMLInputElement) {
                console.log("e.target.vlaue:", e.target.checked)
                room.readyStartGame.input(e.target.checked)
            }
        })
        room.readyStartGame.addInputEventListener(updateReadyCheckBox)

        watch(room.game.lastPut, (newValue) => {
            console.log("lastPut:" + newValue.x)
            const yourTurn = room.game.gameData.value?.yourTurn
            if (Link4.isGameX(newValue.x) && yourTurn == true) {
                console.log("watch gameActionPut")
                room.gameActionPut(newValue.x)
            }
        })

        watch(room.game.finishGame, () => {
            console.log("watch finishGame")
            room.finishGame()
        })


    })
})()

const gameState = computed(() => {
    return room.game.gameData.value?.gameState
})

const numberOfSession = computed(() => {
    return Number(room.roomInfo.value?.numberOfSession)
})

const canGameStart = computed(() => {
    return room.roomInfo.value?.canGameStart
})

const yourColor = computed(() => {
    if (room.game.gameData.value?.playerNum == 1) {
        return "red"
    } else {
        return "yellow"
    }
})

const remotePlayerColor = computed(() => {
    if (room.game.gameData.value?.playerNum == 1) {
        return "yellow"
    } else {
        return "red"
    }
})

const remotePlayerReady = computed(() => {
    if (room.roomInfo.value?.remotePlayerReady) {
        return "OK"
    } else {
        return "not ready"
    }
})
</script>

<template>
    <div class="room" v-show="gameState == 'unstarted'">
        <header class="roomHeader">
            <div class="roomHeaderLeft">
                <span> Room ID : {{ room.id }} </span>
                <img src="../assets/copy.svg" alt="copyRoomId" class="copyImage">
                <span id="copyRoomIdMessage"></span>
            </div>
            <div>
                {{ `players in room: ${numberOfSession}/2` }}
            </div>
        </header>
        <main class="roomMain">
            <div class="roomPlayerSelf">
                <img src="../assets/person.svg" alt="person" class="personImage">
                <p>YOU</p>
                <p>Are you ready? : <input type="checkbox" id="readyStartGame" :vlaue="room.readyStartGame.value"></p>
                <p>{{ "your color : " + yourColor }}</p>
            </div>
            VS
            <div class="roomPlayerRemote">
                <img src="../assets/person_off.svg" v-show="numberOfSession == 1" alt="person" class="personImage">
                <img src="../assets/person.svg" v-show="numberOfSession == 2" alt="person" class="personImage">
                <p v-show="numberOfSession == 1">NO PLYAER</p>
                <p v-show="numberOfSession == 2">OPPONENT</p>
                <p>{{ "ready? : " + remotePlayerReady }}</p>
                <p>{{ remotePlayerColor }}</p>
            </div>
        </main>
        <footer class="roomFooter">
            <button id="exitRoom" :disabled="gameState != 'unstarted'">EXIT ROOM</button>
            <button id="gameStart" :disabled="!canGameStart && gameState == 'unstarted'">GAME START</button>
        </footer>
    </div>
    <div class="play" v-show="gameState == 'playing' || gameState == 'gameset'">
        <Game :game="room.game"></Game>
    </div>
</template>
