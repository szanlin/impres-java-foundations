import codecs
import re
import jinja2
import markdown
import pygments
import logging

from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

LOG=logging.getLogger('test')
console = logging.StreamHandler()
console.setLevel(logging.INFO)

with codecs.open('java-presentation.html', 'w', encoding='utf8') as outfile:		
    md_src = codecs.open('java-foundations.md', encoding='utf8').read()
    slides_src = markdown.markdown(md_src).split('<hr />\n')

    title = slides_src.pop(0)

    head_title = title.split('>')[1].split('<')[0]

    slides = []

    for slide_src in slides_src:
        header, content = slide_src.split('\n', 1)

        while '<code>!' in content:
            lang_match = re.search('<code>!(.+)\n', content)

            if lang_match:
                lang = lang_match.group(1)
				
                code = content.split(lang, 1)[1].split('</code>', 1)[0]

                lexer = get_lexer_by_name(lang)

                formatter = HtmlFormatter(linenos='inline', noclasses=True,
                                          nobackground=True)

                pretty_code = pygments.highlight(code, lexer, formatter)
                pretty_code = pretty_code.replace('&amp;', '&')

                before_code = content.split('<code>', 1)[0]
                after_code = content.split('</code>', 1)[1]

                content = before_code + pretty_code + after_code

        slides.append({'header': header, 'content': content})

    template = jinja2.Template(open('base.html').read())

    outfile.write(template.render(locals()))
