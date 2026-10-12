// Import CSS
import '../css/style.css'
import '../css/game.css'
import '../css/home.css'
import '../css/room.css'

import { createApp } from "vue";
import App from "../components/App.vue";

import { router } from "./router.ts";

createApp(App)
    .use(router)
    .mount("#app")

console.log("start");
