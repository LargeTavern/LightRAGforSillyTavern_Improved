# LightRAG for SillyTavern (修改版)

中文 | [English](README.md)

一个经过增强的LightRAG项目分支，通过API代理优化了与SillyTavern（酒馆）的无缝集成。

## 🤖 什么是LightRAG？

LightRAG是一个先进的检索增强生成(RAG)系统，旨在通过集成外部知识源来增强大型语言模型(LLM)的能力。这种集成使系统能够生成更准确、更符合上下文的响应，以满足用户需求。与传统的依赖平面数据表示的RAG系统不同，LightRAG将图结构整合到文本索引和检索过程中。这种双层检索系统增强了从低层次和高层次知识发现的综合信息检索能力。使用图结构和向量表示可以有效检索相关实体及其关系，在保持上下文相关性的同时显著提高响应时间。LightRAG还采用增量更新算法，确保新数据的及时集成，使系统在快速变化的数据环境中保持有效和响应。大量实验验证表明，与现有方法相比，检索准确性和效率都有显著提高。LightRAG是开源的，可在[GitHub](https://github.com/HKUDS/LightRAG)上获取。

根据LightRAG for SillyTavern原作者的测试，其性能显著优于SillyTavern的数据库功能。据其发现，使用LightRAG的LLM检索能力比SillyTavern中的基础RAG实现准确度高出约两倍。

## ✨ 相比原始分支的改进

- ⚡ 更新到最新的LightRAG代码库
- 🔧 增强的代码优化和清理
- 📚 增强的历史消息处理
- 🌐 已翻译成英文（参见`english-master`分支）

## 🔧 前置要求

- Anaconda或Miniconda（推荐）

## 🚀 快速开始

1. 运行 `InstallRequirements.bat` 安装环境并设置您的Anaconda/Miniconda环境
2. 运行 `SetupRAG.bat` 初始化RAG
3. 将 .env.example 复制为 .env 并更新环境变量（如果您不习惯手动操作，也可以使用 `SetupEnv.bat`）
4. 执行 `Start.bat` 启动API服务器

## 📝 许可证

本项目采用GNU Affero通用公共许可证(AGPL)授权，同时上游项目和LightRAG采用MIT许可证。

## 🙏 致谢

- 基于香港大学的原始LightRAG项目构建
- 特别感谢来自类脑 ΟΔΥΣΣΕΙΑ Discord服务器的**HerSophia**（Discord: @goddess_boreas）创建了原始的LightRAG for SillyTavern

---
*用❤️为SillyTavern社区制作*