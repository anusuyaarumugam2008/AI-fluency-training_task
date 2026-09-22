# Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent

## Scenario

The selected private-data scenario is a student attendance assistant. The assistant helps a teacher review attendance records, identify students with low attendance, and prepare a short summary. The attendance information is private data stored in a local file.

## Plain Chatbot

A plain chatbot mainly uses an LLM to generate responses. It can explain attendance concepts or describe how attendance percentages are calculated. However, it cannot automatically read the private attendance file unless the data is manually copied into the conversation.

If a teacher asks which students have low attendance, the chatbot can explain the calculation method, but it cannot identify the real students without receiving the actual attendance data. It does not normally use external tools or a multi-step loop.

The main limitation of a plain chatbot in this scenario is that it does not directly access or process the private attendance records.

## Rule-Based Workflow

A rule-based workflow follows predefined instructions and conditions. It does not use an LLM to make decisions. For example, it can read an attendance file, calculate each student's attendance percentage, and classify students below 75 percent as having low attendance.

The workflow can access private data if it has been programmed to read the file. It is predictable and repeatable for known inputs. However, it is not flexible. If the teacher asks a new question that was not included in the rules, the workflow may fail or require new programming.

## AI Agent

An AI agent combines an LLM, tools, and a loop. It understands the teacher's request, selects an appropriate tool, reads the private attendance data, processes the result, observes the output, and continues taking actions until the task is completed.

For example, an AI agent can read the attendance file, calculate attendance percentages, identify students below the required threshold, and prepare a summary. It can handle different questions more flexibly than a fixed workflow.

The agent can access private data only when it has permission and when suitable tools are provided. Its main limitation is that it may make incorrect decisions if the instructions, tools, or data are not properly controlled.

## Comparison Table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | Can answer general questions but cannot automatically access the attendance file | Limited to predefined rules | Flexible because it can interpret different requests |
| Decision-making | Generates a response using the LLM | Follows fixed if-then conditions | Reasons about the task and chooses the next action |
| Tool usage | Usually does not use tools | Uses programmed tools | Selects and uses tools such as file readers and calculators |
| Private-data access | Cannot access private data unless it is manually provided | Can access specified private files | Can access private data through authorized tools |
| Multi-step task handling | Usually handles a single request | Handles fixed steps in a fixed order | Uses an LLM, tools, and a loop |
| Automation | Low to medium | High for predictable tasks | High for flexible tasks |
| Reliability | May provide general or incorrect answers | Reliable for known inputs and rules | Powerful but requires controls and testing |

## Suitability Analysis

The AI agent is the most suitable approach for the student attendance scenario when the teacher may ask different types of questions. The agent can understand the request, access the attendance data, perform calculations, and create a useful summary.

A rule-based workflow is suitable when the task is always the same, such as calculating attendance percentages every day. It is predictable and reliable, but it is less flexible when the request changes.

A plain chatbot is suitable for general explanations, such as explaining how an attendance percentage is calculated. It is not the best choice when the assistant must access and analyze real private attendance records.

## Conclusion

A plain chatbot is most appropriate for general conversation, explanations, brainstorming, and questions that do not require private data or external tools.

A rule-based workflow is most appropriate for predictable and repetitive tasks with fixed steps and clear conditions. It is useful when consistency and reliability are more important than flexibility.

An AI agent is most appropriate for tasks that require interpretation, private-data access, tool usage, decision-making, and multiple steps. An AI agent combines an LLM, tools, and a loop to observe results and continue working until the task is completed.
