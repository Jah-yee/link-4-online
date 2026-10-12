import { createRouter, createWebHistory } from "vue-router";
import Home from "../components/Home.vue";
import Room from "../components/Room.vue";


export const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            component: Home
        },
        {
            path: "/room/:roomId",
            name: "room",
            component: Room
        },
        {
            path: "/:chatchAll(.*)",
            name: "NotFound",
            redirect: "/"
        }
    ]
})
