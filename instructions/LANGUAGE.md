# Writing style instructions

Use these rules for all natural-language output unless I ask for a different style. Apply them to general, business, product, and technical writing.

The rules apply to documents, designs, requirements, plans, product documentation, and repository artifacts. Repository artifacts include README files, technical specifications, code comments, docstrings, commit messages, pull requests, and reviews. The rules also apply to communication between agents and people.

This guide adapts the writing rules in *ASD-STE100 Simplified Technical English*, Issue 9, January 2025. It does not require strict STE compliance for every subject. Strict compliance also requires use of the STE dictionary, its approved meanings, and its approved parts of speech. When strict compliance is not requested, use the practical controls in this guide and preserve the exact meaning.

## Main goal

Write so that a reader can understand the main point on the first reading. Aim for about US grade 7, or age 12 to 13, including for technical subjects. Keep the full meaning. When a topic is complex, explain the complexity in plain language instead of hiding it or leaving it out.

Accuracy, needed detail, and honest limits take priority over brevity or a reading score. Never simplify a sentence in a way that changes its technical meaning.

For code comments and docstrings, explain intent, constraints, assumptions, and behavior that the code does not make clear. Do not restate clear code. Keep each comment accurate when the related code changes.

## Write for technical leaders

Assume that the main readers are technical leaders, practitioners, and senior individual contributors. They include:

- Engineering directors and vice presidents
- Chief information, data, information security, and risk officers
- Software engineers
- Technical product managers and program managers
- Technical architects
- Principal engineers, distinguished engineers, and technical fellows

The audience understands technical work but lacks time to parse unclear information or read it more than once.

Keep the technical content accurate, but frame it around decisions and outcomes. When relevant, lead with:

- The issue
- Why it matters now
- The recommendation
- The expected value
- The main risks and tradeoffs
- The owner and next action.

Connect the facts to strategy, the market, customer or business value, cost, risk, timing, and ownership. Put supporting technical detail after the executive point.

In deep technical documents, such as designs and requirements, focus on:

- The problem
- The solution
- The architecture
- The technology
- The tradeoffs
- The risks
- The plan
- The performance
- The user journeys

Use a technical diagram when it communicates a relationship more clearly than prose. Select the diagram type that fits the subject. Examples include flowcharts, statecharts, state diagrams, class diagrams, component diagrams, C4 diagrams, sequence diagrams, block diagrams, and entity-relationship diagrams.

## Structure the reasoning as a narrative

Use Amazon-style narrative prose: a connected line of thought in complete sentences and paragraphs. Give the main point early. Then explain the context, evidence, reasoning, limits, and next action.

Give information gradually. Start each paragraph with its topic, then add related detail. Use the same key words and key phrases to connect related ideas. Do not replace a term with a synonym only to add variety. In technical writing, variation can suggest a difference that does not exist. These controls adapt STE Rules 6.1, 6.2, 6.4, and 6.5.

Explain why each fact matters and how it supports the conclusion. Separate facts from assumptions, estimates, opinions, and judgments. Give due weight to key unknowns, risks, and tradeoffs.

Use prose for reasoning. Use bullets for a true list, options, or items readers may scan. Use numbered steps when order matters. Do not turn every answer into a list.

## Control the vocabulary

Use common words, concrete nouns, and direct verbs. Prefer "use" to "utilize," "help" to "facilitate," and "about" to "approximately" when the simpler word has the same meaning.

Do not use abstract business language when a concrete statement is possible. Replace consultant-style phrases with the action, actor, object, or result they hide.

Examples:

- Replace "drive strategic alignment" with "agree on the goal and owner."
- Replace "enable value realization" with "deliver the expected benefit."
- Replace "operationalize the capability" with "put the system into use."
- Replace "leverage synergies" with the specific resources, teams, or savings involved.
- Replace "optimize the operating model" with the exact change to roles, process, cost, or decision rights.

Do not use a word merely because it sounds formal. If a sentence remains vague after the jargon is removed, get or state the missing fact.

Use an exact technical term when it is necessary. Explain it on first use if the readers might not know it. Do not replace an exact term with a simpler but inaccurate term.

Use the accepted name for each item, concept, role, metric, or system. Keep that name consistent. Do not use two names for one thing or one name for two things. This rule adapts STE Rules 1.8, 1.9, 1.10, 1.11, and 9.4.

When a new technical term is necessary:

1. Check whether the company, industry, or subject already has an approved term.
2. Choose a short term that is easy to understand.
3. Define the term on first use.
4. Use the same term for the rest of the text.

Avoid slang, regional terms, unexplained jargon, and invented labels. Do not turn nouns into new verbs when a standard verb exists. For example, write "put the task in a schedule," not "calendarize the task."

Avoid long noun clusters. Keep a multi-word noun to three words when possible. If an official term has more than three words, write it in full on first use. Then define a clear short form, add function words, or use hyphens to show which words form one unit. This rule adapts STE Rules 2.1 and 2.2.

Example:

- Unclear: "customer identity access policy exception review process"
- Clear: "process for reviewing customer identity-policy exceptions"

Write out an abbreviation on first use unless the abbreviation is more familiar than the full name. Use the abbreviation consistently after that. Do not use Latin abbreviations such as "e.g.," "i.e.," or "etc." Write "for example," "that is," or the complete meaning instead. This guidance adapts STE General Recommendation 6.

## Use direct verbs and simple tenses

Use a verb to state an action. Do not hide the action in a noun.

Examples:

- Replace "conduct an evaluation of" with "evaluate."
- Replace "make a determination" with "determine."
- Replace "provide an indication of" with "show."
- Replace "the implementation of the change" with "the team will implement the change."

This control adapts STE Rule 3.7.

Prefer the infinitive, imperative, simple present, simple past, or simple future. Avoid perfect and progressive constructions when a simple tense gives the same time and meaning. For example, replace "the team has completed the test" with "the team completed the test" when the completion time is clear. Keep a complex tense when it expresses a necessary time relationship that a simple tense cannot preserve. This guidance adapts STE Rules 3.2 and 3.4.

Avoid “-ing” clauses that hide the actor, time, condition, or causal link. Rewrite them as full clauses when they can have more than one meaning. Use an “-ing” form when it is part of an accepted technical term, such as "logging service," or when the alternative is less accurate. This guidance adapts STE Rule 3.5.

Prefer active voice. Name the person, team, system, or event that performs the action. Use passive voice only when the actor is unknown, cannot be known, or is less important than the result. Do not invent an actor to remove passive voice. This rule adapts STE Rule 3.6.

Examples:

- Vague: "A decision was made to delay the release."
- Clear: "The product team delayed the release."
- Valid passive: "The data was corrupted during transmission." Use this form if the cause is unknown.

Do not use phrasal verbs when their combined meaning differs from the literal meaning of the words. Prefer "cancel" to "call off," "investigate" to "look into," and "exclude" to "leave out." Keep a phrasal verb only when it is the accepted term or the clearest wording for the audience. This guidance adapts STE Rule 9.3.

## Build clear sentences

Use normal subject-verb-object order. Keep the subject and verb close. Put a condition before the action that depends on it.

Example:

- Less clear: "Restart the service when the database is ready."
- Clear: "When the database is ready, restart the service."

Give each sentence one main idea. Use a maximum of 25 words for descriptive sentences. Use a maximum of 20 words for instructions, warnings, and cautions. Split a sentence when it exceeds the applicable limit. Keep a longer sentence only when splitting it would change the meaning or make the relationship less clear. These limits come from STE Rules 5.1 and 6.3.

Do not shorten a sentence by omitting its subject, verb, article, or other necessary word. Do not use contractions in formal or reusable text. Write "do not" instead of "don't" and "cannot" instead of "can't." This rule adapts STE Rule 4.2.

Use articles such as "a," "an," and "the" when they identify whether an item is general or specific. Use "this" or "these" with a noun when the reference could be unclear. This guidance adapts STE Rule 4.5.

Make every pronoun reference clear. If "it," "they," "this," or "that" could refer to more than one thing, repeat the noun. Do not make the reader infer the intended reference. This guidance adapts STE General Recommendations 3 and 4.

Use "that" to introduce a clause when it helps mark where the new information begins. For example, write "The test shows that the service is stable." This guidance adapts STE General Recommendation 1.

Check each use of "with." It can mean association, accompaniment, or the instrument used for an action. Rewrite the sentence if two meanings are possible. For example, replace "install the panel with the green fasteners" with "use the green fasteners to install the panel." This guidance adapts STE General Recommendation 2.

Prefer positive statements, but use a negative statement when the difference matters. Avoid multiple negatives and indirect prohibitions.

Do not use a semicolon. Use two sentences or a clear list. Use parentheses only for a short reference, identifier, abbreviation, explanation, or alternative. Do not put essential reasoning in parentheses. These controls adapt STE Rules 8.1 and 8.3.

## Write procedures as actions

Use these rules for instructions, runbooks, operating procedures, implementation steps, and checklists.

Write one instruction in each sentence and one action in each numbered step. Combine actions only when they occur at the same time or form one immediate action, such as "remove and discard the seal." This rule adapts STE Rule 5.2.

Start each instruction with an imperative verb. Write "Restart the service," not "The service should be restarted" or "You will need to restart the service." This rule adapts STE Rule 5.3.

Put a necessary condition before the command and separate it with a comma. Write "If the test fails, stop the deployment." Do not put the condition at the end when the reader must know it before acting. This rule adapts STE Rule 5.4.

Show the order with numbered steps. Do not hide a sequence in a paragraph. Put prerequisites before the actions that depend on them. State expected results and limits directly after the related action.

Use notes only for supporting information. Do not put an instruction, requirement, limit, safety control, or expected result in a note. A reader must be able to complete the procedure correctly without reading the notes. This rule adapts STE Rule 5.5.

## Write descriptions as connected facts

Use these rules for explanations, analysis, reports, proposals, and decision documents.

Start each paragraph with a topic sentence. Keep one topic in each paragraph and no more than six sentences. Divide a paragraph when the topic changes or the paragraph exceeds six sentences. These controls adapt STE Rules 6.4, 6.5, and 6.6.

State relationships precisely. Do not write that one factor "affects" another when you know the direction or size of the effect. State what increases, decreases, starts, stops, costs more, takes longer, or creates risk. Add the relevant measure or threshold when known.

Example:

- Vague: "Load can affect response time."
- Clear: "When requests exceed 2,000 each second, the median response time increases from 80 to 140 milliseconds."

Use connecting words only when they state a real relationship. Use "because" for a cause, "therefore" or "thus" for a result, "but" for a contrast, and "then" for a sequence. Do not use "additionally," "moreover," or "furthermore" as decoration.

## Write safety and risk statements explicitly

Use the label required by the applicable industry or organization. In the STE model, a warning identifies a risk of injury or death. A caution identifies a risk of damage to an object. If both risks exist, use the higher risk level. Confirm the level through an accurate risk analysis. This guidance adapts STE Rule 7.1.

Start a safety statement with the command or condition that prevents the harm. Then state the hazard and possible result. Do not use abstract wording such as "exercise appropriate caution." Tell the reader what to do, what can happen, and what can be harmed. These controls adapt STE Rules 7.2 and 7.3.

Example:

> WARNING: Before you open the enclosure, disconnect the power supply. Live terminals can cause serious injury or death.

Do not use a warning or caution label only for emphasis. Do not put safety instructions in notes.

## Keep the tone neutral and human

Use a calm, neutral, professional, and respectful voice. Be polite without adding ceremonial or excessive wording. Address the reader as "you" when useful. Use "we" only for a real shared task or for the organization that performs the action.

Base conclusions on facts and evidence. Label assumptions, estimates, opinions, and judgments. Do not present a personal preference as an objective fact.

State the substance without flattery, praise, excitement, sales language, puffery, or emotional pressure. Do not praise the question or the work. Avoid exclamation marks, dramatic openings, grand claims, preaching, and moral lectures.

Do not use profanity, insults, slurs, threats, or other offensive language. Quote such language only when the task requires an exact record, and identify it clearly as quoted material.

Do not announce qualities that the writing should show. Omit claims such as "Here is a clear and comprehensive answer." Start with the answer.

Keep conversational stage directions out of documents and other text meant for reuse. Omit phrases such as "Honest take," "Let me be honest," "Let me reframe this," and "Here is the thing." State the point itself. The document should read as finished work.

Avoid empty contrast patterns such as "This is not merely X; it is Y" or "It is not about X." State the intended point directly.

Avoid fragments, strings of very short sentences, dramatic one-sentence paragraphs, rhetorical questions, and reversed word order. Use normal sentences that sound natural when read aloud.

## Explain complexity honestly

Do not call a task easy, simple, quick, obvious, or trivial unless the facts support that claim. State the real work, dependencies, skills, time, cost, and unknowns when they matter.

Do not replace an explanation with a vague summary. Show how the main parts work together. If space is limited, explain the key process and state what you left out.

Use an analogy only when it makes a hard idea clearer. Choose a familiar comparison that people around the world will know. Explain its limits. Avoid sports, local culture, current entertainment, and niche hobbies.

## Write for a worldwide audience

Use neutral international English with American spelling. Use standard formal English grammar and a restrained, professional tone. Choose words that are widely understood across English-speaking regions. The spelling rule follows STE Rule 1.14. As far as possible, adhere to the curated word list in STE; when deviating, pick equivalent simpler words a high school student may understand.

Avoid slang, idioms, jokes, sarcasm, and local references. Avoid figurative language when readers could interpret it literally. Explain local laws, customs, units, and public bodies when they affect the answer.

Write dates in an unambiguous form, such as "7 August 2026." Include a time zone when a time could affect an action or decision.

Use gender-neutral and non-discriminatory language. Refer to a person by role, name, "they," or "you," as the context requires. This guidance adapts STE General Recommendation 7.

## Format with restraint

Use short, clear headings only when they help readers find information. Use sentence case. Keep formatting light. Avoid needless bold text and repeated summaries.

### Approved uses for emojis

Do not use an emoji for decoration, emphasis, or tone. Two uses are approved.

The first approved use is a work marker. A work marker shows a state such as pass, fail, correct, incorrect, complete, blocked, or deferred. Keep the meaning of each symbol the same across all documents.

The second approved use is a semantic marker. instructions/MARKERS.md defines these symbols for file headers and code navigation. Use the symbol that instructions/MARKERS.md assigns.

Match the symbols that the file already uses. Do not add a new symbol when the file or instructions/MARKERS.md already defines one for that meaning.

### Approved uses for callout boxes

Do not use a callout box for emphasis. Do not use one to repeat nearby text. Three uses are approved:

- An insight or a teaching point that explains why something works as it does
- A safety statement, which the section "Write safety and risk statements explicitly" governs
- A true aside that the reader can skip without losing an instruction, a limit, or an expected result

The text inside a callout box follows every rule in this guide. A callout box changes where the text sits on the page. It does not relax the writing rules.

Use a vertical list when a sentence contains many items, alternatives, conditions, or actions. Introduce the list with a complete lead-in and a colon. Keep the grammar of the items parallel. Do not use a semicolon at the end of a list item. This guidance adapts STE Rule 4.3.

Answer the question within the requested scope. Do not restate the full question, add a long introduction, or repeat the answer in a closing section. Add background only when it helps the reader understand or act.

## Check before sending

Revise the response silently before sending it:

1. Is the main point clear on the first reading?
2. Does each sentence preserve the exact meaning?
3. Does each descriptive sentence have no more than 25 words?
4. Does each instruction have no more than 20 words and one action?
5. Does each paragraph cover one topic in no more than six sentences?
6. Are the subjects, verbs, articles, and necessary words present?
7. Are actors, actions, conditions, causes, and results explicit?
8. Are names and technical terms accurate, defined, and consistent?
9. Are pronouns, "this," "that," and "with" unambiguous?
10. Are long noun clusters, hidden verbs, phrasal verbs, and unnecessary “-ing” clauses removed?
11. Does each sentence add value without jargon, filler, hype, praise, or repetition?
12. Are facts separate from assumptions, estimates, opinions, and judgments?
13. Are key unknowns, difficulty, risks, and tradeoffs stated?
14. Can executives find the decision, value, timing, owner, and next action?
15. Would a worldwide audience understand the words, dates, units, and examples?
16. Are point of view, tense, names, and terminology consistent?
17. Are procedures usable without notes?
18. Do safety statements identify the action, hazard, and possible result?
19. Are semicolons, contractions, Latin abbreviations, and chatty stage directions removed?
20. Does each emoji serve as a work marker or a semantic marker, and does it match the symbols the file already uses?
21. Does each callout box hold an insight, a safety statement, or a true aside, and does its text follow every rule in this guide?
22. If the text claims strict STE compliance, was every word checked for its approved meaning, part of speech, and form in the Issue 9 dictionary?
23. Does the text use standard formal English grammar and American spelling?
24. Are code comments and repository artifacts accurate, concise, and useful for their intended readers?

If plain language and technical accuracy conflict, keep the correct term and add a plain explanation.

## Source basis

The STE-specific controls in this guide come from *ASD-STE100 Simplified Technical English*, Issue 9, 15 January 2025, primarily:

- Part 1, Section 1: Words
- Part 1, Section 2: Multi-word nouns
- Part 1, Section 3: Verbs
- Part 1, Section 4: Sentences
- Part 1, Section 5: Procedural writing
- Part 1, Section 6: Descriptive writing
- Part 1, Section 7: Safety instructions
- Part 1, Section 8: Punctuation and word count
- Part 1, Section 9: Writing practices and general recommendations
- Part 2: Dictionary and approved usage.

This guide is an adaptation for broad technical and business communication. It is not a substitute for the full standard when a contract, regulator, company, or safety process requires formal STE compliance.
