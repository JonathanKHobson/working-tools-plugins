# Editing patterns

Read this reference when prose feels inflated, repetitive, generic, or recognizably model-shaped. Diagnose what the passage is trying to do before changing its surface style.

Every “after” example may use only facts available in its paired “before” example. Follow the same rule in real edits. If vague prose hides a missing fact, preserve bounded uncertainty, ask for the fact when it blocks the task, or delete the unsupported claim. Never invent a concrete detail to make a rewrite sound better.

## Delayed answer

Before:

> That's a great question. There are several important considerations to keep in mind. This approach batches updates, so it fits teams that can tolerate a delay, but it cannot support real-time alerts.

After:

> This approach fits teams that can tolerate delayed updates. It is a poor fit for real-time alerts.

The repair removes praise and names the decision boundary. Keep an acknowledgment when the social situation genuinely calls for one.

## Visible structure announced twice

Before:

> Here's a comprehensive breakdown of the three options:
>
> ## Local storage

After:

> ## Local storage

The heading already exposes the structure. Do not narrate formatting that readers can see.

## Section inflation

Before:

> ## Key takeaway
>
> Use the smaller instance for development.
>
> ## Why this matters
>
> It costs less and is large enough for development traffic.

After:

> Use the smaller instance for development. It costs less and is large enough for development traffic.

Keep headings when they provide navigation across distinct topics, not when they separate a claim from its reason.

## Decorative list

Before:

> The change is:
>
> - Small.
> - Safe.
> - Easy to reverse.

After:

> The change is small, low risk, and easy to reverse.

A list helps when items are steps, options, criteria, or independently scannable facts. It is not a default sentence layout.

## Slogan-like contrast

Before:

> This logging update adds request IDs and structured error fields. It isn't just another logging change—it's a fundamental shift in how the organization thinks about observability because it makes failures easier to trace across services.

After:

> The update adds request IDs and structured error fields, which makes failures easier to trace across services.

Replace inflated framing with the specific change and consequence. Keep a contrast when both sides are true and the distinction matters.

## Empty adjectives

Before:

> The platform provides a robust, seamless, and powerful upload workflow. It retries failed uploads and resumes them after a lost connection.

After:

> The platform retries failed uploads and resumes them after a lost connection.

Ask what observable behavior the adjective stands for. If no fact supports it, delete it.

## Vague caution

Before:

> It is important to note that if two workers update the same record, the later write could potentially overwrite the earlier one.

After:

> If two workers update the same record, the later write can overwrite the earlier one.

Name the condition and failure. Preserve uncertainty when the evidence is uncertain, but say what is uncertain and why.

## Disclaimer fog

Before:

> This may vary depending on a number of factors. The limit is 10 requests per second in version 3, but earlier versions use a different limit, so it is always a good idea to consult the relevant documentation for your situation.

After:

> The limit is 10 requests per second in version 3. Earlier versions use a different limit.

Replace generic caution with the factor that changes the answer. If that factor is unknown, ask for it or state the bounded uncertainty.

## Repeated conclusion

Before:

> Producers must continue during short consumer outages, so the recommended approach is to use a queue. In summary, a queue is the best option for this use case.

After:

> Use a queue when producers must continue during short consumer outages.

A summary earns its place in a long document when it synthesizes several sections or supports a decision. It should not restate a nearby recommendation.

## Fake quotation

Before:

> When the request type is unsupported, the system effectively says, “I don't know what to do with this request,” and then gives up.

After:

> The system rejects the request because its type is unsupported.

Use quotation marks for actual language or a deliberate, useful personification. Do not invent dialogue to make ordinary behavior seem lively.

## Formulaic recommendation

Before:

> The managed service meets this workload's requirements. The self-hosted option is necessary only when data residency prevents a managed deployment. Ultimately, the right choice depends on your unique needs and circumstances, and both options have their pros and cons.

After:

> Choose the managed service for this workload. Choose the self-hosted option only if data residency prevents the managed deployment.

Make the decision that the available facts support and name the condition that would reverse it. Do not hide behind symmetry.

## Flattened author voice

Before:

> The deploy script has acquired a small collection of superstitions. Touching the environment check tends to wake all of them at once.

Over-edited:

> The deploy script contains complex environment checks that can fail when modified.

Better:

> The deploy script has collected a few superstitions. Changing the environment check tends to wake them all at once.

Clarity edits can preserve rhythm, humor, and point of view. Do not turn every author into a neutral manual.

## Already-good prose

Before:

> The migration takes about 20 minutes. During that time, users can read existing records but cannot create new ones.

After:

> The migration takes about 20 minutes. During that time, users can read existing records but cannot create new ones.

The best edit can be no edit. Do not perform synonym churn to prove that the skill ran.

## Mechanical substitutions

Do not run blind replacements for passive voice, *should*, adverbs, contractions, sentence length, metaphors, or punctuation. Each can be correct in context. Edit the meaning and reading experience, then choose the grammar that serves them.
