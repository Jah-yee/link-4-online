import { ref, type Ref } from "vue";

console.log("GameManager");

export class Link4 {
	gameData: Ref<Link4.GameData | null> = ref(null)
	lastPut: Ref<{ x: number }> = ref({ x: 0 })
	finishGame: Ref<{}> = ref({})

	constructor() { }
	static isGameState(value: unknown): value is Link4.GameState {
		return (
			value !== null &&
			typeof value == "string" &&
			(
				value == "unstarted" ||
				value == "playing" ||
				value == "gameset"
			)
		)
	}

	static isSell(value: unknown): value is Link4.Sell {
		return (
			value !== null &&
			typeof value == "number" &&
			!Number.isNaN(value) &&
			(
				value == 0 ||
				value == 1 ||
				value == 2
			)
		)
	}

	static isBoard(value: unknown): value is Link4.Board {
		if (!(value !== null && Array.isArray(value))) return false
		return value.flat().map((item) => this.isSell(item))
			.reduce((item, nextItem) => item == true && nextItem == true)
	}

	static isGameData(value: unknown): value is Link4.GameData {
		return (
			value !== null &&
			typeof value == "object" &&
			"board" in value &&
			"playerNum" in value &&
			"yourTurn" in value &&
			"gameState" in value &&
			"winningLine" in value &&
			Link4.isBoard(value.board) &&
			typeof value.playerNum == "number" &&
			(
				value.playerNum == 1 ||
				value.playerNum == 2
			) &&
			typeof value.yourTurn == "boolean" &&
			Link4.isGameState(value.gameState) &&
			Link4.isWinningLine(value.winningLine)
		)
	}

	static isWinPattern(value: unknown): value is Link4.WinPattern {
		const isTuple2Number = (value: unknown): value is [number, number] => {
			return (
				value != null &&
				Array.isArray(value) &&
				value.length == 2 &&
				typeof value[0] == "number" &&
				typeof value[1] == "number"
			)
		}
		return (
			typeof value == "object" &&
			value != null &&
			"startPosition" in value &&
			"direction" in value &&
			"len" in value &&
			isTuple2Number(value.startPosition) &&
			isTuple2Number(value.direction) &&
			typeof value.len == "number"
		)
	}

	static isWinningLine(value: unknown): value is Link4.WinningLine {
		console.log("start isWinningLine", Array.isArray(value))
		if (!Array.isArray(value)) return false;
		const reuzlt = value.every((item) => this.isWinPattern(item))
		console.log("isWnningLine every", reuzlt)
		return reuzlt
	}

	static isGameX(value: unknown): value is Link4.GameX {
		return (
			typeof value == "number" &&
			value >= 0 &&
			value <= 6
		)
	}
}

export namespace Link4 {
	export type Sell = 0 | 1 | 2
	export type Board = Sell[][]
	export type GameState = "unstarted" | "playing" | "gameset";
	export type GameX = 0 | 1 | 2 | 3 | 4 | 5 | 6
	export type WinPattern = {
		startPosition: [number, number]
		direction: [number, number]
		len: number
	}
	export type WinningLine = WinPattern[]
	export type GameData = {
		board: Board
		playerNum: 1 | 2,
		yourTurn: boolean
		gameState: GameState
		winningLine: WinningLine
	}
}
