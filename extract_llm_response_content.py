
from promptflow.core import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(llm_response: str) -> str:
    print(llm_response)
    return llm_response#["choices"][0]["message"]["content"]
