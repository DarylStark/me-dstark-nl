import events.EventRetrieverTivoliVredenburg

a = events.EventRetrieverTivoliVredenburg()
e = a.retrieve_events()

for x in e:
    print(x.title)
