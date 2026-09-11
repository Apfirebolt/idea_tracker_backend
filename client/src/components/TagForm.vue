<template>
  <form @submit.prevent="submitForm" class="space-y-5">
    <!-- Tag Name Field -->
    <div>
      <label for="name" class="block text-xs font-semibold uppercase tracking-wider text-dark/80 mb-2">
        Tag Name <span class="text-danger">*</span>
      </label>
      <div class="relative">
        <input
          id="name"
          v-model="form.name"
          type="text"
          class="w-full pl-4 pr-10 py-2.5 text-sm text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200"
          required
          placeholder="e.g. backend, ai, ui-design"
        />
        <TagIcon class="w-5 h-5 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>
      <!-- Live Preview Badge -->
      <div v-if="form.name.trim()" class="mt-2 flex items-center gap-2">
        <span class="text-xs text-gray-400">Preview:</span>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-secondary/15 text-primary border border-secondary/30">
          #{{ form.name.trim() }}
        </span>
      </div>
    </div>

    <!-- Tag Description Field -->
    <div>
      <label for="description" class="block text-xs font-semibold uppercase tracking-wider text-dark/80 mb-2">
        Description <span class="text-danger">*</span>
      </label>
      <div class="relative">
        <textarea
          id="description"
          v-model="form.description"
          rows="3"
          class="w-full p-3.5 pr-10 text-sm text-dark bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-secondary/40 focus:border-secondary focus:bg-white transition-all duration-200 resize-none"
          required
          placeholder="Brief summary of what this tag classifies..."
        ></textarea>
        <DocumentTextIcon class="w-5 h-5 text-gray-400 absolute right-3 top-3.5 pointer-events-none" />
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex items-center justify-end gap-3 pt-2">
      <button
        type="button"
        @click="$emit('close')"
        class="px-4 py-2.5 text-sm font-semibold text-gray-600 hover:text-dark hover:bg-gray-100 rounded-xl transition cursor-pointer"
      >
        Cancel
      </button>

      <button
        type="submit"
        class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm bg-primary text-white shadow-md shadow-primary/20 hover:opacity-95 active:scale-[0.98] transition-all duration-200 cursor-pointer"
      >
        <CheckIcon v-if="props.tag?.name" class="w-4 h-4" />
        <PlusIcon v-else class="w-4 h-4" />
        <span>{{ props.tag?.name ? 'Update Tag' : 'Create Tag' }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, onMounted, watch } from "vue";
import {
  TagIcon,
  DocumentTextIcon,
  PlusIcon,
  CheckIcon,
} from "@heroicons/vue/24/outline";

const emit = defineEmits(["addTag", "close", "updateTag"]);

const props = defineProps({
  tag: {
    type: Object,
    default: null,
  },
});

const form = reactive({
  name: "",
  description: "",
});

function submitForm() {
  if (!form.name.trim() || !form.description.trim()) {
    return;
  }

  if (props.tag && props.tag.name) {
    emit("updateTag", { ...props.tag, ...form });
  } else {
    emit("addTag", { ...form });
  }
}

const syncData = () => {
  if (props.tag) {
    form.name = props.tag.name || "";
    form.description = props.tag.description || "";
  } else {
    form.name = "";
    form.description = "";
  }
};

watch(() => props.tag, syncData, { deep: true });

onMounted(syncData);
</script>