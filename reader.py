import json
import time

COLORS = {
    "r": "\033[31m",
    "g": "\033[32m",
    "y": "\033[33m",
    "b": "\033[34m",
    "w": "\033[0m"
}


with open("scenario.json", "r", encoding="utf-8") as f:
    scenario = json.load(f)


def colorize(text):
    for color, code in COLORS.items():
        text = text.replace(f"<{color}>", code).replace(f"</{color}>", COLORS["w"])
    return text


def say(text):
    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(0.025)


def playNode(node):
    for line in node.get("dialog", []):
        time.sleep(line["delay"])
        say(colorize(line["text"]))


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
        if i + 1 == len(default):
            i -= 1
        return getChoice(node, i + 1)
    return choices[userChoice].get("next")


def start_reader():
    currentNode = "start"

    while currentNode:
        node = scenario.get(currentNode)
        playNode(node)
        currentNode = getChoice(node)
