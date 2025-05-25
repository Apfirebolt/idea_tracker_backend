<template>
  <form
    @submit.prevent="submitForm"
    class="max-w-md mx-auto p-6 bg-white rounded shadow"
  >
    <div class="mb-4">
      <label for="title" class="block text-gray-700 font-bold mb-2"
        >Title</label
      >
      <div class="relative">
        <input
          id="title"
          v-model="form.title"
          type="text"
          class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300 pr-10"
          required
          placeholder="Enter idea title"
        />
        <PencilAltIcon
          class="w-5 h-5 text-gray-400 absolute right-3 top-3 pointer-events-none"
        />
      </div>
    </div>
    <div class="mb-4">
      <label for="description" class="block text-gray-700 font-bold mb-2"
        >Description</label
      >
      <div class="relative">
        <textarea
          id="description"
          v-model="form.description"
          class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300 pr-10"
          rows="4"
          required
          placeholder="Describe your idea"
        ></textarea>
        <PencilAltIcon
          class="w-5 h-5 text-gray-400 absolute right-3 top-3 pointer-events-none"
        />
      </div>
    </div>
    <div class="mb-4">
      <div class="mb-2">
        <span
          v-for="tag in form.tags"
          :key="tag"
          class="inline-flex items-center bg-primary text-white text-xs px-3 py-2 rounded mr-2 mb-1"
        >
          {{ tag }}
          <XCircleIcon
            class="w-6 h-6 ml-1 cursor-pointer text-white hover:text-red-500"
            @click="deselectTags(tag)"
          />
        </span>
      </div>
      <label for="tags" class="block text-gray-700 font-bold mb-2">Tags</label>
      <select
        id="tags"
        v-model="form.tags"
        multiple
        class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300"
      >
        <option v-for="tag in props.tags" :key="tag" :value="tag.name" class="bg-secondary py-2 px-1 text-white text-center">
          {{ tag.name }}
        </option>
      </select>
    </div>
    <button
      type="submit"
      :disabled="isIdeaFormDisabled"
      :class="[
      'flex items-center justify-center gap-2 px-4 py-2 rounded transition',
      isIdeaFormDisabled
        ? 'bg-secondary text-white cursor-not-allowed'
        : 'bg-tertiary text-white hover:bg-blue-700',
      ]"
    >
      <PlusIcon class="w-5 h-5" />
      Submit
    </button>
  </form>
</template>

<script setup>
import { reactive, onMounted, computed } from "vue";
import { toast } from "vue3-toastify";
import { XCircleIcon, PencilAltIcon, PlusIcon } from "@heroicons/vue/solid";
const emit = defineEmits(["addIdea", "close", "updateIdea"]);

const props = defineProps({
  idea: {
    type: Object,
    default: () => ({
      title: "",
      description: "",
    }),
  },
  tags: {
    type: Array,
    default: () => [],
  },
});

const isIdeaFormDisabled = computed(() => {
  // Disable form if there are no tags available
  return props.tags.length === 0;
});

const form = reactive({
  title: "",
  description: "",
  tags: [],
});

function submitForm() {
  // check if title and description are not empty
  if (!form.title.trim() || !form.description.trim()) {
    toast.error("Title and description cannot be empty.");
    return;
  }
  // check if at least one tag is selected
  if (form.tags.length === 0) {
    toast.error("Please select at least one tag.");
    return;
  }
  // Handle form submission logic here
  if (props.idea) {
    emit("updateIdea", { ...props.idea, ...form });
  } else {
    emit("addIdea", form);
  }
}

const deselectTags = (id) => {
  // Deselect a tag by removing it from the form.tags array
  form.tags = form.tags.filter((tag) => tag !== id);
  toast.info(`Tag "${id}" deselected.`);
};

onMounted(() => {
  // if there are no tags, set the error and ask user to add tags
  if (props.tags.length === 0) {
    toast.error("Please add tags before submitting an idea.");
    return;
  }

  if (props.idea) {
    form.title = props.idea.title;
    form.description = props.idea.description;
    // populate tags with tag name if tags are present in the idea
    form.tags = props.idea.tags ? props.idea.tags.map(tag => tag.name) : [];
  }
});
</script>
