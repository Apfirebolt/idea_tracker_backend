<template>
  <div class="min-h-screen flex items-center justify-center bg-light px-4 sm:px-6 lg:px-8">
    <!-- Card Container -->
    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl border border-gray-100 p-8 sm:p-10 transition-all">
      
      <!-- Brand & Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-primary/10 text-primary mb-3">
          <LockClosedIcon class="w-6 h-6 text-primary" />
        </div>
        <h1 class="text-2xl sm:text-3xl font-bold text-primary tracking-tight">
          Welcome back
        </h1>
        <p class="text-sm text-dark/70 mt-1">
          Enter your details to access your account
        </p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="login" class="space-y-5">
        <!-- Error Alert -->
        <div
          v-if="error"
          class="flex items-center gap-2 p-3 text-sm text-danger bg-danger/10 border border-danger/20 rounded-lg"
          role="alert"
        >
          <ExclamationCircleIcon class="w-5 h-5 shrink-0" />
          <span>{{ error }}</span>
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
              autocomplete="username"
            />
            <EnvelopeIcon class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>

        <!-- Password Field -->
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label for="password" class="block text-xs font-semibold uppercase tracking-wider text-dark/80">
              Password
            </label>
            <router-link
              to="/forgot-password"
              class="text-xs font-medium text-secondary hover:text-primary transition-colors"
            >
              Forgot password?
            </router-link>
          </div>
          <div class="relative">
            <input
              v-model="password"
              id="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
              required
              class="w-full pl-10 pr-10 py-2.5 text-sm text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200"
              autocomplete="current-password"
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
          class="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-primary text-white font-medium text-sm rounded-xl shadow-md shadow-primary/25 hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 active:scale-[0.99] disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-200 cursor-pointer"
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
          <span>{{ isLoading ? "Signing in..." : "Sign In" }}</span>
        </button>
      </form>

      <!-- Footer -->
      <div class="mt-8 pt-6 border-t border-gray-100 text-center">
        <p class="text-sm text-dark/70">
          Don't have an account?
          <router-link
            to="/register"
            class="font-semibold text-secondary hover:text-primary transition-colors ml-1"
          >
            Create an account
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
  EyeIcon,
  EyeSlashIcon,
  ExclamationCircleIcon,
} from "@heroicons/vue/24/solid";

const email = ref("");
const password = ref("");
const error = ref("");
const showPassword = ref(false);
const isLoading = ref(false);

const auth = useAuth();

const login = async () => {
  error.value = "";

  if (!email.value || !password.value) {
    error.value = "Please enter both email and password.";
    return;
  }

  isLoading.value = true;
  try {
    await auth.loginAction({
      email: email.value,
      password: password.value,
    });
  } catch (e) {
    error.value = e?.response?.data?.message || "Invalid email or password.";
  } finally {
    isLoading.value = false;
  }
};
</script>