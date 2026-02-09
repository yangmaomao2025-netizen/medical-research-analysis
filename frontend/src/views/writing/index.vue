<template>
  <div class="writing-page">
    <h2>论文写作助手</h2>
    
    <!-- 功能选择 -->
    <el-tabs v-model="activeTab" type="border-card">
      <el-tab-pane label="大纲生成" name="outline">
        <el-form :model="outlineForm" label-position="top">
          <el-form-item label="论文标题">
            <el-input v-model="outlineForm.title" placeholder="请输入论文标题" />
          </el-form-item>
          
          <el-form-item label="论文类型">
            <el-select v-model="outlineForm.paper_type" style="width: 100%">
              <el-option label="原创研究(Original Article)" value="research_article" />
              <el-option label="综述(Review)" value="review" />
              <el-option label="病例报告(Case Report)" value="case_report" />
              <el-option label="Meta分析" value="meta_analysis" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="包含章节">
            <el-checkbox-group v-model="outlineForm.sections">
              <el-checkbox label="abstract">摘要</el-checkbox>
              <el-checkbox label="introduction">引言</el-checkbox>
              <el-checkbox label="methods">方法</el-checkbox>
              <el-checkbox label="results">结果</el-checkbox>
              <el-checkbox label="discussion">讨论</el-checkbox>
              <el-checkbox label="conclusion">结论</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="generateOutline">
              生成大纲
            </el-button>
          </el-form-item>
        </el-form>
        
        <!-- 结果 -->
        <div v-if="outlineResult" class="result-box">
          <el-divider />
          <h4>生成的大纲</h4>
          <el-input v-model="outlineResult.outline" type="textarea" :rows="15" readonly />
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="文本润色" name="polish">
        <el-form :model="polishForm" label-position="top">
          <el-form-item label="原文">
            <el-input 
              v-model="polishForm.text" 
              type="textarea" 
              :rows="8"
              placeholder="请输入需要润色的文本"
            />
          </el-form-item>
          
          <el-form-item label="润色类型">
            <el-radio-group v-model="polishForm.polish_type">
              <el-radio label="grammar">语法修正</el-radio>
              <el-radio label="clarity">清晰表达</el-radio>
              <el-radio label="academic">学术增强</el-radio>
              <el-radio label="concise">精简表达</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item label="目标期刊（选填）">
            <el-input v-model="polishForm.target_journal" placeholder="如：Nature Medicine" />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="polishText">
              开始润色
            </el-button>
          </el-form-item>
        </el-form>
        
        <!-- 结果 -->
        <div v-if="polishResult" class="result-box">
          <el-divider />
          <h4>润色结果</h4>
          <el-input v-model="polishResult.polished_text" type="textarea" :rows="15" readonly />
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="参考文献" name="references">
        <el-form :model="refForm" label-position="top">
          <el-form-item label="研究主题">
            <el-input v-model="refForm.topic" placeholder="请输入研究主题" />
          </el-form-item>
          
          <el-form-item label="关键词">
            <el-select
              v-model="refForm.keywords"
              multiple
              filterable
              allow-create
              placeholder="输入关键词后按回车"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="suggestReferences">
              推荐文献
            </el-button>
          </el-form-item>
        </el-form>
        
        <!-- 结果 -->
        <div v-if="refResult" class="result-box">
          <el-divider />
          <h4>推荐文献</h4>
          <pre>{{ refResult.suggestions }}</pre>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('outline')
const loading = ref(false)

const outlineForm = reactive({
  title: '',
  paper_type: 'research_article',
  sections: ['abstract', 'introduction', 'methods', 'results', 'discussion', 'conclusion']
})

const polishForm = reactive({
  text: '',
  polish_type: 'academic',
  target_journal: ''
})

const refForm = reactive({
  topic: '',
  keywords: []
})

const outlineResult = ref<any>(null)
const polishResult = ref<any>(null)
const refResult = ref<any>(null)

const generateOutline = async () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    outlineResult.value = {
      outline: `# 论文大纲：${outlineForm.title}\n\n## 1. Abstract\n- **主题**：研究概述\n- **要点**：...`,
      title: outlineForm.title,
      paper_type: outlineForm.paper_type
    }
    ElMessage.success('大纲生成成功')
  }, 2000)
}

const polishText = async () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    polishResult.value = {
      polished_text: polishForm.text,
      original_text: polishForm.text,
      polish_type: polishForm.polish_type
    }
    ElMessage.success('润色完成')
  }, 2000)
}

const suggestReferences = async () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    refResult.value = {
      suggestions: '推荐文献列表...',
      topic: refForm.topic,
      keywords: refForm.keywords
    }
    ElMessage.success('文献推荐完成')
  }, 2000)
}
</script>

<style scoped>
.writing-page {
  h2 {
    margin-bottom: 20px;
  }
  
  .result-box {
    margin-top: 20px;
    
    h4 {
      margin-bottom: 15px;
    }
  }
  
  pre {
    background: #f5f7fa;
    padding: 15px;
    border-radius: 4px;
    overflow-x: auto;
  }
}
</style>
