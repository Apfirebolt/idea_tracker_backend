import { defineStore } from "pinia";
import { ref } from "vue";
import { toast } from 'vue3-toastify';
import Cookie from "js-cookie";
import router from "../routes";
import httpClient from "../plugins/interceptor";
import emitter from '../plugins/eventBus';

export const useAuth = defineStore("auth", {
  state: () => ({
    authData: Cookie.get("user") ? JSON.parse(Cookie.get("user")) : null,
    loading: ref(false),
  }),

  getters: {
    getAuthData() {
      return this.authData;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async loginAction(loginData) {
      try {
        const response = await httpClient.post("auth/login", loginData);
        if (response.data) {
          this.authData = response.data;
          toast.success("Login successful!");
          Cookie.set("user", JSON.stringify(response.data), { expires: 30 });
          router.push("/dashboard");
        }
      } catch (error) {
        let message = "An error occurred!";
        this.error = error;
        if (error.response && error.response.data) {
          toast.error(error.response.data.detail || message);
        }
        return error;
      } finally {
        this.loading = false;
      }
    },

    async registerAction(registerData) {
      try {
        const response = await httpClient.post("auth/register", registerData);
        if (response.data && response.status === 201) {
          this.authData = response.data;
          toast.success("Registration successful!");
          Cookie.set("user", JSON.stringify(response.data), { expires: 30 });
          router.push("/dashboard");
        }
      } catch (error) {
        if (error.response && error.response.data) {
          toast.error(error.response.data.detail);
        }
        // toast.error(message);
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async getProfileData() {
      try {
        // get the token from the cookie
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).token}`,
        };
        const response = await httpClient.get("users/profile", { headers });
        console.log(response.data);
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    logout() {
      toast.success("Logout successful!");
      emitter.emit('logout');
      this.authData = null;
      Cookie.remove("user");
      router.push("/login");
    },

    resetAuth() {
      this.authData = {};
    },
  },
});