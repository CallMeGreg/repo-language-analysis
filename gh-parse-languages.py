"""
Before using this script, it's expected that you have used a variation of the following command to generate a repos.json input file:

> gh repo list <your organization name> --limit <your repo limit> --json nameWithOwner,languages --jq '.[] | (.languages) = [.languages[].node.name]' > repos.json

This script takes in the path to your repos.json file, and optionally a specific language to target, and determines the frequency of the identified language(s).
"""

import json
import argparse
import math


def calculateLanguageDistribution(json: list[dict], lang: str, top_n: int) -> None:
    # count occurrences of each language for across each repo:
    language_occurrences = {}
    for pair in json:
        for current_language in pair['languages']:
            if current_language in language_occurrences:
                language_occurrences[current_language] += 1
            else:
                language_occurrences[current_language] = 1

    # sort language_occurrences by number of occurrences:
    language_occurrences = {k: v for k, v in sorted(language_occurrences.items(), key=lambda item: item[1], reverse=True)}

    # setup print formatting:
    percentage_width = 2

    # more print formatting:
    repo_width = 0 if lang else len(str(max(language_occurrences.values())))

    # print results:
    for idx, language in enumerate([lang] if lang else language_occurrences):
        # calculate language percentages:
        language_percent = math.floor(language_occurrences[language] / len(json) * 100)
        # more print formatting:
        repo_text = "repo " if language_occurrences[language] == 1 else "repos"
        # print results:
        print(f"{language_occurrences[language]:{repo_width}} {repo_text} ({language_percent:{percentage_width}}%) that include the language: {language}")
        # exit if top_n set and printed
        if idx >= top_n - 1:
            break


def main():
    # parse arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='JSON file to read from')
    parser.add_argument('-l', '--language', required=False, help='language to search for')
    parser.add_argument('-t', '--top', required=False, help='top N languages to display', type=int, default=100)
    args = parser.parse_args()

    # read in lines from `gh repo list` command:
    json_obj = []
    with open(args.file, 'r') as f:
        for line in f:
            json_obj.append(json.loads(line))

    # call function to calculate language distribution:
    header = f"top {args.top}" if args.top else len(json_obj)
    print(f"--- Parsing {header} repositories ---")
    calculateLanguageDistribution(
        json=json_obj,
        lang=args.language,
        top_n=args.top,
    )


main()
