<template>
  <div class="min-h-screen bg-slate-50/75 py-8 px-4 sm:px-6 lg:px-8 text-slate-800">
    <div class="max-w-7xl mx-auto space-y-8">
      
      <!-- Top Action Bar -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white/80 backdrop-blur-md p-6 rounded-2xl border border-slate-200/80 shadow-sm">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-primary font-montserrat">
            Idea Hub Dashboard
          </h1>
          <p class="text-sm text-slate-500 mt-1">
            Track, prioritize, and manage conceptual workflows and tag taxonomies.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <button
            @click="openTagForm"
            class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 active:scale-[0.98] transition duration-150 cursor-pointer shadow-sm"
          >
            <TagIcon class="w-4 h-4 text-slate-500" />
            <span>Add Tag</span>
          </button>
          <button
            @click="openIdeaForm"
            class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-primary hover:bg-primary/90 active:scale-[0.98] transition duration-150 cursor-pointer shadow-sm shadow-primary/20"
          >
            <PlusIcon class="w-4 h-4" />
            <span>New Idea</span>
          </button>
        </div>
      </div>

      <!-- KPI Metrics Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <!-- Ideas Metric Card -->
        <div class="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm flex items-center justify-between">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">Total Ideas</p>
            <p class="text-3xl font-extrabold text-primary font-montserrat mt-2">
              {{ ideas.items && ideas.items.length ? ideas.items.length : 0 }}
            </p>
            <span class="text-xs text-slate-400 mt-1 inline-block">Active milestones in backlog</span>
          </div>
          <div class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
            <LightBulbIcon class="w-6 h-6" />
          </div>
        </div>

        <!-- Tags Metric Card -->
        <div class="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm flex items-center justify-between">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">Active Tags</p>
            <p class="text-3xl font-extrabold text-emerald-600 font-montserrat mt-2">
              {{ tags.length ? tags.length : 0 }}
            </p>
            <span class="text-xs text-slate-400 mt-1 inline-block">Custom categorizations</span>
          </div>
          <div class="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600">
            <TagIcon class="w-6 h-6" />
          </div>
        </div>

        <!-- Completed Metric Card -->
        <div class="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm flex items-center justify-between">
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">Completed</p>
            <p class="text-3xl font-extrabold text-secondary font-montserrat mt-2">
              {{ completedIdeas ? completedIdeas : 0 }}
            </p>
            <span class="text-xs text-slate-400 mt-1 inline-block">Archived and delivered</span>
          </div>
          <div class="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center text-secondary">
            <CheckBadgeIcon class="w-6 h-6" />
          </div>
        </div>
      </div>

      <!-- Recent Ideas Section -->
      <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div class="px-6 py-5 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-bold text-slate-900 font-montserrat">Recent Ideas</h2>
            <p class="text-xs text-slate-500 mt-0.5">Explore, search, filter, and inspect registered ideas</p>
          </div>
          <span class="text-xs font-medium px-2.5 py-1 bg-slate-100 text-slate-600 rounded-full">
            {{ ideas.items?.length || 0 }} entries
          </span>
        </div>

        <div class="p-6">
          <div v-if="ideas.items && ideas.items.length" class="rounded-xl overflow-hidden border border-slate-200/70">
            <ag-grid-vue
              class="ag-theme-alpine custom-ag-grid"
              style="width: 100%; height: 420px"
              :columnDefs="columnDefs"
              :rowData="ideas.items"
              :modules="modules"
              :defaultColDef="defaultColDef"
              :gridOptions="gridOptions"
            />
          </div>
          <div v-else class="text-center py-12">
            <LightBulbIcon class="w-10 h-10 text-slate-300 mx-auto mb-2" />
            <p class="text-sm font-medium text-slate-600">No ideas found</p>
            <p class="text-xs text-slate-400 mt-1">Click "New Idea" to register your first workflow item.</p>
          </div>
        </div>
      </div>

      <!-- Recent Tags Section -->
      <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div class="px-6 py-5 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-bold text-slate-900 font-montserrat">Defined Tags</h2>
            <p class="text-xs text-slate-500 mt-0.5">Metadata markers linked across ideas</p>
          </div>
          <span class="text-xs font-medium px-2.5 py-1 bg-slate-100 text-slate-600 rounded-full">
            {{ tags.length || 0 }} tags
          </span>
        </div>

        <div class="p-6">
          <div v-if="tags.length" class="rounded-xl overflow-hidden border border-slate-200/70">
            <ag-grid-vue
              class="ag-theme-alpine custom-ag-grid"
              style="width: 100%; height: 350px"
              :columnDefs="tagColumnDefs"
              :rowData="tags"
              :modules="modules"
              :defaultColDef="defaultColDef"
              :gridOptions="gridOptions"
            />
          </div>
          <div v-else class="text-center py-12">
            <TagIcon class="w-10 h-10 text-slate-300 mx-auto mb-2" />
            <p class="text-sm font-medium text-slate-600">No tags defined yet</p>
            <p class="text-xs text-slate-400 mt-1">Create tags to segment ideas effectively.</p>
          </div>
        </div>
      </div>

    </div>

    <!-- Tag Form Modal Dialog -->
    <TransitionRoot appear :show="isTagFormOpen" as="template">
      <Dialog as="div" @close="closeTagForm" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-200 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-150 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-200 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-150 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-2xl transition-all border border-slate-100">
                <div class="flex items-center justify-between pb-4 border-b border-slate-100">
                  <DialogTitle as="h3" class="text-lg font-bold text-primary font-montserrat">
                    {{ selectedTag ? 'Edit Tag' : 'Create New Tag' }}
                  </DialogTitle>
                  <button @click="closeTagForm" class="text-slate-400 hover:text-slate-600 transition">
                    <XMarkIcon class="w-5 h-5" />
                  </button>
                </div>
                <div class="mt-4">
                  <TagForm @close="closeTagForm" @addTag="addTag" @updateTag="editTagUtility" :tag="selectedTag" />
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Idea Form Modal Dialog -->
    <TransitionRoot appear :show="isIdeaFormOpen" as="template">
      <Dialog as="div" @close="closeIdeaForm" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-200 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-150 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-200 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-150 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white p-6 sm:p-8 text-left align-middle shadow-2xl transition-all border border-slate-100">
                <div class="flex items-center justify-between pb-4 border-b border-slate-100">
                  <DialogTitle as="h3" class="text-lg font-bold text-primary font-montserrat">
                    {{ selectedIdea ? 'Update Idea' : 'Add New Idea' }}
                  </DialogTitle>
                  <button @click="closeIdeaForm" class="text-slate-400 hover:text-slate-600 transition">
                    <XMarkIcon class="w-5 h-5" />
                  </button>
                </div>
                <div class="mt-5">
                  <IdeaForm
                    @close="closeIdeaForm"
                    @addIdea="addIdea"
                    @updateIdea="editIdeaUtility"
                    :idea="selectedIdea"
                    :tags="tags"
                  />
                </div>
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
import { useRouter } from "vue-router";
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
  TagIcon,
  LightBulbIcon,
  CheckBadgeIcon,
  XMarkIcon,
} from "@heroicons/vue/24/outline";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";

const router = useRouter();
const ideaStore = useIdeaStore();
const tagStore = useTagStore();
const isIdeaFormOpen = ref(false);
const isTagFormOpen = ref(false);
const selectedIdea = ref(null);
const selectedTag = ref(null);
const modules = ref([ClientSideRowModelModule]);

const ideas = computed(() => ideaStore.getIdeas);
const tags = computed(() => tagStore.getTags);
const completedIdeas = computed(() => ideaStore.getCompletedIdeasCount);

// Clean styled cell renderers
const columnDefs = ref([
  {
    field: "id",
    headerName: "ID",
    width: 90,
    maxWidth: 100,
    sortable: true,
    filter: true,
    cellClass: "font-mono text-xs text-slate-500 font-semibold flex items-center",
  },
  {
    field: "title",
    headerName: "Title",
    flex: 1.5,
    minWidth: 160,
    sortable: true,
    filter: true,
    cellClass: "font-semibold text-slate-900 flex items-center",
  },
  {
    field: "status",
    headerName: "Status",
    width: 140,
    sortable: true,
    filter: true,
    cellRenderer: (params) => {
      const val = params.value ? params.value.toLowerCase() : "pending";
      const isDone = val === "completed" || val === "done";
      const badge = document.createElement("span");
      badge.innerText = params.value || "Draft";
      badge.className = isDone
        ? "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200"
        : "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200";
      return badge;
    },
  },
  {
    field: "description",
    headerName: "Description",
    flex: 2,
    minWidth: 200,
    sortable: true,
    filter: true,
    cellClass: "text-slate-600 text-sm flex items-center truncate",
  },
  {
    headerName: "Actions",
    field: "actions",
    width: 210,
    suppressMenu: true,
    sortable: false,
    filter: false,
    cellRenderer: (params) => {
      const container = document.createElement("div");
      container.className = "flex items-center gap-1.5 h-full";

      const viewBtn = document.createElement("button");
      viewBtn.innerText = "View";
      viewBtn.className = "px-2.5 py-1 text-xs font-medium text-slate-700 hover:bg-slate-100 rounded-md transition";
      viewBtn.onclick = () => goToIdeaDetail(params.data.id);

      const editBtn = document.createElement("button");
      editBtn.innerText = "Edit";
      editBtn.className = "px-2.5 py-1 text-xs font-medium text-secondary hover:bg-secondary/10 rounded-md transition";
      editBtn.onclick = () => editIdea(params.data);

      const deleteBtn = document.createElement("button");
      deleteBtn.innerText = "Delete";
      deleteBtn.className = "px-2.5 py-1 text-xs font-medium text-danger hover:bg-danger/10 rounded-md transition";
      deleteBtn.onclick = () => deleteIdea(params.data.id);

      container.appendChild(viewBtn);
      container.appendChild(editBtn);
      container.appendChild(deleteBtn);

      return container;
    },
  },
]);

const tagColumnDefs = ref([
  {
    field: "id",
    headerName: "ID",
    width: 90,
    maxWidth: 100,
    sortable: true,
    filter: true,
    cellClass: "font-mono text-xs text-slate-500 font-semibold flex items-center",
  },
  {
    field: "name",
    headerName: "Tag Name",
    flex: 1,
    sortable: true,
    filter: true,
    cellRenderer: (params) => {
      const tag = document.createElement("span");
      tag.innerText = `# ${params.value}`;
      tag.className = "inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-slate-100 text-slate-700";
      return tag;
    },
  },
  {
    headerName: "Actions",
    field: "actions",
    width: 150,
    suppressMenu: true,
    sortable: false,
    filter: false,
    cellRenderer: (params) => {
      const container = document.createElement("div");
      container.className = "flex items-center gap-1.5 h-full";

      const editBtn = document.createElement("button");
      editBtn.innerText = "Edit";
      editBtn.className = "px-2.5 py-1 text-xs font-medium text-secondary hover:bg-secondary/10 rounded-md transition";
      editBtn.onclick = () => editTag(params.data);

      const deleteBtn = document.createElement("button");
      deleteBtn.innerText = "Delete";
      deleteBtn.className = "px-2.5 py-1 text-xs font-medium text-danger hover:bg-danger/10 rounded-md transition";
      deleteBtn.onclick = () => deleteTag(params.data.id);

      container.appendChild(editBtn);
      container.appendChild(deleteBtn);

      return container;
    },
  },
]);

const defaultColDef = ref({
  flex: 1,
  minWidth: 100,
  resizable: true,
});

const gridOptions = ref({
  animateRows: true,
  rowHeight: 48,
  headerHeight: 44,
});

const openIdeaForm = () => {
  selectedIdea.value = null;
  isIdeaFormOpen.value = true;
};
const closeIdeaForm = () => {
  isIdeaFormOpen.value = false;
};

const openTagForm = () => {
  selectedTag.value = null;
  isTagFormOpen.value = true;
};
const closeTagForm = () => {
  isTagFormOpen.value = false;
};

const addIdea = async (idea) => {
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

const goToIdeaDetail = (ideaId) => {
  router.push({ name: "IdeaDetail", params: { ideaId } });
};

onMounted(async () => {
  await ideaStore.getIdeasAction();
  await tagStore.getTagsAction();
});
</script>

<style scoped>
.custom-ag-grid {
  --ag-border-color: #f1f5f9;
  --ag-header-background-color: #f8fafc;
  --ag-header-foreground-color: #475569;
  --ag-header-cell-hover-background-color: #f1f5f9;
  --ag-odd-row-background-color: #ffffff;
  --ag-row-hover-color: #f8fafc;
  --ag-selected-row-background-color: #f1f5f9;
  --ag-font-family: inherit;
  --ag-font-size: 13px;
}
</style>