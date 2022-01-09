# Education Today

This module is responsible for collecting department and faculty information from US universities. It also includes the backend for a UI and a distributed crawler.

## Setup

1. Install dependencies.

```
pip3 install -r requirements.txt 
```

2. Set up MySQL database. Please setup the database according to the .sql files in data/. You can easily import each table with TablePlus ([Import from .sql with TabluePlus](https://tableplus.com/blog/2018/10/import-export-database.html)). After setting up your own database, please change the MySQL connector accordingly in [file1](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/282056dde9148be6a736747dc3d55edeef36371f/api.py#L12), [file2](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/282056dde9148be6a736747dc3d55edeef36371f/faculty/celery_scheduler.py#L7), and [file3](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/282056dde9148be6a736747dc3d55edeef36371f/faculty/tasks.py#L14).

3. Run tests
```
 // running the following command should print a list of department names
 python3 department/algorithm.py

 // running the following command should print a list of faculty info
 python3 faculty/algorithm.py
```

## Usage

##### Run Backend for the UI

```bash
# please run this command on Owl2
# To run the frontend, please refer to https://github.com/Forward-UIUC-2021F/juefei-chen-faculty-info-frontend
flask run --host=0.0.0.0 --port=3113
```

Please refer to the end of each python file referred below for examples of calling functions.

 ##### Scrape Department Data

```bash
cd department
python3 algorithm.py
```

##### Scrape Faculty Data

```bash
cd faculty
python3 algorithm.py
```

##### Scrape LinkedIn Data

Scraping LinkedIn profiles requires a valid LinkedIn account. When scraping LinkedIn profiles, the provided account will be kept signed in.

If no faculty information is printed during the execution, please register a LinkedIn account, and change [this line](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/406d8928cd68e1c6e891646bdd9a3eb9f2f5bb51/faculty/LinkedIn/get_linkedin_data.py#L109). LinkedIn has a strict limitation on scraping rate, so please do **not** change [this line](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/406d8928cd68e1c6e891646bdd9a3eb9f2f5bb51/faculty/LinkedIn/get_linkedin_data.py#L76) and [this line](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/406d8928cd68e1c6e891646bdd9a3eb9f2f5bb51/faculty/LinkedIn/get_linkedin_data.py#L93). If ths scraping rate is too fast, your account are very likely to be banned forever. However, if you are only scraping a few profiles (less than 10), then you can change [this line](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/406d8928cd68e1c6e891646bdd9a3eb9f2f5bb51/faculty/LinkedIn/get_linkedin_data.py#L76) to get the result faster.

```bash
cd faculty/LinkedIn
python3 get_linkedin_data.py
```

##### Scrape Orcide Data

```bash
cd faculty/Orcid
python3 get_orcid_data.py
```

## Algorithmic Design for Scraping Faculty Information
Scraping department information shares the same workflow as scraping faculty information.

##### 1. Introduction

The goal is: for any given (university, department) pair, be able to scrape the information (name, position, email, phone, and research interest) of all faculty members in the department.
To reach this goal, we made an assumption that faculty information is stored as a list (also called a cluster) in the HTML of the faculty-listing pages, see below.

![1](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/main/readme_img/1.png)

Work flow of the scraping process:
```
def function(university, department)
	possibleURLs = search_on_google(university, department)
	for url in possibleURLs:
		html = scrape(url)
		result = extract_facutly_info(html)
		if is_valid(result):
			return result
```

In the function, search_on_google, we create a query “(university) (department) faculty”, and return a list of urls from the google search result page. For example, for a pair (UIUC, CS), the query would be “UIUC CS faculty”
There are two important functions, extract_faculty_data and is_valid in the pseudo code above, and the details will be discussed in the following sections

##### 2. Methods of extracting data

##### 2.1 Construct DOM tree for the HTML

This step is straightforward, see the example below

![2](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/main/readme_img/2.png)

During implementation, class names in html tags are also included, e.g. `<div class="name">`. If there exist multiple tags with the same name, add index to make each tag path unique. For the example above, as there are two `<p>` tags, the second one is renamed to `<p1>`. Therefore, the tag path leading to faculty position would be `<li><div><p>` while the tag path for research interest is `<li><div><p1>`

##### 2.2. Annotate All Text Elements

##### 2.2.1 Name

When checking if a string is “Name” type, we compared it to the previously scraped DBLP authors’ names (https://dblp.org/pers?prefix=, millions of names). We also have a list of forbidden words which appear in DBLP authors’ names, but on faculty listing pages, they are very unlikely to appear in faculty’s names, such as “map” and “majors”. If any of these forbidden words appear in a string, we would say this string is not “Name” type.

##### 2.2.2 Position

['professor', 'associate', 'assistant', 'lecturer', 'assoc', 'adjunct', 'faculty', 'instructor', 'director', 'asst', 'emeritus', 'prof']

If any of the words above appears in a string, then the string is “Position” type.

These words are manually extracted from the most popular words among thousands of faculty positions.

##### 2.2.3 Email

Check if the string contains '@', and '.edu' or '.com'

##### 2.2.4 Phone

Check if the string contains 10 digits

##### 2.2.5 Research Interest

Compare the string to the research interests collected from Google Scholar’s Profiles, e.g. https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=austin&btnG=


##### 2.3 Find the Cluster

Create a dictionary for each text element. Keys are tag path, and values are the corresponding categories. See an example below:

![3](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/main/readme_img/3.png)

In the example above, the tag path to the cluster should be: `<body><div><div><main><div><div><div><ul>`.
The reason is that this tag path appears in the first 8 records, and after the `<ul>` tag, tag names diverged into `<li2>, <li2>,<li3>...` Meanwhile, since the last tag path is highly different from the others, its corresponding text element should have been mistakenly annotated as research interest.

Pseudo code for identifying the tag path to the cluster:
```
i = 0
N = the number of tag paths whose text elements types are not None
target_tag_path = []
threshold = 0.2
while True:
	popular_tag, n = most frequent i-th tag among all tag paths, and its fequency
	if n / N > threshold:
		target_tag_path.append(popular_tag)
	else:
		break
	i += 1
```

##### 2.4 Find Tag Path to Each Category in Cluster

First extract the cluster from the full DOM tree, see an example below:

![4](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/main/readme_img/4.png)

With an algorithm similar to the pseudo-code in section 2.3, we are able to find the tag path to each category of target data in the cluster.
Note that even if there are variations in the structure of information listed for some faculty members, e.g. some faculty may have their email address listed, while others may not, we are still able to identify tag paths correctly with class names in tags.


##### 2.5 Extract Data with Tag Paths in the Cluster

With the cluster and the tag paths identified above, we can extract all faculty’s information from the cluster


##### 2.6 Handle Websites with Complex Structures

Previously, we discussed how to extract faculty info based on the assumption that there exists a cluster containing the target data, which is faculty info here. There is another assumption that it is possible to identify tag paths to each category of target data. Although for most websites, we can identify correct tag paths simply based on tags and their class names, there are some websites that may not have class names in tags, or the class names for a certain field are not the same. In this section, we will discuss how to handle situations where these two assumptions do not hold.

##### 2.6.1 Target data are separated into multiple clusters

##### Problem Description

Normally, we are expecting there is a cluster containing all faculty info, for example:

```
<div class=’faculty_info’>
	<li>...</li>
	<li>...</li>
	<li>...</li>
	…
</div>
```

However, faculty info may exist in several such clusters, for example:

```
<div class=’professor_info’>
	<li>...</li>
	<li>...</li>
	<li>...</li>
	…
</div>
…
<div class=’associate_professor_info’>
	<li>...</li>
	<li>...</li>
	<li>...</li>
	…
</div>
```

##### Solution

Previously, we are using a dictionary described in section 2.3 to locate the cluster (in this dictionary, keys are tag paths, and values are the corresponding categories). Now, after identifying the largest cluster containing faculty info, we remove all elements in that cluster from the dictionary and try to locate the second largest cluster.


##### 2.6.2 Cannot identify tag path

Consider the following example, it is impossible to use a tag path to locate different categories of data.

```
<div> 
	<li> 	
		<a> prof A </a>
		<a> Professor </a> 
		<a> a@gmail.com </a> 
		<a class=phone> 217 000 0001 </a> 
		<a> Research Interest: AI </a> 
	</li> 
	<li> 
		<a> prof B </a>
		<a> Associate Professor </a> 
		<a> Office: … </a> 
		<a> b@gmail.com </a> 
		<a class=phone> 217 000 0002 </a> 
		<a> Research Interest: Web </a> 
	</li> 
	<li> 
		<a> prof C </a>
		<a> Professor </a> 
		<a> c@gmail.com </a> 
		<a class=phone> 217 000 0003 </a> 
	</li> 
</div> 
```

Here, we introduced the technique of **Anchors**. Anchors must have the properties: easy to locate and always appear. See all children of a parent tag as an ordered list, anchor points can be the first or last index of the list, and it can also be some tag with class names.
In the example above, it is difficult to locate email addresses, because email addresses do not have specific class names. So we need to consider relative positions to anchor points. Here we have three options: 1. Start point; 2. Endpoint; 3. `<a class=phone>`. If we choose the start point as anchor points, there is a problem: the second block contains office information while others do not. So we are only 66% sure that email addresses are 1 unit under the start point. Similar to choosing the endpoint, we are also 66% sure that email addresses are 2 units above the endpoint (the third block does not contain research interest). However, if we choose `<a class=phone>`, we can see that email addresses are always one unit above `<a class=phone>`. Therefore, we should choose `<a class=phone>` as the best anchor point. When locating email addresses, we can use this path: `<div><li><a class=phone><move one unit upwards>`

##### 3 Result Validation
We are using the following rules to validate the faculty info extracted from websites

1. Faculty names should never be empty
2. No duplicated faculty names
3. Use the annotator to validate results (more tests required)

In our implementation, if the result is not satisfying, it will be remembered in a variable, then the extraction process will be run again. And in this round, when identifying the cluster, all text elements extracted from the previous round will not be considered again. 
This process is for handling the cases when the annotator makes too many mistakes. Consider the case when there are only 5 faculty members in a department, but dozens of noise are misrecognized are research interest (the performance of annotating research interest is not always satisfying). In this case, if the noise is gathered in another cluster, then we could not find the correct cluster. On the other hand, the data extracted from the wrong cluster cannot pass the validation process, since faculty names are empty. Therefore, these noises will be automatically remembered, and the whole workflow will be executed again, starting from locating the cluster.

Note that as our current annotator for research interest does not perform very well, in our latest implementation, we only use text elements that are annotated as name or position to locate the cluster. This feature may require more tests. To disable this feature, comment out [this line](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/406d8928cd68e1c6e891646bdd9a3eb9f2f5bb51/faculty/find_possible_list.py#L3) and uncomment [this line](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/406d8928cd68e1c6e891646bdd9a3eb9f2f5bb51/faculty/find_possible_list.py#L4).

##### 4 Quick Fix to the System

The performance of this system highly depends on the accuracy of the annotator. If the annotator makes too many errors, then there is no way to extract faculty info. 
If this system did not perform well, please uncomment [this line](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/406d8928cd68e1c6e891646bdd9a3eb9f2f5bb51/faculty/get_data_from_multiple_lists.py#L220-L221), and run again. This time, you can see the text elements and their annotated categories. If you see some noise are annotated as “Name”, add each word in the noise into [this file](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/406d8928cd68e1c6e891646bdd9a3eb9f2f5bb51/faculty/annotator/name/forbiden.txt).