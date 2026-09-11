<template>
  <footer class="bg-primary text-light border-t border-white/10 pt-16 pb-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Top Grid: Brand & Information Pillars -->
      <div class="grid grid-cols-1 md:grid-cols-12 gap-10 pb-12 border-b border-white/10">
        
        <!-- Brand & Mission Column -->
        <div class="md:col-span-5 space-y-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-lg bg-secondary/20 flex items-center justify-center text-secondary border border-secondary/30">
              <LightBulbIcon class="w-5 h-5" />
            </div>
            <span class="text-xl font-bold font-montserrat tracking-tight text-white">
              Idea Tracker
            </span>
          </div>
          <p class="text-sm text-light/75 leading-relaxed max-w-sm">
            A modular workspace designed to help developers, writers, and creators capture sparks of inspiration, structure scripts, and track project execution seamlessly.
          </p>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-light/70">
            <span class="w-2 h-2 rounded-full bg-secondary"></span>
            Built with Vue 3, Tailwind CSS &amp; FastAPI
          </div>
        </div>

        <!-- Pillar 1: Workspace & Scripting -->
        <div class="md:col-span-4 space-y-3">
          <h3 class="text-sm font-semibold uppercase tracking-wider text-secondary font-montserrat">
            Ideate &amp; Execute
          </h3>
          <p class="text-sm text-light/80 leading-relaxed">
            Manage drafts, tag taxonomies, and pipeline milestones in one focused dashboard built for agile creative routines.
          </p>
          <ul class="space-y-1.5 text-xs text-light/70 pt-1">
            <li class="flex items-center gap-1.5">
              <span class="text-secondary">•</span> Categorized brainstorm logs
            </li>
            <li class="flex items-center gap-1.5">
              <span class="text-secondary">•</span> Full-text metadata indexing
            </li>
          </ul>
        </div>

        <!-- Pillar 2: Community & Connectivity -->
        <div class="md:col-span-3 space-y-3">
          <h3 class="text-sm font-semibold uppercase tracking-wider text-secondary font-montserrat">
            Ecosystem
          </h3>
          <p class="text-sm text-light/80 leading-relaxed">
            Open-source and continuously evolving. Contribute workflows, submit issues, or fork the repository.
          </p>
          <div class="pt-2">
            <a
              href="https://github.com/"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold text-white bg-white/10 hover:bg-white/15 border border-white/10 active:scale-[0.98] transition-all duration-150"
            >
              <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24" aria-hidden="true">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-6.6-1.113-1.279 0-2.49.463-3.447 1.309z" />
              </svg>
              <span>GitHub</span>
            </a>
          </div>
        </div>

      </div>

      <!-- Bottom Bar: Copyright & Meta -->
      <div class="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-light/60">
        <div>
          &copy; {{ currentYear }} Idea Tracker. All rights reserved.
        </div>
        <div class="flex items-center gap-6">
          <a href="#" class="hover:text-white transition-colors">Privacy Policy</a>
          <a href="#" class="hover:text-white transition-colors">Terms of Service</a>
          <a href="https://github.com/" target="_blank" rel="noopener noreferrer" class="hover:text-white transition-colors">Documentation</a>
        </div>
      </div>

    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';
import { LightBulbIcon } from '@heroicons/vue/24/outline';

const currentYear = computed(() => new Date().getFullYear());
</script>