import scrapy
import re
from urllib.parse import urlparse, parse_qs, urlencode
from raksha_logger import logger


class WeddingSpider(scrapy.Spider):
    name = "wedding"

    def start_requests(self):
        base_url = (
            'https://www.wedding-spot.com/wedding-venues/?pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1'
        )
        yield scrapy.Request(base_url, callback=self.discover_venues, meta={'page': 1})

    def discover_venues(self, response):
        current_page = response.meta.get('page', 1)
        logger.info(f"Processing page {current_page}: {response.url}")

        venue_urls = response.css('div.onWhenS div.venueCard--wrapper > a::attr(href)').getall()
        logger.info(f"Found {len(venue_urls)} venues on page {current_page}")

        if not venue_urls:
            logger.warning(f"No venue urls found on page {current_page}.")
            return

        for url in venue_urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_venue)

        next_button = response.css('button[aria-label="Next Page"]')
        is_disabled = next_button.css('::attr(disabled)').get() is not None

        if next_button and not is_disabled:
            next_page = current_page + 1
            parsed_url = urlparse(response.url)
            query_params = parse_qs(parsed_url.query)
            query_params['page'] = [str(next_page)]

            new_query = urlencode(query_params, doseq=True)
            next_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{new_query}"

            logger.info(f"Proceeding to page {next_page}")
            yield scrapy.Request(next_url, callback=self.discover_venues, meta={'page': next_page})
        else:
            logger.success(f"Pagination completed at {current_page}")

    def parse_venue(self, response):
        venue_title = response.css('div[itemType=venue-name]::text').get()

        raw_number = response.css('div.styles--visibleMobile a#call-venue::attr(href)').get()
        venue_number = 'N/A'
        if raw_number:
            match = re.search(r'tel:([\d-]+)', raw_number)
            if match:
                venue_number = re.sub(r'\D', '', match.group(1))

        venue_highlights = response.css('div.styles--visibleMobile div.VenueHighlights--label::text').getall()

        raw_capacity = response.xpath('//h3[contains(text(), "Guest capacity:")]/following-sibling::p[1]/text()').get()
        venue_capacity = 'N/A'
        if raw_capacity:
            match = re.search(r'up to (\d+)', raw_capacity, re.IGNORECASE)
            if match:
                venue_capacity = match.group(1)
            else:
                match = re.search(r'\d+', raw_capacity)
                if match:
                    venue_capacity = match.group()

        venue_address = response.xpath('//h3[contains(text(), "Location:")]/following-sibling::p[1]/text()').get()
        formatted_address = venue_address.strip() if venue_address else 'N/A'

        logger.info(f"Scraped venue: {venue_title}")

        yield {
            'URL': response.url,
            'Venue name': venue_title,
            'Phone': venue_number,
            'Venue highlights': venue_highlights,
            'Guest capacity': venue_capacity,
            'Address': formatted_address
        }
