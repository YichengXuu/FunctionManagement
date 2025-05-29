# 软件项目管理与功能点评估平台

## 项目简介

本项目是一个面向软件项目管理和功能点评估的Web平台，支持企业、分析师等多角色协作，实现项目全流程管理、功能点（Function Point）分析与自动化评估。平台前后端分离，界面现代，功能完善，适用于软件造价评估、项目管理等场景。

---

## 功能概述

- **用户注册与登录**：支持企业注册、分析师/管理员登录，权限分明。
- **项目管理**：项目的创建、分配、需求描述、负责人管理。
- **功能点管理**：
  - 增删改查功能点（支持类型、复杂度、备注等字段）
  - 批量导入/导出功能点（CSV格式）
  - 自动计算功能点评分（支持ILF、EIF、EI、EO、EQ五类及三种复杂度）
- **功能点评估与结果管理**：
  - 一键计算项目功能点评分
  - 结果导出（CSV等格式）
  - 历史评估记录查询
- **个人信息与密码管理**：支持用户信息修改、密码重置
- **现代化前端界面**：基于Element Plus，交互友好，支持多角色切换

---

## 技术栈

- **前端**：Vue 3、Element Plus、Vuex、Vue Router、ECharts、Axios、TypeScript
- **后端**：Flask、SQLAlchemy、MySQL
- **依赖管理**：npm、pip

---

## 快速上手

### 1. 后端启动

1. 进入`back/`目录：
   ```bash
   cd back
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置数据库（默认使用MySQL，需在`app.py`中配置`SQLALCHEMY_DATABASE_URI`）
4. 启动后端服务：
   ```bash
   python app.py
   ```
   默认监听5000端口。

### 2. 前端启动

1. 进入`front/`目录：
   ```bash
   cd front
   ```
2. 安装依赖：
   ```bash
   npm install
   ```
3. 启动开发服务器：
   ```bash
   npm run serve
   ```
   默认监听8080端口。
4. 构建生产包：
   ```bash
   npm run build
   ```

---

## 目录结构说明

```
FunctionManagement/
  back/      # 后端Flask服务
    app.py  # 主程序，API接口
    models.py  # ORM模型
    config.py  # 配置
    requirements.txt  # 依赖
  front/     # 前端Vue 3项目
    src/
      views/  # 主要页面（登录、注册、首页、功能点管理等）
      components/  # 公共组件
      assets/  # 静态资源
    package.json  # 前端依赖
```

---

## 常见问题与调试

- **数据库连接失败**：请检查MySQL服务是否启动，`app.py`中的数据库配置是否正确。
- **端口冲突**：如5000/8080端口被占用，请在启动命令中指定其他端口。
- **依赖安装失败**：建议使用Python 3.8+和Node.js 16+，如遇问题可尝试升级pip/npm。
- **前后端跨域问题**：后端已启用CORS，前端请求默认指向`localhost:5000`。

---

## 贡献与许可

- 欢迎提交Issue和PR，完善功能与文档。
- 本项目遵循MIT License。

---

### **导出的 CSV 文件格式**

**1. function_points.csv**

| **name** | **type** | **complexity** | **base_value** | **created_at**      | **comment**           |
| -------- | -------- | -------------- | -------------- | ------------------- | --------------------- |
| Input A  | EI       | LOW            | 3              | 2024-11-18 10:30:00 | Sample comment        |
| File B   | ILF      | MEDIUM         | 10             | 2024-11-18 11:00:00 | Internal logical file |

**2. calculation_records.csv**

| **created_at**      | **GSC_AFP** | **UFP** | **SCF_AFP** | **VAF** | **total_weight** | **scf_stage** |
| ------------------- | ----------- | ------- | ----------- | ------- | ---------------- | ------------- |
| 2024-11-18 10:30:00 | 82.719      | 65      | 81.9        | 1.01    | 36.0             | 2             |
| 2024-11-18 11:00:00 | 70.5        | 55      | 70.0        | 1.05    | 40.0             | 1             |

## 联系方式

如有问题或建议，请联系项目维护者。
