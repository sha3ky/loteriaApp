// import { boot } from 'quasar/wrappers'
// import axios from 'axios'

// // Be careful when using SSR for cross-request state pollution
// // due to creating a Singleton instance here;
// // If any client changes this (global) instance, it might be a
// // good idea to move this instance creation inside of the
// // "export default () => {}" function below (which runs individually
// // for each client)
// const api = axios.create({ baseURL: 'https://api.example.com' })

// export default boot(({ app }) => {
//   // for use inside Vue files (Options API) through this.$axios and this.$api

//   app.config.globalProperties.$axios = axios
//   // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
//   //       so you won't necessarily have to import axios in each vue file

//   app.config.globalProperties.$api = api
//   // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
//   //       so you can easily perform requests against your app's API
// })

// export { api }


import axios from 'axios';
import BASE_URL from "../variosJs/config";
import routes from "../router/routesDefinition";

const api = axios.create({
  baseURL: `${BASE_URL}`, // Replace with your API base URL
});
// console.log(api);

// Add a request interceptor to include the token in headers
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        console.log("Refresh Token:", refreshToken);
        const response = await axios.post(`${BASE_URL}/api/token/refresh/`, {
          refresh: refreshToken,
        });

        // Update the access token
        localStorage.setItem('accessToken', response.data.access);

        // Retry the failed request with the new token
        error.config.headers.Authorization = `Bearer ${response.data.access}`;
        return api.request(error.config);
      } catch (refreshError) {
        // Handle refresh token failure (e.g., logout user)
        console.error('Token refresh failed:', refreshError);
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        routes.push('/'); // Redirect to login page
      }
    }
    return Promise.reject(error);
  }
);
export { api };
