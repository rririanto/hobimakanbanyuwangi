COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

HTML_MINIFY = True
COMPRESS_ROOT = os.path.join(SITE_ROOT, '../static')


INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
