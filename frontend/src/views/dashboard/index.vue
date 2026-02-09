<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>我的文献</span>
              <el-icon><Document /></el-icon>
            </div>
          </template>
          <div class="stat-value">128</div>
          <div class="stat-label">篇文献</div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>我的项目</span>
              <el-icon><FolderOpened /></el-icon>
            </div>
          </template>
          <div class="stat-value">5</div>
          <div class="stat-label">个在研项目</div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>我的论文</span>
              <el-icon><Trophy /></el-icon>
            </div>
          </template>
          <div class="stat-value">12</div>
          <div class="stat-label">篇发表论文</div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>H指数</span>
              <el-icon><Star /></el-icon>
            </div>
          </template>
          <div class="stat-value">8</div>
          <div class="stat-label">学术影响力</div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card title="快捷入口">
          <el-row :gutter="10">
            <el-col :span="8">
              <el-button type="primary" size="large" class="quick-btn">
                <el-icon><Upload /></el-icon>
                上传文献
              </el-button>
            </el-col>
            <el-col :span="8">
              <el-button type="success" size="large" class="quick-btn">
                <el-icon><Plus /></el-icon>
                新建项目
              </el-button>
            </el-col>
            <el-col :span="8">
              <el-button type="warning" size="large" class="quick-btn">
                <el-icon><Search /></el-icon>
                文献检索
              </el-button>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card title="待办事项">
          <el-empty description="暂无待办事项" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.stat-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #909399;
    font-size: 14px;
  }
  
  .stat-value {
    font-size: 32px;
    font-weight: bold;
    color: #303133;
    margin: 10px 0;
  }
  
  .stat-label {
    color: #909399;
    font-size: 12px;
  }
}

.mt-20 {
  margin-top: 20px;
}

.quick-btn {
  width: 100%;
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>
