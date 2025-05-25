import { defineStore } from "pinia";
import { ref } from "vue";
import { toast } from "vue3-toastify";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import router from "../routes";

export const useScriptStore = defineStore("script", {
  state: () => ({
    script: ref({}),
    scripts: ref([]),
    loading: ref(false),
  }),

  getters: {
    getScript() {
      return this.script;
    },
    getScripts() {
      return this.scripts;
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
    async addScript(scriptData) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.post("scripts", scriptData, {
          headers,
        });
        if (response.status === 201) {
          toast.success("Script added successfully!");
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

    async getScriptAction(scriptId) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.get("scripts/" + scriptId, {
          headers,
        });
        this.script = response.data;
      } catch (error) {
        if (error.status === 401) {
          toast.error("Unauthorized access. Please log in.", {
            rtl: true,
            limit: 3,
            position: toast.POSITION.BOTTOM_CENTER,
          });
          this.redirectToLogin();
        }
        console.log(error);
      } finally {
        this.loading = false;
      }
    },

    async getScriptsAction(page = 1) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.get("scripts?page=" + page, {
          headers,
        });
        this.scripts = response.data;
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async deleteScript(scriptId) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.delete("scripts/" + scriptId, {
          headers,
        });
        if (response.status === 204) {
          toast.success("Script deleted successfully!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async updateScript(scriptData) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.put(
          "scripts/" + scriptData.id,
          scriptData,
          {
            headers,
          }
        );
        if (response.status === 200) {
          toast.success("Script updated successfully!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    resetScriptData() {
      this.script = {};
      this.scripts = [];
    },
  },
});
