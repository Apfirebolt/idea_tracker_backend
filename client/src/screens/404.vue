<template>
    <div class="min-h-screen flex flex-col items-center justify-center bg-gray-100">
        <h1 class="text-9xl font-extrabold text-gray-400 tracking-widest">404</h1>
        <div class="bg-blue-500 px-2 text-sm rounded rotate-12 absolute mt-20">
            Page Not Found
        </div>
        <p class="mt-8 text-gray-600 text-lg">
            Sorry, the page you are looking for does not exist.
        </p>
        <router-link
            to="/"
            class="mt-6 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
            Go Home
        </router-link>
    </div>
</template>

<script setup>
// No script needed for this simple 404 page
</script>