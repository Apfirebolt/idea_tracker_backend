<template>
  <form
    @submit.prevent="submitForm"
    class="mx-auto p-6 bg-white rounded shadow"
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
          placeholder="Enter Script title"
        />
        <PencilAltIcon
          class="w-5 h-5 text-gray-400 absolute right-3 top-3 pointer-events-none"
        />
      </div>
    </div>
    <div class="mb-4">
      <label for="description" class="block text-gray-700 font-bold mb-2"
        >Script Content</label
      >
      <div class="relative">
        <textarea
          id="description"
          v-model="form.script_content"
          class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300 pr-10"
          rows="15"
          required
          placeholder="Describe your Script"
        ></textarea>
        <PencilAltIcon
          class="w-5 h-5 text-gray-400 absolute right-3 top-3 pointer-events-none"
        />
      </div>
    </div>

    <button
      type="submit"
      class="flex items-center justify-center gap-2 px-4 py-2 bg-tertiary text-white hover:bg-blue-700 rounded transition"
    >
      <PlusIcon class="w-5 h-5" />
      Submit
    </button>
  </form>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import { PencilAltIcon, PlusIcon } from "@heroicons/vue/solid";

const props = defineProps({
  script: {
    type: Object,
    default: () => ({
      title: "",
      script_content: "",
    }),
  },
});
const emit = defineEmits(["addScript", "close", "updateScript"]);

const form = reactive({
  script_content: "",
});

function submitForm() {
  console.log("Submitting script form", form);
  emit("addScript", form);
}

onMounted(() => {
  if (props.script) {
    form.script_content = props.script.script_content;
    form.title = props.script.title || "";
  }
});
</script>
