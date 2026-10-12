import { Link4 as Link4 } from "./game"

export namespace WebsocketBody {
    export type Action =
        "JOIN"
        | "CANJOIN"
        | "CREATE"
        | "CANGAMESTART"
        | "GAMESTART"
        | "GAMEACTION"
        | "EXITROOM"
        | "USERINFO"
        | "GAMEFINISH"

    export interface BaseBody {
        action: Action
    }


    export interface CanJoinRoomBody extends BaseBody {
        action: "CANJOIN"
        roomId: number
    }

    export interface JoinRoomBody extends BaseBody {
        action: "JOIN",
    }

    export interface ExitRoom extends BaseBody {
        action: "EXITROOM"
    }

    export interface CreateRoomBody {
        action: "CREATE"
    }

    export interface GameStart extends BaseBody {
        action: "GAMESTART"
    }

    export interface CanGameStart extends BaseBody {
        action: "CANGAMESTART"
    }

    export interface GameActionPut extends BaseBody {
        action: "GAMEACTION"
        gameAction: "PUT"
        x: Link4.GameX
    }

    export interface UserInfo extends BaseBody {
        action: "USERINFO"
        readyStartGame: boolean
    }

    export interface GameFinish extends BaseBody {
        action: "GAMEFINISH"
    }
}


export namespace WebsocketMessage {
    export type Message =
        "ROOMINFO"
        | "GAMESTART"
        | "GAMEINFO"
        | "GAMEFINISH"

    export type BaseMessage = {
        message: Message
    }

    export interface RoomInfo extends BaseMessage {
        message: "ROOMINFO"
        numberOfSession: number,
        roomId: number
        canGameStart: boolean
        remotePlayerReady: boolean
    }

    export interface GameStart extends BaseMessage {
        message: "GAMESTART"
    }

    export interface FinishGame extends BaseMessage {
        message: "GAMEFINISH"
    }

    export type WinPatern = {
        startPosition: number[]
        direction: number[]
        len: number
    }

    export type WinningLine = WinPatern[]
    export interface GameInfo extends BaseMessage {
        message: "GAMEINFO"
        gameData: Link4.GameData
    }
}

export const WebsocketMessage = {
    isMessage(value: unknown): value is WebsocketMessage.Message {
        return (
            value !== null &&
            typeof value == "string" &&
            (
                value == "ROOMINFO"
                || value == "GAMESTART"
                || value == "GAMEINFO"
                || value == "GAMEFINISH"
            )
        )
    },

    isBaseMessage(value: unknown): value is WebsocketMessage.BaseMessage {
        return (
            typeof value === "object" &&
            value !== null &&
            "message" in value &&
            this.isMessage(value.message)
        )
    },

    isRoomInfo(value: unknown): value is WebsocketMessage.RoomInfo {
        return (
            this.isBaseMessage(value) &&
            "numberOfSession" in value &&
            "roomId" in value &&
            "canGameStart" in value &&
            "remotePlayerReady" in value &&
            this.isMessage(value.message) &&
            typeof value.numberOfSession === "number" &&
            typeof value.roomId === "number" &&
            typeof value.canGameStart === "boolean" &&
            typeof value.remotePlayerReady === "boolean"
        )
    },

    isGameInfo(value: unknown): value is WebsocketMessage.GameInfo {
        return (
            this.isBaseMessage(value) &&
            this.isMessage(value.message) &&
            value.message == "GAMEINFO" &&
            "gameData" in value &&
            Link4.isGameData(value.gameData)
        )
    },

    isGameStart(value: unknown): value is WebsocketMessage.GameStart {
        return (
            this.isBaseMessage(value) &&
            value.message == "GAMESTART"
        )
    },

    isGameFinish(value: unknown): value is WebsocketMessage.FinishGame {
        return (
            this.isBaseMessage(value) &&
            value.message == "GAMEFINISH"
        )
    },
}

