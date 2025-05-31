"""
File Readers
Specific readers for different file formats
"""
import os
import json
from abc import ABC, abstractmethod

# Try to import optional dependencies
try:
    import ebooklib
    from ebooklib import epub
    EPUB_AVAILABLE = True
except ImportError:
    EPUB_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    try:
        import fitz  # PyMuPDF
        PDF_AVAILABLE = True
        USE_PYMUPDF = True
    except ImportError:
        PDF_AVAILABLE = False
        USE_PYMUPDF = False

class BaseReader(ABC):
    """Base class for file readers"""
    
    @abstractmethod
    def read(self, filepath):
        """Read file and return content"""
        pass

class TextReader(BaseReader):
    """Reader for text files"""
    
    def read(self, filepath):
        """Read text file"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as file:
                        content = file.read()
                        return {
                            'type': 'text',
                            'title': os.path.basename(filepath),
                            'content': content,
                            'chapters': [{'title': 'Full Text', 'content': content}]
                        }
                except UnicodeDecodeError:
                    continue
            
            raise ValueError("Could not decode file with any supported encoding")
            
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")

class EpubReader(BaseReader):
    """Reader for EPUB files"""
    
    def read(self, filepath):
        """Read EPUB file"""
        if not EPUB_AVAILABLE:
            raise ImportError("ebooklib is required to read EPUB files")
        
        try:
            book = epub.read_epub(filepath)
            
            # Extract metadata
            title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else os.path.basename(filepath)
            author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else "Unknown"
            
            # Extract chapters
            chapters = []
            content_items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
            
            for item in content_items:
                # Parse HTML content and extract text
                content = item.get_content().decode('utf-8')
                # Simple HTML stripping (you might want to use BeautifulSoup for better parsing)
                text_content = self._strip_html(content)
                
                if text_content.strip():
                    chapters.append({
                        'title': f"Chapter {len(chapters) + 1}",
                        'content': text_content
                    })
            
            # Combine all content
            full_content = '\n\n'.join([chapter['content'] for chapter in chapters])
            
            return {
                'type': 'epub',
                'title': title,
                'author': author,
                'content': full_content,
                'chapters': chapters
            }
            
        except Exception as e:
            raise Exception(f"Error reading EPUB file: {str(e)}")
    
    def _strip_html(self, html_content):
        """Simple HTML tag removal"""
        import re
        # Remove HTML tags
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', html_content)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

class PdfReader(BaseReader):
    """Reader for PDF files"""
    
    def read(self, filepath):
        """Read PDF file"""
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 or PyMuPDF is required to read PDF files")
        
        try:
            if 'USE_PYMUPDF' in globals() and USE_PYMUPDF:
                return self._read_with_pymupdf(filepath)
            else:
                return self._read_with_pypdf2(filepath)
                
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def _read_with_pypdf2(self, filepath):
        """Read PDF using PyPDF2"""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract metadata
            metadata = pdf_reader.metadata
            title = metadata.get('/Title', os.path.basename(filepath)) if metadata else os.path.basename(filepath)
            
            # Extract text from all pages
            chapters = []
            full_content = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    chapters.append({
                        'title': f"Page {page_num + 1}",
                        'content': page_text
                    })
                    full_content += page_text + "\n\n"
            
            return {
                'type': 'pdf',
                'title': title,
                'content': full_content,
                'chapters': chapters
            }
    
    def _read_with_pymupdf(self, filepath):
        """Read PDF using PyMuPDF"""
        import fitz
        
        doc = fitz.open(filepath)
        
        # Extract metadata
        metadata = doc.metadata
        title = metadata.get('title', os.path.basename(filepath)) if metadata else os.path.basename(filepath)
        
        # Extract text from all pages
        chapters = []
        full_content = ""
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_text = page.get_text()
            
            if page_text.strip():
                chapters.append({
                    'title': f"Page {page_num + 1}",
                    'content': page_text
                })
                full_content += page_text + "\n\n"
        
        doc.close()
        
        return {
            'type': 'pdf',
            'title': title,
            'content': full_content,
            'chapters': chapters
        }
