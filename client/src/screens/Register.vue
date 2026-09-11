<template>
  <div class="min-h-screen flex items-center justify-center bg-light px-4 sm:px-6 lg:px-8 py-10">
    <!-- Card Container -->
    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl border border-gray-100 p-8 sm:p-10 transition-all">
      
      <!-- Brand & Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-primary/10 text-primary mb-3">
          <UserPlusIcon class="w-6 h-6 text-primary" />
        </div>
        <h1 class="text-2xl sm:text-3xl font-bold text-primary tracking-tight">
          Create an account
        </h1>
        <p class="text-sm text-dark/70 mt-1">
          Join today and get started in seconds
        </p>
      </div>

      <!-- Registration Form -->
      <form @submit.prevent="register" class="space-y-4">
        <!-- Error Alert -->
        <div
          v-if="error"
          class="flex items-center gap-2 p-3 text-sm text-danger bg-danger/10 border border-danger/20 rounded-lg"
          role="alert"
        >
          <ExclamationCircleIcon class="w-5 h-5 shrink-0" />
          <span>{{ error }}</span>
        </div>

        <!-- Username Field -->
        <div>
          <label for="username" class="block text-xs font-semibold uppercase tracking-wider text-dark/80 mb-1.5">
            Username
          </label>
          <div class="relative">
            <input
              v-model="username"
              id="username"
              type="text"
              placeholder="johndoe"
              required
              class="w-full pl-10 pr-4 py-2.5 text-sm text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200"
              autocomplete="username"
            />
            <UserIcon class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>

        <!-- Email Field -->
        <div>
          <label for="email" class="block text-xs font-semibold uppercase tracking-wider text-dark/80 mb-1.5">
            Email Address
          </label>
          <div class="relative">
            <input
              v-model="email"
              id="email"
              type="email"
              placeholder="name@company.com"
              required
              class="w-full pl-10 pr-4 py-2.5 text-sm text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200"
              autocomplete="email"
            />
            <EnvelopeIcon class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>

        <!-- Password Field -->
        <div>
          <label for="password" class="block text-xs font-semibold uppercase tracking-wider text-dark/80 mb-1.5">
            Password
          </label>
          <div class="relative">
            <input
              v-model="password"
              id="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="At least 8 characters"
              required
              class="w-full pl-10 pr-10 py-2.5 text-sm text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200"
              autocomplete="new-password"
            />
            <LockClosedIcon class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-dark transition-colors focus:outline-none"
              tabindex="-1"
            >
              <EyeSlashIcon v-if="showPassword" class="w-5 h-5" />
              <EyeIcon v-else class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full mt-2 flex items-center justify-center gap-2 py-2.5 px-4 bg-primary text-white font-medium text-sm rounded-xl shadow-md shadow-primary/25 hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 active:scale-[0.99] disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-200 cursor-pointer"
        >
          <svg
            v-if="isLoading"
            class="animate-spin h-4 w-4 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
          </svg>
          <span>{{ isLoading ? "Creating account..." : "Create Account" }}</span>
        </button>
      </form>

      <!-- Footer -->
      <div class="mt-8 pt-6 border-t border-gray-100 text-center">
        <p class="text-sm text-dark/70">
          Already have an account?
          <router-link
            to="/login"
            class="font-semibold text-secondary hover:text-primary transition-colors ml-1"
          >
            Sign in
          </router-link>
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuth } from "../store/auth";
import {
  EnvelopeIcon,
  LockClosedIcon,
  UserIcon,
  UserPlusIcon,
  EyeIcon,
  EyeSlashIcon,
  ExclamationCircleIcon,
} from "@heroicons/vue/24/solid";

const username = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const showPassword = ref(false);
const isLoading = ref(false);

const auth = useAuth();

const register = async () => {
  error.value = "";

  if (!username.value || !email.value || !password.value) {
    error.value = "Please fill in all fields.";
    return;
  }

  isLoading.value = true;
  try {
    await auth.registerAction({
      username: username.value,
      email: email.value,
      password: password.value,
    });
  } catch (e) {
    error.value = e?.response?.data?.message || "Registration failed. Please try again.";
  } finally {
    isLoading.value = false;
  }
};
</script>