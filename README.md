# Background
This repo serves to streamline analysis of the prgogramming languages used across a GitHub Organization. One use case for doing so is to identify which subset of repositories contain a language that is supported by [CodeQL](https://codeql.github.com/docs/).

# Pre-requisites
1. [GitHub CLI](https://cli.github.com/)
2. [Python 3](https://www.python.org/downloads/)
3. Read access to repos in the target GitHub organization

# How it works
Using the GitHub CLI, we can pull data about the repositories in an organization (particularly repo names and languages). We can then parse these results using the GitHub CLI's built-in json parser. Finally, we analyze the parsed list of repos & languages with a python script.

## Step 1
Pull the list of repositories (and their languages) that you would like to analyze, and save them to a file. Some example commands to do so are listed below.

_List all repos in an organization:_

```shell
gh repo list ORGANIZATION --limit 100 \
--json languages,nameWithOwner \
--jq '.[] | (.languages) = [.languages[].node.name]' \
> repos.json
```

_List all repos that contain at least one CodeQL supported programming language:_

```shell
gh repo list ORGANIZATION --limit 100 \
--json nameWithOwner,languages \
--jq '
.[] | (.languages) = [.languages[].node.name] | 
select(.languages | any(. == "JavaScript" or . == "TypeScript" or . == "Python" or . == "Ruby" or . == "Java" or . == "C#" or . == "C" or . == "C++" or . == "Go" or . == "Kotlin"))' \
> repos.json
```

_List all repos that contain at least one CodeQL supported _interpreted_ programming language AND zero CodeQL supported _compiled_ languages:_

```shell
gh repo list ORGANIZATION --limit 100 \
--json nameWithOwner,languages \
--jq '
.[] | (.languages) = [.languages[].node.name] |                      
select(.languages | all(. != "Java" and . != "C#" and . != "C" and . != "C++" and . != "Go” and . != “Kotlin”)) |
select(.languages | any(. == "JavaScript" or . == "TypeScript" or . == "Python" or . == "Ruby"))' \
> repos.json
```

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

<img width="570" alt="Screenshot 2023-03-27 at 1 08 24 PM" src="https://user-images.githubusercontent.com/110078080/228015102-af19fa02-2139-41ab-8a07-bd6b47140bda.png">
