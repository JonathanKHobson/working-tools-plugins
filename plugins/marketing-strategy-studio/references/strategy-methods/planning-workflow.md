## Planning Workflow

1. Build the context spine: product, buyer, problem, proof, constraints,
   channel history, and the user's tolerance for publicness, cost, and manual
   work.
2. Choose the smallest viable lane. Do not open SEO, paid ads, content,
   outreach, and community all at once unless the user explicitly needs a
   portfolio of options.
3. Convert the lane into an artifact:
   - campaign brief
   - launch packet
   - SEO refresh list
   - ad-angle matrix
   - lifecycle sequence outline
   - performance diagnosis
   - Shareables report
4. Put proof near claims. If proof is missing, turn it into a research task or
   a clearly labeled assumption.
5. Record the existing authorization or the remaining decision needed before
   an external action. Make the final payload reviewable where a hold applies.
6. Define measurement honestly: input, leading indicator, lagging indicator,
   source, denominator, and review date.

For a quick local scaffold, use the bundled no-network helper:

```bash
python3 "${MARKETING_PLUGIN_ROOT:-.}/skills/marketing-strategy-operator/scripts/marketing_strategy_scaffold.py" \
  "Product or campaign name" \
  --mode campaign \
  --audience "target reader" \
  --goal "specific outcome" \
  --channels "LinkedIn, newsletter, SEO"
```
