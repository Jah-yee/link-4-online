import { shallowRef, type ShallowRef } from "vue";

export function qs<T extends Element = HTMLElement>
    (selector: string, parent: ParentNode = document): T | null {
    return parent.querySelector<T>(selector);
}

export function qsAll<T extends Element = HTMLElement>
    (selector: string, parent: ParentNode = document): NodeListOf<T> | null {
    return parent.querySelectorAll<T>(selector);
}

export function createRequest(url: string, method: "GET" | "POST", body: Object) {
    return new Request(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    })
}

export class Debounce<T> {
    #value: ShallowRef<T>
    #setTimeoutId: number
    #reflectionDelay: number
    #reflectionHandler: Function
    #inputEventListener: Function[] = []
    constructor(value: T, reflectionDelay: number, reflectionHandler: Function) {
        this.#value = shallowRef(value)
        this.#reflectionDelay = reflectionDelay
        this.#setTimeoutId = setTimeout(() => this.reflection(), this.#reflectionDelay);
        this.#reflectionHandler = reflectionHandler
    }

    input(value: T) {
        this.#value.value = value
        clearTimeout(this.#setTimeoutId)
        this.#setTimeoutId = setTimeout(() => this.reflection(), this.#reflectionDelay);
        if (this.#inputEventListener) {
            this.#inputEventListener.forEach((callback) => {
                callback(this.value)
            })
        }
    }

    reflection() {
        console.log("reflection", this)
        this.#reflectionHandler(this.#value)
    }

    addInputEventListener(callback: Function) {
        this.#inputEventListener.push(callback)
    }

    get value() {
        return this.#value.value
    }
}
