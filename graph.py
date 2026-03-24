from langgraph.graph import StateGraph, START, END
from core import JobSearchState
from agents import scraper_agent, extractor_agent, evaluator_agent, writer_agent


workflow = StateGraph(JobSearchState)

workflow.add_node("scraper", scraper_agent)
workflow.add_node("extractor", extractor_agent)
workflow.add_node("evaluator", evaluator_agent)
workflow.add_node("writer", writer_agent)

workflow.add_edge(START, "scraper")         # 1. Start by scraping the webpage
workflow.add_edge("scraper", "extractor")   # 2. Pass raw text to the extractor
workflow.add_edge("extractor", "evaluator") # 3. Pass structured skills to the evaluator
workflow.add_edge("evaluator", "writer")    # 4. Pass the evaluation to the writer
workflow.add_edge("writer", END)            # 5. Finish the workflow and return final state

workflow_app = workflow.compile()
