import json
import time

with open("scenario.json", "r", encoding="utf-8") as f:
    scenario = json.load(f)


def say(text):
    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(0.02)


def playNode(node):
    for line in node.get("dialog", []):
        time.sleep(line["delay"])
        say(line["text"])


def getChoice(node, i=0):
    choices = node.get("choices", {})
    for key, value in choices.items():
        if "text" in value:
            print(f"{value['text']}")
    userChoice = input("\n>_").strip().lower()
    if userChoice not in choices:
        default = choices.get("default", [])
        say(default[i])
        print()
        if i+1 == len(default):
            i -= 1
        getChoice(node, i + 1)
    return choices[userChoice].get("next")


currentNode = "start"

while currentNode:
    node = scenario.get(currentNode)
    playNode(node)
    currentNode = getChoice(node)
