<template>
  <div class="message" :class="typeClass">
    <span class="message-type">{{ typeLabel }}</span>
    <span class="message-content">{{ message }}</span>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  message: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: "info",
    validator: (value) =>
      ["info", "success", "error", "warning"].includes(value),
  },
});

const typeClass = computed(() => `message--${props.type}`);
const typeLabel = computed(
  () => props.type.charAt(0).toUpperCase() + props.type.slice(1)
);
</script>

<style scoped>
.message {
  padding: 12px 16px;
  border-radius: 4px;
  margin: 8px 0;
  display: flex;
  align-items: center;
  font-size: 16px;
}

.message-type {
  font-weight: bold;
  margin-right: 8px;
}

.message--info {
  background: #e6f7ff;
  color: #1890ff;
}

.message--success {
  background: #f6ffed;
  color: #52c41a;
}

.message--error {
  background: #fff1f0;
  color: #f5222d;
}

.message--warning {
  background: #fffbe6;
  color: #faad14;
}
</style>
