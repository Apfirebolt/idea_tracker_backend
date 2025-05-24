import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import router from "../routes";

export const useTagStore = defineStore("tag", {
  state: () => ({
    tag: ref({}),
    tags: ref([]),
    message: ref(""),
    error: ref(""),
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
    getMessage() {
      return this.message;
    },
    getError() {
      return this.error;
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
          this.message = "Tag created successfully!";
        }
      } catch (error) {
        console.log(error);
        if (error.response.status === 400) {
          let message = "Bad request";
          if (error.response.data.detail) {
            this.error = error.response.data.detail;
          }
        }
      } finally {
        this.loading = false;
        // reset message and error after some time
        setTimeout(() => {
          this.message = "";
          this.error = "";
        }, 5000);
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
        if (response.status === 204) {
          this.message = response.data.message || "Tag deleted successfully!";
        }
      } catch (error) {
        console.log(error);
        if (error.response && error.response.status === 404) {
          this.error = "Tag not found!";
        } else if (error.response && error.response.status === 403) {
          this.error = "You do not have permission to delete this tag.";
        } else {
          this.error = "An error occurred while deleting the tag.";
        }
        return error;
      } finally {
        this.loading = false;
        // reset message and error after some time
        setTimeout(() => {
          this.message = "";
          this.error = "";
        }, 5000);
      }
    },

    async updateTag(tagData) {
      console.log("tagData", tagData);
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.put("tags/" + tagData.id, tagData, {
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

    resetTagData() {
      this.tag = {};
      this.tags = [];
    },
  },
});
