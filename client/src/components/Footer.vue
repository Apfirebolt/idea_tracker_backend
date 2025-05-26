<template>
  <footer class="py-10 px-8 bg-dark text-light dark:bg-slate-700 dark:text-white">
    <div class="container mx-auto px-12 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
        <div class="text-center md:text-left text-sm">
          &copy; {{ currentYear }} Idea Tracker
        </div>
        <div class="text-center text-sm">
          Built with Vue 3, Tailwind CSS and FastAPI
        </div>
        <div class="text-center md:text-right text-sm">
          <a href="https://github.com/" target="_blank" rel="noopener" class="underline hover:text-primary">GitHub</a>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
        <div class="text-center md:text-left">
          <h2 class="text-2xl font-semibold text-light mb-3">
            Manage your ideas and scripts efficiently
          </h2>
          <p>
            Idea Tracker is a simple yet powerful tool to help you organize your creative ideas and scripts.
          </p>
        </div>
        <div class="text-center my-3">
          <h2 class="text-2xl font-semibold text-light mb-3">
            Share your ideas and creativity with the world
          </h2>
          <p>
            Whether you're a writer, developer, or just someone with great ideas, Idea Tracker is here to help you keep track of them.
          </p>
        </div>
        <div class="text-center md:text-right">
          <h2 class="text-2xl font-semibold text-light mb-3">
            Stay connected
          </h2>
          <p>
            Follow us on social media to get the latest updates and features.
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import { defineComponent, computed } from 'vue'

export default defineComponent({
  setup() {
    const currentYear = computed(() => new Date().getFullYear())

    return {
      currentYear,
    }
  },
})
</script>