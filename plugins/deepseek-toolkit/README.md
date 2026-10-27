# DeepSeek Toolkit

Run a bounded supplied-text task through NVIDIA's DeepSeek endpoint, inspect the actual returned model and completion status, and check the result against supplied evidence. The worker has no browsing, file, shell, MCP or agent tools. It submits only the text supplied on stdin.

Start with [DeepSeek operation](skills/deepseek-operation/SKILL.md). The bundled Python worker has input/output limits, makes one attempt and never retries or switches providers automatically. Optional usage recording contains metadata only and remains a recipient choice.

NVIDIA currently advertises a free developer endpoint, but access, quotas, pricing and terms can change. Verify the recipient account's current allowance before use. Package installation and `--check` do not authenticate the account or test inference. [Provider source checks](docs/provider-source-checks.json) distinguish public documentation from live access.

The toolkit does not create an account, accept terms, install OpenCode, configure a coding agent or supply credentials. A separate recipient-configured OpenCode launcher is optional; it is not installed or guaranteed by this package. Its interactive sessions are outside text-worker tracking.

Run `python3 -B -m unittest discover -s tests -v` for the mocked worker checks. They require no model calls. Code, documentation, provider names and recipient data have separate [licensing boundaries](LICENSING.md).
