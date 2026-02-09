<template>
  <div class="project-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-title">
        <h3>我的项目</h3>
        <p>管理和跟踪您的科研项目</p>
      </div>
      <el-button type="primary" size="large" @click="handleCreate">
        <el-icon><Plus /></el-icon>新建项目
      </el-button>
    </div>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">5</div>
          <div class="stat-label">在研项目</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">2</div>
          <div class="stat-label">招募中</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">8</div>
          <div class="stat-label">已完成</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">85%</div>
          <div class="stat-label">平均进度</div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 项目列表 -->
    <el-card class="project-list">
      <template #header>
        <div class="list-header">
          <span>项目列表</span>
          <el-radio-group v-model="filterStatus" size="small">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="in_progress">进行中</el-radio-button>
            <el-radio-button label="recruiting">招募中</el-radio-button>
            <el-radio-button label="completed">已完成</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      
      <el-table :data="projectList" stripe>
        <el-table-column label="项目名称" min-width="250">
          <template #default="{ row }">
            <div class="project-name">
              <div class="name-text" @click="handleDetail(row)">{{ row.title }}</div>
              <div class="name-meta">
                <el-tag v-for="tag in row.keywords" :key="tag" size="small" effect="plain">
                  {{ tag }}
                </el-tag>
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTypeTag(row.project_type)">{{ getTypeText(row.project_type) }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="进度" width="200">
          <template #default="{ row }">
            <div class="progress-cell">
              <el-progress :percentage="row.progress_percent" />
              <span class="progress-text">{{ row.progress_percent }}%</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="时间" width="180">
          <template #default="{ row }">
            <div>{{ row.start_date }} ~</div>
            <div>{{ row.end_date }}</div>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleDetail(row)">详情</el-button>
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const filterStatus = ref('')

const projectList = ref([
  {
    id: '1',
    title: '基于AI的肺癌早期筛查系统研究',
    keywords: ['肺癌', 'AI', '影像诊断'],
    project_type: 'clinical_trial',
    status: 'in_progress',
    progress_percent: 65,
    start_date: '2025-01-15',
    end_date: '2026-01-14'
  },
  {
    id: '2',
    title: '糖尿病患者视网膜病变预测模型',
    keywords: ['糖尿病', '视网膜', '预测模型'],
    project_type: 'retrospective',
    status: 'recruiting',
    progress_percent: 20,
    start_date: '2025-03-01',
    end_date: '2025-12-31'
  },
  {
    id: '3',
    title: '新型抗生素对耐药菌的体外活性研究',
    keywords: ['抗生素', '耐药菌', '体外实验'],
    project_type: 'basic_research',
    status: 'completed',
    progress_percent: 100,
    start_date: '2024-01-01',
    end_date: '2024-12-31'
  }
])

const getTypeTag = (type: string) => {
  const map: Record<string, string> = {
    clinical_trial: 'primary',
    retrospective: 'success',
    basic_research: 'warning',
    real_world: 'info'
  }
  return map[type] || ''
}

const getTypeText = (type: string) => {
  const map: Record<string, string> = {
    clinical_trial: '临床试验',
    retrospective: '回顾性研究',
    basic_research: '基础研究',
    real_world: '真实世界研究'
  }
  return map[type] || type
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'info',
    recruiting: 'success',
    in_progress: 'primary',
    completed: 'success',
    suspended: 'danger'
  }
  return map[status] || ''
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '待立项',
    recruiting: '招募中',
    in_progress: '进行中',
    completed: '已完成',
    suspended: '已暂停'
  }
  return map[status] || status
}

const handleCreate = () => {
  console.log('新建项目')
}

const handleDetail = (row: any) => {
  console.log('查看详情', row)
}

const handleEdit = (row: any) => {
  console.log('编辑', row)
}
</script>

<style scoped>
.project-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    .header-title {
      h3 {
        margin: 0;
        color: #303133;
      }
      
      p {
        margin: 5px 0 0;
        color: #909399;
        font-size: 14px;
      }
    }
  }
  
  .stats-row {
    margin-bottom: 20px;
    
    .stat-card {
      text-align: center;
      
      .stat-value {
        font-size: 32px;
        font-weight: bold;
        color: #409EFF;
      }
      
      .stat-label {
        margin-top: 5px;
        color: #909399;
        font-size: 14px;
      }
    }
  }
  
  .project-list {
    .list-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .project-name {
      .name-text {
        color: #409EFF;
        cursor: pointer;
        font-weight: 500;
        
        &:hover {
          text-decoration: underline;
        }
      }
      
      .name-meta {
        margin-top: 5px;
      }
    }
    
    .progress-cell {
      display: flex;
      align-items: center;
      gap: 10px;
      
      .el-progress {
        flex: 1;
      }
      
      .progress-text {
        font-size: 12px;
        color: #606266;
        min-width: 35px;
      }
    }
  }
}
</style>
