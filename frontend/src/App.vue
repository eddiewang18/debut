<template>
    <div class="app">
      <!-- 左側側邊欄 -->
      <nav :class="{ collapsed: isCollapsed }" class="sidebar">
        <button class="toggle-btn" @click="toggleSidebar">
          {{ isCollapsed ? ">>" : "<<" }}
        </button>
        <div class="links">
          <RouterLink to="/" class="nav-link">首頁</RouterLink>
          <RouterLink to="/machine" class="nav-link">機種設定</RouterLink>
        </div>
      </nav>
      
      <!-- 右側主要內容區 -->
      <div class="content">
        <RouterView></RouterView>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  // 控制側邊欄展開/收合
  const isCollapsed = ref(false);
  
  const toggleSidebar = () => {
    isCollapsed.value = !isCollapsed.value;
  };
  </script>
  
  <style scoped>
  /* 基本佈局 */
  .app {
    display: flex;
    height: 100vh;
    font-family: Arial, sans-serif;
    color: #333;
  }
  
  /* 左側側邊欄樣式 */
  .sidebar {
    width: 25%;
    max-width: 300px;
    min-width: 80px;
    background-color: #2c3e50;
    color: #ecf0f1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    transition: width 0.3s ease;
    overflow: hidden;
  }
  
  .sidebar.collapsed {
    width: 80px;
  }
  
  .sidebar .toggle-btn {
    background: none;
    border: none;
    color: inherit;
    font-size: 1rem;
    cursor: pointer;
    padding: 10px;
    align-self: flex-end;
  }
  
  .sidebar .links {
    display: flex;
    flex-direction: column;
    width: 100%;
    padding: 10px;
  }
  
  .nav-link {
    text-decoration: none;
    color: #ecf0f1;
    padding: 10px 15px;
    border-radius: 5px;
    transition: background 0.3s ease;
  }
  
  .nav-link:hover {
    background-color: #34495e;
  }
  
  .sidebar.collapsed .nav-link {
    text-align: center;
    font-size: 0.9rem;
    padding: 10px 5px;
  }
  
  /* 右側內容樣式 */
  .content {
    flex: 1;
    padding: 20px;
    background-color: #ecf0f1;
    overflow-y: auto;
  }
  </style>
  