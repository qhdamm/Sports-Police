from ragas.langchain.evalchain import RagasEvaluatorChain
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_relevancy,
    context_recall,
)
from datasets import Dataset
from rag import create_prompt, generate_response

def ragas(questions, ground_truths):
    
    # Inference
    answers=[]; contexts=[]
    for query in questions:
        answers.append(rag_chain.invoke(query))
        contexts.append([docs.page_content for docs in retriever.get_relevant_documents(query)])
    
    examples = [
        {"query": q, "ground_truths": [eval_answers[i]]}
        for i, q in enumerate(eval_questions)]

    # create evaluation chains
    faithfulness_chain = RagasEvaluatorChain(metric=faithfulness)
    answer_rel_chain = RagasEvaluatorChain(metric=answer_relevancy)
    context_rel_chain = RagasEvaluatorChain(metric=context_relevancy)
    context_recall_chain = RagasEvaluatorChain(metric=context_recall)

    # evaluate the answers
    predictions = qa.batch(examples)
    f = faithfulness_chain.evaluate(examples, predictions)
    c = context_recall_chain.evaluate(examples, predictions)
    ar = answer_rel_chain.evaluate(examples, predictions)
    cr = context_rel_chain.evaluate(examples, predictions)

    

    return predictions, f, c, ar, cr

if __name__ = "__main__":
    eval_questions = [
                'How is diving scored?',
                'I think the score is too low, why?',
                'How do you feel about receiving a score of 72?'
                ]
    eval_answers = [
                "Fact: In diving competitions, a panel of seven judges submits scores for each dive. The highest two and lowest two scores are discarded, leaving three scores that are summed to determine the diver's execution score. This execution score is then multiplied by the dive's degree of difficulty to calculate the diver's total score.\
                Your opinion: This scoring system appears well-designed to minimize the impact of outlier scores, ensuring that a diver's performance is evaluated more consistently and fairly.",
                "Fact: Your entry angle deviated from the vertical by 48°, placing you in the 1st percentile. This means that 99% of other competitors had a more vertical entry. Additionally, the straightness of your body during entry deviated by 99°, which placed you in the 0th percentile, indicating a significant misalignment of your body during entry.\
                Your opinion: The substantial deviations in both entry angle and body alignment were critical factors that significantly impacted your score, leading to the lower result.",
                "Fact: The final score is calculated by multiplying the sum of the scores from three judges by the difficulty level. Based on this, the predicted final score should have been 43.2 (4.5 * 3 * 3.2).\
                Your opinion: While there might be some bias involved, it's not conclusive enough to make a definitive judgment."
                ]
    predictions, f, c, ar, cr = ragas()
    print(f"result: {predictions}")
    print(f"faithfulness score: {f}")
    print(f"context recall score: {c}")
    print(f"answer relevancy score: {ar}")
    print(f"context relevancy score: {cr}")