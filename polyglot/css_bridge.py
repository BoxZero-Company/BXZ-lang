# polyglot/css_bridge.py
import re

class CSSBridge:
    @staticmethod
    def parse_css(css_content: str):
        """Parse CSS and return rules"""
        rules = []
        pattern = r'([^{]+)\{([^}]+)\}'
        
        for match in re.finditer(pattern, css_content):
            selector = match.group(1).strip()
            declarations = {}
            
            for decl in match.group(2).split(';'):
                if ':' in decl:
                    prop, val = decl.split(':', 1)
                    declarations[prop.strip()] = val.strip()
            
            rules.append({
                'selector': selector,
                'declarations': declarations
            })
        
        return rules
    
    @staticmethod
    def minify_css(css_content: str) -> str:
        """Minify CSS content"""
        # Remove comments
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        # Remove whitespace
        css_content = re.sub(r'\s+', ' ', css_content)
        # Remove spaces around brackets
        css_content = re.sub(r'\s*\{\s*', '{', css_content)
        css_content = re.sub(r'\s*\}\s*', '}', css_content)
        
        return css_content.strip()