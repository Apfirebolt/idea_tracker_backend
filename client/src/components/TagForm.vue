<template>
  <form @submit.prevent="submitForm">
    <div>
      <label for="name">Tag Name</label>
      <input
        id="name"
        v-model="form.name"
        type="text"
        required
        placeholder="Enter tag name"
      />
    </div>
    <div>
      <label for="description">Description</label>
      <textarea
        id="description"
        v-model="form.description"
        placeholder="Enter tag description"
      ></textarea>
    </div>
    <button type="submit">Save Tag</button>
  </form>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({
    name: '',
    description: '',
});

const emit = defineEmits(['submit']);

function submitForm() {
    emit('submit', { ...form.value });
    form.value.name = '';
    form.value.description = '';
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
}
label {
  font-weight: bold;
}
input,
textarea {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}
button {
  align-self: flex-start;
  padding: 0.5rem 1rem;
}
</style>
