<template>
  <form
    @submit.prevent="submitForm"
    class="max-w-md mx-auto p-6 bg-white rounded shadow"
  >
    <div class="mb-4">
      <label for="name" class="block text-gray-700 font-bold mb-2">Name</label>
      <div class="relative">
        <input
          id="name"
          v-model="form.name"
          type="text"
          class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300 pr-10"
          required
          placeholder="Enter tag name"
          style="padding-right: 2.5rem;"
        />
        <PencilAltIcon
          class="w-5 h-5 text-gray-400 absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none"
        />
      </div>
    </div>
    <div class="mb-4 relative">
      <label for="description" class="block text-gray-700 font-bold mb-2"
        >Description</label
      >
      <textarea
        id="description"
        v-model="form.description"
        class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300 pr-10"
        rows="4"
        required
        placeholder="Enter tag description"
      ></textarea>
      <PencilAltIcon
        class="w-5 h-5 text-gray-400 absolute right-3 top-10 pointer-events-none"
      />
    </div>
    <button
      type="submit"
      class="bg-tertiary text-white px-4 py-2 rounded hover:bg-blue-700 transition flex items-center gap-2"
    >
      <PlusIcon class="w-5 h-5" />
      Submit
    </button>
  </form>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import { PencilAltIcon, PlusIcon } from "@heroicons/vue/solid";

const emit = defineEmits(["addTag", "close", "updateTag"]);

const props = defineProps({
  tag: {
    type: Object,
    default: () => ({
      name: "",
      description: "",
    }),
  },
});

const form = reactive({
  name: "",
  description: "",
});

function submitForm() {
  // Handle form submission logic here
  console.log("Form submitted:", form);
  if (props.tag) {
    emit("updateTag", { ...props.tag, ...form });
  } else {
    emit("addTag", { ...form });
  }
}

onMounted(() => {
  if (props.tag) {
    form.name = props.tag.name;
    form.description = props.tag.description;
  }
});
</script>
