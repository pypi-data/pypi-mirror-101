from abc import ABC
from html.parser import HTMLParser
from typing import Union

from sytk.logger import Logger
from .element import Element


class _SupParser(HTMLParser, ABC):
    def __init__(self, node: Element, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.node = node
        self._logger = Logger(self.__class__.__name__)

    def handle_starttag(self, tag, attrs):
        # generate child node
        child_node = Element(tag, attrs, self.node)
        self._logger.debug(f"created new node: {child_node}")
        # bond the child node with current node
        self.node.children.append(child_node)
        # explore child node
        self.node = child_node
        self._logger.debug(f"entered {self.node}\n")

    def handle_data(self, data):
        self.node.data = ''.join([self.node.data, data])
        self.node.text = ''.join([self.node.text, data])
        node = self.node.copy()
        while node.parent is not None:
            node = node.parent
            node.text = ''.join([node.text, data])
        self._logger.debug(f"added data {repr(data)} to {self.node}\n")

    def handle_endtag(self, tag):
        # return to parent node
        self.node = self.node.parent
        self._logger.debug(f"returned to {self.node}\n")


# An EzParser is actually a Element with a 'root' tag
class EzParser(Element):

    def __init__(self, html: Union[str, bytes], decoding: str='utf-8'):
        super().__init__('root')
        if type(html) is bytes:
            html = html.decode(decoding)
        _SupParser(self).feed(html)
