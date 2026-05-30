# polyglot/html_bridge.py
import webbrowser
import tempfile
import os

class HTMLBridge:
    @staticmethod
    def render_html(html_content: str, open_browser: bool = True):
        """Render HTML content"""
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.html', 
            delete=False
        )
        temp_file.write(html_content)
        temp_file.close()
        
        if open_browser:
            webbrowser.open(f'file://{temp_file.name}')
        
        return temp_file.name
    
    @staticmethod
    def validate_html(html_content: str) -> tuple:
        """Validate HTML syntax"""
        # Basic HTML validation
        errors = []
        if '<html>' not in html_content:
            errors.append("Missing <html> tag")
        if '<body>' not in html_content:
            errors.append("Missing <body> tag")
        
        return len(errors) == 0, errors