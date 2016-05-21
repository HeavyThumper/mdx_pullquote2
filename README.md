# mdx_pullquote2

##PullQuote Extension for Python-Markdown

Adds generation of Pull Quotes to Python-Markdown. Pull Quotes are
text that should be highlighted within a paragraph. This extension
copies the delimited text into a span that appears prior to the
enclosing paragraph - CSS makes the rest of the magic happen for
positioning.

I started with the markdown-pullquote created by Arun Ravindran
located at:
    https://github.com/arocks/markdown-pullquote
That's why this is mdx_pullquote2.

Arun's version used inlinepattern - so it was limited in where the
pull quote could be located. My extension uses blockprocessor to
create a discrete span outside of the enclosing paragraph - so vertical
positioning can be completely controlled by CSS.

This uses the same syntax as Arun's - basic hyperlink syntax with +
as the target, e.g.:

    This can be whatever you want. And [not even a whole](+) sentence.

This will work for multiple Pull Quotes in the same paragraph - though
the CSS likely needs some tweaking for proper positioning.

This is not only my first Python-Markdown extension - it's my first
time working with Python, period. So it took a bit to get things
to where they seem to work right - and I left a bunch of comments to
help me if I need to tweak it. So there's probably some perfectly
obvious items here - but I prefer overcommenting to puzzles.

On the other hand, I'd love to hear about more elegant/efficient
methods to accomplish the same processing. By all means please
play with this as you will.

If you make use of this, I'd appreciate hearing about it. Just so
I know I'm not the only one trying to do this stuff.

Original code Copyright 2016 Daniel L. Miller

License: see LICENSE.md
