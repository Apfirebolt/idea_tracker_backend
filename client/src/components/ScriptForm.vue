<template>
  <form
    @submit.prevent="submitForm"
    class="mx-auto p-6 bg-white rounded shadow"
  >
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
import { toast } from "vue3-toastify";
import { XCircleIcon, PencilAltIcon, PlusIcon } from "@heroicons/vue/solid";

const props = defineProps({
  script: {
    type: Object,
    default: () => ({
      script_content: "",
    }),
  },
});
const emit = defineEmits(["addScript", "close", "updateScript"]);

const form = reactive({
  script_content: "",
});

function submitForm() {
  if (props.script) {
    emit("updateScript", { ...props.script, ...form });
  } else {
    emit("addScript", form);
  }
}

onMounted(() => {
  if (props.script) {
    form.script_content = props.script.script_content;
  }
});
</script>
