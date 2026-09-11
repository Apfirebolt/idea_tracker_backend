<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <!-- Title Field -->
    <div>
      <label for="title" class="block text-xs font-semibold uppercase tracking-wider text-dark/80 mb-2">
        Title <span class="text-danger">*</span>
      </label>
      <div class="relative">
        <input
          id="title"
          v-model="form.title"
          type="text"
          class="w-full pl-4 pr-10 py-2.5 text-sm text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200"
          required
          placeholder="e.g. AI-driven Content Pipeline"
        />
        <PencilSquareIcon class="w-5 h-5 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>
    </div>

    <!-- Description Field -->
    <div>
      <label for="description" class="block text-xs font-semibold uppercase tracking-wider text-dark/80 mb-2">
        Description <span class="text-danger">*</span>
      </label>
      <div class="relative">
        <textarea
          id="description"
          v-model="form.description"
          rows="4"
          class="w-full p-3.5 pr-10 text-sm text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200 resize-none"
          required
          placeholder="Detail the scope, inspiration, and core workflow of this idea..."
        ></textarea>
        <DocumentTextIcon class="w-5 h-5 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
      </div>
    </div>

    <!-- Tags Selection -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <label class="block text-xs font-semibold uppercase tracking-wider text-dark/80">
          Tags <span class="text-danger">*</span>
        </label>
        <span class="text-xs text-gray-400">
          {{ form.tags.length }} selected
        </span>
      </div>

      <!-- Selected Active Chips -->
      <div v-if="form.tags.length" class="flex flex-wrap gap-1.5 mb-3 p-2 bg-gray-50 rounded-xl border border-dashed border-gray-200">
        <span
          v-for="tagName in form.tags"
          :key="tagName"
          class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-primary text-white shadow-sm"
        >
          #{{ tagName }}
          <button
            type="button"
            @click="deselectTag(tagName)"
            class="hover:text-danger focus:outline-none transition-colors"
          >
            <XMarkIcon class="w-3.5 h-3.5" />
          </button>
        </span>
      </div>

      <!-- Quick Interactive Tag Selector -->
      <div v-if="props.tags.length" class="p-3 bg-gray-50/50 border border-gray-200 rounded-xl space-y-2">
        <p class="text-xs text-gray-500">Click to add/remove tags:</p>
        <div class="flex flex-wrap gap-2 max-h-36 overflow-y-auto pr-1">
          <button
            type="button"
            v-for="tag in props.tags"
            :key="tag.id || tag.name"
            @click="toggleTag(tag.name)"
            :class="[
              'px-2.5 py-1 rounded-lg text-xs font-medium border transition-all duration-150',
              form.tags.includes(tag.name)
                ? 'bg-secondary text-white border-secondary shadow-sm shadow-secondary/25'
                : 'bg-white text-gray-600 border-gray-200 hover:border-secondary/60 hover:text-primary'
            ]"
          >
            {{ form.tags.includes(tag.name) ? '✓' : '+' }} {{ tag.name }}
          </button>
        </div>
      </div>

      <div v-else class="text-xs text-amber-600 bg-amber-50 border border-amber-200 rounded-xl p-3 flex items-center gap-2">
        <span>No tags available. Please define tags before creating an idea.</span>
      </div>
    </div>

    <!-- Edit Context: Status & Shared Toggle -->
    <div v-if="props.idea" class="p-4 bg-gray-50/60 border border-gray-100 rounded-xl grid grid-cols-1 sm:grid-cols-2 gap-4 items-center">
      <div>
        <label for="status" class="block text-xs font-semibold uppercase tracking-wider text-dark/80 mb-1.5">
          Lifecycle Status
        </label>
        <div class="relative">
          <select
            id="status"
            v-model="selectedStatus"
            class="w-full px-3 py-2 text-sm text-dark bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary transition appearance-none cursor-pointer"
          >
            <option
              v-for="option in statusOptions"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
          <ChevronUpDownIcon class="w-4 h-4 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>
      </div>

      <!-- Shared Switch -->
      <div class="flex items-center justify-between sm:justify-start gap-3 sm:pt-4">
        <label for="shared" class="text-sm font-medium text-dark/90 cursor-pointer select-none">
          Share publicly
        </label>
        <button
          type="button"
          id="shared"
          role="switch"
          :aria-checked="form.is_shared"
          @click="form.is_shared = !form.is_shared"
          :class="[
            'relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none',
            form.is_shared ? 'bg-primary' : 'bg-gray-200'
          ]"
        >
          <span
            :class="[
              'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow-sm ring-0 transition duration-200 ease-in-out',
              form.is_shared ? 'translate-x-5' : 'translate-x-0'
            ]"
          />
        </button>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex items-center justify-end gap-3 pt-2">
      <button
        type="button"
        @click="$emit('close')"
        class="px-4 py-2.5 text-sm font-semibold text-gray-600 hover:text-dark hover:bg-gray-100 rounded-xl transition"
      >
        Cancel
      </button>

      <button
        type="submit"
        :disabled="isIdeaFormDisabled"
        :class="[
          'inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm shadow-md transition-all duration-200 cursor-pointer',
          isIdeaFormDisabled
            ? 'bg-gray-200 text-gray-400 shadow-none cursor-not-allowed'
            : 'bg-primary text-white shadow-primary/20 hover:opacity-95 active:scale-[0.98]'
        ]"
      >
        <CheckIcon v-if="props.idea" class="w-4 h-4" />
        <PlusIcon v-else class="w-4 h-4" />
        <span>{{ props.idea ? 'Update Idea' : 'Save Idea' }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, onMounted, computed, ref } from "vue";
import { toast } from "vue3-toastify";
import {
  PencilSquareIcon,
  DocumentTextIcon,
  PlusIcon,
  CheckIcon,
  XMarkIcon,
  ChevronUpDownIcon,
} from "@heroicons/vue/24/outline";

const emit = defineEmits(["addIdea", "close", "updateIdea"]);

const props = defineProps({
  idea: {
    type: Object,
    default: null,
  },
  tags: {
    type: Array,
    default: () => [],
  },
});

const isIdeaFormDisabled = computed(() => {
  return props.tags.length === 0;
});

const form = reactive({
  title: "",
  description: "",
  tags: [],
  is_shared: false,
});

const statusOptions = ref([
  { value: "draft", label: "Draft" },
  { value: "open", label: "Open" },
  { value: "in-progress", label: "In Progress" },
  { value: "on-hold", label: "On Hold" },
  { value: "completed", label: "Completed" },
  { value: "closed", label: "Closed" },
]);
const selectedStatus = ref(statusOptions.value[0].value);

const toggleTag = (tagName) => {
  if (form.tags.includes(tagName)) {
    form.tags = form.tags.filter((t) => t !== tagName);
  } else {
    form.tags.push(tagName);
  }
};

const deselectTag = (tagName) => {
  form.tags = form.tags.filter((t) => t !== tagName);
};

function submitForm() {
  if (!form.title.trim() || !form.description.trim()) {
    toast.error("Title and description cannot be empty.");
    return;
  }
  if (form.tags.length === 0) {
    toast.error("Please select at least one tag.");
    return;
  }

  if (props.idea) {
    form.status = selectedStatus.value;
    emit("updateIdea", { ...props.idea, ...form });
  } else {
    emit("addIdea", { ...form });
  }
}

onMounted(() => {
  if (props.tags.length === 0) {
    toast.error("Please add tags before submitting an idea.");
    return;
  }

  if (props.idea) {
    form.title = props.idea.title || "";
    form.description = props.idea.description || "";
    form.is_shared = props.idea.is_shared === 1 || props.idea.is_shared === true;
    form.tags = props.idea.tags
      ? props.idea.tags.map((t) => (typeof t === "string" ? t : t.name))
      : [];
    if (props.idea.status) {
      selectedStatus.value = props.idea.status;
    }
  }
});
</script>