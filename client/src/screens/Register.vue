<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">Register</h2>
      <form @submit.prevent="register">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2" for="username">Username</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3">
              <UserIcon class="h-5 w-5 text-gray-400" />
            </span>
            <input
              v-model="username"
              id="username"
              placeholder="Enter your username"
              type="text"
              required
              class="w-full pl-10 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              autocomplete="username"
            />
          </div>
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 mb-2" for="email">Email</label>
          <div class="relative">
            <MailIcon class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
            <input
              v-model="email"
              placeholder="Enter your email"
              id="email"
              type="email"
              required
              class="w-full pl-10 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              autocomplete="email"
            />
          </div>
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 mb-2" for="password">Password</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3">
              <LockClosedIcon class="h-5 w-5 text-gray-400" />
            </span>
            <input
              v-model="password"
              placeholder="Enter your password"
              id="password"
              type="password"
              required
              class="w-full pl-10 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              autocomplete="new-password"
            />
          </div>
        </div>
        <button
          type="submit"
          class="w-full bg-primary text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Register
        </button>
        <p class="my-3">
          Already have an account?
          <router-link to="/login" class="text-tertiary hover:underline">
            Login
          </router-link>
        </p>
        <p v-if="error" class="text-red-500 mt-4 text-center">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuth } from "../store/auth";
import {
  MailIcon,
  LockClosedIcon,
  UserIcon
} from "@heroicons/vue/solid";

const username = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const auth = useAuth();

const register = async () => {
  error.value = "";
  if (!username.value || !email.value || !password.value) {
    error.value = "Please enter username, email, and password.";
    return;
  }
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
