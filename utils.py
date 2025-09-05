EXIT_WORDS = {"exit", "quit", "stop", "bye", "goodbye"}

def is_exit(text: str) -> bool:
    t = text.strip().lower()
    return any(t == w or t.startswith(w) for w in EXIT_WORDS)
