import asyncio
from groq import Groq
from fastmcp import Client


async def query_mcp_tool(tool_name: str, params: dict):
    """
    Entry point to call MCP tools.
    :param tool_name: Name of the tool to be called
    :param params: Parameters to pass to the tool
    :return: Result returned by the tool
    """
    async with Client("http://127.0.0.1:4200/demo") as client:
        return await client.call_tool(tool_name, params)


async def chat_with_tools(user_query: str):
    """
    Main chat function with tool support:
    1. Connects to the Groq LLM service
    2. Fetches available tools from MCP and converts to OpenAI function schema
    3. Sends user query to the LLM and lets the model decide if tools should be used
    4. Executes tool calls if needed and sends results back to the LLM to get final response
    """

    # Initialize Groq LLM client
    llm_client = Groq(api_key="gsk_xxxx")

    # Get tool list dynamically from MCP
    async with Client("http://127.0.0.1:4200/demo") as mcp_client:
        tools = await mcp_client.list_tools()

        # Convert MCP tool schema to OpenAI-compatible tool format
        tool_schemas = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": tool.inputSchema.get("type", "object"),
                        "properties": {prop_name: prop_def for prop_name, prop_def in tool.inputSchema["properties"].items()},
                        "required": tool.inputSchema.get("required", []),
                    },
                },
            }
            for tool in tools
        ]

    # First call: Ask LLM to decide whether tools should be used
    response = llm_client.chat.completions.create(
        model="qwen/qwen3-32b", 
        messages=[{"role": "user", "content": user_query}], 
        tools=tool_schemas, 
        tool_choice="auto"
    )

    message = response.choices[0].message
    print(message.tool_calls)

    if message.tool_calls:
        print("Tool calls detected:")

        results = []
        for call in message.tool_calls:
            print(f"Calling tool: {call.function.name} ...")
            result = await query_mcp_tool(call.function.name, eval(call.function.arguments))
            results.append(result)
            print(f"Tool result: {result}")

        # Second call: Ask LLM to generate final reply using tool results
        final_response = llm_client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {"role": "system", "content": "The following are tool results. Please answer the user's question in natural language."},
                {"role": "user", "content": user_query},
                message,
                *[{"role": "tool", "tool_call_id": call.id, "name": call.function.name, "content": str(results[idx])} for idx, call in enumerate(message.tool_calls)],
            ],
            tool_choice="none",
        )
        print("\nFinal response:", final_response.choices[0].message.content)
    else:
        print("Direct response:", message.content)


if __name__ == "__main__":
    USER_QUERY = "查询北京天气和贵州茅台股价"

    # Run the chat function with the external user input
    asyncio.run(chat_with_tools(USER_QUERY))
