import hashlib
import gi
gi.require_version('Gdk', '3.0')
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

class Hash(Extension):
    def __init__(self):
        super(Hash, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        argument = (event.get_argument() or '').encode('utf-8')
        keyword = event.get_keyword()

        # Find the keyword id using the keyword (since the keyword can be changed by users)
        for kwId, kw in extension.preferences.items():
            if kw == keyword:
                keywordId = kwId

        # Show the algorithm specified as keyword, or all if the keyword was "hash"
        algos = hashlib.algorithms_guaranteed if keywordId == 'hash' else [keywordId]

        for algo in algos:
            try:
                seed = hashlib.new(algo)
                seed.update(argument)
                hash = seed.hexdigest()
                items.append(ExtensionResultItem(icon='icon.svg', name=hash, description=algo, on_enter=CopyToClipboardAction(hash), highlightable=False))
            except:
                pass

        return RenderResultListAction(items)

if __name__ == '__main__':
    Hash().run()
