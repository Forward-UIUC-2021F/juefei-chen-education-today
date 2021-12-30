# Education Today

The goal is to get faculty information from US universities. 
Please clone this repo and run it on one of the Owl servers.

## Introduction

### General Work Flow

1. Get a list of university names (from US News)

2. Scrape department/major names for each university

3. Extract faculty information for each department/major from universities' official websites

4. Get detailed faculty information from LinkedIn and Orcid

### Work Flow of Scraping Faculty/Department Info

1. Search on Google to find possible URLs
2. For each URL, annotate all text elements on HTML
3. Convert raw HTML into a tree-like structure, and find the cluster containing target data
4. Find patterns and extract all faculty/department information



## Usage

Please refer to the end of each python file referred below for examples of calling functions.

### Scrape Department Data

```bash
cd department
python3 algorithm.py
```

### Scrape Faculty Data

```bash
cd faculty
python3 algorithm.py
```

### Scrape LinkedIn Data

```bash
cd faculty/LinkedIn
python3 get_linkedin_data.py
```

### Scrape Faculty Data

```bash
cd faculty/Orcid
python3 get_orcid_data.py
```
