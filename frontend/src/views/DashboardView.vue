<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Navigation -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-primary-600">InfinityInsight</h1>
          </div>

          <div class="flex items-center space-x-4">
            <router-link to="/datasets" class="text-gray-700 hover:text-primary-600">
              Datasets
            </router-link>
            <router-link to="/analyze" class="text-gray-700 hover:text-primary-600">
              Analyze
            </router-link>
            <router-link to="/ml" class="text-gray-700 hover:text-primary-600">
              ML
            </router-link>
            <router-link to="/chat" class="text-gray-700 hover:text-primary-600">
              Chat
            </router-link>

            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-700">{{ user?.full_name }}</span>
              <button @click="handleLogout" class="btn-secondary text-sm">
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900">
          Welcome back, {{ user?.full_name }}!
        </h2>
        <p class="mt-2 text-gray-600">
          Start analyzing your data with powerful AI-driven insights
        </p>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="card hover:shadow-lg transition-shadow cursor-pointer" @click="$router.push('/datasets')">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-primary-100 rounded-lg p-3">
              <svg class="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold">Upload Data</h3>
              <p class="text-gray-600 text-sm">Import your datasets</p>
            </div>
          </div>
        </div>

        <div class="card hover:shadow-lg transition-shadow cursor-pointer" @click="$router.push('/analyze')">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-green-100 rounded-lg p-3">
              <svg class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold">Run Analysis</h3>
              <p class="text-gray-600 text-sm">Statistical tests & more</p>
            </div>
          </div>
        </div>

        <div class="card hover:shadow-lg transition-shadow cursor-pointer" @click="$router.push('/chat')">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-purple-100 rounded-lg p-3">
              <svg class="h-8 w-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold">Chat with Data</h3>
              <p class="text-gray-600 text-sm">Natural language queries</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="card">
        <h3 class="text-xl font-semibold mb-4">Getting Started</h3>
        <div class="space-y-4">
          <div class="border-l-4 border-primary-500 pl-4">
            <h4 class="font-medium">1. Upload your data</h4>
            <p class="text-sm text-gray-600">Support for CSV, Excel, SPSS, and more</p>
          </div>
          <div class="border-l-4 border-primary-500 pl-4">
            <h4 class="font-medium">2. Explore and profile</h4>
            <p class="text-sm text-gray-600">Get instant insights and data summaries</p>
          </div>
          <div class="border-l-4 border-primary-500 pl-4">
            <h4 class="font-medium">3. Run analyses</h4>
            <p class="text-sm text-gray-600">SPSS-equivalent statistical tests, ML models, and more</p>
          </div>
          <div class="border-l-4 border-primary-500 pl-4">
            <h4 class="font-medium">4. Chat with your data</h4>
            <p class="text-sm text-gray-600">Ask questions in plain English</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
