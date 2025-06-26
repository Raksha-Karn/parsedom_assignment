# Parsedom Assignment - Raksha Karn

I am very efficient in Python, so for this assignment I am using Scrapy as I have used this in lots of my projects already and also, this website is not dynamic or client-side rendered, we can get the data quickly and easily.

Based on your URL, the website has 20 listing pages currently, so I have scraped all 20 pages with 720 total detail pages. You can see the scraped data using the link below.

Link to Sample Data: [Intern_assignment_Raksha_Karn_Google_Sheets](https://docs.google.com/spreadsheets/d/1EHXJjnr5s-dmj49wHWOq9WEkldgTrvLeJNB9L-GJGcc/edit?usp=sharing)

## Project Setup and Running

- Make sure you have python and pip in your computer.
- Clone this repository using `git clone https://github.com/Raksha-Karn/parsedom_assignment.git`
- Install the required packages using `pip install -r requirements.txt`
- Go to the project folder using `cd parsedom_assignment`
- Run the code using `scrapy crawl wedding -O result.csv`
- After the code has completed running, you can see the final result in result.csv file in your folder.

## How It Works

- Step 1: For pagination, I found out that the URL for the next page can be found by adding the page number to the URL's query parameter like '?page=2'.
- Step 2: I ran an infinite loop until I reached the page where the next page button has the 'disabled' property.
- Step 3: After pagination is done, I get the URL for the detail page in each listings page using the CSS selector.
- Step 4: In the details page, for each required property, I use CSS selector, Xpath and regex to get the data.

## My Other Scraping projects

- RemoteOk Scraper - This scraper scrapes https://remoteok.com using Selenium. [Link to the repository](https://github.com/Raksha-Karn/Remote-Ok-Scraper)

- CoinMarketCap Scraper - This scraper scrapes https://coinmarketcap.com using Scrapy. [Link to the repository](https://github.com/Raksha-Karn/CoinMarketCap-Scraper)

- LinkedIn Scraper - This scraper scrapes https://linkedin.com using Selenium. [Link to the repository](https://github.com/Raksha-Karn/InScraper)

- Reddit Scraper - This scraper scrapes https://reddit.com using Scrapy. [Link to the repository](https://github.com/Raksha-Karn/Reddit-Scraper)
