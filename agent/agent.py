
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools.return_policy_tool import retrieve_return_policy

# Initialize LLM
llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)

# Define system prompt
system_prompt = """
You are an AI Shopping Assistant.

Your responsibilities:

1. Understand the customer's question.
2. If the question is about return policy,
   refund, exchange, or cancellation,
   use retrieve_return_policy.
3. Answer only using the retrieved policy information.
4. Never invent store policies.
5. If the information is unavailable,
   clearly tell the customer.
6. Give simple and accurate answers.
"""

# Register tools
tools = [
    retrieve_return_policy
]

# Create Agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)

# Test Agent
response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "How many days do I have to return a product?"
        }
    ]
})

print(response["messages"][-1].content)
