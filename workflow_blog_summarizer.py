from __future__ import annotations as _annotations
import asyncio
import logging
from dataclasses import dataclass
from typing import Literal

import httpx
import nest_asyncio
from rich.logging import RichHandler
from rich.console import Console
from rich import print
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from pydantic_ai.agent import Agent
from pydantic_ai.models.openai import OpenAIModel, OpenAIModelSettings
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=False)]
)
logger = logging.getLogger(None)

nest_asyncio.apply()

class InputDep(BaseModel):
    url: str = Field(..., title="URL")

class BlogSummary(BaseModel):
    # original_text: str = Field(..., title="Original Text") -- only if you want to archive the original text used
    title: str = Field(..., title="Title")
    summary: str = Field(..., title="Summary")
    content_type: Literal['blog', 'news', 'documentation', 'other'] = Field(..., title="Content Type") 

class PageContent(BaseModel):
    title: str = Field(..., title="Title")
    core_content: str = Field(..., title="Core Content")

def download_page_content(url: str) -> str:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.'
        }
        
        logger.info(f"Downloading page content from {url}")
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        logger.info(f"Page content downloaded from {url}")
        
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup.get_text().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    except httpx.HTTPStatusError as e:
        logger.error(f'HTTP error occurred: {str(e)}')
        return f'HTTP error occurred: {str(e)}'
    
agent_webpage_crawl = Agent(
    name='Webpage Crawl Agent',
    model=OpenAIModel('gpt-4o-mini'),
    result_type=PageContent,
    model_settings=OpenAIModelSettings(
        max_tokens=3000, # gpt-4o-mini max output token is 16,400
        temperature=0.1,
    )
)

agent_summarizer = Agent(
    name='Summary Agent',
    model=OpenAIModel('gpt-4o'),
    result_type=BlogSummary,
    model_settings=OpenAIModelSettings(
        max_tokens=2000,
        temperature=0.5,
    ),
    system_prompt=("""
		You are a blog summarizer designed to provide concise and informative summaries of blog content. 
        When given a page title and its content, summarize the blog in 2–3 sentences, capturing the main idea, key points, 
        and purpose in a neutral and clear tone. Format your response with bullet points to highlight:
		- The core topic or thesis of the blog
		- One or two significant details or arguments
		- The intended takeaway or conclusion    
    """)
)

@dataclass
class GetPageContent(BaseNode[InputDep]):
    """Node to get the content of a blog post"""

    async def run(self, ctx: GraphRunContext) -> SummarizeContent:
        page_content = download_page_content(ctx.state.url)
        prompt = (f"""Page Content: {page_content}\n\nUser: Based on the page content above, return only the origianl text that
                    associated with title, core content. """)
        
        logger.info(f'Running GetPageContent with prompt: {prompt}')

        result = await agent_webpage_crawl.run(prompt)
     
        return SummarizeContent(result.data)
    
@dataclass
class SummarizeContent(BaseNode[PageContent, None]):
    """Node to summarize the content of a blog post"""
    page_content: PageContent

    async def run(self, ctx: GraphRunContext) -> End[BlogSummary]:
        if self.page_content.core_content is None:
            logger.info('No content to summarize')
            return End("No content to summarize")
        
        logger.info(f'Summarizing content: {self.page_content.core_content}')
        result = await agent_summarizer.run(
           self.page_content.model_dump_json()
        )
        return End(result.data)

summary_graph = Graph(nodes=[GetPageContent, SummarizeContent], name='Blog Summary Workflow')

async def main():
    result = await summary_graph.run(GetPageContent(), state=input_data)
    return result.output

if __name__ == '__main__':
    url = 'https://resources.workable.com/employee-compensation-development'
    input_data = InputDep(url=url)
    response = asyncio.run(main())

    print(f'Title: {response.title}')
    print(f'Content Type: {response.content_type}')
    print('Summary:')
    print(response.summary)