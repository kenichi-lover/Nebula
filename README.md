# Nebula

现代化轻量公告板与内容发布平台。

Nebula 是基于 FastAPI 与 PostgreSQL 构建的自托管信息发布系统，专注于公告、通知、备忘录和动态内容展示。

项目采用现代 Glass UI 设计风格，支持亮色与暗色主题，适合作为个人博客首页、团队公告墙、校园通知系统或内部信息门户。

---

## 项目特点

### 简洁

专注于内容发布。

不做复杂社交功能。

---

### 自托管

用户完全掌控数据。

支持：

* Linux
* Docker
* VPS
* NAS

部署简单。

---

### 现代化界面

采用：

* Glassmorphism
* Aurora Background
* Dark Mode
* Responsive Design

提供良好的桌面与移动端体验。

---

### 高性能

基于：

* FastAPI
* AsyncPG
* PostgreSQL

支持异步请求与高并发访问。

---

## 适用场景

### 个人博客

发布：

* 技术文章
* 学习笔记
* 项目日志

---

### 团队公告板

发布：

* 工作通知
* 会议安排
* 项目状态

---

### 校园系统

发布：

* 课程通知
* 活动公告
* 实验室消息

---

### NAS 首页

作为家庭服务器入口页面。

展示：

* 公告
* 服务状态
* 快捷入口

---

## 技术栈

### Backend

* FastAPI
* SQLModel
* PostgreSQL
* AsyncPG
* Pydantic Settings

### Frontend

* Jinja2
* TailwindCSS
* Vanilla JavaScript

### Tooling

* UV
* Git

---

## 项目结构

```text
nebula/

app/

├── config/
│   ├── database.py
│   └── settings.py
│
├── models/
│
├── schemas/
│
├── services/
│
├── routers/
│
└── utils/

static/
├── css/
└── js/

templates/
├── base.html
├── navbar.html
└── board.html

main.py
pyproject.toml
.env
README.md
```

---

## 当前功能

### 已完成

* Dashboard
* Glass UI
* Dark Mode
* Responsive Layout
* PostgreSQL 集成
* SQLModel 支持

---

### 开发中

* Notice CRUD
* 分类管理
* 搜索功能
* 置顶公告
* Markdown 支持

---

### 计划功能

* 用户登录
* 权限管理
* 文件上传
* 富文本编辑器
* RSS 输出
* WebSocket 实时刷新

---

## 开发启动

安装依赖：

```bash
uv sync
```

配置环境变量：

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/nebula_db
```

启动项目：

```bash
uv run fastapi dev main.py
```

访问：

```text
http://127.0.0.1:8000
```

---

## 设计理念

Nebula 不追求庞大复杂的功能。

它更像一块数字公告牌。

简单。

稳定。

易维护。

让信息展示回归本质。

---

## License

MIT

