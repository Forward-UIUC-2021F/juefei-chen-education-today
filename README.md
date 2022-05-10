## This module will be used to extract the faculty information for a specific department

## Description of the submodule:
This module is designed to achieve the following tasks:
1. Extract top university information for a specific field given the url or HTML document (similar to USAToday)
2. For each university in the extracted list, find the faculty information for the specified department

`NOTE`: All the files have the same description and functionality as mentioned in the master branch
Please Refer to: [Main branch README](https://github.com/Forward-UIUC-2021F/juefei-chen-education-today/blob/main/README.md#algorithmic-design-for-scraping-faculty-information)

## Installation:

1. Run the following line:
    > pip3 install -r requirements.txt

2. Download the file 'normalized_name_set.txt' from the following url and place it in the root folder:
https://drive.google.com/drive/folders/14fj4O7DsAk-zfBHs7EaH5IafuQ-GaFQ_?usp=sharing

## Instructions to run:

1. Run the following command by replacing \<department\> with department name (Eg: 'mathematics') and \<university\> with the university name (Eg: 'UIUC')
    >  python3 algorithm.py --department \<department> --url \<url>

    Example:
    >  python3 algorithm.py --department mathematics --url https://www.usnews.com/best-graduate-schools/top-science-schools/mathematics-rankings --urlmap_path mathematics_url_map.json

    Here ```--urlmap_path``` (used to provide specific URL's to scrape faculty information from) is path to a file which contains data of the below format:
    ```
    {
        "Columbia University": "https://www.math.columbia.edu/people/faculty-by-rank/",
        "California Institute of Technology": "https://pma.caltech.edu/people?cat_one=all&cat_two=Mathematics",
        "Arizona State University": "https://math.asu.edu/faculty/",
        "Michigan State University": "https://math.msu.edu/Directory",
        "Northeastern University": "https://cos.northeastern.edu/our-people/"
    }
    ```

2. If a HTML file containing the top institution information is available it can be passed instead of the URL. (This can be useful for website which load the information after scrolling Eg: USAToday). For pasing the raw_html run the following command with the path to the .html file

    >  python3 algorithm.py --department \<department> --raw_html \<raw_html_path>
    
    Example:
    >  python3 algorithm.py --department mathematics --raw_html './raw_html.html'

3. One can use the following parameters for further tuning the results:
- > --name_penalty : This is a fraction between 0 and 1 which can be used to indicate the penalty to be applied for each wrongly classified name in scraped document.

- > --google_priority: This is a float value which can be used to give priority to the result order in google search. i.e. if this values is above 1, then the topmost results in google will get a higher score than lower documents

    Example
    > python3 algorithm.py --department mathematics --raw_html './raw_html.html' --name_penalty=0.2 --google_priority=1.3

## Results:
The results which include the list of top institutions and their corresponding faculty information (as a json) would be available in /results/ folder

### Output format:


```bash
[
	{
		'Name': ...,
		'Position': ...,
		'Research Interest': ...,
		'Email': ...,
		'Phone': ...
	},
	{
		'Name': ...,
		'Position': ...,
		'Research Interest': ...,
		'Email': ...,
		'Phone': ...
	},
	...
]
```