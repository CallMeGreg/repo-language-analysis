# Archived
This repository has been archived and replaced by an easier to use `gh` extension that can be found here: https://github.com/CallMeGreg/gh-language

# Overview
This repo helps analyze the prgogramming languages used across a GitHub Organization. One use case for doing so is to identify the distribution of repositories that contain a language supported by [CodeQL](https://codeql.github.com/docs/).

# Pre-requisites
1. [GitHub CLI](https://cli.github.com/)
2. [Python 3](https://www.python.org/downloads/)
3. Read access to repos in the target GitHub organization

# How it works
Using the GitHub CLI, we can pull data about the repositories in an organization (specifically repo names and languages). We can then parse these results using the GitHub CLI's built-in json parser. Finally, we analyze the parsed list of repos & languages with a python script to determine the frequnecy of each language.

## Step 1
Set environment variables for your target organization name and repository limit:

```shell
export ORGANIZATION=your-organization-name-here
export REPO_LIMIT=100
```

## Step 2
Pull the list of repositories (and their languages) that you would like to analyze, and save them to a file. Some example commands to do so are listed below.

_List all repos in an organization:_

```shell
gh repo list $ORGANIZATION --limit $REPO_LIMIT \
--json languages,nameWithOwner \
--jq \
'.[] | (.languages) = [.languages[].node.name]' \
> repos.json
```

_List all repos that contain at least one CodeQL supported language:_

```shell
gh repo list $ORGANIZATION --limit $REPO_LIMIT \
--json nameWithOwner,languages \
--jq \
'.[] | (.languages) = [.languages[].node.name] | 
select(.languages | any(. == "JavaScript" or . == "TypeScript" or . == "Python" or . == "Ruby" or . == "Java" or . == "C#" or . == "C" or . == "C++" or . == "Go" or . == "Kotlin"))' \
> repos.json
```

_List all repos that contain at least one CodeQL supported *_*interpreted*_* language AND zero CodeQL supported *_*compiled*_* languages:_

```shell
gh repo list $ORGANIZATION --limit $REPO_LIMIT \
--json nameWithOwner,languages \
--jq \
'.[] | (.languages) = [.languages[].node.name] |
select(.languages | all(. != "Java" and . != "C#" and . != "C" and . != "C++" and . != "Go" and . != "Kotlin")) |
select(.languages | any(. == "JavaScript" or . == "TypeScript" or . == "Python" or . == "Ruby"))' \
> repos.json
```

## Step 3
Analyze the languages in the targted list of repositories by running the `gh-parse-languages.py` python script.

```
usage: gh-parse-languages.py [-h] -f FILE [-l LANGUAGE] [-t TOP]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  JSON file to read from
  -l LANGUAGE, --language LANGUAGE
                        language to search for
  -t TOP, --top TOP     top N languages to display
```

Example:
```shell
python3 gh-parse-languages.py -f repos.json
```

<img width="570" alt="Screenshot 2023-03-27 at 1 08 24 PM" src="https://user-images.githubusercontent.com/110078080/228015102-af19fa02-2139-41ab-8a07-bd6b47140bda.png">

## (Optional) Step 4
If you would like to convert the output from the previous `gh` commands into valid json format for your own further analysis, use the following command:
```shell
sed '1s/^/[/;$!s/$/,/;$s/$/]/' repos.json > formatted_repos.json
```

# Find a problem?
Please open an [issue](https://github.com/CallMeGreg/repo-language-analysis/issues/new)!
