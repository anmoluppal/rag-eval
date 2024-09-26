from pathlib import Path

from datasets import Dataset
from dotenv import load_dotenv
from ragas import evaluate, RunConfig
from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision

from src.ground_truth import GroundTruthProvider
from src.mock_rag import MockRag


def main():
    ground_truth_provider = GroundTruthProvider(Path("./assets/ground_truth.csv"))
    rag = MockRag(Path("./assets/recipe.txt"))

    eval_dataset = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": []
    }

    for query in ground_truth_provider.get_all_questions():
        eval_dataset["question"].append(query)
        eval_dataset["answer"].append(rag.get_answer(query))
        eval_dataset["contexts"].append(rag.get_contexts(query))
        eval_dataset["ground_truth"].append(ground_truth_provider.get_ground_truth_answer(query))

    result = evaluate(
        dataset=Dataset.from_dict(eval_dataset),
        metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
        run_config=RunConfig(max_workers=1, max_retries=1)
    )

    print(result)


if __name__ == "__main__":
    load_dotenv()
    main()
