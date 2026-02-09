import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue')
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '首页', icon: 'HomeFilled' }
      },
      {
        path: '/literatures',
        name: 'Literatures',
        component: () => import('@/views/literature/index.vue'),
        meta: { title: '文献管理', icon: 'Document' }
      },
      {
        path: '/projects',
        name: 'Projects',
        component: () => import('@/views/project/index.vue'),
        meta: { title: '我的项目', icon: 'FolderOpened' }
      },
      {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/views/profile/index.vue'),
        meta: { title: '个人中心', icon: 'UserFilled' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
