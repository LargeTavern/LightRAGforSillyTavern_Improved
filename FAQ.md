# LightRAG for SillyTavern FAQ

## Q1: What is LightRAG?
LightRAG is a Retrieval-Augmented Generation (RAG) system developed by researchers at the University of Hong Kong. It enhances large language models by integrating graph structures into text indexing and retrieval processes. The system uses a dual-level retrieval approach that combines both low-level (specific entities and relationships) and high-level (broader topics and themes) information discovery, making it more effective at understanding and retrieving complex information compared to traditional RAG systems.

## Q2: What model should I use?
- For LightRAG operations (knowledge graph creation and keyword extraction):
  - Mid-tier models like GPT-4o-mini and Gemini 1.5 Flash (including the 8B model) work well based on testing (Top of the line models are overkill for these tasks)
  - These handle the graph structure creation and keyword processing effectively

- For embedding:
  - While mxbai-embedding-large works, it's recommended to check the MTEB Leaderboard (https://huggingface.co/spaces/mteb/leaderboard) 
  - Choose the best performing model that fits your system requirements

- For final response generation:
  - You can continue using your current roleplaying model
  - This maintains consistency in character responses while leveraging LightRAG's improved retrieval

## Q3: How is LightRAG compared to SillyTavern's RAG (Data Bank/Vector Storage)?
According to the original creator of LightRAG for SillyTavern, LightRAG's retrieval capabilities are approximately twice as accurate compared to basic RAG implementations.

## Q4: What if I want to update my knowledge graph? Adding or removing documents?
Currently, document management is limited:
- It's not possible to add or remove individual documents
- To make changes, you need to delete your working folder and recreate it entirely
- This is a known limitation of the current implementation

## Q5: Does this replace world info/lorebooks?
No, LightRAG complements rather than replaces world info/lorebooks:
- Rarely used information should be converted to the knowledge graph
- Functional information (constantly active/forced activation) should remain in world info/lorebooks

The original creator of LightRAG for SillyTavern notes:
- For large worldbuilding with tens of thousands of tokens, RAG becomes almost essential
- World info's retrieval capabilities are somewhat inferior to Data Bank, especially with longer texts
- When using LightRAG, non-functional world info should be kept separate

```
但如果真的很需要一个大型世界观，尤其是动辄数万token的世界书，RAG是几乎必不可少的。因为世界书的检索能力比起Data Bank还要差一些，在长文本的情况下世界书的效用已经捉襟见肘。

---

在测试过之后，使用LightRAG时非功能性的世界书就别进来了（）
```

## Q6: Does this improve chat vectorization?
No, LightRAG serves a different purpose:
- Chat vectorization doesn't work effectively in practice
- RAG should only be used to provide additional context when needed (context outside chat history), use it like how you use SillyTavern's Data Bank feature
- Summarization should still be used alongside LightRAG
- Both LightRAG and SillyTavern's RAG actually use more tokens for retrieval, not less - you should use a model with high token input capacity instead

## Q7: What improvements does this fork provide over the original?
The fork includes several significant improvements:
- Integration of the latest LightRAG codebase
- Complete English translation (available in the `english-master` branch)
- Added support for file directory insertion for knowledge graph creation
- Comprehensive codebase cleanup
- Various quality-of-life improvements

## Q8: What is the error I sometimes get while using LightRAG for SillyTavern?
Common issues include:
- Model-related errors:
  * Insufficient model capabilities (hallucinations/poor instruction following)
  * Token limit exceeded
  * Invalid API responses
- System-related issues:
  * Network timeout or connection failure
- Usage issues:
  * Incorrect configuration in .env file

For others, check SillyTavern/LightRAG console and send a bug report if needed.
