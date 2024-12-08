# LightRAG for SillyTavern (modified fork)

[中文](README_zh-CN.md) | English

An enhanced fork of the LightRAG project, optimized for seamless integration with SillyTavern via the use of an API Proxy.

## 🤖 What is LightRAG?

LightRAG is a sophisticated Retrieval-Augmented Generation (RAG) system designed to enhance large language models (LLMs) by integrating external knowledge sources. This integration enables the generation of more accurate and contextually relevant responses tailored to user needs. Unlike traditional RAG systems that rely on flat data representations, LightRAG incorporates graph structures into text indexing and retrieval processes. This dual-level retrieval system enhances comprehensive information retrieval from both low-level and high-level knowledge discovery. The use of graph structures with vector representations facilitates efficient retrieval of related entities and their relationships, significantly improving response times while maintaining contextual relevance. LightRAG also employs an incremental update algorithm to ensure timely integration of new data, allowing the system to remain effective and responsive in rapidly changing data environments. Extensive experimental validation has demonstrated considerable improvements in retrieval accuracy and efficiency compared to existing approaches. LightRAG is open-source and available at [GitHub](https://github.com/HKUDS/LightRAG).


Testing conducted by the original creator of LightRAG for SillyTavern indicates significant performance improvements over SillyTavern's Data Bank feature. According to their findings, the LLM retrieval capabilities using LightRAG are approximately twice as accurate compared to basic RAG implementations found in SillyTavern.

## ✨ Improvements Over the Original Fork

- ⚡ Updated to latest LightRAG codebase
- 🔧 Enhanced code optimization and cleanup
- 📚 Enhanced history message processing
- 🌐 Translated to English (see the `english-master` branch)

## 🔧 Prerequisites

- Anaconda or Miniconda (recommended)

## 🚀 Quick Start

1. Run `InstallRequirements.bat` to install the environments and setup your Anaconda/Miniconda environment
2. Run `SetupRAG.bat` to initialize the RAG
3. Copy .env.example to .env and update the Environment Variables (or use `SetupEnv.bat` if you feel uncomfortable to do so)
4. Execute `Start.bat` to launch the API server

## 📝 License

This project is licensed under the GNU Affero General Public License (AGPL), with MIT license coming from the upstrem project and LightRAG.

## 🙏 Acknowledgments

- Built upon the original LightRAG project from the University of Hong Kong
- Special thanks to **HerSophia** (@goddess_boreas on Discord) from the 类脑 ΟΔΥΣΣΕΙΑ Discord server for creating the original LightRAG for SillyTavern

---
*Made with ❤️ for the SillyTavern community*