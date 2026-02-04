import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from post.models import NewsPost
from .models import ScraperSource, ScraperJob


class NewsScraperService:
    def __init__(self, source: ScraperSource, user):
        self.source = source
        self.user = user
        self.job = None
    
    def scrape(self):
        self.job = ScraperJob.objects.create(
            source=self.source,
            started_by=self.user,
            status='running'
        )
        
        try:
            response = requests.get(
                self.source.url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                timeout=30
            )
            response.raise_for_status()
            print(response)
            soup = BeautifulSoup(response.content, 'lxml')
            
            news_data = self._extract_news_data(soup)
            print(type(soup))
            if news_data:
                news_post = self._create_or_update_news(news_data)

                self.job.items_scraped = 1
                self.job.items_published = 1
                self.job.status = 'completed'
                self.job.completed_at = timezone.now()
                self.job.save()
                
                self.source.last_scraped_at = timezone.now()
                self.source.success_count += 1
                self.source.status = 'active'
                self.source.save()
                
                return {
                    'success': True,
                    'news_post': news_post,
                    'job': self.job
                }
            else:
                raise Exception("Não foi possível extrair dados da página")
        
        except Exception as e:
            print(e)
            self.job.status = 'failed'
            self.job.error_message = str(e)
            self.job.completed_at = timezone.now()
            self.job.save()
            
            self.source.error_count += 1
            self.source.status = 'error'
            self.source.save()
            
            return {
                'success': False,
                'error': str(e),
                'job': self.job
            }
    
    def _extract_news_data(self, soup):

        try:
            data = {}
            
            title_element = soup.select_one(self.source.title_selector)
            if title_element:
                data['title'] = title_element.get_text(strip=True)
            else:
                return None
            
            content_element = soup.select_one(self.source.content_selector)
            if content_element:
                paragraphs = content_element.find_all('p')
                data['content'] = '\n\n'.join(
                    [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                )
            else:
                return None
            
            if self.source.image_selector:
                image_element = soup.select_one(self.source.image_selector)
                if image_element:
                    data['image_url'] = image_element.get('src')
            
            data['summary'] = data['content'][:200] + '...' if len(data['content']) > 200 else data['content']
            
            return data
        
        except Exception as e:
            print(f"Erro ao extrair dados: {str(e)}")
            return None
    
    def _create_or_update_news(self, news_data):
        slug = slugify(news_data['title'])
        
        news_post, created = NewsPost.objects.get_or_create(
            slug=slug,
            defaults={
                'title': news_data['title'],
                'content': news_data['content'],
                'summary': news_data['summary'],
                'source_url': self.source.url,
                'source_type': 'scraped',
                'author': self.user,
                'status': 'published',
                'published_at': timezone.now()
            }
        )
        
        if not created:
            news_post.content = news_data['content']
            news_post.summary = news_data['summary']
            news_post.updated_at = timezone.now()
            news_post.save()
        
        return news_post


def run_scraping_for_source(source_id, user):

    try:
        source = ScraperSource.objects.get(id=source_id, status='active')
        scraper = NewsScraperService(source, user)
        return scraper.scrape()
    except Exception as e:

        return {
            'success': False,
            'error': str(e)
        }