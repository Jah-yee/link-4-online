import { router } from './router';
import type { WebsocketBody, CreateRoomBody } from './type';
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
    // rezultじゃなくてresultですね
    const result = await fetch(request).then(
        value => value.text()
    )
    return (result == "true")
}

export const createRoom = async () => {
    const body: CreateRoomBody = {
        action: "CREATE"
    }
    const request = createRequest(targetUrl, "POST", body)
    const result = Number(await fetch(request).then(
        value => value.text()
    ))
    if (typeof result == 'number') {
        router.push(`/room/${result}`)
    }
}
