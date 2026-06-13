from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os 
from langgraph.graph import StateGraph
import json
load_dotenv()

llm = ChatGroq(
    model= "llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),temperature=0.7
)
def suggest_description_and_tag(state):

    allowed_tags = ["Groceries", "Coding", "Health & Fitness", "Finance", "Education", "Personal", 'Work']

    prompt = f"""
    You are an expert productivity assistant. Your job is to generate a personalized task description AND categorize the task.

    Task Title: "{state['title']}"
    Allowed Tags: {allowed_tags}

    Rules:
    1. Generate a description that is unique, practical, actionable, and between 20 to 25 words.
    2. Select exactly ONE tag from the Allowed Tags list. If unsure, select "Personal".
    3. Respond ONLY with a valid JSON object. Do not include markdown blocks, explanation, or extra text.

    Expected Output Format:
    {{
        "description": "Your 20-25 words description here.",
        "tag": "SelectedTag"
    }}
    """

    response = llm.invoke(prompt)
    
    try:
        
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        result_data = json.loads(content)
        assigned_tag = result_data.get("tag", "Personal")
        
       
        if assigned_tag not in allowed_tags:
            assigned_tag = "Personal"
            
        description = result_data.get("description", "")
        
    except Exception as e:
        
        assigned_tag = "Personal"
        description = response.content

    return {
        "title": state["title"],
        "description": description,
        "tag": f"#{assigned_tag}" 
    }


builder = StateGraph(dict)
builder.add_node("generate_metadata", suggest_description_and_tag)
builder.set_entry_point("generate_metadata")
builder.set_finish_point("generate_metadata")


graph = builder.compile()


class TaskAutomationController:
   async def process_task_automation(self, title: str) -> dict:
        
        initial_state = {"title": title}
        output = graph.invoke(initial_state)
        return output

