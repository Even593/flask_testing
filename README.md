# Flask Auth 应用部署指南

## 概述
这是一个使用 Flask 和 JWT 的身份验证 API 应用，已完全容器化，支持 Docker 部署。

## 系统要求
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM (推荐)
- 端口 5001 可用

## 快速开始

### 1. 克隆并进入项目目录
```bash
cd /Users/even/Desktop/flask_auth
```

### 2. 使用 Docker Compose 启动服务
```bash
# 构建镜像并启动容器（后台运行）
docker-compose up --build -d

# 查看容器状态
docker-compose ps

# 查看应用日志
docker-compose logs -f flask_auth
```

### 3. 验证服务运行
```bash
# 检查应用是否响应
curl http://localhost:5001/

# 预期输出: {"message":"Flask Auth API"}
```

## 📍 API 访问地址

| 环境 | URL | 端口 |
|------|-----|------|
| 本地开发 | `http://localhost:5001/api/` | 5001 |
| 外部网络 | `http://<服务器IP>:5001/api/` | 5001 |
| 容器内部 | `http://localhost:5000/api/` | 5000 |

## 🔐 API 端点

### 公开端点 (无需认证)

#### 1. 用户注册
```bash
curl -X POST http://localhost:5001/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "YourPassword123"
  }'
```

**响应示例:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com"
  }
}
```

#### 2. 用户登录
```bash
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "YourPassword123"
  }'
```

**响应示例:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login successful"
}
```

### 受保护端点 (需要 JWT 认证)

#### 3. 获取用户资料
```bash
# 使用登录返回的 access_token
curl -X GET http://localhost:5001/api/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**响应示例:**
```json
{
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

## 🧪 完整测试流程

### 步骤 1: 注册测试用户
```bash
curl -X POST http://localhost:5001/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```

### 步骤 2: 登录获取令牌
```bash
# 执行登录并提取令牌
TOKEN=$(curl -s -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "TestPassword123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "JWT Token: $TOKEN"
```

### 步骤 3: 测试受保护端点
```bash
# 测试个人资料端点
curl -X GET http://localhost:5001/api/profile \
  -H "Authorization: Bearer $TOKEN"

# 测试无效令牌
curl -X GET http://localhost:5001/api/profile \
  -H "Authorization: Bearer invalid_token" -v
```

## 🐳 Docker 部署选项

### 选项 A: Docker Compose (推荐)
```bash
# 开发环境
docker-compose up -d

# 生产环境 (更改环境变量)
docker-compose -f docker-compose.yml up -d
```

### 选项 B: 纯 Docker 命令
```bash
# 构建镜像
docker build -t flask-auth-app .

# 运行容器
docker run -d \
  --name flask_auth_api \
  -p 5001:5000 \
  -e FLASK_ENV=development \
  -e SECRET_KEY=your-secret-key \
  -e JWT_SECRET_KEY=your-jwt-secret \
  -e SEED_DB=true \
  -v $(pwd)/instance:/app/instance \
  flask-auth-app
```

### 选项 C: 运行测试套件
```bash
# 使用测试配置
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## ⚙️ 配置说明

### 环境变量
| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `FLASK_ENV` | `development` | Flask 环境: development, production, testing |
| `SECRET_KEY` | `change-this-in-production` | Flask 应用密钥 |
| `JWT_SECRET_KEY` | `change-this-jwt-secret-in-production` | JWT 签名密钥 |
| `SEED_DB` | `true` | 是否初始化测试用户数据 |

### 端口配置
- 容器端口: `5000` (应用运行端口)
- 主机端口: `5001` (映射到容器端口 5000)
- 如需更改端口，修改 `docker-compose.yml`:
  ```yaml
  ports:
    - "8080:5000"  # 主机端口:容器端口
  ```

### 数据持久化
- 数据库文件: `./instance/dev.db` (SQLite)
- 通过 Docker volume 挂载实现数据持久化
- 停止容器后数据不会丢失

## 🔧 故障排除

### 常见问题及解决方案

#### 1. 端口冲突
**症状**: `docker-compose up` 失败，提示端口已占用
**解决**:
```bash
# 检查占用端口的进程
lsof -i :5001

# 修改端口映射
# 编辑 docker-compose.yml，更改端口：
# ports:
#   - "5002:5000"
```

#### 2. 容器启动失败
**症状**: 容器不断重启或退出
**解决**:
```bash
# 查看详细日志
docker-compose logs --tail=100 flask_auth

# 检查数据库权限
chmod 755 ./instance

# 重新构建镜像
docker-compose down -v
docker-compose up --build -d
```

#### 3. API 无法访问
**症状**: 本地可访问，外部网络无法访问
**解决**:
- 确认应用绑定到 `0.0.0.0` (已配置)
- 检查防火墙规则
- 云服务器需要配置安全组允许端口 5001 入站

#### 4. JWT 认证失败
**症状**: `401 Unauthorized` 错误
**解决**:
```bash
# 检查令牌是否正确
echo $TOKEN

# 重新登录获取新令牌
curl -X POST http://localhost:5001/api/login ...

# 检查令牌有效期 (默认15分钟)
```

### 诊断命令
```bash
# 查看容器状态
docker-compose ps
docker ps -a | grep flask_auth

# 查看应用日志
docker-compose logs -f flask_auth
docker logs flask_auth_api --tail=50

# 检查容器网络
docker inspect flask_auth_api | grep IPAddress
docker network ls
docker network inspect flask_auth_default

# 进入容器调试
docker exec -it flask_auth_api bash
docker exec flask_auth_api python -c "from app import db; print('Tables:', db.metadata.tables.keys())"
```

## 🚀 生产环境部署建议

### 1. 安全加固
```bash
# 生成强密钥
python -c "import secrets; print('SECRET_KEY:', secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY:', secrets.token_hex(32))"

# 创建 .env 文件
cat > .env << EOF
SECRET_KEY=your-generated-secret-key
JWT_SECRET_KEY=your-generated-jwt-secret-key
FLASK_ENV=production
SEED_DB=false
EOF
```

### 2. 使用生产数据库
**当前使用 SQLite，建议升级到:**
- PostgreSQL (推荐)
- MySQL
- MariaDB

### 3. 添加 HTTPS
```yaml
# nginx 反向代理配置示例
# docker-compose.prod.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - flask_auth
```

### 4. 性能优化
```dockerfile
# 修改 Dockerfile 添加 Gunicorn
RUN pip install gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
```

### 5. 监控和日志
- 添加 `/health` 健康检查端点
- 配置结构化日志 (JSON 格式)
- 添加 Prometheus 指标收集

## 📂 项目结构
```
flask_auth/
├── app/                    # 应用代码
│   ├── __init__.py        # 应用工厂
│   ├── config.py          # 配置管理
│   ├── models.py          # 数据模型
│   ├── routes/           # API 路由
│   └── errors.py         # 错误处理
├── tests/                 # 测试代码
├── instance/             # 数据库文件
├── Dockerfile           # Docker 构建配置
├── docker-compose.yml   # 开发环境编排
├── docker-compose.test.yml # 测试环境编排
├── requirements.txt     # Python 依赖
└── run.py              # 应用入口点
```

## 📞 支持与维护

### 常用维护命令
```bash
# 停止服务
docker-compose down

# 停止并删除 volume
docker-compose down -v

# 重启服务
docker-compose restart flask_auth

# 更新代码后重新部署
docker-compose down
git pull origin main
docker-compose up --build -d

# 清理未使用的资源
docker system prune -f
docker volume prune -f
```

### 监控应用状态
```bash
# 实时日志
docker-compose logs -f flask_auth

# 资源使用情况
docker stats flask_auth_api

# 数据库状态
docker exec flask_auth_api ls -lh /app/instance/
docker exec flask_auth_api python -c "from app.models import User; print('User count:', User.query.count())"
```

## 版本信息
- Flask: 3.1.0
- Flask-JWT-Extended: 4.7.1
- Flask-SQLAlchemy: 3.1.1
- Python: 3.12 (容器内)

---

**提示**: 生产环境部署前，请务必备份数据并测试所有功能。建议先在测试环境验证部署流程。