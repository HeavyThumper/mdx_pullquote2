"""
PullQuote Extension for Python-Markdown
=============================================

Adds generation of Pull Quotes to Python-Markdown. Pull Quotes are
text that should be highlighted within a paragraph. This extension
copies the delimited text into a span that appears prior to the
enclosing paragraph - CSS makes the rest of the magic happen for
positioning.

Original code Copyright 2016 Daniel L. Miller

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

from __future__ import absolute_import
from __future__ import unicode_literals
#from . import Extension
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from itertools import chain
import re


class PullQuoteProcessor(BlockProcessor):
    """ Process Pull Quotes. """

    RE_PULLQ = re.compile(r"\[([^\]]+)\]\(\+\)")
    emptystring = ''

    def test(self, parent, block):
	""" Possibly this is overkill. However, in my testing things
	    were breaking - so I'd rather defend against it. Don't know
	    why None blocks get passed...but we don't need to check them.
	    And since the RegEx pattern is a minimum of 5 chars (actually 6)
	    anything less doesn't need to be tested either """

	if (block is None) or (len(block) < 5):
#	    print 'failed test - block is either none or too short\n'
	    return False
	""" There should be an easier way to this. All the examples I've seen
	    show simple constructs like ''.join(str) - but when I try it
	    I get errors involving typeNone. Using ' '.join(str) works - which
	    isn't what we want, so I create a string variable with an empty
	    string and use that for joining. It works, even if it isn't elegant """
	line = self.emptystring.join(block)
	line = line.strip('\n')
	line = line.strip('\t')
#	print 'line is: ' + line
	return bool(self.RE_PULLQ.search(line))

    def run(self, parent, blocks):
	""" Pop the first block off the passed blocks to process.
	    This reduces the amount remaining for further processing """
        raw_block = blocks.pop(0)
#	print 'Raw Block is: ' + raw_block
        m = self.RE_PULLQ.search(raw_block)
	theStart = raw_block[:m.start()]
	theRest = raw_block[m.end():]

#	print 'The Start is: ' + theStart
	""" Things are acting weird here so do some more testing. Tired
	    of fighting Python - so we'll do some brute forcing. Odds are
	    any remaining text greater than 10 characters is relevant so
	    we'll use the without qualm. But less than 10 - worth stripping
	    whitespace to see if it's just empty and skip it. And since
	    I keep getting None, or Tuple, or various other garbage complaints,
	    we'll force type convert - shouldn't be too expensive since we're
	    dealing with less than 10 chars """

	line = str(theRest) 
#	print 'The Rest is: ' + line
#	print 'Length of The Rest is: ' + str(len(line))
	if len(str(line)) < 20:
#	    line = ''.join(line)
	    line = line.strip('\n')
	    line = line.strip('\t')
#	    print 'Length of Stripped line is: ' + str(len(line))
	    if len(line) < 1:
		theRest = False

#	print 'Raw Block is: ' + raw_block
#	print 'Length of The Rest is: ' + str(len(theRest))
#	if theRest is None or len(theRest) < 1:
#	    theRest = False
#	if theRest:
#	    emptystring = ''
#	    theRest = emptystring.join(theRest)
#	    print 'The Rest is: ' + theRest

	""" m is a MatchObject - based on the RegEx the PullQuote text
	    should be in group 1. We want to create a new span element
	    with the PullQuote - and also leave the text in place
	    (while stripping the delimeters) """
	if m:
            pqtext = m.group(1)
#	    print 'pq text: ' + pqtext
	    self.parser.state.set('pullquote')
	    pq = etree.SubElement(parent, 'span')
	    pq.text = pqtext
	    pq.attrib['class'] = 'pullquote'
#	    blocks.insert(0, pqtext)
	    """ A little counterintuitive, but - we're working with an ordered
		list of objects (blocks). We have removed the entire first block
		from the list. We now need to first put whatever came after the
		pull quote at the beginning of the list. Then place the raw pull
		quote itself before that. Then whatever was leading the pull quote
		in front of that. In other words, we're pushing into the text string
		from the beginning, shoving the remaining text over. Well, now it
		sounds perfectly obvious - but it didn't the first few times I ran this..."""
	    """ Next thing we learned - each block is it's own paragraph. Therefore we can't
		call blocks.insert for each item, instead we need to concatenate and call it
		once. Otherwise we introduce new paragraph marks that weren't intended """
	    if theRest:
		putback = theStart + pqtext + theRest
	    else:
		putback = theStart + pqtext
#	    blocks.insert(0, theRest)
#	    blocks.insert(0, pqtext)
#	    blocks.insert(0, theStart)
	    blocks.insert(0, putback)
	    self.parser.state.reset()
	else:
	    return False


class PullQuoteExtension(Extension):
    """ Add pull quotes to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of PullQuoteProcessor to BlockParser. """
        md.parser.blockprocessors.add('pullquote2',
                                      PullQuoteProcessor(md.parser),
                                      '_begin')


def makeExtension(*args, **kwargs):
    return PullQuoteExtension(*args, **kwargs)
