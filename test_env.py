import os

# ==================== 方法1：直接从系统环境变量读取 ====================
print("=" * 50)
print("🔍 测试从系统环境变量读取 API Key")
print("=" * 50)

api_key = os.environ.get("DEEPSEEK_API_KEY")

if api_key:
    print(f"✅ 成功获取 API Key！")
    print(f"📌 API Key 长度: {len(api_key)} 个字符")
    print(f"📌 API Key 前8位: {api_key[:8]}...")
    print(f"📌 API Key 后4位: ...{api_key[-4:]}")
else:
    print("❌ 未找到 DEEPSEEK_API_KEY 环境变量")
    print("💡 请先设置环境变量：")
    print("   PowerShell: $env:DEEPSEEK_API_KEY='sk-xxx'")
    print("   CMD: set DEEPSEEK_API_KEY=sk-xxx")

print("\n" + "=" * 50)

# ==================== 方法2：查看所有包含 DEEPSEEK 的环境变量 ====================
print("🔍 查找所有包含 'DEEPSEEK' 的环境变量")
print("=" * 50)

found_vars = []
for key, value in os.environ.items():
    if "DEEPSEEK" in key.upper():
        found_vars.append(key)
        # 隐藏敏感信息，只显示前几位
        if "KEY" in key.upper() or "SECRET" in key.upper() or "TOKEN" in key.upper():
            print(f"   {key} = {value[:8]}... (长度: {len(value)})")
        else:
            print(f"   {key} = {value}")

if not found_vars:
    print("   ❌ 未找到任何包含 'DEEPSEEK' 的环境变量")

print("\n" + "=" * 50)

# ==================== 方法3：尝试使用 os.getenv() ====================
print("🔍 测试 os.getenv() 方法")
print("=" * 50)

api_key_2 = os.getenv("DEEPSEEK_API_KEY")

if api_key_2:
    print(f"✅ os.getenv() 也成功获取到了 Key！")
    print(f"📌 两种方法获取的 Key 是否一致: {api_key == api_key_2}")
else:
    print("❌ os.getenv() 未获取到 Key")

print("\n" + "=" * 50)

# ==================== 方法4：验证 Key 格式是否正确 ====================
print("🔍 验证 API Key 格式")
print("=" * 50)

if api_key:
    # 检查是否以 sk- 开头
    if api_key.startswith("sk-"):
        print("✅ API Key 格式正确（以 sk- 开头）")
    else:
        print("⚠️ API Key 格式异常（应以 sk- 开头）")
    
    # 检查长度（DeepSeek 的 Key 通常在 30-50 个字符之间）
    if 30 <= len(api_key) <= 60:
        print(f"✅ API Key 长度合适 ({len(api_key)} 字符)")
    else:
        print(f"⚠️ API Key 长度异常 ({len(api_key)} 字符)，通常在 30-60 字符之间")
    
    # 检查是否包含空格
    if " " in api_key:
        print("❌ API Key 包含空格，请去除！")
    else:
        print("✅ API Key 没有多余空格")
    
    # 检查是否包含换行符
    if "\n" in api_key:
        print("❌ API Key 包含换行符，请去除！")
    else:
        print("✅ API Key 没有换行符")

print("\n" + "=" * 50)

# ==================== 方法5：测试能否用于 API 请求 ====================
if api_key and api_key.startswith("sk-") and " " not in api_key:
    print("🔍 测试 API Key 是否有效（发送测试请求）")
    print("=" * 50)
    
    import requests
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "你好"}],
        "max_tokens": 10,
        "stream": False,
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ API Key 完全有效！")
            result = response.json()
            print(f"📌 模型回复: {result['choices'][0]['message']['content']}")
        elif response.status_code == 401:
            print("❌ API Key 无效（认证失败）")
            print(f"📌 错误详情: {response.text}")
        else:
            print(f"⚠️ API 返回状态码: {response.status_code}")
            print(f"📌 错误详情: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

print("\n" + "=" * 50)
print("🔍 测试完成")
print("=" * 50)

# ==================== 快速诊断总结 ====================
print("\n📋 诊断总结：")
print("-" * 30)

if api_key:
    print("✅ 环境变量已正确设置")
    if api_key.startswith("sk-") and " " not in api_key:
        print("✅ API Key 格式正确")
    else:
        print("⚠️ API Key 格式可能有问题")
else:
    print("❌ 环境变量未设置或读取失败")
    print("\n💡 请按以下方法设置：")
    print("")
    print("  【方法1 - PowerShell（推荐）】")
    print("  $env:DEEPSEEK_API_KEY='你的API Key'")
    print("")
    print("  【方法2 - CMD】")
    print("  set DEEPSEEK_API_KEY=你的API Key")
    print("")
    print("  【方法3 - 永久设置】")
    print("  1. Win + X → 系统 → 高级系统设置")
    print("  2. 环境变量 → 新建用户变量")
    print("  3. 变量名: DEEPSEEK_API_KEY")
    print("  4. 变量值: 你的API Key")
    print("  5. 重启终端")