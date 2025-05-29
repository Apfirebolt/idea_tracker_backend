<template>
  <div class="min-h-screen mt-16 bg-gray-100 p-8">
    <Loader v-if="loading" />
    <div class="max-w-2xl mx-auto bg-white p-8 rounded shadow">
      <h1 class="text-3xl font-bold text-primary mb-6 text-center">
        User Details
      </h1>
      <div v-if="user" class="space-y-4">
        <div>
          <span class="font-semibold text-gray-700">Username:</span>
          <span class="ml-2 text-gray-900">{{ user.username }}</span>
        </div>
        <div>
          <span class="font-semibold text-gray-700">Email:</span>
          <span class="ml-2 text-gray-900">{{ user.email }}</span>
        </div>
        <!-- Add more user fields as needed -->
      </div>
      <div v-else class="text-center text-gray-500">
        No user data available.
      </div>
      <div class="mt-8 text-center">
        <router-link
          to="-1"
          class="inline-flex items-center text-primary hover:underline"
          @click.prevent="$router.back()"
        >
          <svg
            class="w-5 h-5 mr-1"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M15 19l-7-7 7-7"
            />
          </svg>
          Back
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from "../store/user";
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import Loader from "../components/Loader.vue";

const route = useRoute();
const userStore = useUserStore();
const user = computed(() => userStore.getUser);
const loading = computed(() => user.loading);

onMounted(async () => {
  const userId = route.params.userId;
  if (userId) {
    await userStore.getUserAction(userId);
  } else {
    console.error("User ID is not provided in the route parameters.");
  }
});
</script>
