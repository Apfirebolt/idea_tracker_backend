import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import emitter from "../plugins/eventBus";


export const useIdeaStore = defineStore("idea", {
  state: () => ({
    idea: ref({}),
    ideas: ref([]),
    loading: ref(false),
  }),

  getters: {
    getIdea() {
      return this.idea;
    },
    getIdeas() {
      return this.ideas;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    getAuthHeaders() {
      // Call useAuth() inside an action where Pinia is active
      const auth = useAuth();
      return {
        Authorization: `Bearer ${auth.authData.access_token}`,
      };
    },
    async addIdea(ideaData) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.post("ideas", ideaData, {
          headers,
        });
        if (response.status === 201) {
          console.log("response", response);
        }
      } catch (error) {
        console.log(error);
        if (error.response.status === 400) {
          let message = "Bad request";
          if (error.response.data.message) {
            message = error.response.data.message;
          }
          console.log("Error message", message);
        }
      } finally {
        this.loading = false;
      }
    },

    async getIdeaAction(ideaId) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.get("ideas/" + ideaId, {
          headers,
        });
        this.idea = response.data;
      } catch (error) {
        console.log(error);
      }
    },

    async getIdeasAction(page = 1) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.get("ideas?page=" + page, {
          headers,
        });
        this.ideas = response.data;
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async deleteIdea(ideaId) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.delete("ideas/" + ideaId, {
          headers,
        });
        if (response.status === 200) {
          console.log("response", response);
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    resetIdeaData() {
      this.idea = {};
      this.ideas = [];
    },
  },
});
