from .base_agent import BaseAgent
from bs4 import BeautifulSoup
from typing import Dict, Any
import json
import httpx


class WebScraperAgent(BaseAgent):
    """Agent 1: Scrapes web pages and extracts product/idea information."""

    def __init__(self):
        system_prompt = """You are an expert web content analyzer specializing in SaaS and web app products.

Your task is to analyze web page content and extract comprehensive information about the product or idea.

If the content is limited (due to bot protection or sparse pages), use your knowledge and the URL/domain to infer reasonable information.

Extract and structure the following information:
1. Product/Idea Title
2. Description (2-3 sentences)
3. Key Features (list of features with descriptions)
4. Target Audience (who is this for?)
5. Value Proposition (main benefit/selling point)
6. Category (SaaS, web app, tool, platform, etc.)
7. Pain Points Addressed (what problems does it solve?)

Return your response as a valid JSON object with these keys:
{
    "title": "...",
    "description": "...",
    "features": ["feature1", "feature2", ...],
    "target_audience": "...",
    "value_proposition": "...",
    "category": "...",
    "pain_points": ["pain1", "pain2", ...]
}

Be thorough but concise. Focus on the core value and unique aspects."""

        super().__init__("WebScraperAgent", system_prompt)

    def scrape_url(self, url: str) -> str:
        """Use httpx + BeautifulSoup to scrape the web page."""
        self.log(f"Scraping URL: {url}")

        try:
            # Use more realistic headers to avoid 403
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
            }

            with httpx.Client(follow_redirects=True, timeout=30.0) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                content = response.text

            # Parse with BeautifulSoup to clean it up
            soup = BeautifulSoup(content, 'lxml')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            # Limit to reasonable size (GPT-4 context)
            text = text[:15000]

            self.log(f"Successfully scraped {len(text)} characters")
            return text

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                self.log("⚠️  Site returned 403 - may have bot protection. Using fallback analysis...")
                # For 403 errors, provide fallback content
                return self._fallback_url_analysis(url)
            raise Exception(f"Failed to scrape URL: {str(e)}")
        except Exception as e:
            self.log(f"⚠️  Scraping failed: {str(e)}. Using fallback analysis...")
            return self._fallback_url_analysis(url)

    def _fallback_url_analysis(self, url: str) -> str:
        """Fallback analysis when scraping fails."""
        domain = url.replace('https://', '').replace('http://', '').split('/')[0]
        return f"""URL Analysis for: {url}
Domain: {domain}

Note: The website has bot protection (Cloudflare or similar), so content extraction was limited.

Based on the domain name and URL structure, this appears to be a web application or SaaS product.

The domain suggests: {domain}

Please analyze what type of product this might be based on the domain name and any typical use cases for such a domain.
Make reasonable inferences about:
- Likely product category
- Potential target audience
- Possible features
- Value proposition

For example:
- If it's an "app" domain, it's likely a web/mobile application
- If it mentions specific industries, that's the target
- Common SaaS patterns suggest features

Use your knowledge to fill in reasonable details that would make sense for this domain."""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a URL and extract product information.

        Input: {"url": "https://..."}
        Output: {"url": "...", "extracted_data": {...}, "raw_content": "..."}
        """
        url = input_data.get("url")
        if not url:
            raise ValueError("URL is required")

        # Scrape the page
        raw_content = self.scrape_url(url)

        # Analyze with GPT-4
        self.log("Analyzing content with GPT-4...")
        prompt = f"""Analyze the following web page content and extract product/idea information.

Web page content:
{raw_content}

Return the information as a valid JSON object as specified in your system prompt.
Be intelligent about inferring information even if content is limited."""

        response = self.call_gpt(prompt, response_format="json_object")

        # Parse the JSON response
        try:
            extracted_data = json.loads(response)
        except json.JSONDecodeError:
            raise Exception("Failed to parse GPT-4 response as JSON")

        self.log(f"Successfully extracted data for: {extracted_data.get('title', 'Unknown')}")

        return {
            "url": url,
            "extracted_data": extracted_data,
            "raw_content": raw_content[:5000]  # Store limited raw content for reference
        }
