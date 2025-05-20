<template>
    <form @submit.prevent="submitForm" class="max-w-md mx-auto p-6 bg-white rounded shadow">
        <div class="mb-4">
            <label for="title" class="block text-gray-700 font-bold mb-2">Title</label>
            <input id="title" v-model="form.title" type="text"
                class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300" required
                placeholder="Enter idea title" />
        </div>
        <div class="mb-4">
            <label for="description" class="block text-gray-700 font-bold mb-2">Description</label>
            <textarea id="description" v-model="form.description"
                class="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300" rows="4"
                required placeholder="Describe your idea"></textarea>
        </div>
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
            Submit
        </button>
    </form>
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({
    title: '',
    description: ''
})

function submitForm() {
    // Handle form submission logic here
    console.log('Form submitted:', form)
}
</script>