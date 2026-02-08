
# Introduction

In high scale web services, logging is crucial to understand what happened when an issue occurs. Metrics are important to understand where something is happening and how the service is behaving.

For example, when a customer reports that their API calls are failing, we need to understand:
- Which API is failing? One, some or all?
- How is it failing? Is it failing with any of the 5xx HTTP errors in which case it is a service error. Is it failing with any of the 4xx errors in which case it is a user error.
- How often is it failing? Are 100%, 50%, 10% or 5% of API calls failing?
- What are the correlated failures at the same time? E.g. are timeouts spiking which could be a GC pause or data fetch latency issue. 
- 