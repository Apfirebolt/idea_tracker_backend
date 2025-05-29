<template>
  <div class="min-h-screen mt-16 bg-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
      <div
        class="flex justify-between items-center bg-white px-4 py-6 rounded-lg shadow-lg mb-6"
      >
        <h1 class="text-3xl font-bold text-primary">Explore Ideas</h1>
      </div>
      <div
        v-if="sharedIdeas.items && sharedIdeas.items.length === 0"
        class="text-center text-gray-500 text-lg"
      >
        No ideas shared yet.
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="idea in sharedIdeas.items"
          :key="idea.id"
          class="bg-white rounded-lg shadow-lg p-5 flex flex-col cursor-pointer hover:shadow-xl transition-shadow duration-200"
          @click="goToIdeaDetail(idea.id)"
        >
          <h3 class="text-xl font-semibold mb-2">{{ idea.title }}</h3>
          <p class="text-gray-600 mb-4">{{ idea.description }}</p>
          <div class="flex space-x-2 mt-4">
            <span
              v-for="tag in idea.tags"
              :key="tag.id"
              class="bg-secondary text-white px-2 py-1 rounded"
            >
              {{ tag.name }}
            </span>
          </div>
        </div>
      </div>

      <div
        class="flex justify-between items-center bg-white px-4 mt-4 py-6 rounded-lg shadow-lg mb-6"
      >
        <h1 class="text-3xl font-bold text-primary">Explore Users</h1>
      </div>
      <div
        v-if="users.items && users.items.length === 0"
        class="text-center text-gray-500 text-lg"
      >
        No users found.
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="user in users.items"
          :key="user.id"
          class="bg-white rounded-lg shadow-lg p-5 flex flex-col cursor-pointer hover:shadow-xl transition-shadow duration-200"
          @click="goToUserProfile(user.id)"
        >
          <h3 class="text-xl font-semibold mb-2">{{ user.name }}</h3>
          <p class="text-gray-600 mb-4">{{ user.email }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useIdeaStore } from "../store/idea";
import { useUserStore } from "../store/user";
import { useRouter } from "vue-router";
import { computed, onMounted } from "vue";

const router = useRouter();
const ideaStore = useIdeaStore();
const userStore = useUserStore();

const sharedIdeas = computed(() => ideaStore.getSharedIdeas);
const users = computed(() => userStore.getUsers);

const goToIdeaDetail = (ideaId) => {
  router.push({ name: "IdeaDetail", params: { ideaId } });
};

const goToUserProfile = (userId) => {
  router.push({ name: "UserDetail", params: { userId } });
};

onMounted(async () => {
  await ideaStore.getSharedIdeasAction();
  await userStore.getUsersAction();
});
</script>
