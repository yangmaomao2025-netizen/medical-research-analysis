<template>
  <div class="literature-page">
    <!-- 搜索栏 -->
    <el-card class="search-card">
      <el-input
        v-model="searchForm.keyword"
        placeholder="搜索标题、摘要、关键词..."
        size="large"
        clearable
        class="search-input"
      >
        <template #append>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>搜索
          </el-button>
        </template>
      </el-input>
      
      <el-row :gutter="10" class="filter-row">
        <el-col :span="4">
          <el-select v-model="searchForm.literature_type" placeholder="文献类型" clearable>
            <el-option label="学术期刊" value="journal" />
            <el-option label="会议论文" value="conference" />
            <el-option label="学位论文" value="thesis" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.year_from" placeholder="起始年份" clearable>
            <el-option v-for="year in yearOptions" :key="year" :label="year" :value="year" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.is_sci" placeholder="SCI收录" clearable>
            <el-option label="SCI" :value="true" />
            <el-option label="非SCI" :value="false" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button @click="resetFilter">重置</el-button>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 操作栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleUpload">
        <el-icon><Upload /></el-icon>上传文献
      </el-button>
      <el-button @click="handleImport">数据库导入</el-button>
    </div>
    
    <!-- 文献列表 -->
    <el-table :data="tableData" stripe class="literature-table">
      <el-table-column type="selection" width="55" />
      <el-table-column label="标题" min-width="300">
        <template #default="{ row }">
          <div class="title-cell">
            <div class="title-text" @click="handlePreview(row)">{{ row.title }}</div>
            <div class="title-meta">
              <el-tag v-for="disease in row.diseases?.slice(0, 3)" :key="disease" size="small">
                {{ disease }}
              </el-tag>
            </div>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column label="作者" width="150" >
        <template #default="{ row }">
          <span>{{ row.first_author || row.authors?.[0] }}</span>
          <span v-if="row.authors?.length > 1" class="author-more">等</span>
        </template>
      </el-table-column>
      
      <el-table-column label="期刊/会议" width="180">
        <template #default="{ row }">
          <div>{{ row.journal }}</div>
          <div v-if="row.impact_factor" class="if-text">IF: {{ row.impact_factor }}</div>
        </template>
      </el-table-column>
      
      <el-table-column prop="year" label="年份" width="80" />
      
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handlePreview(row)">预览</el-button>
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const searchForm = reactive({
  keyword: '',
  literature_type: '',
  year_from: '',
  is_sci: undefined as boolean | undefined
})

const yearOptions = Array.from({ length: 20 }, (_, i) => (2026 - i).toString())

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 128
})

// 模拟数据
const tableData = ref([
  {
    id: '1',
    title: '人工智能在医学影像诊断中的应用研究进展',
    diseases: ['肺癌', '医学影像', '人工智能'],
    authors: ['张三', '李四', '王五'],
    first_author: '张三',
    journal: '中华医学杂志',
    impact_factor: 3.5,
    year: 2025
  },
  {
    id: '2',
    title: '基于深度学习的肺结节检测算法研究',
    diseases: ['肺结节', '深度学习', 'CT影像'],
    authors: ['李四', '赵六'],
    first_author: '李四',
    journal: 'Nature Medicine',
    impact_factor: 82.9,
    year: 2025
  }
])

const handleSearch = () => {
  console.log('搜索', searchForm)
}

const resetFilter = () => {
  Object.assign(searchForm, {
    keyword: '',
    literature_type: '',
    year_from: '',
    is_sci: undefined
  })
}

const handleUpload = () => {
  console.log('上传文献')
}

const handleImport = () => {
  console.log('数据库导入')
}

const handlePreview = (row: any) => {
  console.log('预览', row)
}

const handleEdit = (row: any) => {
  console.log('编辑', row)
}
</script>

<style scoped>
.literature-page {
  .search-card {
    margin-bottom: 20px;
    
    .search-input {
      margin-bottom: 15px;
    }
    
    .filter-row {
      margin-top: 10px;
    }
  }
  
  .toolbar {
    margin-bottom: 20px;
  }
  
  .literature-table {
    .title-cell {
      .title-text {
        color: #409EFF;
        cursor: pointer;
        font-weight: 500;
        
        &:hover {
          text-decoration: underline;
        }
      }
      
      .title-meta {
        margin-top: 5px;
      }
    }
    
    .author-more {
      color: #909399;
      margin-left: 5px;
    }
    
    .if-text {
      color: #67C23A;
      font-size: 12px;
      margin-top: 2px;
    }
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
