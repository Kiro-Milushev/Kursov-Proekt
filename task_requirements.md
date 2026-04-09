\# Implementation Plan: ContractClear AI

\## 1. Project Overview

This project has the main goal of evaluating the legal risk of a contract or Terms of Service (TOS) before a user signs or agrees to it. The evaluation criteria is a provided legal document and the user's designated role (e.g., Tenant, Freelancer, Consumer). The evaluator will be a Large Language Model (LLM) and the final output will be a risk score from 0 to 10 with a list of red flags and a plain English summary of the agreement.

\## 2. Tech Stack Requirements

\* \*\*Backend Framework:\*\* Python, FastAPI.

\* \*\*Frontend:\*\* HTML & Vanilla JavaScript.

\* \*\*Styling:\*\* Tailwind CSS.

\* \*\*LLM Provider:\*\* Cloudflare.

\* \*\*Target Model:\*\* \`\[BLANK / TO BE DETERMINED\]\`

\## 3. Practices to follow

\* \*\*At all times you should write pythonic code.\*\*

\* \*\*Do not have duplicate code blocks.\*\*

\* \*\*Do not have overwhelmingly large functions, only 50 lines and a single responsibility.\*\*

\* \*\*Have proper spacing inside of the different code blocks.\*\*

\* \*\*Have proper naming for each file, variable, method, etc - follow PEP-8 convention.\*\* Make sure the chosen names reflect the purpose of the given method or variable.

\* \*\*Make sure that there is no dead code inside of the project\*\* - all methods and files should have a clear purpose.

\* \*\*Be modular\*\* - make sure that each significant step of the plan is split into different files to have clean and readalbe code.

\* \*\*For sensitive data like API keys, utilize python-dotenv files to keep this information secure.\*\*

\* \*\*Do not include a comments regularly under every line, but have a well-thought docstring at the beggining of the file.\*\* They should describe the purpose of the file in the general pipeline.

\## 4. General Pipeline Structure

1\. \*\*Client Input (Frontend Phase 1):\*\* The landing page prompts the user to upload their contract/document.

\* Supported formats: \`.docx\` or \`.pdf\`.

\* Validation: If a valid file is provided, the 'Proceed' button becomes active. Otherwise, display an error message.

2\. \*\*Client Input (Frontend Phase 2):\*\* The user is transferred to a second view to paste their specific role or context (e.g., "I am the freelance graphic designer", "I am the tenant renting this apartment").

\* Validation: Minimum of 15 characters to ensure sufficient context.

\* Validation: Regex script must block URLs (e.g., checking if the string starts with \`http://\` or \`https://\`) to force pasted text, not links.

\* Action: Clicking 'Scan for Risks' triggers the request.

3\. \*\*Client Request (Frontend -> Backend):\*\* JavaScript sends an asynchronous \`POST\` request. This payload must be \`multipart/form-data\` because it contains both the contract file and the plain-text role/context.

4\. \*\*File Parsing & Validation (Backend):\*\* \* FastAPI receives the file and text.

\* The backend uses \`PyPDF2\` (or \`pdfminer.six\`) for PDFs, and \`python-docx\` for Word documents to extract raw string text from the uploaded file.

5\. \*\*Prompt Construction (Backend):\*\* The extracted contract text and the user role are injected into a strict JSON-enforcing System Prompt featuring a predefined risk scoring algorithm.

6\. \*\*LLM API Call (Backend -> Cloudflare):\*\* Direct, authenticated HTTP request to the Cloudflare LLM endpoint.

7\. \*\*Response Parsing (Backend):\*\* Parses the raw string into a Python dictionary, handles JSON format errors, and returns a clean HTTP response.

8\. \*\*UI Render (Frontend):\*\* JavaScript dynamically updates the DOM to display the Final Risk Score (0-10), a list of Red Flags (dangerous clauses), and a Plain English Summary.

\## 5. Scoring Algorithm & Prompt Engineering (Document-Agnostic)

To guarantee consistency and objectivity across any contract type (NDAs, Leases, Employment Contracts, TOS), the LLM will calculate the risk score based on a strict 10-point algorithmic rubric injected via the System Prompt.

\*\*Instructions for the AI Agent:\*\*

The agent must implement the system prompt exactly as written below. The prompt is designed to force the LLM to dynamically map the contract's clauses into four universal risk categories before scoring the document based on the user's role.

\*\*The 10-Point Universal Risk Rubric (Higher Score = Higher Risk):\*\*

\* \*\*Financial Liabilities (Max 4 points):\*\* Evaluates hidden fees, automatic renewals, penalty clauses, or unfair payment terms. +1 point for every unreasonable financial burden placed on the user.

\* \*\*Data & Privacy (Max 3 points):\*\* Evaluates rights to sell, share, or misuse user data/intellectual property. +3 if they can fully own/sell your data/IP, +1.5 if data is collected but protected, +0 if privacy is fully respected.

\* \*\*Termination & Exit (Max 2 points):\*\* Evaluates how difficult it is to cancel the agreement. +2 if it is extremely difficult, costly, or legally perilous to exit the contract, +1 for moderate friction.

\* \*\*Vagueness & Broad Language (Max 1 point):\*\* Evaluates overly broad language that heavily favors the drafter. +1 point if the language lacks specific boundaries and exposes the user to undefined scope.