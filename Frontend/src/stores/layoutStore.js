import { defineStore } from 'pinia';

export const useLayoutStore = defineStore('layout', {
  state: () => ({
    showToolbar: true, // Initial state for toolbar visibility
  }),
  actions: {
    toggleToolbar(value) {
      // console.log(`Toolbar visibility set to: ${value}`);
      this.showToolbar = value;
    },
  },
});


