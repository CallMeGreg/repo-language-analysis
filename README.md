# Background
This repo serves to streamline analysis of the prgogramming languages used across a GitHub Organization. One use case for doing so is to identify which repositories contain a language that is supported by [CodeQL](https://codeql.github.com/docs/).

# Pre-requisites
1. [GitHub CLI](https://cli.github.com/)
2. [Python 3](https://www.python.org/downloads/)
3. Read access to repos in the target GitHub organization

# How it works
Using the GitHub CLI, we can pull data about the repositories in an organization (particularly repo names and languages). We can then parse these results using the GitHub CLI's built-in json parser. Finally, we analyze the parsed list of repos & languages with a python script.

## Step 1
Pull the list of repositories/languages that you would like to evaluate, and save them to a file. Some example commands are provided below.

List all repos in an organization:
`gh repo list ORGANIZATION --limit 100 --json languages,nameWithOwner --jq '.[] | (.languages) = [.languages[].node.name]' > repos.json`

List all repos that contain at least one CodeQL supported programming language:
`gh repo list ORGANIZATION --limit 100 --json nameWithOwner,languages --jq '.[] | (.languages) = [.languages[].node.name] | select(.languages | any(. == "JavaScript" or . == "TypeScript" or . == "Python" or . == "Ruby" or . == "Java" or . == "C#" or . == "C" or . == "C++" or . == "Go" or . == "Kotlin"))' > repos.json`

List all repos that contain at least one CodeQL supported _interpreted_ programming language AND zero CodeQL supported _compiled_ languages:


## Step 2
Analyze the languages in the targted list of repositories by running the `gh-parse-languages.py` python script (located in this repo).

```
usage: gh-parse-languages.py [-h] -f FILE [-l LANGUAGE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  JSON file to read from
  -l LANGUAGE, --language LANGUAGE
                        language to search for
```
Example: `python3 gh-parse-languages.py -f repos.json`

# Example gh commands
Listed below are several examples of how you can analyze the languages used in an organization. Make sure that the `--limit` flag and ORGANIZATION name are updated for your specific needs.

`gh repo list ORGANIZATION --limit 100 --json languages,nameWithOwner --jq '.[] | (.languages) = [.languages[].node.name]’`
