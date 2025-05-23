import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import router from "../routes";

export const useTagStore = defineStore("tag", {
  state: () => ({
    tag: ref({}),
    tags: ref([]),
    loading: ref(false),
  }),

  getters: {
    getTag() {
      return this.tag;
    },
    getTags() {
      return this.tags;
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
    async addTag(tagData) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.post("tags", tagData, {
          headers,
        });
        if (response.status === 201) {
          toast.success("Tag created!");
        }
      } catch (error) {
        console.log(error);
        if (error.response.status === 400) {
          let message = "Bad request";
          if (error.response.data.message) {
            message = error.response.data.message;
          }
          toast.error(message);
        }
      } finally {
        this.loading = false;
      }
    },

    async getTagAction(tagId) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.get("tags/" + tagId, {
          headers,
        });
        this.tag = response.data;
      } catch (error) {
        console.log(error);
      }
    },

    async getTagsAction(page = 1) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.get("tags?page=" + page, {
          headers,
        });
        this.tags = response.data;
      } catch (error) {
        console.log('Error fetching tags:', error.status);
        if (error.status === 401) {
          this.redirectToLogin();
        } else if (error.status === 403) {
          console.log("Forbidden");
        } else if (error.status === 404) {
          console.log("Tags not found");
        }
        return error;
      } finally {
        this.loading = false;
      }
    },

    async deleteTag(tagId) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.delete("tags/" + tagId, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Tag deleted!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async updateTag(tagData) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.put("tags/" + tagData.id, tagData, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Tag updated!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    resetTagData() {
      this.tag = {};
      this.tags = [];
    },
  },
});
