from typing import Dict, Any, Optional
from jinja2 import Environment, Template as Jinja2Template, TemplateError
import hashlib
import json

class RenderService:
    def __init__(self, cache_enabled: bool = False):
        self.cache_enabled = cache_enabled
        self.cache = {}  # Simple in-memory cache for development
        self.env = Environment(
            autoescape=True,
            # Add more Jinja2 configuration as needed
        )

    def _get_cache_key(self, template_id: int, context: Dict[str, Any]) -> str:
        """Generate a cache key based on template ID and context."""
        context_hash = hashlib.md5(
            json.dumps(context, sort_keys=True).encode()
        ).hexdigest()
        return f"template:{template_id}:context:{context_hash}"

    def _cache_get(self, key: str) -> Optional[str]:
        """Get rendered content from cache."""
        if not self.cache_enabled:
            return None
        return self.cache.get(key)

    def _cache_set(self, key: str, content: str) -> None:
        """Store rendered content in cache."""
        if self.cache_enabled:
            self.cache[key] = content

    def render_template(
        self,
        html_content: str,
        css_content: Optional[str] = None,
        js_content: Optional[str] = None,
        context: Dict[str, Any] = None,
        template_id: Optional[int] = None
    ) -> str:
        """Render a template with given context and optional CSS/JS."""
        context = context or {}
        
        # Check cache if template_id is provided
        if template_id and self.cache_enabled:
            cache_key = self._get_cache_key(template_id, context)
            cached = self._cache_get(cache_key)
            if cached:
                return cached

        try:
            # Create and render template
            template = self.env.from_string(html_content)
            rendered_html = template.render(**context)

            # Inject CSS if present
            if css_content:
                rendered_html = rendered_html.replace(
                    "</head>",
                    f"<style>{css_content}</style></head>"
                )

            # Inject JS if present
            if js_content:
                rendered_html = rendered_html.replace(
                    "</body>",
                    f"<script>{js_content}</script></body>"
                )

            # Cache the result if template_id is provided
            if template_id and self.cache_enabled:
                cache_key = self._get_cache_key(template_id, context)
                self._cache_set(cache_key, rendered_html)

            return rendered_html

        except TemplateError as e:
            raise ValueError(f"Template rendering error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing template: {str(e)}")

    def validate_template_syntax(self, html_content: str) -> Dict[str, Any]:
        """Validate Jinja2 template syntax."""
        try:
            self.env.parse(html_content)
            return {
                "is_valid": True,
                "errors": []
            }
        except Exception as e:
            return {
                "is_valid": False,
                "errors": [str(e)]
            }

    def clear_cache(self, template_id: Optional[int] = None) -> None:
        """Clear the render cache.
        
        Args:
            template_id: If provided, only clear cache for this template.
                       If None, clear entire cache.
        """
        if not self.cache_enabled:
            return

        if template_id:
            # Clear specific template cache
            keys_to_remove = [
                k for k in self.cache.keys()
                if k.startswith(f"template:{template_id}:")
            ]
            for key in keys_to_remove:
                self.cache.pop(key, None)
        else:
            # Clear all cache
            self.cache.clear()

    def get_template_variables(self, html_content: str) -> Dict[str, Any]:
        """Extract and analyze template variables and structures."""
        try:
            ast = self.env.parse(html_content)
            variables = set()
            blocks = set()
            
            def visit_node(node):
                if hasattr(node, 'name'):
                    if node.name == 'block':
                        blocks.add(node.name)
                    else:
                        variables.add(node.name)
                for child in node.iter_child_nodes():
                    visit_node(child)
            
            visit_node(ast)
            
            return {
                "variables": sorted(list(variables)),
                "blocks": sorted(list(blocks)),
                "has_extends": any(
                    node.__class__.__name__ == 'Extends'
                    for node in ast.iter_child_nodes()
                )
            }
        except Exception as e:
            raise ValueError(f"Error analyzing template: {str(e)}")

    def create_preview_context(self, variables: list) -> Dict[str, Any]:
        """Create a preview context with dummy data for template variables."""
        context = {}
        for var in variables:
            # Create dummy data based on variable name
            if "list" in var.lower() or "items" in var.lower():
                context[var] = [
                    {"id": 1, "name": "Item 1"},
                    {"id": 2, "name": "Item 2"}
                ]
            elif "date" in var.lower():
                context[var] = "2024-01-01"
            elif "time" in var.lower():
                context[var] = "12:00:00"
            elif "enabled" in var.lower() or "active" in var.lower():
                context[var] = True
            elif "count" in var.lower() or "number" in var.lower():
                context[var] = 42
            else:
                context[var] = f"Sample {var}"
        
        return context 