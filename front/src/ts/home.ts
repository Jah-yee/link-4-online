import { router } from './router';
import type { WebsocketBody } from './type';
import { createRequest } from './util';

const targetUrl = `${import.meta.env.VITE_API_BASE_URL}/room`

export const canJoinRoom = async (roomId: number = NaN): Promise<boolean> => {
    if (Number.isNaN(roomId)) return false
    if (!(typeof roomId == "number")) return false
    const body: WebsocketBody.CanJoinRoomBody = {
        action: 'CANJOIN',
        roomId: roomId
    }
    const request = createRequest(targetUrl, "POST", body)
    const rezult = await fetch(request).then(
        value => value.text()
    )
    return (rezult == "true")
}

export const createRoom = async () => {
    const body: WebsocketBody.CreateRoomBody = {
        action: "CREATE"
    }
    const request = createRequest(targetUrl, "POST", body)
    const rezult = Number(await fetch(request).then(
        value => value.text()
    ))
    if (typeof rezult == 'number') {
        router.push(`/room/${rezult}`)
    }
}
