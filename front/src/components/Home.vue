<script setup lang="ts">
import { canJoinRoom, createRoom } from "../ts/home.ts"
import { qs } from "../ts/util.ts";
import { useRouter } from "vue-router";

const router = useRouter()
const redirectRoom = async (e: SubmitEvent) => {
    e.preventDefault()
    const form = qs<HTMLFormElement>("#joinRoomForm")
    if (!form) return
    const formData = new FormData(form)
    const roomId = Number(formData.get("roomId"))
    if (Number.isNaN(roomId)) return
    if (await canJoinRoom(roomId)) {
        return router.push(`/room/${roomId}`)
    } else {
        const roomIdInput = qs<HTMLInputElement>("#roomId")
        if (roomIdInput) {
            roomIdInput.setCustomValidity("The room does not exist or is full.")
            roomIdInput.reportValidity()
        }
    }
}
const canselErrorMessage = () => {
    const roomIdInput = qs<HTMLInputElement>("#roomId")
    if (roomIdInput) {
        roomIdInput.setCustomValidity("")
    }
}
</script>

<template>
    <div class="home">
        <h1 class="title">Link 4 Online</h1>
        <button id="createRoom" @click="createRoom">create room</button>
        <form @submit="redirectRoom" id="joinRoomForm" autocomplete="off">
            <input type="number" required name="roomId" id="roomId" @input="canselErrorMessage"
                placeholder="room ID: 1234">
            <input type="submit" value="join room"><br>
        </form>
    </div>
</template>
