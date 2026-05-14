---
layout: '../../layouts/KnowledgeLayout.astro'
title: "Hallucination in AI"
description: "A comprehensive deep dive into Hallucination in AI, covering concepts and real-world usage in Artificial Intelligence."
date: "2026-05-14"
tags: ["factual accuracy", "grounding", "LLMs", "reliability"]
cta_link: "https://www.amazon.com/Evaluating-AI-Systems-Testing-Agents/dp/B0GSVPQ667/ref=sr_1_19"
---

## Introduction to Hallucinations

In 2023, two lawyers in New York used ChatGPT to research legal precedents for a personal injury lawsuit. They asked the AI for relevant cases, and ChatGPT provided detailed summaries of six past court cases, complete with legal citations, judges' names, and docket numbers. The lawyers submitted these cases in federal court.

There was only one problem: **None of those cases existed.** ChatGPT had entirely fabricated them. The lawyers were sanctioned by the judge, and the incident became global news.

This phenomenon is known as a **Hallucination**. It occurs when a Generative AI model produces a response that sounds highly confident, perfectly fluent, and entirely plausible, but is completely factually incorrect or disconnected from reality. 

Hallucinations are the single greatest barrier to deploying Large Language Models (LLMs) in high-stakes enterprise environments (like healthcare, finance, and law).

## Why Do LLMs Hallucinate?

To understand why hallucinations occur, you must understand how LLMs are engineered. 

**LLMs are not databases; they are probability engines.** 
When an LLM generates text, it is not "looking up a fact" in a table. It is simply calculating the mathematical probability of the next word.

If you ask the model: *"Who was the first person to walk on Mars?"*
The model does not know that nobody has walked on Mars. It looks at the words "first person," "walk," and "Mars." Its neural weights strongly associate space exploration with the name "Neil Armstrong." Therefore, it confidently generates the sentence: *"Neil Armstrong was the first person to walk on Mars in 1969."* 

It generated a grammatically perfect sentence that was statistically probable based on its training data, but factually absurd. 

## Types of Hallucinations

1.  **Intrinsic Hallucinations**: The AI directly contradicts the information provided in the prompt. (Prompt: *"Summarize this text which says the car is blue."* Output: *"The text describes a red car."*)
2.  **Extrinsic Hallucinations**: The AI adds logical but entirely fabricated details that were not in the source material. (Prompt: *"Summarize the life of Abraham Lincoln."* Output: *"Lincoln, who loved playing baseball, was president..."* Lincoln did not play baseball, but the AI associated 19th-century Americana with baseball).

## How to Mitigate Hallucinations (Grounding)

Because hallucinations are an inherent mathematical feature of autoregressive models, they cannot be completely eliminated. However, data engineers use several architectural strategies to suppress them.

### 1. Retrieval-Augmented Generation (RAG)
This is the industry standard. Instead of letting the AI guess the answer from its latent memory, you force it to read a document. 
*   *Prompt*: "Using **ONLY** the provided text below, answer the question. If the answer is not in the text, say 'I don't know'."
By constraining the LLM to a specific factual context window, you "Ground" the model in reality, drastically reducing the chance it will invent facts.

### 2. Low Temperature
The `Temperature` parameter in an API call controls the randomness of the output. A high temperature (e.g., `0.9`) encourages the AI to pick less probable words, increasing creativity (and hallucinations). Lowering the temperature to `0.0` forces the model to be mathematically rigid, picking the most conservative, highly probable word every time.

### 3. Verification Agents
In Agentic architectures, developers use a second LLM as a "Judge." The first LLM generates an answer. The second LLM is prompted to aggressively fact-check the first LLM's answer against the source documents. Only if the Judge approves the answer is it shown to the user.

## Conclusion

Hallucinations are the ultimate double-edged sword of Generative AI. The exact same mathematical mechanism that allows an LLM to hallucinate a fake court case is the mechanism that allows it to creatively write a brilliant sci-fi novel. Controlling this statistical creativity—forcing the model to be rigid when facts matter and creative when brainstorming—is the primary engineering challenge of the AI era.
