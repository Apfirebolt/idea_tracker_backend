<template>
  <div class="min-h-screen bg-slate-50/75 py-10 px-4 sm:px-6 lg:px-8 text-slate-800">
    <Loader v-if="loading" />

    <div class="max-w-2xl mx-auto space-y-6">
      <!-- Back Navigation Button -->
      <div>
        <button
          @click="$router.back()"
          class="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-primary transition-colors cursor-pointer"
        >
          <ArrowLeftIcon class="w-4 h-4" />
          <span>Back</span>
        </button>
      </div>

      <!-- User Profile Card -->
      <div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
        <!-- Top Profile Banner Decor -->
        <div class="h-28 bg-linear-to-r from-primary/90 via-primary to-secondary/80 relative">
          <div class="absolute -bottom-10 left-6 sm:left-8">
            <div class="w-20 h-20 rounded-2xl bg-white p-1 shadow-md border border-slate-100">
              <div class="w-full h-full rounded-xl bg-primary text-white font-bold font-montserrat flex items-center justify-center text-2xl">
                {{ getInitials(user?.name || user?.username || user?.email) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Profile Details Body -->
        <div class="pt-14 p-6 sm:p-8 space-y-6">
          <div v-if="user" class="space-y-6">
            <!-- Name & Status Badge -->
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 pb-5 border-b border-slate-100">
              <div>
                <h1 class="text-2xl font-bold text-primary font-montserrat tracking-tight">
                  {{ user.name || user.username }}
                </h1>
                <p class="text-xs text-slate-400 mt-0.5">Idea Tracker Community Member</p>
              </div>
              <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 self-start sm:self-auto">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                Active
              </span>
            </div>

            <!-- Attribute Rows -->
            <div class="grid grid-cols-1 gap-4">
              <!-- Username Row -->
              <div class="flex items-center gap-4 p-4 rounded-xl bg-slate-50/75 border border-slate-100">
                <div class="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center shrink-0">
                  <UserIcon class="w-5 h-5" />
                </div>
                <div class="min-w-0 flex-1">
                  <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Username</p>
                  <p class="text-sm font-semibold text-slate-800 truncate mt-0.5">
                    @{{ user.username }}
                  </p>
                </div>
              </div>

              <!-- Email Row -->
              <div class="flex items-center gap-4 p-4 rounded-xl bg-slate-50/75 border border-slate-100">
                <div class="w-10 h-10 rounded-xl bg-secondary/15 text-secondary flex items-center justify-center shrink-0">
                  <EnvelopeIcon class="w-5 h-5" />
                </div>
                <div class="min-w-0 flex-1">
                  <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Email Address</p>
                  <p class="text-sm font-semibold text-slate-800 truncate mt-0.5">
                    {{ user.email }}
                  </p>
                </div>
              </div>

              <!-- Member Since Row (if available) -->
              <div v-if="user.created_at" class="flex items-center gap-4 p-4 rounded-xl bg-slate-50/75 border border-slate-100">
                <div class="w-10 h-10 rounded-xl bg-slate-200/60 text-slate-600 flex items-center justify-center shrink-0">
                  <CalendarDaysIcon class="w-5 h-5" />
                </div>
                <div class="min-w-0 flex-1">
                  <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Member Since</p>
                  <p class="text-sm font-semibold text-slate-800 truncate mt-0.5">
                    {{ new Date(user.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }) }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-12">
            <div class="w-12 h-12 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3">
              <UserIcon class="w-6 h-6" />
            </div>
            <p class="text-base font-semibold text-slate-700">User profile not found</p>
            <p class="text-xs text-slate-400 mt-1">
              The requested user account does not exist or has been removed.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useUserStore } from "../store/user";
import Loader from "../components/Loader.vue";
import {
  ArrowLeftIcon,
  UserIcon,
  EnvelopeIcon,
  CalendarDaysIcon,
} from "@heroicons/vue/24/outline";

const route = useRoute();
const userStore = useUserStore();

const user = computed(() => userStore.getUser);
const loading = computed(() => userStore.loading);

const getInitials = (identifier) => {
  if (!identifier) return "?";
  const parts = identifier.trim().split(" ");
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return identifier.slice(0, 2).toUpperCase();
};

onMounted(async () => {
  const userId = route.params.userId;
  if (userId) {
    await userStore.getUserAction(userId);
  } else {
    console.error("User ID is not provided in the route parameters.");
  }
});
</script>