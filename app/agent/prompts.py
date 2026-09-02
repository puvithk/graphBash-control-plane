

INTEND_CLASSIFIER_PROMPT = """
Based on the user's query and the previous conversation, classify the intent of the query.

Current Query: {query}

Previous Conversation:
{memory}

Task:
Determine the user's intent from the current query and format the response as a JSON object with the following structure:


Rules:
1. If the query is a question, the intent should be a short description of what information is being requested.
2. If the query is a command, the intent should describe the action to be taken.
3. If the query seems to be related to system operations, security, or configuration, set `needs_policy_evaluation` to `true`.
4. If the query is a simple greeting or conversational, set `needs_policy_evaluation` to `false`.

Output:
Return ONLY the JSON object, without any additional text or explanation.

"""