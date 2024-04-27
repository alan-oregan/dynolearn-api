import json
import azure.functions as func
import logging

from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

hub = HuggingFaceEndpoint(repo_id="NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO")

tasks_template = """<|im_start|>system
You are a helpful designer for a childrens digital game company<|im_end|>
<|im_start|>user
{name} is {age} years old and has a reading level age of {reading_level}. They need help with {teaching_task}.

Make a list of 10 suitable game scene tasks to learn {teaching_task}.

Just list out each item 1 by 1 as a JSON list. Only provide the list of tasks, do not include the question or any other information, just the list of tasks.<|im_end|>
<|im_start|>assistant
"""

tasks_prompt = PromptTemplate(
    template=tasks_template,
    input_variables=["name", "age", "reading_level", "teaching_task"],
)


class Tasks(BaseModel):
    tasks: List = Field(description="list of game scene tasks")


parser = JsonOutputParser(pydantic_object=Tasks)

tasks_prompt_json = PromptTemplate(
    template=tasks_template,
    input_variables=["name", "age", "reading_level", "teaching_task"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

tasks_chain = tasks_prompt_json | hub | parser


@app.route(route="generateTasks")
def generateTasks(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("generateTasks function processed a request.")

    try:
        req_body = req.get_json()
        name = req_body.get("name")
        age = req_body.get("age")
        reading_level = req_body.get("reading_level")
        teaching_task = req_body.get("teaching_task")
    except ValueError:
        pass

    if name and age and reading_level and teaching_task:
        return func.HttpResponse(
            json.dumps(
                tasks_chain.invoke(
                    {
                        "name": name,
                        "age": age,
                        "reading_level": reading_level,
                        "teaching_task": teaching_task,
                    }
                )
            ),
            status_code=200,
            mimetype="application/json",
        )

    return func.HttpResponse(
        "Pass {name, age, reading_level, teaching_task} in the request body for generated tasks.",
        status_code=200,
    )
