import requests

server = "http://localhost:5279"

channels = [
    "@rossmanngroup",
    "@cc",
    "@lbryfoundation",
    "@distrotube",
    "@luke",
    "@thelinuxgamer",
    "@lbryfoundationpodcast",
    "@lbry",
    "@odysee",
    "@dollarvigilante",
    "@upperechelongamers",
]
max_channel_length = len(max(channels, key = len))

hub_server = requests.post(server, json={"method": "status"}).json()["result"]["wallet"]["servers"][0]["host"]

results = []

page_size = 50
for channel in channels:
    page = 1
    total_time = 0.0
    result = {"channel": channel, "times": []}
    while page <= 20:
        response = requests.post(server, json={"method":"claim_search", "params":{
            "channel": channel,
            "page_size": page_size,
            "page": page,
            "no_totals": True}})
        time = response.elapsed.total_seconds()
        total_time += time
        result["times"].append(time)
        print(time)
        page += 1
        if len(response.json()["result"]["items"]) < 50:
            result["items"] = (page - 1) * page_size + len(response.json()["result"]["items"])
            break
        elif page == 20:
            result["items"] = 1000

    result["total_time"] = total_time
    results.append(result)

    print("Channel: %s" % channel)
    print("Total time %.2fs" % total_time)


total_time = sum(x["total_time"] for x in results)
total_items = sum(x["items"] for x in results)



with open(hub_server + "-" + str(round(total_time, 2)) + ".txt", 'w') as file:
    file.write(f"""Server:       {hub_server}
Channels:     {len(channels)}
Claims found: {total_items}
Total time:   {round(total_time, 2)}s
Claims/s:     {round(total_items/total_time, 2)}

""")

    for result in results:
        channel = result["channel"]
        file.write(f"""{channel}({result["items"]}):{((max_channel_length - len(channel)) + (4 - len(str(result["items"]))))* " "} {round(result["total_time"],2)}s
""")
    file.write('\n')
        
    for result in results:
        channel = result["channel"]
        file.write(f"""{channel}({result["items"]})\nTotal time: {round(result["total_time"],2)}s
""")
        for time in result["times"]:
            page = str(result["times"].index(time))
            file.write(f"""Page: {page}{(5 - len(page)) * " " } {str(round(time,2))}s
""")
        file.write('\n')



