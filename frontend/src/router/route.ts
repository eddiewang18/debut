import { createRouter, createWebHashHistory } from "vue-router";

import Home from "@/components/Home.vue";
import Machine from "@/components/Machine.vue";
import Machine_line_record from "@/components/Machine_line_record.vue";

const routes = [
    {
        path: "/",
        component: Home
    },
    {
        path: "/machine",
        component: Machine
    },
    {
        path: "/machine_line_record",
        component: Machine_line_record
    },
]

const router = createRouter(
    {
        history: createWebHashHistory(),
        routes
    }
)

export default router