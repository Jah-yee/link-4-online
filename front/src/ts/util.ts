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
    #vlaue: ShallowRef<T>
    #setTimeoutId: number
    #reflectionDelay: number
    #reflectionHandler: Function
    #inputEventLister: Function[] = []
    constructor(vlaue: T, reflactionDelay: number, reflectionHandler: Function) {
        this.#vlaue = shallowRef(vlaue)
        this.#reflectionDelay = reflactionDelay
        this.#setTimeoutId = setTimeout(() => this.reflection(), this.#reflectionDelay);
        this.#reflectionHandler = reflectionHandler
    }

    input(value: T) {
        this.#vlaue.value = value
        clearTimeout(this.#setTimeoutId)
        this.#setTimeoutId = setTimeout(() => this.reflection(), this.#reflectionDelay);
        if (this.#inputEventLister) {
            this.#inputEventLister.forEach((calllback) => {
                calllback(this.value)
            })
        }
    }

    reflection() {
        console.log("reflection", this)
        this.#reflectionHandler(this.#vlaue)
    }

    addInputEventListener(calllback: Function) {
        this.#inputEventLister.push(calllback)
    }

    get value() {
        return this.#vlaue.value
    }
}
