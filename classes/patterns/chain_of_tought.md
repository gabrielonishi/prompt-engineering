# Chain of Tought

Prompting technique for breaking down a complex problem into multiple, simpler problems.

Example:

```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?

A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 5 + 6 = 11. The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?

A: The cafeteria had 23 apples originally. They used 20 to make lunch. So they had 23 - 20 = 3. They bought 6 more apples, so they have 3 + 6 = 9. The answer is 9.
```

### When To Use

 - Mathematics and Arithmetic
 - Commonsense and Symbolic Reasoning
 - Complex decision making

### Limitation

Works best with very big language models (over 100 billion parameters)

### Implementation

 - Select k exemplars each as a triple ⟨input, chain of thought, output⟩.
 - Build prompt by concatenating those k exemplars, then appending the new input and a request like “Let’s think step by step.”
 - Invoke the LLM (greedy or sampled decoding) to generate both the intermediate reasoning and the final answer.
 - Parse the model’s output: extract the chain‑of‑thought text and the final answer.

### Rationale

By explicitly eliciting intermediate reasoning in natural language, the model decomposes complex, multi‑step problems into manageable sub‑steps, unlocking emergent reasoning capabilities in very large models.

### Performance Metrics:

 - GSM8K (math word problems): Solve rate jumps from ≈18% (standard prompting) to ≈58% with CoT on PaLM 540B, achieving new SOTA and outperforming finetuned GPT‑3+verifier.
 - SVAMP & MAWPS: Similar >2× improvements;
 - AQuA & ASDiv: Within 2% of best finetuned models;
 - Commonsense & Symbolic Tasks: Consistent gains across CSQA, StrategyQA, date/sports understanding, last‑letter concatenation, coin‑flip state tracking, including OOD generalization.

### References: 

 - Wei et al., “Chain‑of‑Thought Prompting Elicits Reasoning in Large Language Models,” NeurIPS 2022.
 - https://learnprompting.org/docs/intermediate/chain_of_thought
