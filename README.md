# Nostr News Bot

A simple bot that will fetch articles from NPR and Reuters, randomly select one, and then publish it to the Nostr relays within the script

## Private Key Management

As written, the bot will read your nsec from a config.yaml file that should look like this:
`nsec: yourNsecHere`

Storing an nsec in plain text is probably not a great idea, so open to recommendations about how best to manage this. 


