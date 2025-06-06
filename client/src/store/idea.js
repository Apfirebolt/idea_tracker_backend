import { defineStore } from "pinia";
import { ref } from "vue";
import { toast } from 'vue3-toastify';
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import router from "../routes";
import emitter from "../plugins/eventBus";


export const useIdeaStore = defineStore("idea", {
  state: () => ({
    idea: ref({}),
    ideas: ref([]),
    sharedIdeas: ref([]),
    loading: ref(false),
  }),

  getters: {
    getIdea() {
      return this.idea;
    },
    getIdeas() {
      return this.ideas;
    },
    getSharedIdeas() {
      return this.sharedIdeas;
    },
    getCompletedIdeasCount() {
      return this.ideas && this.ideas.items && this.ideas.items.filter(idea => idea.status === 'completed').length;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    redirectToLogin() {
      // Redirect to the login page
      router.push({ name: "Login" });
    },
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
          toast.success("Idea added successfully!");
        }
      } catch (error) {
        if (error.response.status === 400) {
          let message = "Bad request";
          if (error.response.data.detail) {
            toast.error(error.response.data.detail);
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
        if (error.status === 401) {
          toast.error("Unauthorized access. Please log in.", {
              rtl: true,
              limit: 3,
              position: toast.POSITION.BOTTOM_CENTER,
            },);
          this.redirectToLogin();
        }
        console.log(error);
      } finally {
        this.loading = false;
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

    async getSharedIdeasAction(page = 1) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.get("ideas/shared?page=" + page, {
          headers,
        });
        this.sharedIdeas = response.data;
      } catch (error) {
        if (error.status === 401) {
          toast.error("Unauthorized access. Please log in.", {
              rtl: true,
              limit: 3,
              position: toast.POSITION.BOTTOM_CENTER,
            },);
          this.redirectToLogin();
        }
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
        if (response.status === 204) {
          toast.success("Idea deleted successfully!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async updateIdea(ideaData) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.put("ideas/" + ideaData.id, ideaData, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Idea updated successfully!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async addComment(payload) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.post(`ideas/${payload.idea_id}/comments`, payload, {
          headers,
        });
        if (response.status === 201) {
          toast.success("Comment added successfully!");
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
