import { createRouter, createWebHistory } from 'vue-router';
import InputPage from '@/components/InputPage.vue';
import LoadingPage from '@/components/LoadingPage.vue';
import OutputPage from '@/components/OutputPage.vue';

const routes = [
  {
    path: '/',
    name: 'InputPage',
    component: InputPage
  },
  {
    path: '/loading',
    name: 'LoadingPage',
    component: LoadingPage
  },
  {
    path: '/output',
    name: 'OutputPage',
    component: OutputPage
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
