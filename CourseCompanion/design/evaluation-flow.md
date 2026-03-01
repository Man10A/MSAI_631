```mermaid

flowchart LR
    T["10-question test set\n(tests-4.txt)"]
    B["Run baseline test\ncollect answers"]
    L["Label answers:\n✅ correct / ⚠ partial / ❌ unknown"]
    Tune["Adjust retrieval settings\n(e.g., top_k = 5)"]
    Rerun["Re-run same 10 questions"]
    Doc["Document final accuracy\n+ known limitations"]

    T --> B --> L --> Tune --> Rerun --> Doc

  ...