// import { createPinia } from 'pinia';
// import { setupRouteGuards } from 'src/router'; // Optional: For route guards

// export default async ({ app, router }) => {
//   const pinia = createPinia();

//   // Use Pinia with the app
//   app.use(pinia);

//   // Optional: If you have route guards, set them up here
//   setupRouteGuards(router);
// };

import { createPinia } from 'pinia';
import { setupRouteGuards } from 'src/router/routes'; // Adjust path as needed

export default async ({ app, router }) => {
  const pinia = createPinia();

  app.use(pinia);

  // Set up route guards
  setupRouteGuards(router);
};
