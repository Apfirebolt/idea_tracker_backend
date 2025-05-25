<template>
  <div class="min-h-screen mt-16 bg-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
      <div v-if="idea" class="flex justify-between items-center">
        <h1 class="text-3xl font-bold mb-6 text-gray-800">{{ idea.title }}</h1>

        <div class="flex space-x-2">
          <button
            @click="openScriptForm"
            class="bg-primary text-white px-4 py-2 rounded-md shadow hover:bg-blue-600 transition duration-200 flex items-center"
          >
            <PlusIcon class="w-5 h-5 mr-2" />
            Add Script
          </button>
        </div>
      </div>
      
      <div v-if="idea.tags && idea.tags.length">
        <h2 class="font-semibold mb-1">Tags:</h2>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in idea.tags"
            :key="tag.id"
            class="bg-secondary text-white px-2 py-1 rounded text-sm"
          >
            {{ tag.name }}
          </span>
        </div>
      </div>
      <div class="mt-6">
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
    <TransitionRoot appear :show="isScriptFormOpen" as="template">
      <Dialog as="div" @close="closeScriptForm" class="relative z-10">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div
            class="flex min-h-full items-center justify-center p-4 text-center"
          >
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel
                class="w-full max-w-xl transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
              >
                <DialogTitle
                  as="h3"
                  class="text-lg font-medium leading-6 text-center my-3 p-2 bg-secondary text-gray-900"
                >
                  Add Script Form
                </DialogTitle>
                <ScriptForm @close="closeScriptForm" @addTag="addScript" />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { useIdeaStore } from "../store/idea";
import { useScriptStore } from "../store/script";
import { onMounted, ref, computed } from "vue";
import ScriptForm from "../components/ScriptForm.vue";
import { PlusIcon } from "@heroicons/vue/solid";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import Loader from "../components/Loader.vue";

const route = useRoute();
const ideaStore = useIdeaStore();
const scriptStore = useScriptStore();
const isScriptFormOpen = ref(false);
const idea = computed(() => ideaStore.getIdea);
const loading = computed(() => ideaStore.loading);

const openScriptForm = () => {
  isScriptFormOpen.value = true;
};
const closeScriptForm = () => {
  isScriptFormOpen.value = false;
};

const addScript = async (idea) => {
  console.log("Adding idea:", idea);
  closeIdeaForm();
  await scriptStore.addScript(idea);
  await ideaStore.getIdeasAction();
};

onMounted(async () => {
  const ideaId = route.params.ideaId;
  await ideaStore.getIdeaAction(ideaId);
});
</script>
