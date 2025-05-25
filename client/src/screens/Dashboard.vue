<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold mb-6 text-gray-800">Dashboard</h1>
        <div class="flex space-x-2">
          <button
            @click="openIdeaForm"
            class="bg-primary text-white px-4 py-2 rounded-md shadow hover:bg-blue-600 transition duration-200 flex items-center"
          >
            <PlusIcon class="w-5 h-5 mr-2" />
            Add Idea
          </button>
          <button
            @click="openTagForm"
            class="bg-secondary text-dark px-4 py-2 rounded-md shadow hover:bg-green-600 transition duration-200 ml-4 flex items-center"
          >
            <PlusIcon class="w-5 h-5 mr-2" />
            Add Tag
          </button>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-semibold text-tertiary">{{ ideas.items && ideas.items.length ? ideas.items.length : 0 }}</span>
          <span class="text-gray-500 mt-2">Ideas</span>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-semibold text-green-600">{{ tags.length ? tags.length : 0 }}</span>
          <span class="text-gray-500 mt-2">Tags</span>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <span class="text-2xl font-semibold text-tertiary">5</span>
          <span class="text-gray-500 mt-2">Completed</span>
        </div>
      </div>

      <div class="bg-light rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-700">Recent Ideas</h2>
        <ag-grid-vue
          v-if="ideas.items && ideas.items.length"
          class="ag-theme-alpine"
          style="width: 100%; height: 400px"
          :columnDefs="columnDefs"
          :rowData="ideas.items"
          :modules="modules"
          :defaultColDef="defaultColDef"
          :gridOptions="gridOptions"
        />
        <div v-else class="text-center text-gray-500">No ideas available.</div>
      </div>
      <div class="bg-light rounded-lg shadow p-6 mt-4">
        <h2 class="text-xl font-semibold mb-4 text-gray-700">Recent Tags</h2>
        <ag-grid-vue
          v-if="tags.length"
          class="ag-theme-alpine"
          style="width: 100%; height: 400px"
          :columnDefs="tagColumnDefs"
          :rowData="tags"
          :modules="modules"
          :defaultColDef="defaultColDef"
          :gridOptions="gridOptions"
        />
        <div v-else class="text-center text-gray-500">No tags available.</div>
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
                  class="text-lg font-medium leading-6 text-center my-3 p-2 bg-secondary text-gray-900"
                >
                  Add Tag Form
                </DialogTitle>
                <TagForm @close="closeTagForm" @addTag="addTag" @updateTag="editTagUtility" :tag="selectedTag" />
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
                  class="text-lg font-medium leading-6 text-center my-3 bg-secondary p-2 text-gray-900"
                >
                  Add Idea Form
                </DialogTitle>
                <IdeaForm @close="closeIdeaForm" @addIdea="addIdea" @updateIdea="editIdeaUtility" :idea="selectedIdea" :tags="tags" />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { useIdeaStore } from "../store/idea";
import { useTagStore } from "../store/tag";
import IdeaForm from "../components/IdeaForm.vue";
import TagForm from "../components/TagForm.vue";
import { ref, computed, onMounted } from "vue";
import "@ag-grid-community/styles/ag-grid.css";
import "@ag-grid-community/styles/ag-theme-alpine.css";
import { ClientSideRowModelModule } from "@ag-grid-community/client-side-row-model";
import { AgGridVue } from "@ag-grid-community/vue3";
import {
  PlusIcon,
} from "@heroicons/vue/solid";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";

// ag grid config
const columnDefs = ref([
  { field: "id", headerName: "ID", sortable: true, filter: true },
  { field: "title", headerName: "Name", sortable: true, filter: true },
  {
    field: "description",
    headerName: "Description",
    sortable: true,
    filter: true,
  },
  {
    headerName: "Actions",
    field: "actions",
    cellRenderer: (params) => {
      const container = document.createElement("div");
      container.style.display = "flex";
      container.style.gap = "1rem";

      // Edit button
      const editBtn = document.createElement("button");
      editBtn.innerText = "Edit";
      editBtn.className =
      "bg-secondary text-white px-3 py-1 rounded hover:bg-blue-600";
      editBtn.onclick = () => {
      editIdea(params.data);
      };

      // Delete button
      const deleteBtn = document.createElement("button");
      deleteBtn.innerText = "Delete";
      deleteBtn.className =
      "bg-danger text-white px-3 py-1 rounded hover:bg-red-600";
      deleteBtn.onclick = () => {
      deleteIdea(params.data.id);
      };

      container.appendChild(editBtn);
      container.appendChild(deleteBtn);

      return container;
    },
    width: 120,
    suppressMenu: true,
    sortable: false,
    filter: false,
  },
]);

const tagColumnDefs = ref([
  { field: "id", headerName: "ID", sortable: true, filter: true },
  { field: "name", headerName: "Tag Name", sortable: true, filter: true },
  {
    headerName: "Actions",
    field: "actions",
    cellRenderer: (params) => {
      const container = document.createElement("div");
      container.style.display = "flex";
      container.style.gap = "0.5rem";

      // Edit button
      const editBtn = document.createElement("button");
      editBtn.innerText = "Edit";
      editBtn.className =
      "bg-secondary text-white px-3 py-1 rounded hover:bg-blue-600";
      editBtn.onclick = () => {
      editTag(params.data);
      };

      // Delete button
      const deleteBtn = document.createElement("button");
      deleteBtn.innerText = "Delete";
      deleteBtn.className =
      "bg-danger text-white px-3 py-1 rounded hover:bg-red-600";
      deleteBtn.onclick = () => {
      deleteTag(params.data.id);
      };

      container.appendChild(editBtn);
      container.appendChild(deleteBtn);

      return container;
    },
    width: 120,
    suppressMenu: true,
    sortable: false,
    filter: false,
  },
]);

const ideaStore = useIdeaStore();
const tagStore = useTagStore();
const isIdeaFormOpen = ref(false);
const isTagFormOpen = ref(false);
const selectedIdea = ref(null);
const selectedTag = ref(null);
const modules = ref([ClientSideRowModelModule]);

const ideas = computed(() => ideaStore.getIdeas);
const tags = computed(() => tagStore.getTags);

const defaultColDef = ref({
  flex: 1,
  minWidth: 100,
  resizable: true,
});

const gridOptions = ref({
  animateRows: true,
  rowHeight: 50,
  headerHeight: 50,
});

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

const addIdea = async (idea) => {
  console.log("Adding idea:", idea);
  closeIdeaForm();
  await ideaStore.addIdea(idea);
  await ideaStore.getIdeasAction();
};

const addTag = async (tag) => {
  closeTagForm();
  await tagStore.addTag(tag);
  await tagStore.getTagsAction();
};

const deleteIdea = async (id) => {
  await ideaStore.deleteIdea(id);
  await ideaStore.getIdeasAction();
};

const deleteTag = async (id) => {
  await tagStore.deleteTag(id);
  await tagStore.getTagsAction();
};

const editIdea = async (payload) => {
  selectedIdea.value = payload;
  isIdeaFormOpen.value = true;
};

const editIdeaUtility = async (payload) => {
  await ideaStore.updateIdea(payload);
  await ideaStore.getIdeasAction();
  closeIdeaForm();
  selectedIdea.value = null;
};

const editTag = async (payload) => {
  selectedTag.value = payload;
  isTagFormOpen.value = true;
};

const editTagUtility = async (payload) => {
  await tagStore.updateTag(payload);
  await tagStore.getTagsAction();
  closeTagForm();
  selectedTag.value = null;
};

onMounted(async () => {
  await ideaStore.getIdeasAction();
  await tagStore.getTagsAction();
});
</script>
