"""
Compatibility patch for Python 3.14 and Django context copying issue.
This file should be imported after Django is loaded.
"""
import sys


def apply_python314_patch():
    """Apply compatibility patch for Python 3.14."""
    if sys.version_info >= (3, 14):
        try:
            from django.template import context
            import copy
            
            # Store original __copy__ method if it exists
            if hasattr(context.Context, '__copy__'):
                original_copy = context.Context.__copy__
                
                def patched_copy(self):
                    """Patched __copy__ method for Python 3.14 compatibility."""
                    try:
                        return original_copy(self)
                    except (AttributeError, TypeError) as e:
                        error_str = str(e)
                        if "'super' object" in error_str or "has no attribute 'dicts'" in error_str:
                            # Use copy.copy as fallback which should work better
                            try:
                                return copy.copy(self)
                            except Exception:
                                # Manual context creation as last resort
                                new_context = context.Context()
                                # Try to copy dicts attribute
                                try:
                                    if hasattr(self, 'dicts') and self.dicts:
                                        new_context.dicts = [dict(d) for d in self.dicts]
                                except (AttributeError, TypeError):
                                    pass
                                # Copy other important attributes
                                for attr in ['autoescape', 'template_name', 'render_context']:
                                    if hasattr(self, attr):
                                        setattr(new_context, attr, getattr(self, attr))
                                return new_context
                        raise
                
                # Only patch if we haven't already
                if context.Context.__copy__ == original_copy:
                    context.Context.__copy__ = patched_copy
        except (ImportError, AttributeError):
            # Django not yet imported or Context doesn't have __copy__
            pass

