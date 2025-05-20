<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">Login</h2>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2" for="email">Email</label>
          <input
            v-model="email"
            id="email"
            type="email"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            autocomplete="username"
          />
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 mb-2" for="password"
            >Password</label
          >
          <input
            v-model="password"
            id="password"
            type="password"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            autocomplete="current-password"
          />
        </div>
        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Login
        </button>
        <p>
          Don't have an account?
          <router-link to="/register" class="text-blue-600 hover:underline">
            Register
          </router-link>
        </p>
        <p v-if="error" class="text-red-500 mt-4 text-center">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAuth } from "../store/auth";

const email = ref("");
const password = ref("");
const error = ref("");
const auth = useAuth();

const authData = computed(() => auth.getAuthData);

const login = async () => {
  error.value = "";
  // Replace with your actual login logic
  if (!email.value || !password.value) {
    error.value = "Please enter both email and password.";
    return;
  }
  // Simulate login
  try {
    await auth.loginAction({
      email: email.value, 
      password: password.value,
    });
  } catch (e) {
    error.value = "Invalid credentials.";
  }
};
</script>