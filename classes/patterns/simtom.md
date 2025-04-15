# SimToM & SimToM-Domain

Provides a better performance on Theory of Mind benchmarks by asking the model to answer questions based on how elements of a story are perceived from the point of view of a character.

While SimToM is a zero-shot prompt technique, SimToM-Domain uses 3-5 examples. 

### When To Use

 - Tasks that require ToM
 - Tasks with complex stories involving multiple characters

### Limitations

 - Was only tested in medium / large models (over 7 Billion parameters).
 - Models good at ToM might not need it

### Implementation

**SimToM**

Has two passes (prompt-answering cycles)
 - Perspective-Taking Pass
    ```
    The following is a sequence of events:
    {story}
    Which events does {character_name} know
    about?
    ```
 - Question-Answering Pass
    ```
    {story from character_name’s perspective}
    Answer the following question:
    {question}
    ```

### Rationale

Inspired by Simulation Theory’s two‑step cognitive process—first mentally “step into” the character’s knowledge state, then answer the ToM question—this separation prevents LLMs from using omniscient information.

### Performance Metrics:

 - BigTOM False‑Belief: GPT‑3.5‑Turbo: 41.0% → 70.5% (+29.5%); Llama2‑7B: 47.5% → 70.5% (+23.0%)

 - ToMI False‑Belief: GPT‑4: 25.5% → 87.75% (+62.25%); GPT‑3.5‑Turbo: 67.25% → 81.0% (+13.75%)

### Origin: 

Wilf et al., 2023
