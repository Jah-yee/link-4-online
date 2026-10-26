import { ref, type Ref } from "vue"
// import { canJoinRoom } from "./home"
// import { createRequest } from "./util"
import { type WebsocketBody, WebsocketMessage } from "./type";
import { router } from "./router";
import { Link4 } from "./game";
import { Debounce } from "./util";


export class Room {
    #id: number
    #ws: WebSocket | null = null
    game: Link4
    roomState: "OPEN" | "CLOSE" = "OPEN"
    roomInfo: Ref<Room.RoomInfo | null> = ref(null)
    readyStartGame: Debounce<boolean> = new Debounce(false, 1000, () => this.setReadyStartGame())

    constructor(roomId: number) {
        this.#id = roomId
        this.game = new Link4();
        router.afterEach((to, from) => {
            console.log("new URL")
            console.log("from: ", from)
            console.log("to: ", to);
            console.log(/\/room\/\d/)
            console.log(/\/room\/\d/.test(from.fullPath))
            if (/\/room\/\d/.test(from.fullPath)) {
                this.exit()
            }
        })
    }


    join() {
        if (!(this instanceof Room)) {
            throw new TypeError("Can not execute join directly on the class. Call it on an instance")
        }

        try {
            const wsBaseUrl = import.meta.env.VITE_WS_BASE_URL
            const targetWebsocketURL = `${wsBaseUrl}/room/${this.#id}`;
            this.#ws = new WebSocket(targetWebsocketURL)
            console.log("create ws")
            this.#ws.addEventListener("open", () => this.#websocketOpen())
            this.#ws.addEventListener("message", (e: MessageEvent) => this.#websocketMessage(e))
            this.#ws.addEventListener("error", (e: CloseEvent | Event) => this.#websocketError(e))
            this.#ws.addEventListener("close", () => this.#websocketClose())
        } catch (error) {
            console.log("try-catch", error)
        }
    }

    exit() {
        if (!(this instanceof Room)) {
            throw new TypeError("Can not execute exit directly on the class. Call it on an instance")
        }

        if (this.#ws && this.#ws?.readyState < 2) {
            const body: WebsocketBody.ExitRoom = {
                action: "EXITROOM"
            }
            this.#websocketSendJSON(body)
        }
        this.#ws?.close()
        // router.push("/")
    }

    gameStart() {
        if (this.game.gameData.value?.gameState == "unstarted") {
            const body: WebsocketBody.GameStart = {
                action: "GAMESTART"
            }
            this.#websocketSendJSON(body)
        }
    }

    #websocketSendJSON(object: WebsocketBody.BaseBody) {
        console.log("ws:sedJSON", JSON.stringify(object))
        this.#ws?.send(JSON.stringify(object))
    }

    #websocketOpen() {
        const body: WebsocketBody.JoinRoomBody = {
            action: "JOIN"
        }
        this.#websocketSendJSON(body)
    }

    #websocketMessage(e: MessageEvent) {
        const message = JSON.parse(e.data)
        if (!WebsocketMessage.isBaseMessage(message)) return
        if (WebsocketMessage.isRoomInfo(message)) {
            const { numberOfSession, canGameStart, remotePlayerReady } = message
            this.roomInfo.value = {
                numberOfSession,
                canGameStart,
                remotePlayerReady
            }
        }

        if (WebsocketMessage.isGameInfo(message)) {
            console.log("is game info")
            this.game.gameData.value = message.gameData
        }

        if (WebsocketMessage.isGameStart(message)) {
            console.log("GAMESTART")
        }

        if (WebsocketMessage.isGameFinish(message)) {
            // this.readyStartGame.value = false
            this.readyStartGame.input(false)
            console.log("isGameFinish", this.readyStartGame, this.readyStartGame.value)
        }
    }

    #websocketError(e: CloseEvent | Event) {
        console.log("websocket error", e)
    }

    #websocketClose() {
        router.push("/")
    }

    gameActionPut(x: Link4.GameX) {
        const gameData: Link4.GameData = JSON.parse(JSON.stringify(this.game.gameData.value))
        console.log("Room.gameAction_put", x, gameData, gameData.yourTurn, gameData.gameState, Link4.isGameX(x))
        if (gameData.yourTurn == true &&
            gameData.gameState == "playing" &&
            Link4.isGameX(x)) {
            const body: WebsocketBody.GameActionPut = {
                action: "GAMEACTION",
                gameAction: "PUT",
                x: x
            }
            this.#websocketSendJSON(body)
        }
    }

    setReadyStartGame() {
        console.log("setReadyStartGame", this.readyStartGame.value)
        const body: WebsocketBody.UserInfo = {
            action: "USERINFO",
            readyStartGame: this.readyStartGame.value
        }
        this.#websocketSendJSON(body)
    }

    finishGame() {
        const body: WebsocketBody.GameFinish = {
            action: "GAMEFINISH"
        }
        this.#websocketSendJSON(body)
        this.readyStartGame.input(false)
    }


    get id(): number {
        return this.#id
    }

}

export namespace Room {
    export type RoomInfo = {
        numberOfSession: number
        canGameStart: boolean
        remotePlayerReady: boolean
    }
}
