# Module 1 Quick Checks: Answers

**Course:** Python for AI  
**Module 1:** Python Basics for GenAI and Agentic AI  


## Lesson 1.1: Welcome to the GenAI & Agentic AI

**Q1:** b) AI that plans, uses tools and acts in a loop until a goal is done  
**Why:** Agentic AI plans steps, uses tools, and repeats actions until it reaches a goal.

**Q2:** c) Predicting the next token  
**Why:** An LLM generates text by predicting likely next tokens based on its context.

**Q3:** b) Loop  
**Why:** The formula is Agent = LLM + Tools + Memory + Loop.

**Q4:** c) Most businesses use ready-made models through APIs, so applied AI skills are in demand  
**Why:** The course focuses on applying existing AI models to practical tasks.

**Q5:** b) A hallucination  
**Why:** A hallucination is an answer that sounds confident but is wrong or unsupported.

**Q6. Predict the Output**

```text
Hello from kimi!
```

**Why:** The f-string replaces `{model}` with the value `kimi`.

## Lesson 1.2: Setting Up Your AI Dev Toolkit

**Q1:** c) uv  
**Why:** `uv` can install Python and also manage packages and projects.

**Q2:** b) Close and reopen the terminal  
**Why:** A new terminal loads the updated PATH after installation.

**Q3:** b) AI libraries need time to support new versions, so pros use a stable one  
**Why:** A stable Python version avoids compatibility problems with libraries.

**Q4:** b) Ollama  
**Why:** Ollama runs AI models locally, so data stays on your computer.

**Q5:** b) So your commits are linked to your GitHub profile  
**Why:** GitHub uses the commit email to link commits to your profile.

**Q6. Predict the Output**

```text
Python 3.13.16
```

**Why:** `--version` prints the Python version the project uses, which the question gives as 3.13.16.

## Lesson 1.3: Your First Python Project with uv

**Q1:** b) Stores exact package versions so the project runs the same on any machine  
**Why:** `uv.lock` records exact dependency versions for reproducible installs.

**Q2:** c) Keep it out of GitHub (it is in `.gitignore`)  
**Why:** `.venv/` is a local environment and should not be committed.

**Q3:** b) The project becomes a simple project, and scripts still run with `uv run`  
**Why:** Removing `src/` and `[build-system]` makes it a simple project, and `uv run` still works.

**Q4:** b) `uv add ollama`  
**Why:** `uv add` adds a package dependency to the project.

**Q5:** b) It always uses the project's own `.venv`, even if you forgot to activate it  
**Why:** `uv run` runs the command in the project's managed environment.

**Q6. Predict the Output**

```text
Hi, I am Ali and I will become an AI Agent Developer.
```

**Why:** The f-string fills in `{name}` and `{goal}`.

## Lesson 1.4: Talking to Python: print, input and Comments

**Q1:** c) `str`  
**Why:** `input()` always returns text, even when the user types digits.

**Q2:** b) `Python-for-AI`  
**Why:** `sep="-"` puts a hyphen between the printed values.

**Q3:** c) `print(f"Tokens: {50}")`  
**Why:** An f-string converts the number to text, so no error occurs.

**Q4:** b) `temperature = 0.2  # low value for focused, factual answers`  
**Why:** A good comment explains why, not just what the code does.

**Q5:** c) ValueError  
**Why:** `int("abc")` cannot convert the text `abc` into an integer.

**Q6. Predict the Output**

The user types `20`. The `print()` outputs:

```text
201
```

**Why:** `input()` returns the string `"20"`. Adding `"1"` joins the strings and gives `"20"`, not 21. (The `Age: ` prompt appears on screen from `input()`, but it is not part of what `print()` outputs.)

   ```
