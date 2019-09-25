import os
import re
import time

lexicon = './lexicon.keel'
inventory = {}

site_name = 'Craze'
site_title_separator = ' &sdot; '
template_default = """
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.5">
        <title>{title_formatted}</title>
        <link rel="stylesheet" type="text/css" href="/style/style.css">
    </head>
    <body>
        <div class="kbBackground">
            <div class="kbContentWrapper">
                <form class="kbSearchForm" method="post" action="." autocomplete="off">
                    <input name="search" placeholder="{page_title}" autocomplete="off" spellcheck="false"/>
                    <input type="submit" value="Search" style="display:none;"/>
                </form>
                {page_breadcrumb}
                {page_body}
            </div>
            <div class="kbFooter">
                <div class="kbFooterInner">
                    <div class="kbFooterLeft">
                        <a href="http://webring.xxiivv.com" target="_blank" class="webring">
                            <svg class="xxiivv_webring" width="300px" height="300px" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" baseProfile="full" version="1.2">
                                <g transform="translate(0,30)">
                                    <g transform="translate(150,150),rotate(120,0,0)">
                                        <path class="xxiivv_webring" d="M0,-60 a60,60 0 1,0 0,120 l100,0"></path>   
                                    </g>
                                    <g transform="translate(150,150),rotate(240,0,0)">
                                        <path class="xxiivv_webring" d="M0,-60 a60,60 0 1,0 0,120 l100,0"></path>   
                                    </g>
                                    <g transform="translate(150,150),rotate(0,0,0)">
                                        <path class="xxiivv_webring" d="M0,-60 a60,60 0 1,0 0,120 l100,0"></path>   
                                    </g>
                                </g>
                            </svg>
                        </a>
                    </div>
                    <div class="kbFooterRight">
                        CC BY-NC 4.0<br>
                        <a href="/keelback">Keelback 19.8.6</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
"""
template_banner = """
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.5">
        <title>{title_formatted}</title>
        <link rel="stylesheet" type="text/css" href="/style/style.css">
    </head>
    <body>
        <div class="kbBackground">
                <div class="kbBanner" style="background-image:url('{page_banner}');">
                    <div class="kbBannerContent">
                        <form class="kbSearchForm" method="post" action="." autocomplete="off">
                            <input name="search" placeholder="{page_title}" autocomplete="off" spellcheck="false"/>
                            <input type="submit" value="Search" style="display:none;"/>
                        </form>
                    </div>
                </div>
            <div class="kbContentWrapper kbContentShort">
                {page_breadcrumb}
                {page_body}
            </div>
            <div class="kbFooter">
                <div class="kbFooterInner">
                    <div class="kbFooterLeft">
                        <a href="http://webring.xxiivv.com" target="_blank" class="webring">
                            <svg class="xxiivv_webring" width="300px" height="300px" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" baseProfile="full" version="1.2">
                                <g transform="translate(0,30)">
                                    <g transform="translate(150,150),rotate(120,0,0)">
                                        <path class="xxiivv_webring" d="M0,-60 a60,60 0 1,0 0,120 l100,0"></path>   
                                    </g>
                                    <g transform="translate(150,150),rotate(240,0,0)">
                                        <path class="xxiivv_webring" d="M0,-60 a60,60 0 1,0 0,120 l100,0"></path>   
                                    </g>
                                    <g transform="translate(150,150),rotate(0,0,0)">
                                        <path class="xxiivv_webring" d="M0,-60 a60,60 0 1,0 0,120 l100,0"></path>   
                                    </g>
                                </g>
                            </svg>
                        </a>
                    </div>
                    <div class="kbFooterRight">
                        CC BY-NC 4.0<br>
                        <a href="/keelback">Keelback 19.8.6</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
"""

class Page:
    def __init__(self, inventory, name, body = None, unde = None, icon = None, banr = None):
        self.name = name
        self.body = body
        self.unde = unde
        self.over = []
        self.icon = icon
        self.banr = banr
        self.name_url = name.lower().replace(' ', '-')
        inventory[self.name_url] = self

    def assemble(self, template):
        title_formatted = self.name + site_title_separator + site_name
        breadcrumb = self.make_breadcrumb()
        if self.name_url == 'index':
            breadcrumb = ''
        page_body = self.parse_text()
        if self.banr:
            prototype = template.format(
                title_formatted=title_formatted,
                page_banner=self.banr,
                page_title=self.name,
                page_breadcrumb=breadcrumb,
                page_body=page_body
                )
        else:
            prototype = template.format(
                title_formatted=title_formatted,
                page_title=self.name,
                page_breadcrumb=breadcrumb,
                page_body=page_body
                )
        return prototype

    def parse_text(self):
        runes = {
                '!': '<h1>{line}</h1>',
                '?': '<h2>{line}</h2>',
                '&': '<p>{line}</p>',
                '%': '<h3 class="kbQuote">{line}</h3>',
                '>': '{line}',
                ':': '<img src="{line}">',
                '—': '<hr/>',
                '-': '<li>{line}</li>',
                '=': '<li>{line}</li>',
                '$': None,
                '¢': None,
                '*': '<script type="text/javascript" src="/scripts/{line}.js"></script>'
                }
        runes_text = ['!', '?', '&', '%', '-', '=']
        runes_media = [':', '>', '*']
        runes_misc = ['—']
        runes_dynamic = ['$', '¢']
        inlines = {
                'link-local': '<a href="/{target_url}" class="kbAnchorLocal">{target_name}</a>',
                'link-broken': '<span class="kbAnchorBroken">{target_name}</span>',
                'link-external': '<a href="{target_url}" class="kbAnchorExternal">{target_name}</a>',
                'pre': '<span class="kbPreformattedInline">{contents}</span>',
                'italic': ' <em>{contents}</em> ',
                'smcp': ' <span class="kbSmcp">{contents}</span> ',
                'bold': ' <strong>{contents}</strong> '
        }
        multilines = {
                '-': {
                    'open': '<ul class="kbListUnordered">',
                    'close': '</ul>'
                },
                '=': {
                    'open': '<ol class="kbListOrdered">',
                    'close': '</ol>'
                },
                '>': {
                    'open': '<pre class="kbPreformatted">',
                    'close': '</pre>'
                }
        }

        assembly = []
        multiline = ''

        for line in self.body.splitlines():
            rune = line[0]
            line_content = line[2:] if rune in runes else line

            if multiline in multilines and multiline != rune:
                assembly.append(multilines[multiline]['close'])
                multiline = ''

            if multiline == '' and rune in multilines:
                multiline = rune
                assembly.append(multilines[multiline]['open'])

            if rune in runes_media:
                assembly.append(runes[rune].format(line=line_content))
            elif rune in runes_misc:
                assembly.append(runes[rune])
            elif rune in runes_dynamic:
                # Category list
                if rune == '$':
                    assembly.append('<ul class="kbListCategory">')
                    category_parent = line_content.lower().replace(' ', '-')
                    if category_parent in inventory:
                        if inventory[category_parent].over:
                            for child in inventory[category_parent].over:
                                target_url = child
                                target_name = inventory[child].name
                                assembly.append(
                                    '<li><a href="/{target_url}">{target_name}</a></li>'.format(
                                        target_url=target_url,
                                        target_name=target_name
                                        )
                                    )
                    assembly.append('</ul>')
                # Category list with thumbnails
                elif rune == '¢':
                    category_parent = line_content.lower().replace(' ', '-')
                    if category_parent in inventory:
                        if inventory[category_parent].over:
                            assembly.append('<ul class="kbListCategoryIcons">')
                            for child in inventory[category_parent].over:
                                target_icon = inventory[child].icon
                                if target_icon:
                                    target_url = child
                                    target_name = inventory[child].name
                                    assembly.append(
                                        '<li style="background-image:url(\'{target_icon}\');"><a href="/{target_url}">{target_name}</a></li>'.format(
                                            target_icon=target_icon,
                                            target_url=target_url,
                                            target_name=target_name
                                            )
                                        )
                            assembly.append('</ul>')
            elif rune in runes_text:
                format_regex = {
                    'link-local': re.compile(r'(\[\[)(.+?)(\]\])'),
                    'link': re.compile(r'(\[)(.[^\[]+?)(\))'),
                    'pre': re.compile(r'(`)(.+?)(`)'),
                    'italic': re.compile(r'([ (]_)(.+?)(_[) ])'),
                    'smcp': re.compile(r'([ (]\~)(.+?)(\~[) ])'),
                    'bold': re.compile(r'([ (]\*)(.+?)(\*[) ])')
                }

                if line_content == "":
                    line_content = "&nbsp;"

                # TODO: proper format
                for hits in re.findall(format_regex['link-local'], line):
                    match_substr = ''.join(hits)
                    target_name = hits[1]
                    target_url = target_name.lower()
                    if target_url in inventory:
                        line_content = line_content.replace(
                            match_substr, inlines['link-local'].format(
                                target_url=target_url,
                                target_name=target_name
                                )
                            )
                    else:
                        line_content = line_content.replace(
                            match_substr, inlines['link-broken'].format(
                                target_name=target_name
                                )
                            )

                for hits in re.findall(format_regex['link'], line):
                    match_substr = ''.join(hits)
                    if '](' in hits[1]:
                        target_name, target_url = hits[1].split('](')
                        line_content = line_content.replace(
                            match_substr, inlines['link-external'].format(
                                target_url=target_url,
                                target_name=target_name
                                )
                            )
                    elif ']|(' in hits[1]:
                        target_name, target_url = hits[1].split(']|(')
                        line_content = line_content.replace(
                            match_substr, inlines['link-local'].format(
                                target_url=target_url.lower().replace(' ', '-'),
                                target_name=target_name
                                )
                            )

                for hits in re.findall(format_regex['pre'], line):
                    match_substr = ''.join(hits)
                    contents = hits[1]
                    line_content = line_content.replace(
                        match_substr, inlines['pre'].format(
                            contents=contents
                            )
                        )

                for hits in re.findall(format_regex['italic'], line):
                    match_substr = ''.join(hits)
                    contents = hits[1]
                    line_content = line_content.replace(
                        match_substr, inlines['italic'].format(
                            contents=contents
                            )
                        )

                for hits in re.findall(format_regex['smcp'], line):
                    match_substr = ''.join(hits)
                    contents = hits[1]
                    line_content = line_content.replace(
                        match_substr, inlines['smcp'].format(
                            contents=contents
                            )
                        )

                for hits in re.findall(format_regex['bold'], line):
                    match_substr = ''.join(hits)
                    contents = hits[1]
                    line_content = line_content.replace(
                        match_substr, inlines['bold'].format(
                            contents=contents
                            )
                        )

                assembly.append(runes[rune].format(line=line_content))
            else:
                assembly.append(line_content)

        # Close multiline if last element
        if multiline != '':
            if multiline in multilines:
                assembly.append(multilines[multiline]['close'])

        return '\n'.join(assembly)

    def make_breadcrumb(self):
        if self.unde:
            breadcrumb = '<div class="kbBreadcrumb">'
            lineage = [self.name_url]
            while 'index' not in lineage:
                # Check next parent isn't already in lineage to avoid recursion
                if inventory[lineage[-1]].unde is not None and inventory[lineage[-1]].unde not in lineage:
                    lineage.append(inventory[lineage[-1]].unde)
                else:
                    lineage.append('index')
            for generation in reversed(lineage):
                breadcrumb += '<a href="' + generation + '">' + inventory[generation].name + '</a> / '
            breadcrumb = breadcrumb[:-3] + '</div>'
        elif self.name_url == 'index':
            breadcrumb = '<div class="kbBreadcrumb kbBreadcrumbIndex"><a href="/">Index</a></div>'
        else:
            breadcrumb = '<div class="kbBreadcrumb"><a href="/">Index</a> / <a href="' + self.name_url + '">' + self.name + '</a></div>'
        return breadcrumb



# Populate inventory from lexicon
with open(lexicon, 'r') as f:
    lexicon_pages = f.read().split('\n\n')
for page in lexicon_pages:
    if 'BODY:\n' in page:
        page_headers, page_body = page.split('\nBODY:\n')
        page_name = ''
        page_icon = None
        page_banr = None
        page_unde = 'index'
        for idx, line in enumerate(page_headers.splitlines()):
            if idx is 0:
                page_name = line
            else:
                if line[:5] == 'UNDE:':
                    page_unde = line[5:].lower()[1:].replace(' ', '-')
                elif line[:5] == 'ICON:':
                    page_icon = line[6:]
                elif line[:5] == 'BANR:':
                    page_banr = line[6:]
        if page_unde.lower() == 'none':
            page_unde = None
        page_object = Page(inventory, page_name, body=page_body, unde=page_unde, icon=page_icon, banr=page_banr)
    else:
        print('KEELBACK: Page ' + str(page.splitlines()[0]) + ' is missing its BODY definition and has been skipped.')

# Assign overs to pages
for page in inventory.values():
    if page.unde:
        if page.unde in inventory:
            inventory[page.unde].over.append(page.name_url)

# Serve page
def serve(slug):
    slug = slug.lower()[1:].replace(' ', '-')
    slug = 'index' if slug == '' else slug

    if slug in inventory:
        if inventory[slug].banr:
            return inventory[slug].assemble(template_banner)
        else:
            return inventory[slug].assemble(template_default)
    else:
        print('KEELBACK: 404 encountered while trying to access page: ' + str(slug))
        return inventory['404'].assemble(template_default)
