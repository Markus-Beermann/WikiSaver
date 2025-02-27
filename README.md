# Globetrotters - WIKISavers

# Hackathon Project
By Hackathon Team—1

## Overview
### What does it look like?
- The player gets a **random starting location** and a **target location**, both a combination of a capital and a country.
- This is a **travel-based console game** designed to run in **PyCharm** or any Python-compatible terminal.
- The player chooses the **next destination** from a list of capital-country pairs based on all capitals and countries available on the Wikipedia page of their **current location**.
- The player is assigned a **starting budget** that decreases per kilometer traveled.
- The game ends under the following conditions:
  - The player **reaches the target location**.
  - The player **runs out of budget**.
  - The player **chooses to quit**.
- The player can **ask for AI help** at any point, but using AI hints will **cost a percentage of their initial budget**, depending on how helpful the hint is.
- The objective is to **reach the target location in the fewest attempts and with the lowest possible budget**.
- Since **traveling is expensive**, the player should plan efficiently and **choose the shortest routes**.

### Let’s Run the Game!

## Installation
1. Clone the repository or download the project.
git clone https://github.com/AteetVatan/WikiSaver.git

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install  openai
   pip install google-generativeai
   ```
3. Run the project:
   ```bash
   python3 main.py
   ```
## Future Enhancements
- Adding a graphical user interface (GUI) for a more interactive experience.
- Implementing real-world ticket pricing instead of a fixed budget system.
- Introducing multiplayer mode for competitive gameplay.
- 
## Dependencies
- `geopy` - For distance calculations.
- `geonamescache` - For geo locations.
- `wikipedia` - For wikipedia pages.
- `openai` - OpenAI LLM.
- `google-generativeai` - Gemeni LLM.
