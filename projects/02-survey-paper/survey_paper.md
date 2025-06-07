## Introduction

In recent years, **Large Language Models (LLMs)** such as GPT-4, PaLM, and Claude have revolutionized natural language processing by achieving remarkable performance across a wide range of tasks—without task-specific fine-tuning. These successes are made possible in part by a seemingly simple yet powerful idea: **prompting**. Prompting involves carefully crafting the input text to steer the model's behavior, often leveraging examples, instructions, or demonstrations.

As LLMs grow in scale and complexity, **prompt engineering**—the practice of designing effective prompts—has emerged as a central discipline in applied AI. Prompt engineering bridges the gap between foundation models and real-world use cases, allowing non-experts and domain professionals to adapt powerful models to complex reasoning tasks, decision-making scenarios, and creative generation pipelines.

However, the success of prompting is not merely a matter of wording. In recent literature, a rich ecosystem of **prompting techniques** has emerged, each addressing specific challenges:
- overcoming shallow reasoning,
- enabling compositional generalization,
- improving factuality and consistency,
- and reducing dependency on domain-specific datasets or APIs.

These innovations are not isolated; they often build on one another, especially around a pivotal method known as **Chain-of-Thought (CoT) prompting**, which introduced the idea of decomposing problems into intermediate reasoning steps.

---

### Motivation

This survey aims to help researchers and practitioners navigate the evolving space of prompt engineering by:
- Synthesizing the core ideas and mechanisms behind the most influential prompt engineering techniques.
- Tracing their development with respect to the **Chain-of-Thought** paradigm, which serves as a conceptual foundation for many modern strategies.
- Proposing **novel application scenarios** for each technique beyond those introduced in the original papers, with an eye toward domains like law, finance, education, diagnostics, and operations.
- Providing a **comparative synthesis** to highlight each technique’s strengths, limitations, and situational fit.

---

### Objectives

Specifically, this paper seeks to:
1. **Describe** key prompt engineering techniques based on their original research.
2. **Analyze** how each technique evolved from or extends the Chain-of-Thought prompting framework.
3. **Demonstrate** real-world applications of each method through original, domain-specific examples.
4. **Compare** all methods systematically using a unified set of evaluation dimensions, summarized in a comparative table.

---

### Structure of the Paper

The remainder of the paper is organized as follows:

- **Section 2** introduces foundational concepts and defines a taxonomy of prompting strategies.
- **Section 3** presents each technique in depth, following a consistent structure: how it works, its evolution, and a novel application.
- **Section 4** synthesizes the differences among techniques via a comparative table.
- **Section 5** discusses practical trends, insights, and broader implications for prompt engineering as a research and design practice.
- **Section 6** concludes with a summary of findings and directions for future research.


## Chain-of-Thought Prompting

### How It Works

**Chain-of-Thought (CoT) Prompting** is a technique designed to elicit step-by-step reasoning from large language models (LLMs) by providing exemplars that include intermediate reasoning steps. Instead of giving the model a direct input–output pair (as in standard few-shot prompting), CoT uses input–reasoning–output triples.

The process mimics human problem-solving: decomposing a task into intermediate steps and solving them sequentially. For example, in a math word problem, instead of prompting with:

> Q: Roger has 5 tennis balls. He buys 2 more cans of 3 balls each. How many does he have?  
> A: 11

CoT would format it as:

> A: Roger started with 5 balls. 2 cans of 3 = 6 balls. 5 + 6 = 11. The answer is 11.

Key advantages:
- **Interpretability**: Intermediate steps expose model reasoning.
- **Improved Performance**: Significant gains on arithmetic, commonsense, and symbolic reasoning.
- **Scalability**: Emergent ability for models with ≥100B parameters (e.g., PaLM 540B, GPT-3 175B).

The reasoning steps are expressed in natural language, and CoT is effective without fine-tuning — only requiring in-context learning with examples.

---

### How It Evolved Over Chain-of-Thought

CoT prompting is itself a foundational innovation, but it builds conceptually on prior ideas:
- **Natural language rationales** from Ling et al. (2017) and Cobbe et al. (2021) showed the value of intermediate explanations for math reasoning, albeit via supervised training.
- **Few-shot prompting**, popularized by Brown et al. (2020), introduced flexible in-context learning but struggled with multi-step reasoning tasks.

CoT integrates the benefits of both: it enables reasoning via natural language without retraining or large-scale annotation. It also set the stage for further developments:
- **Self-Consistency** (Wang et al., 2022): Sampling multiple CoT outputs and choosing the majority vote.
- **ReAct** (Yao et al., 2022): Extending CoT by allowing the model to interleave reasoning and actions (e.g., tool use).
- **Tree-of-Thought** (Yao et al., 2023): Building upon CoT by exploring multiple reasoning paths.

Thus, CoT functions both as a practical technique and a conceptual baseline for modern prompt-based reasoning paradigms.

---

### Novel Application Example

**Application: Legal Argument Structuring**

Imagine a task where the model assists a paralegal in outlining a legal argument. Given a fact pattern and legal issue, the model should produce a structured reasoning path leading to a likely legal conclusion.

**Prompt Example:**

> Q: Jane slipped and fell on a wet floor in a store. There were no warning signs. She broke her arm. Is the store liable for negligence?  
>
> A:
> 1. To prove negligence, Jane must show: (a) duty of care, (b) breach, (c) causation, and (d) harm.  
> 2. Stores owe customers a duty of care.  
> 3. The absence of warning signs may constitute a breach of that duty.  
> 4. The breach (lack of signage) caused her fall.  
> 5. She suffered harm (broken arm).  
> So the store is likely liable for negligence.

This showcases how CoT can be applied outside math or logic domains to scaffold legal reasoning in an interpretable and structured way.

## Perspective-Taking Prompting (SIMTOM)

### How It Works

**SIMTOM (Simulated Theory of Mind)** is a two-step prompting technique inspired by Simulation Theory in cognitive science. The core idea is that before answering a Theory-of-Mind (ToM) question, a model should simulate what a character knows by taking that character’s perspective. This approach explicitly separates **perspective-taking** and **question-answering** into two prompts.

The SIMTOM procedure works as follows:
1. **Perspective-Taking**: The LLM is prompted to filter the narrative context to include only what a target character knows or perceives. This “filtered story” becomes the new input.
2. **Question-Answering**: The model answers the ToM question based only on the filtered story, simulating the character’s mental state.

This decomposition improves the model’s ability to answer false-belief and mental-state questions. For example:

- **Original story**: Jim places a ball in a box. While Jim is away, Avi moves it to a basket.
- **Question**: Where does Jim think the ball is?
- **SIMTOM Step 1 (Perspective-Taking)**: Jim put the ball in the box.
- **SIMTOM Step 2 (Answering)**: Jim believes the ball is still in the box.

This technique is simple, model-agnostic, and doesn’t require fine-tuning. It yielded significant gains on ToM benchmarks such as BigTOM and ToMI, especially on **false belief** questions.

---

### How It Evolved Over Chain-of-Thought

SIMTOM addresses a limitation of Chain-of-Thought (CoT) prompting: while CoT encourages step-by-step reasoning, it assumes a single global context and doesn’t explicitly distinguish between what is known to the model and what is known to characters in the narrative.

Whereas CoT tends to answer based on omniscient world knowledge, SIMTOM simulates **subjective belief states**. This makes it more effective for tasks involving **Theory of Mind**, such as false beliefs or nested beliefs ("Anne thinks that Sally thinks...").

SIMTOM can be seen as a **specialization of CoT**:
- Both decompose the reasoning process.
- SIMTOM introduces **mental state filtering** before reasoning begins.
- Unlike CoT, SIMTOM **modifies the context**, rather than generating a chain within a static context.

It also outperforms Self-Consistency and Tree-of-Thoughts on ToM tasks, highlighting that correct reasoning often depends on **the correct perspective**, not just logical steps.

---

### Novel Application Example

**Application: Simulating Conflicting Stakeholder Beliefs in Crisis Management**

Imagine using SIMTOM to model conflicting beliefs of different stakeholders during a corporate PR crisis. Each stakeholder has partial information about the event, and a system must simulate their likely actions.

**Scenario**:
- A data breach occurs, but only the CTO and security team are informed initially.
- The marketing lead drafts a statement assuming it’s just a routine maintenance outage.
- The PR team must decide which version of events each stakeholder believes before crafting the public response.

**SIMTOM-style prompting**:
1. **Perspective-Taking for the PR team**:
   > What does the marketing lead know?
   > - They know the system was offline at 2:30 AM.
   > - They received no alerts about breaches.

2. **Question-Answering**:
   > Based on what the marketing lead knows, what kind of statement would they propose?

   > **Answer**: They would draft a message citing system upgrades and apologize for any inconvenience.

This showcases how SIMTOM can guide LLMs to simulate stakeholder-specific beliefs and reasoning in high-stakes, real-world multi-agent environments.

## Plan-and-Solve Prompting (PS and PS+)

### How It Works

**Plan-and-Solve Prompting** is a zero-shot prompting technique designed to improve the reasoning capabilities of large language models (LLMs), particularly by addressing three common issues in Zero-shot Chain-of-Thought (CoT) prompting:  
- **Calculation Errors**  
- **Missing Reasoning Steps**  
- **Semantic Misunderstanding**

The method is built around a two-phase strategy:

1. **Planning Phase**:  
   The LLM is prompted to *devise a plan* that decomposes the problem into manageable subtasks.  
   _Prompt trigger_:  
   > "Let's first understand the problem and devise a plan to solve the problem."

2. **Solving Phase**:  
   The LLM is then prompted to *carry out* each step of the plan sequentially.  
   _Continuation_:  
   > "Then, let's carry out the plan and solve the problem step by step."

The improved version, **PS+**, adds more specific instructions to this base structure:
- Extract relevant variables and corresponding numerals
- Emphasize intermediate calculations
- Attend to commonsense consistency

An optional final step includes an *answer extraction prompt*, such as:  
> "Therefore, the answer (arabic numerals) is ___."

This method is zero-shot, meaning it avoids the need for handcrafted few-shot exemplars, and it is model-agnostic.

---

### How It Evolved Over Chain-of-Thought

Plan-and-Solve (PS) builds directly on the **Chain-of-Thought prompting** framework but introduces a key innovation: **explicit task decomposition before reasoning begins**.

#### Comparison with CoT:
| Feature | CoT | Plan-and-Solve |
|--------|-----|----------------|
| Prompt Style | "Let's think step by step" | "Devise a plan, then carry it out" |
| Planning | Implicit | Explicit |
| Instruction Detail | Minimal | Highly structured (in PS+) |
| Step Order | Emergent | Enforced plan-following |
| Zero-shot Performance | Moderate | Comparable or better than 8-shot CoT |

While CoT expects planning to emerge naturally during step-by-step reasoning, PS explicitly scaffolds it. This is particularly effective in problems where CoT models either:
- Skip steps (missing intermediate reasoning), or
- Miscalculate due to hasty generalizations.

In addition, PS+ often rivals or surpasses **Zero-shot Program-of-Thought (PoT)** and **8-shot Manual-CoT** on math datasets — a significant result for prompting strategies that do not rely on curated demonstrations.

---

### Novel Application Example

**Application: Customer Journey Debugging in E-commerce Analytics**

Suppose an analyst uses a LLM to trace a drop in sales conversions. The process involves multiple factors (ad clicks, cart abandonment, pricing changes) and requires structured problem decomposition. Here's how PS+ could help:

**Prompt Example:**
> Q: The company saw a 25% drop in conversions last week. Ad engagement remained high, but cart abandonment increased. There was also a pricing update on Tuesday. What could explain the conversion drop?  
>
> A: Let's first understand the problem, extract key events and their timings, and devise a plan.  
> Then, let's carry out the plan, reason through each step, and provide the most plausible explanation.  

**Model Output (summarized):**
- Extracted Variables:
  - Conversion drop: 25%
  - Ad engagement: unchanged
  - Cart abandonment: increased
  - Pricing change: mid-week
- Plan:
  1. Evaluate whether pricing changes align with drop in conversions.
  2. Examine timing between pricing update and abandonment.
  3. Rule out ad engagement as a cause.
- Reasoning:
  - The timing suggests the new pricing may have deterred customers post-click.
  - Since ad clicks stayed consistent, the issue likely occurred post-click.
  - Increased abandonment aligns with pricing change → pricing likely at fault.

This application demonstrates how PS+ prompting helps enforce analytic rigor in business intelligence tasks, guiding LLMs to analyze multi-factor problems systematically.

## Program-Aided Language Models (PAL)

### How It Works

**Program-Aided Language Models (PAL)** are a prompt-based technique where the LLM is tasked with generating a program—typically in Python—to solve a problem, but **delegates execution to a symbolic interpreter** (e.g., Python runtime). This approach addresses a key weakness of Chain-of-Thought (CoT) prompting: even if reasoning is correct, LLMs often make **arithmetic or logical mistakes** during execution.

The PAL prompting strategy involves:
1. **Problem Understanding**: The LLM reads a natural language problem.
2. **Code Generation**: The LLM generates interleaved natural language and code statements that describe intermediate steps as a Python program.
3. **External Execution**: The program is passed to a Python interpreter for execution.
4. **Answer Extraction**: The final answer is obtained from the program’s output.

This makes PAL a **neuro-symbolic hybrid**, combining the flexible understanding of LLMs with the precision of symbolic computation.

Example (adapted):
> Q: Olivia has $23. She bought 5 bagels for $3 each. How much money does she have left?  
> ```python
> # Olivia has $23
> money_initial = 23
> # Bagels: 5 at $3 each
> bagels = 5
> bagel_cost = 3
> money_spent = bagels * bagel_cost
> money_left = money_initial - money_spent
> answer = money_left
> ```

PAL achieved **state-of-the-art accuracy** on 13 reasoning benchmarks (math, symbolic, and algorithmic) and outperformed CoT by wide margins, particularly on hard problems involving large numbers.

---

### How It Evolved Over Chain-of-Thought

PAL builds directly upon Chain-of-Thought by preserving its **decomposition strategy**, but introduces two key evolutions:
- **Delegated Execution**: Instead of having the model perform calculations in natural language, PAL offloads this to a Python interpreter.
- **Programmatic Reasoning Chains**: CoT relies on natural language reasoning chains; PAL uses a structured mix of code and natural language.

#### Comparisons:
| Feature | Chain-of-Thought | PAL |
|--------|------------------|-----|
| Reasoning Format | Natural language steps | Python programs + comments |
| Execution | In-model | External interpreter |
| Accuracy on arithmetic | Moderate | High |
| Model dependency | High (must reason and compute) | Reduced (only reason and code) |

PAL also proved to be more robust to **large numerical values**, where CoT performance deteriorated. This evolution aligns with broader trends in **tool-augmented prompting** (e.g., Toolformer, ReAct), where reasoning and action are modularized.

Moreover, PAL generalizes across domains:
- Mathematical (GSM8K, SVAMP)
- Symbolic (BigBench Hard: COLORED OBJECTS)
- Algorithmic (REPEAT COPY, OBJECT COUNTING)

---

### Novel Application Example

**Application: Inventory Reconciliation in Supply Chain Auditing**

In a warehouse management context, LLMs can assist with reconciling inventory records using PAL-style reasoning:

> Q: A warehouse received 1,200 boxes. It shipped 350 to Store A, 200 to Store B, and 100 were returned as defective. How many boxes should remain?

**PAL-style prompt:**
```python
# Initial inventory
inventory = 1200

# Shipments
store_a = 350
store_b = 200

# Returns
defective = 100

# Reconciliation
shipped = store_a + store_b
adjusted_inventory = inventory - shipped - defective
answer = adjusted_inventory
```

By combining natural language understanding with precise programmatic execution, PAL helps ensure the correctness of financial or logistical computations—domains where errors are costly and interpretable reasoning is critical.

---

## Self-Consistency Prompting

### How It Works

**Self-Consistency Prompting** is a decoding strategy designed to enhance Chain-of-Thought (CoT) reasoning in large language models (LLMs) by addressing a key limitation: the reliance on a single, possibly suboptimal, reasoning path. Instead of using greedy decoding (which outputs the most probable next token at each step), Self-Consistency samples multiple **diverse reasoning paths**, then selects the most frequently occurring final answer among them.

**Steps of Self-Consistency Prompting**:
1. **Prompt with CoT**: The model is prompted using a CoT-style example.
2. **Sample Reasoning Paths**: Instead of one deterministic path, the model generates multiple possible reasoning sequences (using stochastic decoding like temperature sampling).
3. **Marginalize Answers**: The final answer is determined via **majority vote** across all sampled outputs.

This approach leverages the idea that diverse correct reasoning paths are more likely to converge on the same correct answer, while incorrect paths tend to produce more varied (and less consistent) results.

> Analogy: It's like asking multiple people to independently solve a logic problem. If most arrive at the same answer via different reasoning chains, you're more confident it's correct.

Empirical results show substantial gains:
- **GSM8K**: +17.9% accuracy
- **SVAMP**: +11.0%
- **AQuA**: +12.2%
- **StrategyQA**: +6.4%
- **ARC-Challenge**: +3.9%

---

### How It Evolved Over Chain-of-Thought

Self-Consistency is an evolutionary extension of Chain-of-Thought prompting:
- CoT introduced **step-by-step reasoning** as a way to boost accuracy and interpretability.
- However, CoT relies on **one reasoning path**, which may be brittle or erroneous.
- Self-Consistency generalizes CoT by **considering multiple plausible reasoning paths** and aggregating over them.

Where CoT assumes one "good" reasoning chain is enough, Self-Consistency accepts that:
- **Correct answers often emerge from different valid chains**, and
- **Incorrect answers are less likely to be repeated across chains**.

This idea is closely related to the concept of **"self-ensemble"** — using one model multiple times with varied decoding to simulate a consensus.

It also connects to other strategies:
- Unlike **ReAct** or **Toolformer**, Self-Consistency **doesn’t require tools or APIs**.
- Compared to **beam search** or **sample-and-rank**, it maintains high output diversity and is unsupervised.

---

### Novel Application Example

**Application: Diagnosing Root Causes in Incident Reports**

Imagine using Self-Consistency prompting to analyze root causes from customer support logs during an outage. Each reasoning path might represent a different hypothesis.

**Prompt Example:**
> Q: A user reports slow load times. Logs show increased latency on Service A, but normal metrics on Services B and C. Database I/O is high. What's the likely root cause?

**Multiple Reasoning Paths**:
1. "High DB I/O likely caused latency in Service A. B and C unaffected → localized issue → root cause: DB overload."
2. "Service A slow; B and C fine → problem not at gateway → logs show DB I/O spike → root cause: DB congestion."
3. "Latency spikes map to write-heavy ops → DB strain → Service A impacted → root cause: DB performance under write load."

**Answer (via majority vote)**: Database performance issues are the most consistent root cause.

This application showcases Self-Consistency’s usefulness in simulating ensemble-style diagnostics in unstructured environments like DevOps and IT support.

## Self-Verification Prompting

### How It Works

**Self-Verification Prompting** is a two-stage reasoning framework that improves the accuracy and robustness of Large Language Models (LLMs) by enabling them to verify their own answers. The idea is inspired by human-like cognitive behavior: after making a decision or drawing a conclusion, people often double-check their reasoning. This technique gives LLMs a similar ability.

The method consists of:
1. **Forward Reasoning**: The LLM generates multiple candidate answers using Chain-of-Thought (CoT) prompting.
2. **Backward Verification**: The model re-evaluates each candidate by treating the conclusion as a known fact and checking whether the original conditions can be inferred from it. This validation produces a **verification score**.

There are two main verification modes:
- **Condition Mask Verification (CMV)**: Mask key numeric or logical conditions from the original input and ask the model to recover them using the candidate conclusion.
- **True-False Item Verification (TFV)**: Ask the model to evaluate whether all parts of the problem remain logically consistent if the candidate answer is assumed correct.

The final answer is selected based on the **highest verification score**, not on likelihood alone. This approach does not require training or external verifiers, only carefully crafted prompts.

Empirically, self-verification improved accuracy across multiple reasoning datasets, e.g.,:
- GSM8K: +4.33%
- SingleEq: +2.39%
- MultiArith: +3.02%
- SVAMP: +1.12%

---

### How It Evolved Over Chain-of-Thought

Self-Verification expands on Chain-of-Thought (CoT) prompting by introducing **bidirectional reasoning**:
- CoT generates answers through **forward inference**: step-by-step reasoning from input to output.
- Self-Verification adds **backward inference**: using the output to check the internal consistency of input assumptions.

This technique addresses a major CoT limitation: **error propagation**. A single mistake in CoT can invalidate the full reasoning chain, and CoT lacks built-in mechanisms to detect such flaws. Self-Verification mitigates this by:
- Reusing the same LLM to **simulate reasoning from conclusion back to premise**.
- Providing interpretable verification scores that allow more reliable answer selection.
- Enabling compatibility with existing techniques such as Self-Consistency, PAL, and Least-to-Most prompting.

This represents a shift from **one-shot deterministic reasoning** to **multi-path, validated reasoning**, aligning with broader trends in using LLMs as reasoners with meta-cognitive faculties.

---

### Novel Application Example

**Application: Scientific Hypothesis Validation in Biomedical Research**

Imagine an LLM being used to assess hypotheses about causal relationships in biomedical literature. Given a proposed hypothesis (e.g., “Gene X regulates Protein Y under stress conditions”), the model must evaluate its plausibility based on experimental evidence and prior knowledge.

**Self-Verification Process**:
1. **Forward Reasoning**:
   > Given: Experimental data shows Gene X expression increases during oxidative stress. Protein Y also increases in the same context.  
   > Hypothesis: Gene X regulates Protein Y.  
   > CoT Output: Gene X is expressed first, followed by Protein Y increase. There is temporal correlation. It is plausible that Gene X regulates Protein Y.

2. **Backward Verification (CMV or TFV)**:
   > Given the hypothesis as a conclusion, can we infer the experimental conditions that must hold true?  
   > Mask: “Gene X expression increases under oxidative stress.”  
   > Ask: “What expression pattern would we expect under oxidative stress?”  
   > If the model consistently reproduces the correct masked conditions, the verification score is high.

This ensures not only that the model generates a plausible hypothesis, but also that it can **support it with verifiable assumptions**, increasing confidence in its scientific reasoning.

## Tree-of-Thought Prompting (ToT)

### How It Works

**Tree-of-Thought (ToT) Prompting** is a structured prompting technique that enhances problem-solving by organizing reasoning into a search tree of intermediate thoughts. Each node in the tree represents a partial solution—a coherent chunk of reasoning—and edges represent logical progressions or refinements.

The core idea is to frame reasoning as **tree search**:
- At each node, the LLM generates multiple "thought" candidates (i.e., plausible next reasoning steps).
- These thoughts are evaluated based on their potential to reach a correct final solution.
- Search algorithms like **breadth-first search (BFS)**, **depth-first search (DFS)**, or **beam search** guide the exploration through the tree.

This method enables the LLM to:
- Backtrack from poor intermediate paths,
- Look ahead across multiple steps,
- Prune impossible or illogical partial solutions,
- Maintain and refine multiple candidate chains of thought simultaneously.

Example use case: solving the “Game of 24” math puzzle
- Generate 3-step thought trees (e.g., (3 × 4) + (6 ÷ 2))
- Keep top-k candidates at each step (e.g., k = 5)
- Evaluate each node as “sure,” “maybe,” or “impossible” based on its potential to reach 24

ToT offers strong performance improvements for tasks that benefit from **strategic exploration and planning**, such as mathematical reasoning, logic puzzles, and coding problems.

---

### How It Evolved Over Chain-of-Thought

ToT generalizes and extends Chain-of-Thought (CoT) prompting by introducing **explicit branching and state evaluation** during reasoning. While CoT promotes linear, step-by-step generation, ToT enables:
- **Parallel exploration** of multiple reasoning paths
- **Reversible progress** (via backtracking)
- **Selective attention** to promising intermediate thoughts

| Feature            | CoT                          | ToT                               |
|--------------------|------------------------------|------------------------------------|
| Reasoning style     | Linear chain                 | Search tree                        |
| Step generation     | One path per prompt          | Multiple branches per state        |
| Evaluation          | Implicit (next token)        | Explicit scoring & pruning         |
| Error recovery      | None                         | Backtracking                       |
| Inspired by         | Human-like rationale         | Human strategic planning           |

ToT also differs from self-consistency and self-verification:
- Self-consistency relies on **sampling multiple outputs** without interaction
- ToT allows **stateful, multi-step deliberation**, potentially with intermediate feedback

Furthermore, variants like **ToT with Controllers (Long, 2023)** use reinforcement learning to adapt search heuristics over time—akin to AlphaGo’s strategy refinement.

---

### Novel Application Example

**Application: Clinical Diagnosis Support with Diagnostic Trees**

In medical triage or diagnostic reasoning, physicians often generate differential diagnoses and refine them through iterative hypothesis testing. ToT can simulate this process for decision support:

**Prompt structure:**
> The patient presents with fever, rash, and joint pain. Lab results are pending.  
> Step 1: Generate 3 possible diagnoses based on symptoms  
> Step 2: For each, predict which labs would be informative  
> Step 3: Interpret labs to support/refute each hypothesis  
> Step 4: Propose final diagnosis

**Tree-of-Thought search behavior:**
- At each node (diagnosis hypothesis), the LLM generates possible next steps (tests or interpretations).
- Nodes are evaluated (e.g., “plausible,” “inconclusive,” “ruled out”).
- The model follows promising diagnostic paths, backtracks from failed ones, and converges on the most consistent hypothesis.

This mirrors real-world diagnostic logic and demonstrates ToT’s strength in navigating multi-path, uncertain environments.

## Least-to-Most Prompting

### How It Works

**Least-to-Most Prompting** is a two-stage prompting strategy designed to improve the ability of large language models (LLMs) to solve complex reasoning tasks—especially those that are harder than the examples seen in prompts. It draws inspiration from educational scaffolding and human problem-solving.

The process involves:

1. **Problem Decomposition**:  
   The LLM is prompted (with decomposition exemplars) to break down a complex problem into a sequence of simpler subproblems.  
   _Example prompt_:  
   > Q: Elsa has 5 apples. Anna has 2 more. How many do they have in total?  
   > A:  
   > 1. How many apples does Anna have?  
   > 2. How many do they have together?

2. **Sequential Solving**:  
   The LLM then solves each subproblem one at a time using previously generated answers as inputs.  
   _Example prompt_:  
   > 1. Anna has 5 + 2 = 7 apples.  
   > 2. Elsa and Anna have 5 + 7 = 12 apples in total.

This step-by-step resolution mimics how humans often tackle hard problems by solving easier intermediate goals. Each subproblem builds on the previous, enabling **compositional generalization**—the ability to solve novel complex problems from simpler, familiar components.

Key results:
- Achieves **99.7% accuracy** on the SCAN benchmark (length split), surpassing chain-of-thought (CoT) by a large margin.
- Enables easy-to-hard generalization in symbolic manipulation and math reasoning without model retraining.

---

### How It Evolved Over Chain-of-Thought

Least-to-Most (LtM) Prompting builds directly on the core idea of Chain-of-Thought (CoT)—decomposing reasoning into smaller steps—but adds a more **structured and recursive framework**.

| Feature                  | Chain-of-Thought             | Least-to-Most Prompting           |
|--------------------------|------------------------------|------------------------------------|
| Reasoning Flow           | Flat step-by-step chain      | Decompose → solve → combine       |
| Subproblem Dependency    | Minimal                      | Answers feed into future steps     |
| Planning Stage           | Implicit or omitted          | Explicit decomposition required    |
| Generalization to Harder Problems | Limited              | Strong (shown on SCAN, GSM8K, DROP) |

LtM addresses CoT’s **easy-to-hard generalization gap**. While CoT performs well when test problems are similar to prompt examples, it degrades significantly on longer or more complex instances. LtM overcomes this by first *teaching the model how to plan*, then using its plan to scaffold the final answer.

It can be combined with:
- **Self-Consistency**: Sample multiple decomposition/solution paths.
- **Program-Aided reasoning (PAL)**: Write code for subproblems.
- **Tree-of-Thoughts**: Search multiple decomposition trees.

---

### Novel Application Example

**Application: Multi-step Budget Planning for Event Management**

Suppose you’re planning a conference and want an LLM to generate a cost estimate. The problem involves multiple interdependent subcomponents (venue, food, logistics, staff). LtM helps by structuring this planning phase.

**Prompt (Decomposition Stage)**:
> Q: Estimate the total cost of hosting a 200-person conference for one day.  
> A:  
> 1. Estimate cost of the venue rental.  
> 2. Estimate catering cost for 200 people.  
> 3. Estimate staffing cost for the event.  
> 4. Sum up all individual costs.

**Prompt (Solving Stage)**:
> 1. Venue rental: $5,000  
> 2. Catering: $40/person × 200 = $8,000  
> 3. Staffing: 10 staff × $200 = $2,000  
> 4. Total: $5,000 + $8,000 + $2,000 = $15,000

By leveraging decomposition, the model can tackle multidimensional planning tasks and produce modular, editable reasoning—ideal for use in decision-support and operations management.
