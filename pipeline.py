from agents import build_reader_agent,build_search_agent,writer_chain,critic_chain

#Base function

def run_research_pipline(topic:str)->dict:
    state={}
     #step 1
    #seach agent working
    # below code is only for cmd when we use this code is not usefull
    print("\n=*50")
    print("step 1 serach agent is woking")

    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages":[("user",f"Find recent, deatiled ,relaible information about:{topic}")]
    })
    state['Search_result'] = search_result['messages'][-1].content[:20000]
    print(state["Search_result"])

  #step 2 reader agent working
    print("\n" + "=" * 50)
    print("Step 2: reader agent working")

    reader_agent=build_reader_agent()
    reader_result=reader_agent.invoke({
    "messages": [
        (
            "user",
            f"""
Based on the following search result about: {topic}

Pick the most relevant URL and scrape it for deeper content.

Search result:
{state['Search_result'][:800]}
"""
        )
    ]
})

    state['scraped_content'] = reader_result['messages'][-1].content
    print(state['scraped_content'])

    #step 3 writer chain
    print("\n" + "=" * 50)
    print("Step 3: writer chain working")

    resrach_combined=(
        f"search_result:{state['Search_result']}"
        f"Deatiled_scarped_content:{state['scraped_content']}"
    )

    state['report']=writer_chain.invoke({
        "topic":topic,
        "reaserch":resrach_combined
    })
    print(state['report'])

    #step 4 critic report
    print("\n" + "=" * 50)
    print("Step 4: critic agent working")

    state['Feedback'] = critic_chain.invoke({
    "report": state['report'],
    "topic": topic
    })

    print(state['Feedback'])

    return state

if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_research_pipline(topic)
