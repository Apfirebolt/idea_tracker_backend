<template>
  <Disclosure
    as="nav"
    v-slot="{ open }"
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-300 backdrop-blur-md border-b',
      isScrolledDown
        ? 'bg-primary/95 border-primary/20 shadow-lg shadow-black/10 py-1'
        : 'bg-primary/85 border-white/10 py-2'
    ]"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-14 sm:h-16">
        <!-- Brand & User Tag -->
        <div class="flex items-center space-x-3 sm:space-x-4">
          <router-link to="/" class="flex items-center space-x-2.5 group">
            <div class="w-9 h-9 rounded-xl bg-secondary/20 flex items-center justify-center text-secondary border border-secondary/30 group-hover:scale-105 transition-transform duration-200">
              <LightBulbIcon class="w-5 h-5" />
            </div>
            <span class="text-xl font-bold font-montserrat tracking-tight text-white group-hover:text-secondary transition-colors">
              Idea Tracker
            </span>
          </router-link>

          <!-- User Badge -->
          <div
            v-if="authData?.user?.username"
            class="hidden md:inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-white/10 text-xs font-medium text-slate-200 border border-white/15"
          >
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>{{ authData.user.username }}</span>
          </div>
        </div>

        <!-- Desktop Navigation Links -->
        <div class="hidden sm:flex items-center space-x-1.5 sm:space-x-2">
          <router-link
            v-for="link in activeLinks"
            :key="link.name"
            :to="link.href"
            class="px-3.5 py-2 rounded-xl text-sm font-medium text-slate-200 hover:text-white hover:bg-white/10 active:scale-[0.98] transition-all duration-150"
            active-class="bg-white/15 text-white font-semibold shadow-inner"
          >
            {{ link.name }}
          </router-link>

          <!-- Auth Actions -->
          <div v-if="authData?.user" class="pl-2 ml-2 border-l border-white/15">
            <button
              @click="auth.logout"
              class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-semibold text-danger hover:bg-danger/15 active:scale-[0.98] transition-all duration-150 cursor-pointer"
            >
              <ArrowRightOnRectangleIcon class="w-4 h-4" />
              <span>Log out</span>
            </button>
          </div>
        </div>

        <!-- Mobile Menu Toggle Button -->
        <div class="flex sm:hidden">
          <DisclosureButton
            class="inline-flex items-center justify-center p-2 rounded-xl text-slate-300 hover:text-white hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-secondary/50 transition-colors"
          >
            <span class="sr-only">Toggle navigation menu</span>
            <Bars3Icon v-if="!open" class="block h-6 w-6" aria-hidden="true" />
            <XMarkIcon v-else class="block h-6 w-6" aria-hidden="true" />
          </DisclosureButton>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation Drawer -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <DisclosurePanel class="sm:hidden border-t border-white/10 bg-primary/95 px-4 pt-3 pb-4 space-y-1 shadow-2xl">
        <div v-if="authData?.user?.username" class="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Signed in as <span class="text-white normal-case font-medium">{{ authData.user.username }}</span>
        </div>

        <router-link
          v-for="link in activeLinks"
          :key="link.name"
          :to="link.href"
          class="block px-3.5 py-2.5 rounded-xl text-base font-medium text-slate-200 hover:text-white hover:bg-white/10 transition-colors"
          active-class="bg-white/15 text-white font-semibold"
        >
          {{ link.name }}
        </router-link>

        <div v-if="authData?.user" class="pt-2 border-t border-white/10 mt-2">
          <button
            @click="auth.logout"
            class="w-full flex items-center justify-center gap-2 px-3.5 py-2.5 rounded-xl text-base font-medium text-white bg-danger hover:bg-danger/90 active:scale-[0.98] transition-all cursor-pointer"
          >
            <ArrowRightOnRectangleIcon class="w-5 h-5" />
            <span>Log out</span>
          </button>
        </div>
      </DisclosurePanel>
    </transition>
  </Disclosure>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useAuth } from "../store/auth";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import {
  Bars3Icon,
  XMarkIcon,
  LightBulbIcon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/vue/24/outline";

const auth = useAuth();
const authData = computed(() => auth.getAuthData);

const isScrolledDown = ref(false);

const links = [
  { name: "Home", href: "/" },
  { name: "Login", href: "/login" },
  { name: "Register", href: "/register" },
];

const authLinks = [
  { name: "Dashboard", href: "/dashboard" },
  { name: "Profile", href: "/profile" },
  { name: "Explore", href: "/explore" },
];

const activeLinks = computed(() =>
  authData.value?.user ? authLinks : links
);

const handleScroll = () => {
  isScrolledDown.value = window.scrollY > 20;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll();
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>