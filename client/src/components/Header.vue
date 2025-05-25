<template>
  <Disclosure :class="['border-b-4 fixed top-0 left-0 z-30 lg:py-2 w-full transition-all duration-300', isScrolledDown ? 'bg-dark dark:bg-slate-800' : 'bg-secondary dark:bg-slate-700 dark:text-white']" as="nav" v-slot="{ open }">
    <div class="mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center h-16">
        <div class="flex items-center w-full justify-between">
          <div class="justify-between flex items-center">
            <h2 class="text-2xl text-white font-bold">
              Idea Tracker
            </h2>
            <span v-if="authData && authData.user && authData.user.username" class="ml-4 text-white text-lg">
              Welcome, {{ authData.user.username }}!
            </span>
          </div>
          
          <div class="hidden sm:block sm:ml-6">
            <div class="flex space-x-4">
              <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->

              <router-link
                v-for="link in (authData && authData.user ? authLinks : links)"
                :key="link.name"
                :to="link.href"
                class="text-white hover:bg-primary transition-all duration-200 hover:text-white px-3 py-2 rounded-md font-medium"
              >
                {{ link.name }}
              </router-link>
              <button
                v-if="authData && authData.user"
                @click="auth.logout"
                class="text-white bg-red-600 hover:bg-red-700 transition-all duration-200 px-3 py-2 rounded-md font-medium"
              >
                Log out
              </button>
            </div>
          </div>
        </div>

        <div class="-mr-2 flex sm:hidden">
          <!-- Mobile menu button -->
          <DisclosureButton
            class="inline-flex items-center justify-center p-2 rounded-md text-info hover:text-white hover:bg-primary transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
          >
            <span class="sr-only">Open main menu</span>
            <MenuIcon v-if="!open" class="block h-6 w-6" aria-hidden="true" />
            <XIcon v-else class="block h-6 w-6" aria-hidden="true" />
          </DisclosureButton>
        </div>
      </div>
    </div>

    <DisclosurePanel class="sm:hidden">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link
          v-for="link in links"
          :key="link.name"
          :to="link.href"
          class="text-gray-300 hover:bg-primary transition-all duration-200 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
        >
          {{ link.name }}
        </router-link>
      </div>
    </DisclosurePanel>
  </Disclosure>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuth } from '../store/auth';
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import { MenuIcon, XIcon } from "@heroicons/vue/outline";

const auth = useAuth();
const authData = computed(() => auth.getAuthData);

const isScrolledDown = ref(false);
const links = [
  { name: 'Home', href: '/' },
  { name: 'Login', href: '/login' },
  { name: 'Register', href: '/register' },
];

const authLinks = [
  { name: 'Dashboard', href: '/dashboard' },
  { name: 'Profile', href: '/profile' }
];

const checkScroll = () => {
  if (window.scrollY > 100) {
    isScrolledDown.value = true;
  } else {
    isScrolledDown.value = false;
  }
};

window.addEventListener('scroll', checkScroll);

onMounted(() => {
  checkScroll();
});

onMounted(() => {
  checkScroll();
});
</script>