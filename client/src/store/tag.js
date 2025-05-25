import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { toast } from 'vue3-toastify';
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
          toast.success("Tag added successfully!");
        }
      } catch (error) {
        console.log(error);
        if (error.response.status === 400) {
          let message = "Bad request";
          if (error.response.data.detail) {
            toast.error(error.response.data.detail);
          }
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
        if (error.status === 401) {
          toast.error("Unauthorized access. Please log in.");
          this.redirectToLogin();
        } else if (error.status === 403) {
          toast.error("You do not have permission to access this resource.");
        } else if (error.status === 404) {
          toast.error("Tags not found.");
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
          toast.success("Tag deleted successfully!");
        }
      } catch (error) {
        console.log(error);
        if (error.response && error.response.status === 404) {
          toast.error("Tag not found.");
        } else if (error.response && error.response.status === 403) {
          toast.error("You do not have permission to delete this tag.");
        } else {
          toast.error("An error occurred while deleting the tag.");
        }
        return error;
      } finally {
        this.loading = false;
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
