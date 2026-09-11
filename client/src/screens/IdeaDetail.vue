<template>
  <div class="min-h-screen bg-slate-50/75 py-8 px-4 sm:px-6 lg:px-8 text-slate-800">
    <Loader v-if="loading" />

    <div class="max-w-6xl mx-auto space-y-8">
      <!-- Top Navigation & Back Action -->
      <div>
        <button
          @click="$router.back()"
          class="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-primary transition-colors cursor-pointer"
        >
          <ArrowLeftIcon class="w-4 h-4" />
          <span>Back to Ideas</span>
        </button>
      </div>

      <!-- Idea Header & Overview Card -->
      <section v-if="idea" class="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 shadow-xs space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 pb-6 border-b border-slate-100">
          <div class="space-y-3 max-w-3xl">
            <div class="flex flex-wrap items-center gap-2">
              <span
                v-if="idea.status"
                class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-secondary/15 text-primary border border-secondary/30 uppercase tracking-wide"
              >
                {{ idea.status }}
              </span>
              <span
                v-if="idea.is_shared === 1 || idea.is_shared === true"
                class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200"
              >
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                Shared Publicly
              </span>
            </div>

            <h1 class="text-2xl sm:text-4xl font-extrabold text-primary font-montserrat tracking-tight">
              {{ idea.title }}
            </h1>

            <p class="text-sm sm:text-base text-slate-600 leading-relaxed whitespace-pre-line">
              {{ idea.description }}
            </p>
          </div>

          <!-- Add Script Button -->
          <button
            @click="openScriptForm"
            class="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-primary shadow-md shadow-primary/20 hover:opacity-95 active:scale-[0.98] transition-all duration-150 cursor-pointer shrink-0"
          >
            <PlusIcon class="w-4 h-4" />
            <span>Add Script</span>
          </button>
        </div>

        <!-- Tags List -->
        <div v-if="idea.tags && idea.tags.length" class="flex items-center gap-2 flex-wrap">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 mr-1">Tags:</span>
          <span
            v-for="tag in idea.tags"
            :key="tag.id || tag.name"
            class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200 transition"
          >
            #{{ tag.name }}
          </span>
        </div>
      </section>

      <!-- Scripts Section -->
      <section class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
              <CodeBracketIcon class="w-4 h-4" />
            </div>
            <h2 class="text-lg font-bold text-slate-900 font-montserrat">Associated Scripts</h2>
          </div>
          <span class="text-xs font-semibold px-2.5 py-1 bg-white border border-slate-200 text-slate-600 rounded-full">
            {{ idea?.scripts?.length || 0 }} Scripts
          </span>
        </div>

        <!-- Empty State -->
        <div
          v-if="!idea?.scripts || idea.scripts.length === 0"
          class="bg-white rounded-2xl border border-slate-200/80 p-12 text-center shadow-xs"
        >
          <CodeBracketIcon class="w-10 h-10 text-slate-300 mx-auto mb-2" />
          <p class="text-sm font-semibold text-slate-700">No scripts yet</p>
          <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            Attach outlines, screenplays, or implementation scripts to this idea board.
          </p>
        </div>

        <!-- Scripts Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div
            v-for="script in idea.scripts"
            :key="script.id"
            class="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs hover:shadow-md transition-shadow flex flex-col justify-between"
          >
            <div>
              <div class="flex items-start justify-between gap-3 mb-3">
                <h3 class="text-base font-bold text-primary font-montserrat line-clamp-1">
                  {{ script.title }}
                </h3>
              </div>
              <div class="p-3.5 bg-slate-50 border border-slate-100 rounded-xl font-mono text-xs text-slate-700 max-h-48 overflow-y-auto whitespace-pre-wrap leading-relaxed">
                {{ script.script_content }}
              </div>
            </div>

            <div class="flex items-center justify-end gap-2 pt-4 mt-4 border-t border-slate-100">
              <button
                @click="openEditScriptForm(script)"
                class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-secondary hover:bg-secondary/10 rounded-lg transition"
              >
                <PencilSquareIcon class="w-3.5 h-3.5" />
                <span>Edit</span>
              </button>
              <button
                @click="deleteScript(script.id)"
                class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-danger hover:bg-danger/10 rounded-lg transition"
              >
                <TrashIcon class="w-3.5 h-3.5" />
                <span>Delete</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Comments / Discussion Section -->
      <section v-if="idea && (idea.is_shared === 1 || idea.is_shared === true)" class="space-y-6">
        <div class="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 shadow-xs space-y-6">
          <div class="flex items-center gap-2 pb-4 border-b border-slate-100">
            <ChatBubbleLeftRightIcon class="w-5 h-5 text-primary" />
            <h2 class="text-lg font-bold text-primary font-montserrat">Discussion &amp; Feedback</h2>
          </div>

          <!-- Add Comment Form -->
          <div class="space-y-3">
            <textarea
              v-model="commentText"
              placeholder="Share constructive thoughts, feedback, or suggestions..."
              class="w-full p-3.5 text-sm text-dark bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all resize-y min-h-[90px]"
            ></textarea>
            <div class="flex justify-end">
              <button
                @click="addComment"
                :disabled="!commentText.trim()"
                class="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-primary shadow-sm hover:opacity-95 active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed transition cursor-pointer"
              >
                <PlusIcon class="w-3.5 h-3.5" />
                <span>Post Comment</span>
              </button>
            </div>
          </div>

          <!-- Comments Feed -->
          <div v-if="idea.comments && idea.comments.length > 0" class="space-y-4 pt-4 border-t border-slate-100">
            <div
              v-for="comment in idea.comments"
              :key="comment.id"
              class="p-4 bg-slate-50/70 border border-slate-100 rounded-xl flex items-start justify-between gap-4"
            >
              <div class="space-y-1.5">
                <div class="flex items-center gap-2">
                  <span class="text-xs font-bold text-slate-800">
                    {{ comment.user?.username || "Community Member" }}
                  </span>
                  <span class="text-[11px] text-slate-400">
                    {{ new Date(comment.created_at).toLocaleString() }}
                  </span>
                </div>
                <p class="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                  {{ comment.content }}
                </p>
              </div>

              <!-- Author Operations -->
              <div
                v-if="user?.user?.id === comment.user?.id"
                class="flex items-center gap-1 shrink-0"
              >
                <button
                  @click="ideaStore.startEditComment(comment)"
                  class="p-1.5 text-slate-400 hover:text-secondary hover:bg-white rounded-lg transition"
                  title="Edit Comment"
                >
                  <PencilSquareIcon class="w-4 h-4" />
                </button>
                <button
                  @click="removeComment(comment.id)"
                  class="p-1.5 text-slate-400 hover:text-danger hover:bg-white rounded-lg transition"
                  title="Delete Comment"
                >
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-6 text-xs text-slate-400 italic">
            No comments yet. Start the conversation!
          </div>
        </div>
      </section>
    </div>

    <!-- Script Form Modal Dialog -->
    <TransitionRoot appear :show="isScriptFormOpen" as="template">
      <Dialog as="div" @close="closeScriptForm" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-200 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-150 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs" />
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
                <div class="flex items-center justify-between pb-4 border-b border-slate-100 mb-5">
                  <DialogTitle as="h3" class="text-lg font-bold text-primary font-montserrat">
                    {{ selectedScript ? "Edit Script" : "Create New Script" }}
                  </DialogTitle>
                  <button @click="closeScriptForm" class="text-slate-400 hover:text-slate-600 transition">
                    <XMarkIcon class="w-5 h-5" />
                  </button>
                </div>

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
import Loader from "../components/Loader.vue";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import {
  PlusIcon,
  TrashIcon,
  PencilSquareIcon,
  ArrowLeftIcon,
  CodeBracketIcon,
  ChatBubbleLeftRightIcon,
  XMarkIcon,
} from "@heroicons/vue/24/outline";

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
  selectedScript.value = null;
  isScriptFormOpen.value = true;
};

const closeScriptForm = () => {
  isScriptFormOpen.value = false;
  selectedScript.value = null;
};

const openEditScriptForm = (script) => {
  selectedScript.value = { ...script };
  isScriptFormOpen.value = true;
};

const addScript = async (scriptPayload) => {
  closeScriptForm();
  if (idea.value?.id) {
    scriptPayload.idea_id = idea.value.id;
    await scriptStore.addScript(scriptPayload);
    await ideaStore.getIdeaAction(idea.value.id);
  }
};

const updateScript = async (scriptPayload) => {
  closeScriptForm();
  await scriptStore.updateScript(scriptPayload);
  if (idea.value?.id) {
    await ideaStore.getIdeaAction(idea.value.id);
  }
};

const deleteScript = async (scriptId) => {
  await scriptStore.deleteScript(scriptId);
  if (idea.value?.id) {
    await ideaStore.getIdeaAction(idea.value.id);
  }
};

const addComment = async () => {
  if (!commentText.value.trim() || !idea.value?.id) return;

  const payload = {
    idea_id: idea.value.id,
    content: commentText.value,
  };
  await ideaStore.addComment(payload);
  await ideaStore.getIdeaAction(idea.value.id);
  commentText.value = "";
};

const removeComment = async (commentId) => {
  await ideaStore.deleteComment(commentId);
  if (idea.value?.id) {
    await ideaStore.getIdeaAction(idea.value.id);
  }
};

onMounted(async () => {
  const ideaId = route.params.ideaId;
  if (ideaId) {
    await ideaStore.getIdeaAction(ideaId);
  }
});
</script>