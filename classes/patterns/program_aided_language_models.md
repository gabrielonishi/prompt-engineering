# Program Aided Language Models (PAL)

Chain of tought extension that uses a programming language interpreter to levrage better results than regular CoT, trusting the LLM to produce the code and the code to calculate results.

### When To Use

Complex math and logic problems that regular CoT can't solve.

### Limitation

### Implementation

### Rationale

LLMs often produce correct reasoning chains but make arithmetic mistakes. PAL uses LLMs for decomposition and understanding, but delegates computation to a reliable symbolic executor (Python). This decouples reasoning from execution, improving robustness and reducing common failure modes in CoT (e.g., incorrect math).

### Performance Metrics:


### Origin: 

