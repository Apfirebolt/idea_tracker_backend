<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">Login</h2>
      <Message v-if="message" :message="message" type="success" />
      <Message v-if="errorMessage" :message="errorMessage" type="error" />
      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2" for="email">Email</label>
          <div class="relative">
            <input
              v-model="email"
              id="email"
              type="email"
              placeholder="Enter your email"
              required
              class="w-full px-3 py-2 pl-10 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              autocomplete="username"
            />
            <MailIcon class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
          </div>
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 mb-2" for="password">Password</label>
          <div class="relative">
            <input
              v-model="password"
              id="password"
              type="password"
              placeholder="Enter your password"
              required
              class="w-full px-3 py-2 pl-10 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              autocomplete="current-password"
            />
            <LockClosedIcon class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
          </div>
        </div>
        <button
          type="submit"
          class="w-full bg-primary text-white py-2 rounded hover:bg-blue-700 transition"
        >
          <span class="inline-flex items-center justify-center">
            Login
          </span>
        </button>
        <p class="my-3">
          Don't have an account?
          <router-link to="/register" class="text-tertiary hover:underline">
            Register
          </router-link>
        </p>
        <p v-if="error" class="text-danger mt-4 text-center">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useAuth } from "../store/auth";
import Message from "../components/Message.vue";

// Import icons from @heroicons/vue/24/outline (install with: npm i @heroicons/vue)
import {
  MailIcon,
  LockClosedIcon
} from "@heroicons/vue/solid";

const email = ref("");
const password = ref("");
const error = ref("");
const auth = useAuth();
const message = computed(() => auth.message);
const errorMessage = computed(() => auth.error);

const login = async () => {
  error.value = "";
  if (!email.value || !password.value) {
    error.value = "Please enter both email and password.";
    return;
  }
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