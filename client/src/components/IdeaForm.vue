<template>
  <form
    @submit.prevent="submitForm"
    class="max-w-xl mx-auto p-6 bg-white rounded shadow"
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
        <option
          v-for="tag in props.tags"
          :key="tag"
          :value="tag.name"
          class="bg-secondary py-2 px-1 text-white text-center"
        >
          {{ tag.name }}
        </option>
      </select>
    </div>

    <div v-if="props.idea" class="mb-4 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label for="status" class="block text-gray-700 font-bold mb-2"
          >Status</label
        >
        <select
          id="status"
          v-model="selectedStatus"
          class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300"
        >
          <option
            v-for="option in statusOptions"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>
      <div class="flex items-center">
        <input
          id="shared"
          type="checkbox"
          v-model="form.is_shared"
          class="mr-2"
        />
        <label for="shared" class="text-gray-700 font-bold select-none">
          Shared
        </label>
      </div>
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
import { reactive, onMounted, computed, ref } from "vue";
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

const statusOptions = ref([
  { value: "draft", label: "Draft" },
  { value: "open", label: "Open" },
  { value: "in-progress", label: "In Progress" },
  { value: "on-hold", label: "On Hold" },
  { value: "completed", label: "Completed" },
  { value: "closed", label: "Closed" },
]);
const selectedStatus = ref(statusOptions.value[0].value);

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
    // merge status and tags with the existing idea
    form.status = selectedStatus.value;
    form.is_shared = form.is_shared || false;
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
    form.is_shared = props.idea.is_shared === 1 ? true : false;
    // populate tags with tag name if tags are present in the idea
    form.tags = props.idea.tags ? props.idea.tags.map((tag) => tag.name) : [];
  }
});
</script>
