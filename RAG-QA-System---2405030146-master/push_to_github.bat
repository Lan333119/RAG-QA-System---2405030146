@echo off
setlocal

set GIT_PATH=C:\Program Files\Git\bin\git.exe
set REPO_URL=https://github.com/Lan333119/RAG-QA-System---2405030146.git

echo 配置Git...
"%GIT_PATH%" config user.name "Lan333119"
"%GIT_PATH%" config user.email "lan333119@example.com"

echo 初始化仓库...
"%GIT_PATH%" init

echo 添加文件...
"%GIT_PATH%" add .

echo 提交...
"%GIT_PATH%" commit -m "Initial commit: RAG智能问答系统"

echo 添加远程仓库...
"%GIT_PATH%" remote add origin %REPO_URL%

echo 推送到GitHub...
"%GIT_PATH%" push -u origin main

echo 完成！

endlocal