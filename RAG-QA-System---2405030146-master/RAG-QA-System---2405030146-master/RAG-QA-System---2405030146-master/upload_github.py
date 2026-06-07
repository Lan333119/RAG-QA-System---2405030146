import os
import zipfile
import base64
import requests
import getpass

def create_project_zip():
    """创建项目压缩包（排除敏感文件）"""
    print("正在创建项目压缩包...")

    exclude_dirs = ['__pycache__', '.git', 'chroma_db', 'chroma_db_new', '.pytest_cache']
    exclude_files = ['*.pyc', 'upload_to_github.py', 'test_debug.py', 'test_search.py',
                    'test_single.py', 'test_no_kb_qa.py', 'test_call_method.py',
                    'test_minimal.py', 'debug_chroma.py', 'debug_ask_step.py', 'rebuild_kb.py',
                    'test_ollama_direct.py', 'test_qa_simple.py', 'test_final_qa.py',
                    'test_simple_qa.py', 'test_call_ollama.py', 'test_no_kb.py', '*.zip']

    zip_path = "RAG-QA-System.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if any(file.endswith(ext.replace('*', '')) for ext in exclude_files):
                    continue

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)

    print(f"✅ 项目已压缩: {zip_path}")
    return zip_path

def upload_via_github_api(zip_path, token):
    """通过 GitHub API 上传文件"""
    print("\n正在上传到 GitHub...")

    repo_owner = "Lan333119"
    repo_name = "RAG-QA-System---2405030146"

    with open(zip_path, 'rb') as f:
        content = f.read()

    encoded_content = base64.b64encode(content).decode('utf-8')

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{zip_path}"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "message": "Upload RAG-QA-System project",
        "content": encoded_content
    }

    try:
        response = requests.put(api_url, json=data, headers=headers, timeout=120)

        if response.status_code in [200, 201]:
            print("✅ 上传成功！")
            print(f"📦 文件位置: https://github.com/{repo_owner}/{repo_name}/blob/main/{zip_path}")
            return True
        else:
            print(f"❌ 上传失败: {response.status_code}")
            print(f"错误: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        return False

def main():
    print("=" * 60)
    print("  RAG-QA-System - GitHub 上传工具")
    print("=" * 60)

    zip_path = create_project_zip()

    print("\n请选择上传方式：")
    print("1. 通过命令行输入 Token（推荐）")
    print("2. 直接输入 Token")

    choice = input("\n请选择 (1/2): ").strip()

    if choice == "1":
        token = getpass.getpass("请输入 GitHub Personal Access Token: ").strip()
    else:
        token = input("请输入 GitHub Personal Access Token: ").strip()

    if not token:
        print("❌ Token 不能为空")
        return

    success = upload_via_github_api(zip_path, token)

    if success:
        print("\n🎉 项目上传完成！")
        print(f"📂 仓库地址: https://github.com/Lan333119/RAG-QA-System---2405030146")
        print("\n⚠️  安全建议：上传完成后，请前往 GitHub 撤销该 Token")
    else:
        print("\n❌ 上传失败，请检查 Token 权限或网络连接")

if __name__ == "__main__":
    main()
