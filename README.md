# PasswordImprover

A simple python password evaluator, generator and improver.

Option 1: 
Tests your password and gives it a score out of 100:
- checks if the password is in rockyou.txt
- checks if any common names are included in the password
- checks for sequences and repetitions
- checks for the inclusion of numbers and symbols
- checks the length


Option 2:
Generates random passwords:
- 3 options for length


Option 3:
Improves your password using a local instance of mistral:
- passes on the missing criteria to the LLM
- given the task to generate a similar but improved password
- returns the new password

### ! Option 3 requires you to have [ollama](https://ollama.com/) installed and mistral downloaded (run 'ollama pull mistral')
