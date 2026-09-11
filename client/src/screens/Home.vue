<template>
  <div class="min-h-screen bg-slate-50 relative overflow-hidden flex flex-col justify-between">
    <!-- Subtle Ambient Background Accents -->
    <div class="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-secondary/10 blur-3xl pointer-events-none" />
    <div class="absolute top-1/3 -right-32 w-96 h-96 rounded-full bg-primary/10 blur-3xl pointer-events-none" />

    <!-- Hero Section -->
    <div class="relative z-10 flex-1 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 py-20 text-center">
      <div class="max-w-3xl mx-auto">
        
        <!-- Status / Pill Badge -->
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white border border-slate-200 shadow-xs mb-8">
          <span class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-secondary/20 text-secondary">
            <SparklesIcon class="w-3.5 h-3.5" />
          </span>
          <span class="text-xs font-semibold text-slate-700 tracking-wide">
            Your Creative Workflow, Elevated
          </span>
        </div>

        <!-- Main Heading -->
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-primary font-montserrat tracking-tight leading-tight mb-6">
          Turn scattered thoughts into
          <span class="text-transparent bg-clip-text bg-linear-to-r from-secondary to-primary">
            actionable ideas
          </span>
        </h1>

        <!-- Subtitle -->
        <p class="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed mb-10">
          Idea Tracker helps developers, writers, and creators capture, organize, and execute brainstormed concepts with flexible taxonomies and structured milestones.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-3.5 mb-16">
          <router-link
            to="/register"
            class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl font-semibold text-sm text-white bg-primary shadow-lg shadow-primary/25 hover:bg-primary/90 active:scale-[0.98] transition-all duration-150 cursor-pointer"
          >
            <span>Get Started Free</span>
            <ArrowRightIcon class="w-4 h-4" />
          </router-link>

          <router-link
            to="/login"
            class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl font-semibold text-sm text-slate-700 bg-white border border-slate-200 shadow-xs hover:bg-slate-50 active:scale-[0.98] transition-all duration-150 cursor-pointer"
          >
            <span>Sign In</span>
          </router-link>
        </div>

        <!-- Mini Feature Highlights -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-left">
          <div class="bg-white/80 backdrop-blur-xs p-5 rounded-2xl border border-slate-200/80 shadow-xs">
            <div class="w-9 h-9 rounded-xl bg-primary/10 text-primary flex items-center justify-center mb-3">
              <LightBulbIcon class="w-5 h-5" />
            </div>
            <h3 class="text-sm font-bold text-slate-900 font-montserrat mb-1">Instant Ideation</h3>
            <p class="text-xs text-slate-500 leading-relaxed">
              Capture quick notes, scripts, and drafts before the spark fades away.
            </p>
          </div>

          <div class="bg-white/80 backdrop-blur-xs p-5 rounded-2xl border border-slate-200/80 shadow-xs">
            <div class="w-9 h-9 rounded-xl bg-secondary/15 text-secondary flex items-center justify-center mb-3">
              <TagIcon class="w-5 h-5" />
            </div>
            <h3 class="text-sm font-bold text-slate-900 font-montserrat mb-1">Tag Taxonomies</h3>
            <p class="text-xs text-slate-500 leading-relaxed">
              Group and cross-reference your ideas using customizable category tags.
            </p>
          </div>

          <div class="bg-white/80 backdrop-blur-xs p-5 rounded-2xl border border-slate-200/80 shadow-xs">
            <div class="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-3">
              <CheckBadgeIcon class="w-5 h-5" />
            </div>
            <h3 class="text-sm font-bold text-slate-900 font-montserrat mb-1">Track Progress</h3>
            <p class="text-xs text-slate-500 leading-relaxed">
              Move ideas through clear statuses from draft to full execution.
            </p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import {
  SparklesIcon,
  ArrowRightIcon,
  LightBulbIcon,
  TagIcon,
  CheckBadgeIcon,
} from "@heroicons/vue/24/outline";
</script>