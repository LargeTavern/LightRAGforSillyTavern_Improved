# LightRAG for SillyTavern (修改版)

中文 | [English](README.md)

一个经过增强的LightRAG项目分支，通过API代理优化了与SillyTavern（酒馆）的无缝集成。

## 🤖 什么是LightRAG？

LightRAG是由香港大学研究人员开发的检索增强生成(RAG)系统。它通过将图结构整合到文本索引和检索过程中来增强大型语言模型。该系统采用双层检索方法，结合了低层次（特定实体和关系）和高层次（更广泛的主题和主题）信息发现，使其在理解和检索复杂信息方面比传统RAG系统更有效。LightRAG采用增量更新算法，确保新数据的及时集成，使系统在快速变化的数据环境中保持有效。该项目是开源的，可在[GitHub](https://github.com/HKUDS/LightRAG)上获取。

根据LightRAG for SillyTavern原作者的测试，其性能显著优于SillyTavern的数据库功能。据其发现，使用LightRAG的LLM检索能力比基础RAG实现准确度高出约两倍。

## ✨ 相比原始分支的改进

- ⚡ 更新到最新的LightRAG代码库
- 🔧 增强的代码优化和清理
- 📚 增强的历史消息处理
- 🌐 已翻译成英文（参见`english-master`分支）

## 🔧 前置要求

- Anaconda或Miniconda（推荐）
- 合适的LLM/嵌入模型（推荐GPT-4o-mini、Gemini-1.5-Flash或同等级别；嵌入模型推荐mxbai-embedding-large或同等级别）

## 🚀 快速开始

1. 运行 `InstallRequirements.bat` 安装环境并设置您的Anaconda/Miniconda环境
2. 运行 `SetupRAG.bat` 初始化RAG
3. 将 .env.example 复制为 .env 并更新环境变量（如果您不习惯手动操作，也可以使用 `SetupEnv.bat`）
4. 执行 `Start.bat` 启动API服务器

## ❗ 故障排除

如果遇到问题：
1. 检查控制台日志
2. 验证.env中的API密钥是否正确设置
3. 确保有足够的（显存）内存可用（如果使用本地模型）

## 📝 许可证

本项目采用GNU Affero通用公共许可证(AGPL)授权，同时上游项目和LightRAG采用MIT许可证。

## 🙏 致谢

- 基于香港大学的原始LightRAG项目构建
- 特别感谢来自类脑 ΟΔΥΣΣΕΙΑ Discord服务器的**HerSophia**（Discord: @goddess_boreas）创建了原始的LightRAG for SillyTavern

---
*用❤️为SillyTavern社区制作*