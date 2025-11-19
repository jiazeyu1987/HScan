#!/bin/bash
# 系统重启脚本

echo "=== 医院监控系统重启脚本 ==="

# 杀死可能存在的相关进程
echo "清理现有进程..."
pkill -f "vite" 2>/dev/null || true
pkill -f "flask" 2>/dev/null || true
pkill -f "python.*run.py" 2>/dev/null || true

# 等待进程清理
sleep 2

# 启动后端服务
echo "启动后端Flask服务..."
cd /workspace/backend
nohup python3 run.py > /workspace/backend/logs/app.log 2>&1 &
BACKEND_PID=$!
echo "后端服务PID: $BACKEND_PID"

# 等待后端启动
sleep 3

# 启动前端服务
echo "启动前端Vite开发服务器..."
cd /workspace/hospital-monitor-antd
nohup pnpm dev > /workspace/hospital-monitor-antl/vite.log 2>&1 &
FRONTEND_PID=$!
echo "前端服务PID: $FRONTEND_PID"

echo "=== 系统重启完成 ==="
echo "后端服务: http://127.0.0.1:5000"
echo "前端服务: http://127.0.0.1:5174"
echo "请等待服务完全启动..."