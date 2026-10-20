
# Tips & Tricks

There are a few tricks that have worked well for us in developing this library. Some of them are below.

## Workflow

When developing a new component, I find it useful to follow these steps:

1. Braindump / brainstorm.
2. Clearly write down all requirements from the braindump / brainstorm.
3. Paste the above to the coding agent along with the following prompt:

   "We are going to develop a new component. CONTENT HERE. Research, Brainstorm with me, plan, write spec into ./specs/ and then only imeplement. This is production software, so ensure that the component is fully implemented with all functionality and comprehensive tests. Make sure that the code adheres to the codebase standards outlined in your instructions."

4. Answer the interview questions that the agent asks. Be clear and specific about what you want it to do.
5. Once the spec is written, review it. I usually use `glow -l -p ./specs/filename`.
6. Once you are satisfied, ask the agent to implement.
7. Test manually. Taste is human. Iterate with the agent until all fixes are complete.

## Finishing

Always finish a session with the following instructions:

   "Update semantic markers, knowledge base files, repository indexes, conversation and status files. Then make sure all changed or new code adheres to codebase standards. Then commit and push."

## Plugins / Skills

As we understand it, *instructions* tell the agent what to do. *Skills* tell the agent how to do it. For example, we ask the agent to *plan* its work but what does that mean. The *superpowers* skills plugin tells the agent how to plan. We use the following plugins:

* frontend-design
* superpowers
* context7
* code-review
* github
* playwright
* supabase
* csharp-lsp
* pyright-lsp
* typescript-lsp

## Startup

When starting a new coding agent session, the following instructions are useful to understand what the agent thinks it's supposed to be doing:

   "Summarize your instructions in this repository."
   
   "Summarize your understanding of this repository leveraging the git log, knowledge base, conversation files, specs, codebase, etc."

## Screenshots

Most coding agents are multimodal. We often use screenshots of errors which we provide to the agent to *show* it what is wrong. Annotating screenshots also helps. Presumably, even video can help, but we haven't tried it.

## WDYT

Sometimes, a design is not obvious. For example, the `SpineMap` component is not a standard type of component or visualization as far as we know. So, we drew a picture of it in a diagramming app and outlined our thoughts on what such a component could be used to visualize. We ended the first covnersation with "wdyt about this?". That led to a multi-turn brainstorming sesison that resulted in a spec and a nice name for the component.

## Open Ended

To ready this repository for publication, we asked the agent to audit the repository. The exact instructions we used was:

   " I want you to audit everything in this repository in preparation for open sourcing it. Make sure it is ready for publishing to the entire world. Validate  copyright headers, semantic markers, knowledge base etc. Ensure all components are production ready with correct documentation and interfaces. Make sure the codebase is clean and adheres to all standards."

## Complex Reorganization

The `./cloud-icons/` folder contains a number of icons for cloud services from the three major hyperscalers. These icons were downloaded from their website. The icons are provided as an archive file containing many different sizes, formats, and naming schemes. There were over 3000+ icons. It would have been very expensive to reorganize, filter, identify, rename everything in a consistent way suitable for use with applications. Instead, we used Gemini to reorganize the icons with instructions such as:

   "Within the folder X, delete every file that does not have \_64 in its name. Then, for the remaining files, strip out \_64 and replace every _ and - character with a space. Make sure that if there are consecutive spaces to collapse into a single space. Trim leading and trailing spaces and capitalize every word. Retain the word AWS as it is since it's an acronym. Once you are done, move these files up one level and delete the containing directory." 

With multiple instructions of the above sort, a tedious, days long reorganization exercise took only about an hour.

