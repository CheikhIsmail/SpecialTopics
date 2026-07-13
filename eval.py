from dataclasses import dataclass, field
from client import ask_rag

@dataclass
class TestCase:
    question: str
    expected_keywords: list[str]
    should_retrieve_from: str

@dataclass
class EvalResult:
    question: str
    answer: str
    keywords_found: list[str]
    keywords_missing: list[str]
    source_found: bool
    score: float = field(init=False)

    def __post_init__(self):
        kw_score = len(self.keywords_found) / max(1, len(self.keywords_found)+len(self.keywords_missing))
        self.score = 0.7 * kw_score + 0.3 * (1.0 if self.source_found else 0.0)

TEST_CASES = [
    TestCase("Was ist die Hauptthese?", ["Hauptthese","Argument"], "mein_dokument.txt"),
    TestCase("Welche Methoden werden beschrieben?", ["Methode","Ansatz"], "mein_dokument.txt"),
    TestCase("Telefonnummer des Autors?", ["nicht","keine","unbekannt"], ""),
]


def run_eval(test_cases):
    results = []
    for tc in test_cases:
        data   = ask_rag(tc.question, top_k=3)
        answer = data["answer"].lower()
        sources = " ".join(data["sources"]).lower()
        found   = [kw for kw in tc.expected_keywords if kw.lower() in answer]
        missing = [kw for kw in tc.expected_keywords if kw.lower() not in answer]
        src_ok  = tc.should_retrieve_from.lower() in sources if tc.should_retrieve_from else True
        results.append(EvalResult(tc.question, data["answer"], found, missing, src_ok))
    return results

def print_report(results):
    avg = sum(r.score for r in results) / len(results)
    for r in results:
        emoji = "✅" if r.score >= 0.7 else "⚠️" if r.score >= 0.4 else "❌"
        print(f"\n{emoji} [{r.score:.0%}] {r.question[:60]}")
        if r.keywords_missing: print(f"   Fehlende Keywords: {r.keywords_missing}")
    print(f"\nDurchschnitt: {avg:.0%}")

results = run_eval(TEST_CASES)
print_report(results)