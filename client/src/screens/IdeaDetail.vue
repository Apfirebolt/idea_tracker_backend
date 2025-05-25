<template>
    <div class="max-w-2xl mx-auto p-8 bg-white rounded shadow mt-8">
        <button @click="$router.back()" class="mb-4 text-blue-600 hover:underline">&larr; Back</button>
        <Loader v-if="loading" />
        <div v-if="idea">
            <h1 class="text-2xl font-bold mb-2">{{ idea.title }}</h1>
            <div class="mb-2 text-gray-600">Status: <span class="font-semibold">{{ idea.status }}</span></div>
            <div class="mb-4 text-gray-700">{{ idea.description }}</div>
            <div v-if="idea.tags && idea.tags.length">
                <h2 class="font-semibold mb-1">Tags:</h2>
                <div class="flex flex-wrap gap-2">
                    <span v-for="tag in idea.tags" :key="tag.id" class="bg-secondary text-white px-2 py-1 rounded text-sm">
                        {{ tag.name }}
                    </span>
                </div>
            </div>
        </div>
        <div v-else class="text-gray-500">Loading...</div>
    </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { useIdeaStore } from "../store/idea";
import { onMounted, computed } from "vue";
import Loader from "../components/Loader.vue";

const route = useRoute();
const ideaStore = useIdeaStore();
const idea = computed(() => ideaStore.getIdea);
const loading = computed(() => ideaStore.loading);

onMounted(async () => {
    const ideaId = route.params.ideaId;
    await ideaStore.getIdeaAction(ideaId);
});
</script>
