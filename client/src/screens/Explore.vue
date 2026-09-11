<template>
  <div class="min-h-screen bg-slate-50/75 py-10 px-4 sm:px-6 lg:px-8 text-slate-800">
    <div class="max-w-7xl mx-auto space-y-12">
      
      <!-- ================= Shared Ideas Section ================= -->
      <section class="space-y-6">
        <!-- Section Header Bar -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
              <LightBulbIcon class="w-5 h-5" />
            </div>
            <div>
              <h1 class="text-2xl font-bold tracking-tight text-primary font-montserrat">
                Explore Shared Ideas
              </h1>
              <p class="text-xs text-slate-500 mt-0.5">
                Discover concepts, workflows, and blueprints curated by the community
              </p>
            </div>
          </div>
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-600 self-start sm:self-auto">
            {{ sharedIdeas.items?.length || 0 }} Published
          </span>
        </div>

        <!-- Empty State -->
        <div
          v-if="!sharedIdeas.items || sharedIdeas.items.length === 0"
          class="bg-white rounded-2xl border border-slate-200/80 p-12 text-center shadow-xs"
        >
          <div class="w-12 h-12 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3">
            <LightBulbIcon class="w-6 h-6" />
          </div>
          <p class="text-base font-semibold text-slate-700">No public ideas available</p>
          <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            Shared ideas will appear here as soon as members publish their brainstorming boards.
          </p>
        </div>

        <!-- Ideas Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <article
            v-for="idea in sharedIdeas.items"
            :key="idea.id"
            @click="goToIdeaDetail(idea.id)"
            class="group bg-white rounded-2xl border border-slate-200/80 p-6 flex flex-col justify-between shadow-xs hover:shadow-md hover:border-secondary/40 transition-all duration-200 cursor-pointer"
          >
            <div>
              <div class="flex items-start justify-between gap-3 mb-3">
                <h3 class="text-lg font-bold text-slate-900 font-montserrat group-hover:text-primary transition-colors line-clamp-1">
                  {{ idea.title }}
                </h3>
                <ArrowUpRightIcon class="w-4 h-4 text-slate-400 group-hover:text-secondary group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform shrink-0 mt-1" />
              </div>

              <p class="text-sm text-slate-600 leading-relaxed line-clamp-3 mb-4">
                {{ idea.description }}
              </p>
            </div>

            <!-- Tags Footer -->
            <div class="pt-4 border-t border-slate-100 mt-auto">
              <div v-if="idea.tags && idea.tags.length" class="flex flex-wrap gap-1.5">
                <span
                  v-for="tag in idea.tags"
                  :key="tag.id || tag.name"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-lg text-xs font-medium bg-secondary/10 text-primary border border-secondary/20"
                >
                  #{{ tag.name }}
                </span>
              </div>
              <span v-else class="text-xs text-slate-400 italic">No tags associated</span>
            </div>
          </article>
        </div>
      </section>

      <!-- ================= Explore Users Section ================= -->
      <section class="space-y-6">
        <!-- Section Header Bar -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-secondary/15 text-secondary flex items-center justify-center">
              <UsersIcon class="w-5 h-5" />
            </div>
            <div>
              <h2 class="text-2xl font-bold tracking-tight text-primary font-montserrat">
                Explore Creators
              </h2>
              <p class="text-xs text-slate-500 mt-0.5">
                Connect with active authors, builders, and creative contributors
              </p>
            </div>
          </div>
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-600 self-start sm:self-auto">
            {{ users.items?.length || 0 }} Members
          </span>
        </div>

        <!-- Empty State -->
        <div
          v-if="!users.items || users.items.length === 0"
          class="bg-white rounded-2xl border border-slate-200/80 p-12 text-center shadow-xs"
        >
          <div class="w-12 h-12 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3">
            <UsersIcon class="w-6 h-6" />
          </div>
          <p class="text-base font-semibold text-slate-700">No users found</p>
          <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            There are currently no active profiles ready for discovery.
          </p>
        </div>

        <!-- Users Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <article
            v-for="user in users.items"
            :key="user.id"
            @click="goToUserProfile(user.id)"
            class="group bg-white rounded-2xl border border-slate-200/80 p-5 flex items-center gap-4 shadow-xs hover:shadow-md hover:border-secondary/40 transition-all duration-200 cursor-pointer"
          >
            <!-- Avatar Initials -->
            <div class="w-12 h-12 rounded-xl bg-primary text-white font-bold font-montserrat flex items-center justify-center text-base shrink-0 group-hover:bg-secondary transition-colors">
              {{ getInitials(user.name || user.username || user.email) }}
            </div>

            <div class="min-w-0 flex-1">
              <h3 class="text-base font-bold text-slate-900 font-montserrat truncate group-hover:text-primary transition-colors">
                {{ user.name || user.username || "Anonymous Creator" }}
              </h3>
              <p class="text-xs text-slate-500 truncate mt-0.5">
                {{ user.email }}
              </p>
            </div>

            <ArrowRightIcon class="w-4 h-4 text-slate-300 group-hover:text-secondary group-hover:translate-x-1 transition-all shrink-0" />
          </article>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useIdeaStore } from "../store/idea";
import { useUserStore } from "../store/user";
import {
  LightBulbIcon,
  UsersIcon,
  ArrowUpRightIcon,
  ArrowRightIcon,
} from "@heroicons/vue/24/outline";

const router = useRouter();
const ideaStore = useIdeaStore();
const userStore = useUserStore();

const sharedIdeas = computed(() => ideaStore.getSharedIdeas || { items: [] });
const users = computed(() => userStore.getUsers || { items: [] });

const goToIdeaDetail = (ideaId) => {
  router.push({ name: "IdeaDetail", params: { ideaId } });
};

const goToUserProfile = (userId) => {
  router.push({ name: "UserDetail", params: { userId } });
};

const getInitials = (identifier) => {
  if (!identifier) return "?";
  const parts = identifier.trim().split(" ");
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return identifier.slice(0, 2).toUpperCase();
};

onMounted(async () => {
  await Promise.allSettled([
    ideaStore.getSharedIdeasAction(),
    userStore.getUsersAction(),
  ]);
});
</script>