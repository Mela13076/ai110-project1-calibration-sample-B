# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

1. If the secret number is 52 and the guess is 50, the game should provide a "Higher" hint; if the guess is 54, it should provide a "Lower" hint. The game incorrectly told me to go "Lower" for a guess of 50 and "Higher" for a guess of 54 when the secret was 52. The return statements in the conditional operators in the check_guess function are swapped, saying "Too Low" when the guess is too high and "Too High" when the guess is too low.

2. Selecting "Easy" mode should update all UI elements (the "blue card" info) to show the 1-20 range and 6 attempts. While the internal logic may change, the blue informational card does not update to reflect the new difficulty parameters. The Streamlit UI component responsible for displaying the game stats is not being re-rendered or updated when the st.selectbox for difficulty changes.

3. Clicking "New Game" should clear all previous game data, including error messages (red boxes) and guess history. The "red message" and the previous game's history remain visible on the screen after a new game starts. The st.session_state variables for history and error messages are not being cleared or overwritten during the new game initialization function.

4. Switching the difficulty level should trigger a fresh game state with a new secret number and reset attempts. Changing the difficulty updates the attempt count, but it does not automatically start a new game unless the "New Game" button is manually pressed. The difficulty selection logic lacks a trigger to reset the secret_number in the st.session_state


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion you accepted and why.
- Give one example of an AI suggestion you changed or rejected and why.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.


## 6. AI Model Comparison (Challenge 4)
I compared GitHub Copilot (GPT-4o) and Google Gemini 1.5 Pro to fix the inverted "Higher/Lower" hints.

GitHub Copilot (GPT-4o):
- The Fix: Swapped the return strings within the existing if/else block.
- Analysis: This was the most "Pythonic" fix because it maintained the original code's style and used the fewest lines of code.

Google Gemini 1.5 Pro:
- The Fix: Suggested refactoring the function using a match statement.
- Analysis: While the code was clean, the explanation was superior; it clearly broke down the mathematical reason why guess > secret must result in a "Lower" hint for the player.

Conclusion: I used the Copilot fix for code consistency, but Gemini provided a better educational breakdown of the "why"
