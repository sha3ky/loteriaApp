// import { createRouter, createWebHashHistory } from 'vue-router';
// import routes from './routesDefinition'; // Assuming you have a separate routes definition file
// import { useLayoutStore } from 'src/stores/layoutStore';

// // Function to set up route guards
// export function setupRouteGuards(router) {
//   router.beforeEach((to, from, next) => {
//     const layoutStore = useLayoutStore();

//     if (to.path === '/adminpage') {
//       layoutStore.toggleToolbar(false);
//     } else {
//       layoutStore.toggleToolbar(true);
//     }

//     next();
//   });
// }

// // Create and export the router instance
// const router = createRouter({
//   history: createWebHashHistory(),
//   routes,
// });

// export default router;

import { createRouter, createWebHashHistory } from "vue-router";
import routes from "./routesDefinition";
import { useLayoutStore } from "src/stores/layoutStore";

const router = createRouter({
  history: createWebHashHistory(),
  routes, // Use the route definitions
});

export function setupRouteGuards(router) {
  router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("accessToken");
    const layoutStore = useLayoutStore();
    if (to.path === "/adminpage") {
      if (!token) {
        layoutStore.toggleToolbar(true); // Show toolbar before redirecting
        return next("/"); // Redirect and exit function
      }
      // Hide toolbar for authenticated users on adminpage
      layoutStore.toggleToolbar(false);
    } else {
      // Show toolbar for non-admin routes
      layoutStore.toggleToolbar(true);
    }
    next(); // Proceed to the route
  });
}
export default router;


