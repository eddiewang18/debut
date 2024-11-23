import { createRouter, createWebHashHistory } from "vue-router";

import Home from "@/components/Home.vue";
import Machine from "@/components/Machine.vue";

const routes = [
    {
        path: "/",
        component: Home
    },
    {
        path: "/machine",
        component: Machine
    },
]

const router = createRouter(
    {
        history: createWebHashHistory(),
        routes
    }
)

export default router