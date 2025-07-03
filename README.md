# 🤖 Tool-Enhanced Chat with Groq and FastMCP

This project demonstrates how to integrate a local tool service (`FastMCP`) with Groq's OpenAI-compatible LLM API (e.g., `qwen/qwen3-32b`) for dynamic function calling. The LLM can interpret user intent, automatically call tools, and respond with a natural language answer.

---

## 📂 Project Structure

```
.
├── server.py       # Tool server (weather and stock) using FastMCP
├── client.py       # Chat client that connects to Groq + FastMCP
├── README.md       # This documentation
```

---

## ✅ Features

- Register tools using `FastMCP` (`weather`, `stock`)
- Use Groq LLM (e.g., Qwen model) to interpret user queries
- Let the LLM decide when to call tools using OpenAI's function-calling schema
- Forward tool results back to LLM for final, natural-language answers

---

## 📦 Requirements

- Python 3.8+
- Install dependencies:

```
pip install groq fastmcp
```

---

## 🚀 Running the Tool Server

The tool server provides two mock tools:

- `weather(city: str)` – Returns static weather info
- `stock(code: str)` – Returns static stock price info

To start the server:

```
python server.py
```

> This launches the FastMCP server at `http://127.0.0.1:4200/demo`

---

## 💬 Running the Chat Client

The chat client will:

1. Connect to the MCP server and load tool schemas
2. Send a user query to Groq's LLM
3. Let the model decide if tools should be invoked
4. Use returned tool results to generate the final reply

To start the client:

```
python client.py
```

You can change the user query by modifying the `USER_QUERY` variable at the bottom of `client.py`.

Example:

```python
USER_QUERY = "查询北京天气和贵州茅台股价"
```

---

## 🧪 Sample Output

```
Tool calls detected:
Calling tool: weather ...
Tool result: {'temp': 25, 'condition': 'Sunny'}
Calling tool: stock ...
Tool result: {'name': '贵州茅台', 'price': 1825.0'}

Final response: 北京当前天气晴，气温25度。贵州茅台当前股价为1825.0元。
```

---

## 🛠 Notes

- Ensure `server.py` is running **before** launching `client.py`
- The tools return mock data; you can replace them with real APIs
- Groq must be accessible and requires a valid `api_key` set in `client.py`
- This project uses synchronous Groq API (as async is not yet supported)

---

## 📄 License

MIT License. Free to use for personal and commercial projects.
