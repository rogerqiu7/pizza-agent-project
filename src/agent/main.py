#from agent.providers.openai import agent
from agent.providers.bedrock import agent as bedrock_agent

question = "What's the weather in San Francisco? and whats the best pizza flavors and why"

def main() -> None:
    result = bedrock_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()