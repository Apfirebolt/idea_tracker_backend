<template>
  <div class="min-h-screen mt-16 bg-gray-100 p-8">
    <Loader v-if="loading" />
    <div class="max-w-7xl mx-auto">
      <div
        v-if="idea"
        class="flex justify-between items-center bg-white px-4 py-3"
      >
        <h1 class="text-3xl font-bold text-primary">{{ idea.title }}</h1>

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

      <div v-if="idea.tags && idea.tags.length" class="mt-4">
        <h2
          class="font-semibold mb-4 text-2xl text-center text-primary bg-white p-2"
        >
          Tags:
        </h2>
        <div class="flex flex-wrap justify-center gap-2">
          <span
            v-for="tag in idea.tags"
            :key="tag.id"
            class="bg-secondary text-white px-2 py-1 rounded"
          >
            {{ tag.name }}
          </span>
        </div>
      </div>
      <div
        v-if="idea.scripts && idea.scripts.length === 0"
        class="mt-8 text-center text-gray-500 text-lg"
      >
        No scripts have been added yet.
      </div>

      <div v-if="idea.scripts && idea.scripts.length > 0" class="mt-4">
        <h2
          class="font-semibold mb-4 text-2xl text-center text-primary bg-white p-2"
        >
          Scripts
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="script in idea.scripts"
            :key="script.id"
            class="bg-white rounded-lg shadow-lg p-5 flex flex-col"
          >
            <h3 class="text-xl font-semibold mb-2">{{ script.title }}</h3>
            <p class="text-gray-600 mb-4">{{ script.script_content }}</p>
            <div class="flex space-x-2 mt-4">
              <button
                @click="openEditScriptForm(script)"
                class="bg-info text-dark px-3 py-1 rounded hover:bg-blue-800 hover:text-light transition text-sm flex items-center"
              >
                <PencilIcon class="w-4 h-4 mr-1" />
                Edit
              </button>
              <button
                @click="deleteScript(script.id)"
                class="bg-danger text-white px-3 py-1 rounded hover:bg-red-600 transition text-sm flex items-center"
              >
                <TrashIcon class="w-4 h-4 mr-1" />
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
      <!-- Comment box if the idea is shared -->
      <div
        v-if="idea.is_shared === 1"
        class="mt-8 bg-white p-4 rounded-lg shadow-md"
      >
        <h2 class="text-xl font-semibold mb-4 text-center text-primary">
          Comments
        </h2>
        <p class="text-gray-600 text-center">
          This idea is shared. You can add comments here.
        </p>
        <!-- Comment form or component can be added here -->
        <div class="mt-4">
          <div class="relative">
            <textarea
              v-model="commentText"
              placeholder="Add a comment..."
              class="w-full p-2 border rounded focus:outline-none focus:ring focus:border-blue-300 pl-10"
              rows="3"
            ></textarea>
            <PencilIcon
              class="w-5 h-5 text-gray-400 absolute left-3 top-3 pointer-events-none"
            />
          </div>
          <button
            @click="addComment"
            class="mt-2 bg-primary text-white px-4 py-2 rounded-md shadow hover:bg-blue-600 transition duration-200 flex items-center"
          >
            <PlusIcon class="w-5 h-5 mr-2" />
            Add Comment
          </button>
        </div>
      </div>
      {{ user }}
      <!-- Show all comments -->
      <div v-if="idea.comments && idea.comments.length > 0" class="mt-6">
        <h2 class="text-xl font-semibold mb-4 text-center text-primary">
          All Comments
        </h2>
        <ul class="space-y-4">
          <li
            v-for="comment in idea.comments"
            :key="comment.id"
            class="bg-white p-4 rounded-lg shadow-md"
          >
            <p class="text-gray-800">{{ comment.content }}</p>
            <p class="text-gray-500 text-sm mt-1">
              {{ new Date(comment.created_at).toLocaleString() }}
            </p>
            <div
              v-if="user && user.user.id === comment.user_id"
              class="flex space-x-2 mt-2"
            >
              <button
                @click="
                  ideaStore
                    .deleteComment(comment.id)
                    .then(() => ideaStore.getIdeaAction(idea.value.id))
                "
                class="bg-danger text-white px-3 py-1 rounded hover:bg-red-600 transition text-sm flex items-center"
              >
                <TrashIcon class="w-4 h-4 mr-1" />
                Delete
              </button>
              <button
                @click="ideaStore.startEditComment(comment)"
                class="bg-info text-dark px-3 py-1 rounded hover:bg-blue-800 hover:text-light transition text-sm flex items-center"
              >
                <PencilIcon class="w-4 h-4 mr-1" />
                Edit
              </button>
            </div>
          </li>
        </ul>
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
                <ScriptForm
                  @close="closeScriptForm"
                  @addScript="addScript"
                  :script="selectedScript"
                  @updateScript="updateScript"
                />
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
import { useAuth } from "../store/auth";
import { useScriptStore } from "../store/script";
import { onMounted, ref, computed } from "vue";
import ScriptForm from "../components/ScriptForm.vue";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { PlusIcon, TrashIcon, PencilIcon } from "@heroicons/vue/solid";
import Loader from "../components/Loader.vue";

const route = useRoute();
const ideaStore = useIdeaStore();
const scriptStore = useScriptStore();
const authStore = useAuth();
const selectedScript = ref(null);
const isScriptFormOpen = ref(false);
const commentText = ref("");
const idea = computed(() => ideaStore.getIdea);
const loading = computed(() => ideaStore.loading);
const user = computed(() => authStore.getAuthData);

const openScriptForm = () => {
  isScriptFormOpen.value = true;
};
const closeScriptForm = () => {
  isScriptFormOpen.value = false;
};

const addScript = async (script) => {
  console.log("Adding idea:", script);
  closeScriptForm();
  // add idea_id to the script
  const ideaId = route.params.ideaId;
  script.idea_id = idea.value.id;
  await scriptStore.addScript(script);
  await ideaStore.getIdeaAction(ideaId);
};

const deleteScript = async (scriptId) => {
  console.log("Deleting script with ID:", scriptId);
  await scriptStore.deleteScript(scriptId);
  await ideaStore.getIdeaAction(idea.value.id);
};

const openEditScriptForm = (script) => {
  isScriptFormOpen.value = true;
  selectedScript.value = script;
};

const updateScript = async (script) => {
  await scriptStore.updateScript(script);
  await ideaStore.getIdeaAction(idea.value.id);
};

const addComment = async () => {
  if (!commentText.value.trim()) {
    return;
  }

  const payload = {
    idea_id: idea.value.id,
    content: commentText.value,
  };
  await ideaStore.addComment(payload);
  await ideaStore.getIdeaAction(idea.value.id);
  commentText.value = "";
};

onMounted(async () => {
  const ideaId = route.params.ideaId;
  await ideaStore.getIdeaAction(ideaId);
});
</script>
