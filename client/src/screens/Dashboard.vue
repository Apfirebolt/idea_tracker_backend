<template>
  <div class="min-h-screen mt-16 bg-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold mb-6 text-gray-800">Dashboard</h1>
      <div>
        <button
          @click="openIdeaForm"
          class="bg-blue-500 text-white px-4 py-2 rounded-md shadow hover:bg-blue-600 transition duration-200"
        >
          Add Idea
        </button>
        <button
          @click="openTagForm"
          class="bg-green-500 text-white px-4 py-2 rounded-md shadow hover:bg-green-600 transition duration-200 ml-4"
        >
          Add Tag
        </button>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-semibold text-blue-600">24</span>
          <span class="text-gray-500 mt-2">Ideas</span>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-semibold text-green-600">8</span>
          <span class="text-gray-500 mt-2">In Progress</span>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-semibold text-purple-600">5</span>
          <span class="text-gray-500 mt-2">Completed</span>
        </div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-700">Recent Ideas</h2>
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th
                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
              >
                Title
              </th>
              <th
                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
              >
                Status
              </th>
              <th
                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
              >
                Created
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="idea in recentIdeas"
              :key="idea.id"
              class="hover:bg-gray-50"
            >
              <td class="px-4 py-2 text-gray-700">{{ idea.title }}</td>
              <td class="px-4 py-2">
                <span
                  :class="{
                    'bg-blue-100 text-blue-800': idea.status === 'New',
                    'bg-green-100 text-green-800':
                      idea.status === 'In Progress',
                    'bg-purple-100 text-purple-800':
                      idea.status === 'Completed',
                  }"
                  class="px-2 py-1 rounded text-xs font-semibold"
                >
                  {{ idea.status }}
                </span>
              </td>
              <td class="px-4 py-2 text-gray-500">{{ idea.created }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <TransitionRoot appear :show="isTagFormOpen" as="template">
      <Dialog as="div" @close="closeTagForm" class="relative z-10">
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
                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
              >
                <DialogTitle
                  as="h3"
                  class="text-lg font-medium leading-6 text-gray-900"
                >
                  Add Tag Form
                </DialogTitle>
                <TagForm @close="closeTagForm" />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
    <TransitionRoot appear :show="isIdeaFormOpen" as="template">
      <Dialog as="div" @close="closeIdeaForm" class="relative z-10">
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
                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
              >
                <DialogTitle
                  as="h3"
                  class="text-lg font-medium leading-6 text-gray-900"
                >
                  Add Idea Form
                </DialogTitle>
                <IdeaForm @close="closeIdeaForm" />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import IdeaForm from "../components/IdeaForm.vue";
import TagForm from "../components/TagForm.vue";
import { ref } from "vue";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";

const isIdeaFormOpen = ref(false);
const isTagFormOpen = ref(false);
const openIdeaForm = () => {
  isIdeaFormOpen.value = true;
};
const closeIdeaForm = () => {
  isIdeaFormOpen.value = false;
};

const openTagForm = () => {
  isTagFormOpen.value = true;
};
const closeTagForm = () => {
  isTagFormOpen.value = false;
};
const recentIdeas = ref([
  {
    id: 1,
    title: "Add dark mode",
    status: "In Progress",
    created: "2024-06-01",
  },
  { id: 2, title: "Mobile app support", status: "New", created: "2024-06-03" },
  { id: 3, title: "Export to CSV", status: "Completed", created: "2024-05-28" },
]);
</script>
