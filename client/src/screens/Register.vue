<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">Register</h2>
      <form @submit.prevent="register">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2" for="username"
            >Username</label
          >
          <input
            v-model="username"
            id="username"
            type="text"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            autocomplete="username"
          />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 mb-2" for="email">Email</label>
          <input
            v-model="email"
            id="email"
            type="email"
            required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            autocomplete="email"
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
            autocomplete="new-password"
          />
        </div>
        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Register
        </button>
        <p>
          Already have an account?
          <router-link to="/login" class="text-blue-600 hover:underline">
            Login
          </router-link>
        </p>
        <p v-if="error" class="text-red-500 mt-4 text-center">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useAuth } from "../store/auth";

const username = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const auth = useAuth();

const authData = computed(() => auth.getAuthData);

const register = async () => {
  error.value = "";
  if (!username.value || !email.value || !password.value) {
    error.value = "Please enter username, email, and password.";
    return;
  }
  // Simulate registration logic
  try {
    await auth.registerAction({
      username: username.value,
      email: email.value,
      password: password.value,
    });
  } catch (e) {
    error.value = "Registration failed.";
  }
};
</script>
