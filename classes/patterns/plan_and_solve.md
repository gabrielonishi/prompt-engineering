# Plan and Solve

Extension of CoT adding a planning step, ensuring the model covers all necessary logic subtasks before evaluating. PS+ is an extension of Plan and Solve that adds intermediate result calculation.

### When To Use

 - Math reasoning
 - Common sense reasoning
 - Symbolic reasoning

### Limitation

 - Approach heavily relies on the trigger sentence. Correct phrasing is crucial

### Implementation

**PS**
```
Q: <problem statement>  
A: Let’s first understand the problem, extract relevant variables and their corresponding numerals,  
   devise a plan to solve the problem, then carry out the plan step by step (pay attention to correct  
   calculation and commonsense).  
```

**PS+**
```
Q: <problem statement>  
A: Let’s first understand the problem, extract relevant variables and their corresponding numerals,  
   devise a plan to solve the problem, then carry out the plan, calculate intermediate results (pay attention to calculation and common sense), solve the problem step by step, and show the answer.
```

### Rationale

Explicitly decomposing a complex task into a planning phase and an execution phase helps the model cover all necessary reasoning steps, mitigating both missing‑step and calculation errors; the detailed instructions focus the model on correct variable handling and arithmetic.

### Performance Metrics:

 - Math Reasoning (GPT‑3 text‑davinci‑003):
    - Average (6 datasets): PS+ 76.7% vs Zero‑shot‑CoT 70.4%
    - GSM8K: 59.3% vs 56.4%
    - SVAMP: 75.7% vs 69.9%
    - MultiArith: 91.8% vs 83.8%
    - AddSub: 92.2% vs 85.3%
    - AQuA: 46.0% vs 38.9%
    - SingleEq: 94.7% vs 88.1%
 - Commonsense: CSQA 71.9% vs 65.2%; StrategyQA 65.4% vs 63.8%
 - Symbolic: Last‑Letter 75.2% vs 64.8%; Coin‑Flip 99.6% vs 96.8%
 - Error Rates (GSM8K): Calculation 5% vs 7%; Missing‑step 7% vs 12%

### References:

 - Lei Wang et al., “Plan‑and‑Solve Prompting: Improving Zero‑Shot Chain‑of‑Thought Reasoning by Large Language Models,” ACL 2023
 - https://learnprompting.org/docs/advanced/decomposition/plan_and_solve?srsltid=AfmBOopQMCt5WFQqWd-wp1iMzVXVgytccOnYo292fcxFywQu2W5cRXop
