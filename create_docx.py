#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
急危状态预警决策方案文档生成器
使用标准库创建docx文件
"""

import zipfile
import os
import tempfile
import shutil
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# DOCX XML命名空间
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
}

# 注册命名空间
for prefix, uri in NAMESPACES.items():
    try:
        from xml.etree.ElementTree import register_namespace
        register_namespace(prefix, uri)
    except:
        pass

def prettify_xml(elem):
    """美化XML输出"""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='UTF-8')

def create_content_types():
    """创建[Content_Types].xml"""
    root = Element('Types', xmlns='http://schemas.openxmlformats.org/package/2006/content-types')
    SubElement(root, 'Default', Extension='rels', ContentType='application/vnd.openxmlformats-package.relationships+xml')
    SubElement(root, 'Default', Extension='xml', ContentType='application/xml')
    SubElement(root, 'Override', PartName='/word/document.xml', 
               ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml')
    SubElement(root, 'Override', PartName='/word/styles.xml', 
               ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml')
    SubElement(root, 'Override', PartName='/word/settings.xml', 
               ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml')
    return prettify_xml(root)

def create_rels():
    """创建_rels/.rels"""
    root = Element('Relationships', xmlns='http://schemas.openxmlformats.org/package/2006/relationships')
    SubElement(root, 'Relationship', Id='rId1', 
               Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument',
               Target='word/document.xml')
    return prettify_xml(root)

def create_document_rels():
    """创建word/_rels/document.xml.rels"""
    root = Element('Relationships', xmlns='http://schemas.openxmlformats.org/package/2006/relationships')
    SubElement(root, 'Relationship', Id='rId1', 
               Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles',
               Target='styles.xml')
    SubElement(root, 'Relationship', Id='rId2', 
               Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings',
               Target='settings.xml')
    return prettify_xml(root)

def create_settings():
    """创建word/settings.xml"""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    root = Element('{%s}settings' % ns)
    SubElement(root, '{%s}zoom' % ns, {'{%s}val' % ns: '100'})
    SubElement(root, '{%s}defaultTabStop' % ns, {'{%s}val' % ns: '720'})
    SubElement(root, '{%s}characterSpacingControl' % ns, {'{%s}val' % ns: 'doNotCompress'})
    SubElement(root, '{%s}compat' % ns)
    return prettify_xml(root)

def create_styles():
    """创建word/styles.xml"""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    root = Element('{%s}styles' % ns)
    
    # 文档默认设置
    doc_defaults = SubElement(root, '{%s}docDefaults' % ns)
    rPrDefault = SubElement(doc_defaults, '{%s}rPrDefault' % ns)
    rPr = SubElement(rPrDefault, '{%s}rPr' % ns)
    SubElement(rPr, '{%s}rFonts' % ns, {'{%s}ascii' % ns: '宋体', '{%s}eastAsia' % ns: '宋体', '{%s}hAnsi' % ns: '宋体'})
    SubElement(rPr, '{%s}sz' % ns, {'{%s}val' % ns: '24'})
    SubElement(rPr, '{%s}szCs' % ns, {'{%s}val' % ns: '24'})
    SubElement(rPr, '{%s}lang' % ns, {'{%s}val' % ns: 'zh-CN', '{%s}eastAsia' % ns: 'zh-CN'})
    
    pPrDefault = SubElement(doc_defaults, '{%s}pPrDefault' % ns)
    pPr = SubElement(pPrDefault, '{%s}pPr' % ns)
    SubElement(pPr, '{%s}spacing' % ns, {'{%s}line' % ns: '360', '{%s}lineRule' % ns: 'auto'})
    
    # 正文样式
    style = SubElement(root, '{%s}style' % ns, {'{%s}type' % ns: 'paragraph', '{%s}default' % ns: '1', '{%s}styleId' % ns: 'Normal'})
    SubElement(style, '{%s}name' % ns, {'{%s}val' % ns: 'Normal'})
    pPr = SubElement(style, '{%s}pPr' % ns)
    SubElement(pPr, '{%s}spacing' % ns, {'{%s}line' % ns: '360', '{%s}lineRule' % ns: 'auto'})
    rPr = SubElement(style, '{%s}rPr' % ns)
    SubElement(rPr, '{%s}rFonts' % ns, {'{%s}ascii' % ns: '宋体', '{%s}eastAsia' % ns: '宋体', '{%s}hAnsi' % ns: '宋体'})
    SubElement(rPr, '{%s}sz' % ns, {'{%s}val' % ns: '24'})
    
    # 标题1样式
    style = SubElement(root, '{%s}style' % ns, {'{%s}type' % ns: 'paragraph', '{%s}styleId' % ns: 'Heading1'})
    SubElement(style, '{%s}name' % ns, {'{%s}val' % ns: 'heading 1'})
    SubElement(style, '{%s}basedOn' % ns, {'{%s}val' % ns: 'Normal'})
    SubElement(style, '{%s}qFormat' % ns)
    pPr = SubElement(style, '{%s}pPr' % ns)
    SubElement(pPr, '{%s}keepNext' % ns)
    SubElement(pPr, '{%s}keepLines' % ns)
    SubElement(pPr, '{%s}spacing' % ns, {'{%s}before' % ns: '240', '{%s}after' % ns: '120'})
    SubElement(pPr, '{%s}outlineLvl' % ns, {'{%s}val' % ns: '0'})
    rPr = SubElement(style, '{%s}rPr' % ns)
    SubElement(rPr, '{%s}b' % ns)
    SubElement(rPr, '{%s}sz' % ns, {'{%s}val' % ns: '36'})
    SubElement(rPr, '{%s}color' % ns, {'{%s}val' % ns: '2E74B5'})
    
    # 标题2样式
    style = SubElement(root, '{%s}style' % ns, {'{%s}type' % ns: 'paragraph', '{%s}styleId' % ns: 'Heading2'})
    SubElement(style, '{%s}name' % ns, {'{%s}val' % ns: 'heading 2'})
    SubElement(style, '{%s}basedOn' % ns, {'{%s}val' % ns: 'Normal'})
    SubElement(style, '{%s}qFormat' % ns)
    pPr = SubElement(style, '{%s}pPr' % ns)
    SubElement(pPr, '{%s}keepNext' % ns)
    SubElement(pPr, '{%s}keepLines' % ns)
    SubElement(pPr, '{%s}spacing' % ns, {'{%s}before' % ns: '200', '{%s}after' % ns: '100'})
    SubElement(pPr, '{%s}outlineLvl' % ns, {'{%s}val' % ns: '1'})
    rPr = SubElement(style, '{%s}rPr' % ns)
    SubElement(rPr, '{%s}b' % ns)
    SubElement(rPr, '{%s}sz' % ns, {'{%s}val' % ns: '28'})
    SubElement(rPr, '{%s}color' % ns, {'{%s}val' % ns: '2E74B5'})
    
    # 标题3样式
    style = SubElement(root, '{%s}style' % ns, {'{%s}type' % ns: 'paragraph', '{%s}styleId' % ns: 'Heading3'})
    SubElement(style, '{%s}name' % ns, {'{%s}val' % ns: 'heading 3'})
    SubElement(style, '{%s}basedOn' % ns, {'{%s}val' % ns: 'Normal'})
    SubElement(style, '{%s}qFormat' % ns)
    pPr = SubElement(style, '{%s}pPr' % ns)
    SubElement(pPr, '{%s}keepNext' % ns)
    SubElement(pPr, '{%s}spacing' % ns, {'{%s}before' % ns: '160', '{%s}after' % ns: '80'})
    SubElement(pPr, '{%s}outlineLvl' % ns, {'{%s}val' % ns: '2'})
    rPr = SubElement(style, '{%s}rPr' % ns)
    SubElement(rPr, '{%s}b' % ns)
    SubElement(rPr, '{%s}sz' % ns, {'{%s}val' % ns: '26'})
    
    return prettify_xml(root)

def create_paragraph(parent, text, style='Normal', bold=False, alignment=None):
    """创建段落"""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    p = SubElement(parent, '{%s}p' % ns)
    
    pPr = SubElement(p, '{%s}pPr' % ns)
    if style != 'Normal':
        SubElement(pPr, '{%s}pStyle' % ns, {'{%s}val' % ns: style})
    if alignment:
        SubElement(pPr, '{%s}jc' % ns, {'{%s}val' % ns: alignment})
    SubElement(pPr, '{%s}spacing' % ns, {'{%s}line' % ns: '360', '{%s}lineRule' % ns: 'auto'})
    
    r = SubElement(p, '{%s}r' % ns)
    rPr = SubElement(r, '{%s}rPr' % ns)
    if bold:
        SubElement(rPr, '{%s}b' % ns)
    SubElement(rPr, '{%s}rFonts' % ns, {'{%s}ascii' % ns: '宋体', '{%s}eastAsia' % ns: '宋体', '{%s}hAnsi' % ns: '宋体'})
    SubElement(rPr, '{%s}sz' % ns, {'{%s}val' % ns: '24'})
    
    t = SubElement(r, '{%s}t' % ns)
    t.text = text
    return p

def create_bullet_paragraph(parent, text, level=0):
    """创建项目符号段落"""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    p = SubElement(parent, '{%s}p' % ns)
    
    pPr = SubElement(p, '{%s}pPr' % ns)
    SubElement(pPr, '{%s}spacing' % ns, {'{%s}line' % ns: '360', '{%s}lineRule' % ns: 'auto'})
    
    # 简单缩进模拟项目符号
    ind = SubElement(pPr, '{%s}ind' % ns, {'{%s}left' % ns: str(720 * (level + 1))})
    
    r = SubElement(p, '{%s}r' % ns)
    rPr = SubElement(r, '{%s}rPr' % ns)
    SubElement(rPr, '{%s}rFonts' % ns, {'{%s}ascii' % ns: '宋体', '{%s}eastAsia' % ns: '宋体', '{%s}hAnsi' % ns: '宋体'})
    SubElement(rPr, '{%s}sz' % ns, {'{%s}val' % ns: '24'})
    
    t = SubElement(r, '{%s}t' % ns)
    t.text = '● ' + text if level == 0 else '○ ' + text
    return p

def create_document():
    """创建文档内容"""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    root = Element('{%s}document' % ns)
    body = SubElement(root, '{%s}body' % ns)
    
    # ===== 标题 =====
    create_paragraph(body, '急危状态预警决策方案', 'Heading1', alignment='center')
    create_paragraph(body, '——北京复兴医院区域医疗协同预警体系建设', 'Normal', alignment='center')
    create_paragraph(body, '', 'Normal')
    
    # ===== 第一章：项目概述与背景 =====
    create_paragraph(body, '第一章 项目概述与背景', 'Heading1')
    
    create_paragraph(body, '1.1 项目背景', 'Heading2')
    create_paragraph(body, '随着我国医疗卫生事业的快速发展，急危重症患者的救治能力成为衡量区域医疗水平的重要指标。北京复兴医院作为西城区核心医疗机构，肩负着辐射周边区域、提升整体急危重症救治能力的重任。', 'Normal')
    create_paragraph(body, '当前，各级医疗机构在急危重症识别和预警方面存在以下问题：', 'Normal')
    create_bullet_paragraph(body, '信息孤岛严重：各级医院信息系统独立运行，缺乏有效的数据共享机制')
    create_bullet_paragraph(body, '预警能力不足：传统的人工评估方式响应慢、准确率低，难以及时发现潜在危重患者')
    create_bullet_paragraph(body, '资源配置不均：危重患者分布与救治资源不匹配，转诊流程不畅')
    create_bullet_paragraph(body, '缺乏协同机制：区域内各级医疗机构之间缺乏统一的急危重症救治协同平台')
    
    create_paragraph(body, '1.2 建设目标', 'Heading2')
    create_paragraph(body, '本项目旨在以北京复兴医院为核心，构建覆盖西城区及周边区域的急危状态智能预警决策体系，实现以下目标：', 'Normal')
    create_bullet_paragraph(body, '建立多源异构数据整合平台，实现EMR、监护设备、检验系统、影像系统的数据融合')
    create_bullet_paragraph(body, '构建智能危重识别模型，对6类器官衰竭、5类临床表现、8类体征进行实时监测评估')
    create_bullet_paragraph(body, '打造多层次预警机制，通过弹窗、短信、APP推送等方式及时通知相关人员')
    create_bullet_paragraph(body, '形成区域医疗协同网络，连接三级医院、二级医院、基层医疗机构')
    create_bullet_paragraph(body, '建立预警处理追踪与反馈闭环，持续优化预警准确率和救治效果')
    
    create_paragraph(body, '1.3 实施范围', 'Heading2')
    create_paragraph(body, '本项目覆盖北京市西城区及周边区域，具体包括：', 'Normal')
    create_bullet_paragraph(body, '驻区三级医院：复兴医院、人民医院等三级综合医院')
    create_bullet_paragraph(body, '区属二级医院：西城区第二医院、广外医院等二级医疗机构')
    create_bullet_paragraph(body, '基层医疗机构：社区卫生服务中心、社区卫生服务站等基层医疗单位')
    create_paragraph(body, '通过构建三级联动的急危重症救治网络，实现区域内医疗资源的优化配置和高效利用。', 'Normal')
    
    # ===== 第二章：技术架构设计 =====
    create_paragraph(body, '第二章 技术架构设计', 'Heading1')
    
    create_paragraph(body, '2.1 总体架构', 'Heading2')
    create_paragraph(body, '本系统采用"云-边-端"协同架构，分为四层：数据采集层、数据处理层、智能分析层、应用服务层。', 'Normal')
    create_bullet_paragraph(body, '数据采集层：负责对接各类医疗信息系统，实现多源异构数据的实时采集')
    create_bullet_paragraph(body, '数据处理层：进行数据清洗、标准化、结构化处理，构建统一数据模型')
    create_bullet_paragraph(body, '智能分析层：基于AI算法实现危重状态识别、风险评估、趋势预测')
    create_bullet_paragraph(body, '应用服务层：提供预警通知、决策支持、协同调度等业务功能')
    
    create_paragraph(body, '2.2 数据采集层', 'Heading2')
    create_paragraph(body, '数据采集层对接以下系统：', 'Normal')
    create_paragraph(body, '（1）电子病历系统（EMR）', 'Heading3')
    create_bullet_paragraph(body, '通过HL7/FHIR标准接口对接医院EMR系统')
    create_bullet_paragraph(body, '采集患者基本信息、病史、诊断、医嘱等结构化数据')
    create_bullet_paragraph(body, '提取病程记录、查房记录等非结构化文本')
    
    create_paragraph(body, '（2）监护设备', 'Heading3')
    create_bullet_paragraph(body, '对接床旁监护仪、呼吸机、输注泵等设备')
    create_bullet_paragraph(body, '实时采集生命体征数据：心率、血压、血氧、呼吸频率等')
    create_bullet_paragraph(body, '支持多种通信协议：HL7、DICOM、自定义协议')
    
    create_paragraph(body, '（3）检验信息系统（LIS）', 'Heading3')
    create_bullet_paragraph(body, '对接实验室信息系统，获取检验结果')
    create_bullet_paragraph(body, '监测血气分析、生化指标、凝血功能等关键指标')
    create_bullet_paragraph(body, '设置危急值自动识别和预警机制')
    
    create_paragraph(body, '（4）影像归档系统（PACS）', 'Heading3')
    create_bullet_paragraph(body, '对接PACS系统获取影像检查报告')
    create_bullet_paragraph(body, '整合CT、X光、超声等影像学诊断结果')
    
    create_paragraph(body, '2.3 数据处理层', 'Heading2')
    create_paragraph(body, '数据处理层采用流批一体架构，实现实时数据处理和批量数据分析：', 'Normal')
    create_bullet_paragraph(body, '数据标准化：将不同系统的数据转换为统一的FHIR标准格式')
    create_bullet_paragraph(body, '数据质量管控：建立数据校验规则，识别并处理异常数据')
    create_bullet_paragraph(body, 'NLP语义提取：利用自然语言处理技术，从病程记录、检查报告中提取关键信息')
    create_bullet_paragraph(body, '时序数据建模：构建患者生命体征时序数据库，支持趋势分析')
    
    create_paragraph(body, '2.4 智能分析层', 'Heading2')
    create_paragraph(body, '智能分析层采用机器学习与规则引擎相结合的混合架构：', 'Normal')
    create_bullet_paragraph(body, '规则引擎：基于临床指南和专家经验，建立危重状态识别规则库')
    create_bullet_paragraph(body, '机器学习模型：利用深度学习算法，构建多器官衰竭预测模型')
    create_bullet_paragraph(body, '知识图谱：构建急危重症医学知识图谱，支持智能推理和辅助诊断')
    create_bullet_paragraph(body, '实时计算引擎：基于Flink实现毫秒级数据处理和预警触发')
    
    create_paragraph(body, '2.5 应用服务层', 'Heading2')
    create_paragraph(body, '应用服务层提供面向不同角色的业务功能：', 'Normal')
    create_bullet_paragraph(body, '医护工作站：集成到医生工作站和护士工作站，提供预警弹窗')
    create_bullet_paragraph(body, '移动端APP：医护人员可随时随地接收预警和处理任务')
    create_bullet_paragraph(body, '管理驾驶舱：为管理者提供数据可视化和决策支持')
    create_bullet_paragraph(body, '协同平台：支持跨机构转诊、远程会诊、资源调度')
    
    # ===== 第三章：六大核心功能模块详解 =====
    create_paragraph(body, '第三章 六大核心功能模块详解', 'Heading1')
    
    create_paragraph(body, '3.1 多源异构数据采集与整合模块', 'Heading2')
    create_paragraph(body, '本模块实现EMR、监护仪、LIS、PACS等多系统数据的统一采集和整合。', 'Normal')
    create_paragraph(body, '核心功能：', 'Normal')
    create_bullet_paragraph(body, '标准化数据接入：支持HL7 V2/V3、FHIR、DICOM等医疗信息标准')
    create_bullet_paragraph(body, '多协议适配器：支持TCP/IP、HTTP/HTTPS、WebSocket等多种通信协议')
    create_bullet_paragraph(body, '设备网关：实现床旁设备的即插即用接入')
    create_bullet_paragraph(body, '数据缓存队列：采用Kafka消息队列，保障数据可靠传输')
    create_bullet_paragraph(body, '数据映射配置：可视化配置界面，灵活应对不同厂商系统差异')
    
    create_paragraph(body, '3.2 数据高效整合与结构化处理模块', 'Heading2')
    create_paragraph(body, '本模块对采集的原始数据进行深度加工，提取有价值的临床信息。', 'Normal')
    create_paragraph(body, '核心功能：', 'Normal')
    create_bullet_paragraph(body, '数据标准化引擎：将异构数据转换为统一的数据模型')
    create_bullet_paragraph(body, 'NLP语义提取：采用BERT等预训练模型，从病历文本中提取实体和关系')
    create_bullet_paragraph(body, '主数据管理：建立患者主索引（EMPI），实现跨系统患者识别')
    create_bullet_paragraph(body, '数据质量控制：自动检测数据异常、缺失、不一致等问题')
    create_bullet_paragraph(body, '临床数据仓库：构建面向主题的临床数据仓库，支持多维分析')
    
    create_paragraph(body, 'NLP处理流程：', 'Normal')
    create_bullet_paragraph(body, '文本预处理：分词、去停用词、实体标注')
    create_bullet_paragraph(body, '实体识别：识别人名、地名、时间、医学术语等实体')
    create_bullet_paragraph(body, '关系抽取：提取实体间的语义关系')
    create_bullet_paragraph(body, '结构化输出：将提取信息转换为结构化数据存储')
    
    create_paragraph(body, '3.3 智能危重识别与综合评估模块', 'Heading2')
    create_paragraph(body, '本模块是本系统的核心，实现对急危重症的智能识别和综合评估。', 'Normal')
    
    create_paragraph(body, '3.3.1 六类器官衰竭评估', 'Heading3')
    create_paragraph(body, '系统对以下六类器官衰竭进行实时监测和评估：', 'Normal')
    create_bullet_paragraph(body, '脑功能衰竭：GCS评分、瞳孔反射、脑电图等')
    create_bullet_paragraph(body, '休克状态：血压、心率、乳酸、尿量等')
    create_bullet_paragraph(body, '呼吸衰竭：血氧饱和度、呼吸频率、血气分析等')
    create_bullet_paragraph(body, '心力衰竭：BNP、心肌酶谱、心电图等')
    create_bullet_paragraph(body, '肝衰竭：转氨酶、胆红素、凝血功能等')
    create_bullet_paragraph(body, '肾衰竭：肌酐、尿素氮、尿量等')
    
    create_paragraph(body, '3.3.2 五类临床表现识别', 'Heading3')
    create_paragraph(body, '系统重点监测以下五类危急临床表现：', 'Normal')
    create_bullet_paragraph(body, '窒息：气道阻塞、呼吸困难程度评估')
    create_bullet_paragraph(body, '大出血：出血量估计、血红蛋白变化趋势')
    create_bullet_paragraph(body, '昏迷：意识状态评估、GCS评分动态监测')
    create_bullet_paragraph(body, '心脏骤停：心电图实时监测、自动识别')
    
    create_paragraph(body, '3.3.3 八类体征实时监测', 'Heading3')
    create_paragraph(body, '系统对以下八类关键体征进行24小时不间断监测：', 'Normal')
    create_bullet_paragraph(body, '体温：核心体温监测，发热/低体温预警')
    create_bullet_paragraph(body, '心率：心率变异性分析，心律失常识别')
    create_bullet_paragraph(body, '血氧：脉搏血氧饱和度监测，低氧预警')
    create_bullet_paragraph(body, '呼吸频率：呼吸模式分析，呼吸暂停检测')
    create_bullet_paragraph(body, '血压：无创/有创血压监测，低血压预警')
    create_bullet_paragraph(body, '意识状态：GCS评分自动计算和趋势分析')
    create_bullet_paragraph(body, '瞳孔：瞳孔大小、对光反射评估')
    create_bullet_paragraph(body, '尿量：每小时尿量监测，肾灌注评估')
    create_bullet_paragraph(body, '皮肤状态：皮肤颜色、温度、湿度评估')
    
    create_paragraph(body, '3.3.4 综合评估算法', 'Heading3')
    create_paragraph(body, '系统采用多维度评分体系对危重程度进行综合评估：', 'Normal')
    create_bullet_paragraph(body, 'APACHE II评分：急性生理与慢性健康评分')
    create_bullet_paragraph(body, 'SOFA评分：序贯器官衰竭评估')
    create_bullet_paragraph(body, 'NEWS评分：国家早期预警评分')
    create_bullet_paragraph(body, 'MEWS评分：改良早期预警评分')
    create_bullet_paragraph(body, '自定义评分：支持医院自定义评分规则')
    
    create_paragraph(body, '3.4 动态监测与状态实时更新模块', 'Heading2')
    create_paragraph(body, '本模块实现患者状态的实时监控和动态更新。', 'Normal')
    create_paragraph(body, '核心功能：', 'Normal')
    create_bullet_paragraph(body, '实时数据流处理：基于Apache Flink实现毫秒级数据处理')
    create_bullet_paragraph(body, '状态机模型：定义患者状态的完整生命周期和转换规则')
    create_bullet_paragraph(body, '趋势分析算法：识别生命体征的变化趋势，预测恶化风险')
    create_bullet_paragraph(body, '异常模式识别：利用机器学习识别异常生理模式')
    create_bullet_paragraph(body, '床位视图：可视化展示病区所有患者的状态分布')
    
    create_paragraph(body, '监测频率配置：', 'Normal')
    create_bullet_paragraph(body, '高危患者：每秒采集一次生命体征')
    create_bullet_paragraph(body, '中危患者：每5分钟采集一次生命体征')
    create_bullet_paragraph(body, '低危患者：每15分钟采集一次生命体征')
    
    create_paragraph(body, '3.5 多层次多渠道预警模块', 'Heading2')
    create_paragraph(body, '本模块构建全方位的预警通知体系，确保预警信息及时触达相关人员。', 'Normal')
    create_paragraph(body, '预警级别划分：', 'Normal')
    create_bullet_paragraph(body, '一级预警（红色）：危及生命，需立即处理（如心脏骤停）')
    create_bullet_paragraph(body, '二级预警（橙色）：高度危险，需5分钟内处理（如严重低血压）')
    create_bullet_paragraph(body, '三级预警（黄色）：中度危险，需15分钟内处理（如轻度低氧）')
    create_bullet_paragraph(body, '四级预警（蓝色）：轻度异常，需密切观察（如单项指标异常）')
    
    create_paragraph(body, '预警渠道：', 'Normal')
    create_bullet_paragraph(body, '弹窗预警：在医生/护士工作站弹出醒目提示，支持声音报警')
    create_bullet_paragraph(body, '短信通知：自动发送短信给值班医生和护士长')
    create_bullet_paragraph(body, 'APP推送：通过手机APP推送实时预警信息')
    create_bullet_paragraph(body, '语音播报：在护士站进行语音播报')
    create_bullet_paragraph(body, '智能手环：医生佩戴智能手环接收震动提醒')
    
    create_paragraph(body, '预警规则引擎：', 'Normal')
    create_bullet_paragraph(body, '支持可视化规则配置')
    create_bullet_paragraph(body, '支持时间窗口条件（如持续低氧5分钟）')
    create_bullet_paragraph(body, '支持多指标组合条件')
    create_bullet_paragraph(body, '支持科室个性化规则')
    
    create_paragraph(body, '3.6 预警处理追踪与反馈闭环模块', 'Heading2')
    create_paragraph(body, '本模块实现预警处理的全程追踪和质量反馈。', 'Normal')
    create_paragraph(body, '核心功能：', 'Normal')
    create_bullet_paragraph(body, '任务派发：预警自动生成处理任务，派发给相关医护人员')
    create_bullet_paragraph(body, '处理计时：记录预警响应时间、处理时间')
    create_bullet_paragraph(body, '处理流程引导：提供标准化的处理流程指引')
    create_bullet_paragraph(body, '结果记录：记录处理措施和患者转归')
    create_bullet_paragraph(body, '质量分析：统计预警准确率、响应及时率等指标')
    
    create_paragraph(body, '反馈闭环机制：', 'Normal')
    create_bullet_paragraph(body, '假阳性反馈：医护人员标记误报，系统学习优化')
    create_bullet_paragraph(body, '漏报分析：定期回顾漏诊病例，完善预警规则')
    create_bullet_paragraph(body, '效果评估：追踪预警后患者的转归情况')
    create_bullet_paragraph(body, '知识积累：将处理经验沉淀为知识库')
    
    # ===== 第四章：分阶段实施路径 =====
    create_paragraph(body, '第四章 分阶段实施路径', 'Heading1')
    create_paragraph(body, '本项目计划分六个阶段实施，总工期约30个月。', 'Normal')
    
    create_paragraph(body, '第一阶段：需求调研与方案设计（第1-3个月）', 'Heading2')
    create_bullet_paragraph(body, '调研复兴医院及西城区各医疗机构的信息化现状')
    create_bullet_paragraph(body, '梳理急危重症救治业务流程')
    create_bullet_paragraph(body, '明确数据采集范围和接口需求')
    create_bullet_paragraph(body, '完成系统总体架构设计')
    create_bullet_paragraph(body, '编制详细实施方案和进度计划')
    
    create_paragraph(body, '第二阶段：基础设施与平台搭建（第4-8个月）', 'Heading2')
    create_bullet_paragraph(body, '部署云服务器和数据库集群')
    create_bullet_paragraph(body, '搭建数据采集中间件和消息队列')
    create_bullet_paragraph(body, '建立区域专网连接各医疗机构')
    create_bullet_paragraph(body, '完成数据标准化引擎开发')
    create_bullet_paragraph(body, '建立EMPI患者主索引系统')
    
    create_paragraph(body, '第三阶段：核心功能开发与测试（第9-14个月）', 'Heading2')
    create_bullet_paragraph(body, '开发多源数据采集适配器')
    create_bullet_paragraph(body, '实现NLP语义提取模块')
    create_bullet_paragraph(body, '开发智能危重识别算法')
    create_bullet_paragraph(body, '构建预警规则引擎')
    create_bullet_paragraph(body, '完成功能测试和性能测试')
    
    create_paragraph(body, '第四阶段：试点运行与优化（第15-20个月）', 'Heading2')
    create_bullet_paragraph(body, '在复兴医院ICU进行试点部署')
    create_bullet_paragraph(body, '采集试点运行数据')
    create_bullet_paragraph(body, '收集用户反馈意见')
    create_bullet_paragraph(body, '优化预警算法和阈值')
    create_bullet_paragraph(body, '完善系统功能和界面')
    
    create_paragraph(body, '第五阶段：区域推广与协同建设（第21-26个月）', 'Heading2')
    create_bullet_paragraph(body, '向西城区二级医院推广部署')
    create_bullet_paragraph(body, '接入基层医疗机构')
    create_bullet_paragraph(body, '建立区域协同救治流程')
    create_bullet_paragraph(body, '培训各机构医护人员使用')
    create_bullet_paragraph(body, '建立运行维护机制')
    
    create_paragraph(body, '第六阶段：全面运行与持续改进（第27-30个月及以后）', 'Heading2')
    create_bullet_paragraph(body, '实现全区覆盖，全面投入使用')
    create_bullet_paragraph(body, '开展系统应用效果评估')
    create_bullet_paragraph(body, '基于实际数据持续优化算法')
    create_bullet_paragraph(body, '扩展AI辅助决策功能')
    create_bullet_paragraph(body, '总结经验，形成可推广的模式')
    
    # ===== 第五章：风险管控与保障措施 =====
    create_paragraph(body, '第五章 风险管控与保障措施', 'Heading1')
    
    create_paragraph(body, '5.1 项目风险识别与应对', 'Heading2')
    
    create_paragraph(body, '技术风险：', 'Heading3')
    create_bullet_paragraph(body, '风险：多源异构数据整合难度大，接口标准不统一')
    create_bullet_paragraph(body, '应对：采用成熟的数据集成平台，预留接口适配层，与各厂商建立技术对接机制')
    
    create_paragraph(body, '数据安全风险：', 'Heading3')
    create_bullet_paragraph(body, '风险：患者隐私数据泄露风险')
    create_bullet_paragraph(body, '应对：严格遵循《个人信息保护法》和《数据安全法》，数据脱敏处理，加密传输存储，建立完善的权限控制体系')
    
    create_paragraph(body, '临床接受度风险：', 'Heading3')
    create_bullet_paragraph(body, '风险：医护人员对系统的接受度和使用意愿不足')
    create_bullet_paragraph(body, '应对：充分调研用户需求，优化交互设计，加强培训推广，建立激励机制')
    
    create_paragraph(body, '系统性能风险：', 'Heading3')
    create_bullet_paragraph(body, '风险：大规模并发数据处理可能导致系统性能下降')
    create_bullet_paragraph(body, '应对：采用分布式架构，进行充分的性能测试，建立弹性伸缩机制')
    
    create_paragraph(body, '5.2 保障措施', 'Heading2')
    
    create_paragraph(body, '组织保障：', 'Heading3')
    create_bullet_paragraph(body, '成立项目领导小组，由医院主要领导担任组长')
    create_bullet_paragraph(body, '建立项目管理办公室，负责日常协调和管理')
    create_bullet_paragraph(body, '明确各部门职责分工，建立协同工作机制')
    
    create_paragraph(body, '技术保障：', 'Heading3')
    create_bullet_paragraph(body, '选择成熟稳定的技术架构和产品')
    create_bullet_paragraph(body, '建立完善的技术文档和运维规范')
    create_bullet_paragraph(body, '配备专业技术团队，提供7×24小时技术支持')
    
    create_paragraph(body, '资金保障：', 'Heading3')
    create_bullet_paragraph(body, '编制详细的项目预算')
    create_bullet_paragraph(body, '建立分阶段资金拨付机制')
    create_bullet_paragraph(body, '预留应急资金应对需求变更')
    
    create_paragraph(body, '制度保障：', 'Heading3')
    create_bullet_paragraph(body, '制定系统使用管理制度')
    create_bullet_paragraph(body, '建立数据安全管理制度')
    create_bullet_paragraph(body, '完善应急预案和灾难恢复机制')
    
    # ===== 第六章：预期效益分析 =====
    create_paragraph(body, '第六章 预期效益分析', 'Heading1')
    
    create_paragraph(body, '6.1 临床效益', 'Heading2')
    create_bullet_paragraph(body, '提高危重患者识别率：预计预警准确率可达90%以上，减少漏诊误诊')
    create_bullet_paragraph(body, '缩短响应时间：平均预警响应时间缩短至5分钟以内')
    create_bullet_paragraph(body, '降低死亡率：预计危重患者死亡率降低15-20%')
    create_bullet_paragraph(body, '优化资源配置：合理分配重症监护资源，提高床位周转率')
    create_bullet_paragraph(body, '改善患者预后：及早发现和处理病情变化，改善长期预后')
    
    create_paragraph(body, '6.2 管理效益', 'Heading2')
    create_bullet_paragraph(body, '提升医疗质量：建立标准化的危重患者管理流程')
    create_bullet_paragraph(body, '降低医疗风险：减少医疗差错和纠纷')
    create_bullet_paragraph(body, '优化运营效率：提高医护人员工作效率，降低人力成本')
    create_bullet_paragraph(body, '支撑决策分析：提供数据支撑，辅助管理决策')
    create_bullet_paragraph(body, '促进区域协同：建立区域医疗协同机制，优化分级诊疗')
    
    create_paragraph(body, '6.3 社会效益', 'Heading2')
    create_bullet_paragraph(body, '提升区域医疗水平：整体提升西城区急危重症救治能力')
    create_bullet_paragraph(body, '增强居民获得感：让群众享受到更优质的医疗服务')
    create_bullet_paragraph(body, '树立行业标杆：形成可推广的区域医疗协同模式')
    create_bullet_paragraph(body, '支撑公共卫生：为突发公共卫生事件应急响应提供支撑')
    
    create_paragraph(body, '6.4 经济效益', 'Heading2')
    create_paragraph(body, '直接效益：', 'Normal')
    create_bullet_paragraph(body, '减少不必要的ICU转入，节约医疗成本约500万元/年')
    create_bullet_paragraph(body, '提高床位周转率，增加医院收入约300万元/年')
    create_bullet_paragraph(body, '降低医疗纠纷赔偿风险')
    create_paragraph(body, '间接效益：', 'Normal')
    create_bullet_paragraph(body, '提升医院品牌价值和竞争力')
    create_bullet_paragraph(body, '吸引优秀人才加盟')
    create_bullet_paragraph(body, '为医院评级和评审加分')
    
    # ===== 结语 =====
    create_paragraph(body, '结语', 'Heading1')
    create_paragraph(body, '本方案构建了以北京复兴医院为核心的区域性急危状态智能预警决策体系，通过六大核心功能模块的协同工作，实现了急危重症的早期识别、及时预警和高效救治。项目的实施将显著提升西城区及周边区域的急危重症救治能力，为患者生命安全提供有力保障，具有重要的临床价值和社会意义。', 'Normal')
    create_paragraph(body, '建议尽快启动项目实施，按照分阶段实施路径稳步推进，确保项目按期高质量完成。同时，建议在实施过程中注重与临床实际需求相结合，持续优化系统功能，真正将系统打造成为医护人员得力的辅助工具。', 'Normal')
    
    # 文档结束标记
    sectPr = SubElement(body, '{%s}sectPr' % ns)
    pgSz = SubElement(sectPr, '{%s}pgSz' % ns, {'{%s}w' % ns: '11906', '{%s}h' % ns: '16838'})
    pgMar = SubElement(sectPr, '{%s}pgMar' % ns, {
        '{%s}top' % ns: '1440', 
        '{%s}right' % ns: '1440',
        '{%s}bottom' % ns: '1440',
        '{%s}left' % ns: '1440'
    })
    
    return prettify_xml(root)

def create_docx(output_path):
    """创建完整的docx文件"""
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 创建目录结构
        os.makedirs(os.path.join(temp_dir, '_rels'))
        os.makedirs(os.path.join(temp_dir, 'word', '_rels'))
        
        # 写入各XML文件
        with open(os.path.join(temp_dir, '[Content_Types].xml'), 'wb') as f:
            f.write(create_content_types())
        
        with open(os.path.join(temp_dir, '_rels', '.rels'), 'wb') as f:
            f.write(create_rels())
        
        with open(os.path.join(temp_dir, 'word', '_rels', 'document.xml.rels'), 'wb') as f:
            f.write(create_document_rels())
        
        with open(os.path.join(temp_dir, 'word', 'document.xml'), 'wb') as f:
            f.write(create_document())
        
        with open(os.path.join(temp_dir, 'word', 'styles.xml'), 'wb') as f:
            f.write(create_styles())
        
        with open(os.path.join(temp_dir, 'word', 'settings.xml'), 'wb') as f:
            f.write(create_settings())
        
        # 打包成docx
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"文档已成功创建: {output_path}")
        return True
        
    finally:
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    output_file = '/home/lei/.openclaw/workspace/reports/急危状态预警决策方案_北京复兴医院_2025.docx'
    create_docx(output_file)
