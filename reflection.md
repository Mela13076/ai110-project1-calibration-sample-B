# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- The first time I ran the game, it appeared functional at a glance, but the logic was fundamentally flawed, making it difficult to win
- Bugs noticed initially: 
  1. If the secret number is 52 and the guess is 50, the game should provide a "Higher" hint; if the guess is 54, it should provide a "Lower" hint. The game incorrectly told me to go "Lower" for a guess of 50 and "Higher" for a guess of 54 when the secret was 52. The return statements in the conditional operators in the check_guess function are swapped, saying "Too Low" when the guess is too high and "Too High" when the guess is too low.

  2. Selecting "Easy" mode should update all UI elements (the "blue card" info) to show the 1-20 range and 6 attempts. While the internal logic may change, the blue informational card does not update to reflect the new difficulty parameters. The Streamlit UI component responsible for displaying the game stats is not being re-rendered or updated when the st.selectbox for difficulty changes.

  3. Clicking "New Game" should clear all previous game data, including error messages (red boxes) and guess history. The "red message" and the previous game's history remain visible on the screen after a new game starts. The st.session_state variables for history and error messages are not being cleared or overwritten during the new game initialization function.

  4. Switching the difficulty level should trigger a fresh game state with a new secret number and reset attempts. Changing the difficulty updates the attempt count, but it does not automatically start a new game unless the "New Game" button is manually pressed. The difficulty selection logic lacks a trigger to reset the secret_number in the st.session_state


---

## 2. How did you use AI as a teammate?

- I primarily used VS Code Copilot (GPT-4o) for refactoring and Gemini 1.5 Pro for logic comparisons. I accepted Copilot’s suggestion to use an on_change callback for the difficulty selector because it provided a clean way to reset the game state automatically. However, I rejected an AI suggestion to use a complex match statement for the hint logic because it didn't match the existing code style and was less readable than a simple if/else fix.

---

## 3. Debugging and testing your fixes

- I verified my fixes by combining manual play-testing with automated pytest cases to ensure no regressions were introduced. I ran a specific test for the "Too High" hint where a guess of 60 against a secret of 50 correctly returned the "Lower" outcome. Copilot helped me design these tests by using the Generate Tests smart action, which identified boundary edge cases like guesses exactly at the range limits.

---

## 4. What did you learn about Streamlit and state?

- The secret number kept changing in the original app because it was defined in the main script flow without being stored in session state, causing it to re-randomize every time the script reran. I would explain to a friend that Streamlit reruns the entire script from top to bottom whenever a user interacts with a widget, and "session state" is like a memory bank that keeps variables alive between those runs. The change that finally stabilized the secret number was wrapping its initialization in a check for if "secret" not in st.session_state.

---

## 5. Looking ahead: your developer habits

- I plan to reuse the habit of marking "crime scenes" with #FIXME comments before asking AI for help, as it keeps the context focused and leads to better suggestions. Next time, I will practice better "session hygiene" by starting new chat sessions for unrelated bugs to prevent the AI from getting confused by old code snippets. This project taught me that AI-generated code is a great starting point, but it requires strict human oversight to catch subtle logic flaws that can break the entire user experience.


## 6. AI Model Comparison (Challenge 4)
I compared GitHub Copilot (GPT-4o) and Google Gemini 1.5 Pro to fix the inverted "Higher/Lower" hints.

GitHub Copilot (GPT-4o):
- The Fix: Swapped the return strings within the existing if/else block.
- Analysis: This was the most "Pythonic" fix because it maintained the original code's style and used the fewest lines of code.

Google Gemini 1.5 Pro:
- The Fix: Suggested refactoring the function using a match statement.
- Analysis: While the code was clean, the explanation was superior; it clearly broke down the mathematical reason why guess > secret must result in a "Lower" hint for the player.

Conclusion: I used the Copilot fix for code consistency, but Gemini provided a better educational breakdown of the "why"
