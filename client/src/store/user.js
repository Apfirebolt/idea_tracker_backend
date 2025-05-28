import { defineStore } from "pinia";
import { ref } from "vue";
import { toast } from "vue3-toastify";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import router from "../routes";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: ref({}),
    users: ref([]),
    loading: ref(false),
  }),

  getters: {
    getUser() {
      return this.user;
    },
    getUsers() {
      return this.users;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    redirectToLogin() {
      router.push({ name: "Login" });
    },
    getAuthHeaders() {
      const auth = useAuth();
      return {
        Authorization: `Bearer ${auth.authData.access_token}`,
      };
    },

    async getUserAction(userId) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.get("users/" + userId, {
          headers,
        });
        this.user = response.data;
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

    async getUsersAction(page = 1) {
      try {
        const headers = this.getAuthHeaders();
        this.loading = true;
        const response = await httpClient.get("users?page=" + page, {
          headers,
        });
        console.log('Users response:', response.data);
        this.users = response.data;
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    resetUserData() {
      this.user = {};
      this.users = [];
    },
  },
});
