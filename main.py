import hashlib
from ulauncher.api import Extension, Result
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

class Hash(Extension):
    def on_input(self, input_text, trigger_id):
        # Show the algorithm specified as keyword, or all if the keyword was "hash"
        algorithms = hashlib.algorithms_guaranteed if trigger_id == 'hash' else [trigger_id]

        for algorithm in algorithms:
            try:
                seed = hashlib.new(algorithm)
                seed.update(input_text.encode())
                hash = seed.hexdigest()
                yield Result(
                    name=hash,
                    description=algorithm,
                    on_enter=CopyToClipboardAction(hash),
                )
            except:
                pass

if __name__ == '__main__':
    Hash().run()
