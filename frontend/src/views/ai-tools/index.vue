<template>
  <div class="ai-tools-page">
    <h2>AI科研助手</h2>
    
    <!-- 功能卡片 -->
    <el-row :gutter="20" class="tools-row">
      <el-col :span="8">
        <el-card class="tool-card" @click="activeTab = 'protocol'">
          <el-icon class="tool-icon" :size="48"><Document /></el-icon>
          <h3>研究方案生成</h3>
          <p>输入研究题目和目的，AI自动生成完整研究方案</p>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="tool-card" @click="activeTab = 'topic'">
          <el-icon class="tool-icon" :size="48"><Lightning /></el-icon>
          <h3>智能选题</h3>
          <p>基于研究领域，推荐创新性和可行性选题</p>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="tool-card" @click="activeTab = 'stats'">
          <el-icon class="tool-icon" :size="48"><DataAnalysis /></el-icon>
          <h3>统计分析</h3>
          <p>根据数据类型和研究设计，推荐统计方法</p>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 研究方案生成 -->
    <el-card v-if="activeTab === 'protocol'" class="form-card">
      <template #header>
        <div class="card-header">
          <span>生成研究方案</span>
        </div>
      </template>
      
      <el-form :model="protocolForm" label-position="top">
        <el-form-item label="研究题目">
          <el-input v-model="protocolForm.title" placeholder="请输入研究题目" />
        </el-form-item>
        
        <el-form-item label="研究类型">
          <el-select v-model="protocolForm.study_type" placeholder="选择研究类型" style="width: 100%">
            <el-option label="随机对照试验(RCT)" value="rct" />
            <el-option label="队列研究" value="cohort" />
            <el-option label="病例对照研究" value="case_control" />
            <el-option label="横断面研究" value="cross_sectional" />
            <el-option label="回顾性研究" value="retrospective" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="疾病/领域">
          <el-input v-model="protocolForm.disease" placeholder="如：肺癌、糖尿病等" />
        </el-form-item>
        
        <el-form-item label="研究目的">
          <el-input 
            v-model="protocolForm.objectives" 
            type="textarea" 
            :rows="3"
            placeholder="描述您的研究目的和主要研究问题"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" @click="generateProtocol">
            生成方案
          </el-button>
        </el-form-item>
      </el-form>
      
      <!-- 结果展示 -->
      <div v-if="protocolResult" class="result-section">
        <el-divider />
        <h4>生成的研究方案</h4>
        <el-input
          v-model="protocolResult.protocol"
          type="textarea"
          :rows="20"
          readonly
        />
      </div>
    </el-card>
    
    <!-- 智能选题 -->
    <el-card v-if="activeTab === 'topic'" class="form-card">
      <template #header>
        <div class="card-header">
          <span>智能选题</span>
        </div>
      </template>
      
      <el-form :model="topicForm" label-position="top">
        <el-form-item label="研究领域">
          <el-input v-model="topicForm.research_area" placeholder="如：肿瘤免疫治疗、心血管疾病等" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" @click="suggestTopics">
            获取选题建议
          </el-button>
        </el-form-item>
      </el-form>
      
      <!-- 结果展示 -->
      <div v-if="topicResult" class="result-section">
        <el-divider />
        <h4>推荐选题</h4>
        <div v-for="(topic, index) in topicResult.topics" :key="index" class="topic-item">
          <h5>{{ topic.title }}</h5>
          <p>{{ topic.description }}</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('protocol')
const loading = ref(false)

const protocolForm = reactive({
  title: '',
  study_type: '',
  disease: '',
  objectives: ''
})

const topicForm = reactive({
  research_area: ''
})

const protocolResult = ref<any>(null)
const topicResult = ref<any>(null)

const generateProtocol = async () => {
  loading.value = true
  // TODO: 调用API
  setTimeout(() => {
    loading.value = false
    protocolResult.value = {
      protocol: `# 研究方案：${protocolForm.title}\n\n## 1. 研究背景与意义\n...`,
      title: protocolForm.title,
      study_type: protocolForm.study_type
    }
    ElMessage.success('方案生成成功')
  }, 2000)
}

const suggestTopics = async () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    topicResult.value = {
      topics: [
        { title: '选题1：XXX', description: '描述...' },
        { title: '选题2：XXX', description: '描述...' }
      ]
    }
    ElMessage.success('选题建议生成成功')
  }, 2000)
}
</script>

<style scoped>
.ai-tools-page {
  h2 {
    margin-bottom: 20px;
    color: #303133;
  }
}

.tools-row {
  margin-bottom: 30px;
}

.tool-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }
  
  .tool-icon {
    color: #409EFF;
    margin-bottom: 15px;
  }
  
  h3 {
    margin: 0 0 10px;
    color: #303133;
  }
  
  p {
    color: #909399;
    font-size: 14px;
    margin: 0;
  }
}

.form-card {
  .card-header {
    font-weight: bold;
    font-size: 16px;
  }
}

.result-section {
  margin-top: 20px;
  
  h4 {
    margin-bottom: 15px;
    color: #303133;
  }
}

.topic-item {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 10px;
  
  h5 {
    margin: 0 0 5px;
    color: #409EFF;
  }
  
  p {
    margin: 0;
    color: #606266;
    font-size: 14px;
  }
}
</style>
