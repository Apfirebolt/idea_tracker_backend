<template>
  <div :class="[fullScreen ? 'min-h-screen' : '', 'flex items-center justify-center']">
    <div
      :class="[sizeClasses, colorClasses]"
      class="animate-spin rounded-full border-solid border-black/10"
      role="status"
      aria-label="Loading"
    >
      <span class="sr-only">Loading...</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  size: {
    type: String,
    default: "md", // "sm" | "md" | "lg"
  },
  color: {
    type: String,
    default: "indigo", // "indigo" | "white" | "blue"
  },
  fullScreen: {
    type: Boolean,
    default: true,
  },
});

const sizeClasses = computed(() => {
  const map = {
    sm: "h-5 w-5 border-2",
    md: "h-9 w-9 border-4",
    lg: "h-14 w-14 border-4",
  };
  return map[props.size] || map.md;
});

const colorClasses = computed(() => {
  const map = {
    indigo: "border-l-indigo-600",
    blue: "border-l-blue-500",
    white: "border-l-white",
  };
  return map[props.color] || map.indigo;
});
</script>