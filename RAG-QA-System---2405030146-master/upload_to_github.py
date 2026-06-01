import os
import zipfile
import requests

def zip_project():
    """压缩项目文件夹"""
    print("正在压缩项目...")
    zip_path = "RAG-QA-System.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # 排除不需要的文件和目录
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'chroma_db', 'chroma_db_new']]
            
            for file in files:
                # 排除临时文件
                if file.endswith('.pyc') or file.endswith('.zip') or file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)
                print(f"  添加: {arcname}")
    
    print(f"项目已压缩为: {zip_path}")
    return zip_path

def upload_to_github(zip_path, repo_url, token):
    """上传到 GitHub"""
    print("\n正在上传到 GitHub...")
    
    # 解析仓库信息
    repo_owner = "Lan333119"
    repo_name = "RAG-QA-System---2405030146"
    
    # GitHub API URL
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/RAG-QA-System.zip"
    
    # 读取压缩文件
    with open(zip_path, 'rb') as f:
        content = f.read()
    
    import base64
    encoded_content = base64.b64encode(content).decode('utf-8')
    
    # 创建请求数据
    data = {
        "message": "Upload project archive",
        "content": encoded_content
    }
    
    # 发送请求
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.put(api_url, json=data, headers=headers, timeout=60)
        
        if response.status_code == 201:
            print("✅ 上传成功！")
            print(f"文件位置: https://github.com/{repo_owner}/{repo_name}/blob/main/RAG-QA-System.zip")
            return True
        else:
            print(f"❌ 上传失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        return False

def main():
    print("=" * 50)
    print("RAG-QA-System 项目上传工具")
    print("=" * 50)
    
    # 压缩项目
    zip_path = zip_project()
    
    # GitHub 配置（请在运行时手动输入）
    token = input("请输入您的 GitHub Personal Access Token: ").strip()
    repo_url = "https://github.com/Lan333119/RAG-QA-System---2405030146"
    
    # 上传
    success = upload_to_github(zip_path, repo_url, token)
    
    if success:
        print("\n🎉 项目上传完成！")
        print(f"\n仓库地址: {repo_url}")
        print("请在 GitHub 网页上手动解压或使用以下命令下载:")
        print(f"git clone {repo_url}.git")
    else:
        print("\n❌ 上传失败，请检查网络连接或尝试其他方法")

if __name__ == "__main__":
    main()
