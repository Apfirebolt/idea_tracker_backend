<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <!-- Title Field -->
    <div>
      <label for="title" class="block text-xs font-semibold uppercase tracking-wider text-dark/80 mb-2">
        Script Title <span class="text-danger">*</span>
      </label>
      <div class="relative">
        <input
          id="title"
          v-model="form.title"
          type="text"
          class="w-full pl-4 pr-10 py-2.5 text-sm text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200"
          required
          placeholder="e.g. Video Pitch Script v1 or Migration Automation Spec"
        />
        <PencilSquareIcon class="w-5 h-5 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>
    </div>

    <!-- Script Content Area -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <label for="script_content" class="block text-xs font-semibold uppercase tracking-wider text-dark/80">
          Script Content <span class="text-danger">*</span>
        </label>
        <span class="text-xs text-gray-400">
          {{ charCount }} characters
        </span>
      </div>

      <div class="relative">
        <textarea
          id="script_content"
          v-model="form.script_content"
          rows="14"
          class="w-full p-4 font-mono text-sm leading-relaxed text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200 resize-y"
          required
          placeholder="Write your outline, narration, code block, or full script breakdown here..."
        ></textarea>
        <DocumentTextIcon class="w-5 h-5 text-gray-400 absolute right-3.5 top-3.5 pointer-events-none" />
      </div>
    </div>

    <!-- Form Action Buttons -->
    <div class="flex items-center justify-end gap-3 pt-2">
      <button
        type="button"
        @click="$emit('close')"
        class="px-4 py-2.5 text-sm font-semibold text-gray-600 hover:text-dark hover:bg-gray-100 rounded-xl transition-colors cursor-pointer"
      >
        Cancel
      </button>

      <button
        type="submit"
        class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm text-white bg-primary shadow-md shadow-primary/20 hover:opacity-95 active:scale-[0.98] transition-all duration-200 cursor-pointer"
      >
        <CheckIcon v-if="props.script && props.script.id" class="w-4 h-4" />
        <PlusIcon v-else class="w-4 h-4" />
        <span>{{ props.script && props.script.id ? "Update Script" : "Save Script" }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, onMounted, computed, watch } from "vue";
import {
  PencilSquareIcon,
  DocumentTextIcon,
  PlusIcon,
  CheckIcon,
} from "@heroicons/vue/24/outline";

const props = defineProps({
  script: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["addScript", "close", "updateScript"]);

const form = reactive({
  title: "",
  script_content: "",
});

const charCount = computed(() => (form.script_content ? form.script_content.length : 0));

const syncData = () => {
  if (props.script) {
    form.title = props.script.title || "";
    form.script_content = props.script.script_content || "";
  } else {
    form.title = "";
    form.script_content = "";
  }
};

watch(() => props.script, syncData, { deep: true });

onMounted(syncData);

function submitForm() {
  if (!form.title.trim() || !form.script_content.trim()) {
    return;
  }

  if (props.script && props.script.id) {
    emit("updateScript", { ...props.script, ...form });
  } else {
    emit("addScript", { ...form });
  }

  form.title = "";
  form.script_content = "";
  emit("close");
}
</script>