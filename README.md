## This module will be used to extract the faculty information for a specific department

## Description of the submodule:
This module is designed to achieve the following tasks:
1. Extract top university information for a specific field given the url or HTML document (similar to USAToday)
2. For each university in the extracted list, find the faculty information for the specified department

NOTE: All the files have the same description and functionality as mentioned in the master branch

## Installation:

1. Run the following line:
> pip3 install -r requirements.txt

## Instructions to run:

1. Run the following command by replacing \<department\> with department name (Eg: 'mathematics') and \<university\> with the university name (Eg: 'UIUC')
>  python3 algorithm.py --department \<department> --url \<url>

>  Eg: python3 algorithm.py --department mathematics --url https://www.usnews.com/best-graduate-schools/top-science-schools/mathematics-rankings --urlmap_path mathematics_url_map.json

2. If a HTML file containing the top institution information is available it can be passed instead of the URL. (This can be useful for website which load the information after scrolling Eg: USAToday). For pasing the raw_html run the following command with the path to the .html file

>  python3 algorithm.py --department \<department> --raw_html \<raw_html_path>

>  Eg: python3 algorithm.py --department mathematics --raw_html './raw_html.html'

## Results:
The results which include the list of top institutions and their corresponding faculty information (as a json) would be available in /results/ folder