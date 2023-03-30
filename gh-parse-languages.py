"""
Before using this script, it's expected that you have used a variation of the following command to generate a repos.json input file:

> gh repo list <your organization name> --limit <your repo limit> --json nameWithOwner,languages --jq '.[] | (.languages) = [.languages[].node.name]' > repos.json

This script takes in the path to your repos.json file, and optionally a specific language to target, and determines the frequency of the identified language(s).
"""

import json
import argparse
import math


def calculateLanguageDistribution(json, lang):
    # count occurences of each language for across each repo:
    language_occurrences = {}
    for pair in json:
        for current_language in pair['languages']:
            if (current_language in language_occurrences):
                language_occurrences[current_language] += 1
            else:
                language_occurrences[current_language] = 1
    
    # sort language_occurrences by number of occurrences:
    language_occurrences = {k: v for k, v in sorted(language_occurrences.items(), key=lambda item: item[1], reverse=True)}

    # setup print formatting:
    percentage_width = 2

    # check if language argument was used:
    if (lang):
        # calculate language percentages:
        language_percent = math.floor(language_occurrences[lang] / len(json) * 100)
        # more print formatting:
        repo_text = "repo " if language_occurrences[lang] == 1 else "repos"
        # print results:
        print(f"{language_occurrences[lang]} {repo_text} ({language_percent:{percentage_width}}%) that include the language: {lang}")
    else:
        # more print formatting:
        repo_width = len(str(max(language_occurrences.values())))
        # print results:
        for language in language_occurrences:
            # calculate language percentages:
            language_percent = math.floor(language_occurrences[language] / len(json) * 100)
            # more print formatting:
            repo_text = "repo " if language_occurrences[language] == 1 else "repos"
            # print results:
            print(f"{language_occurrences[language]:{repo_width}} {repo_text} ({language_percent:{percentage_width}}%) that include the language: {language}")

def main():

    # parse arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='JSON file to read from')
    parser.add_argument('-l', '--language', required=False, help='language to search for')
    args = parser.parse_args()

    # read in lines from `gh repo list` command:
    json_obj = []
    with open(args.file, 'r') as f:
        for line in f:
            json_obj.append(json.loads(line))

    # call function to calculate language distribution:
    print(f"--- Parsing {len(json_obj)} repositories ---")
    calculateLanguageDistribution(json_obj, args.language)

main()