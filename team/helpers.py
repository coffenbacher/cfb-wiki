import logging, json
from importio import importio, latch
import os
log = logging.getLogger()


def sync_queries(queries):
    io = importio.importio(user_id=os.getenv('IMPORTIO_USER_ID'), 
            api_key=os.getenv('IMPORTIO_API_KEY'))
    io.connect()
    queryLatch = latch.latch(len(queries))
    dataRows = []

    # In order to receive the data from the queries we issue, we need to define a callback method
    # This method will receive each message that comes back from the queries, and we can take that
    # data and store it for use in our app
    def callback(query, message):
        log.debug("QueryLatch: %s" % queryLatch)
        
        # Disconnect messages happen if we disconnect the client library while a query is in progress
        if message["type"] == "DISCONNECT":
            log.error("Query in progress when library disconnected")
            log.error(json.dumps(message["data"], indent = 4))
        
        # Check the message we receive actually has some data in it
        if message["type"] == "MESSAGE":
            if "errorType" in message["data"]:
                # In this case, we received a message, but it was an error from the external service
                log.error("Got an error!")
                log.error(json.dumps(message["data"], indent = 4))
            else:
                # We got a message and it was not an error, so we can process the data
                log.debug("Got data!")
                log.debug(json.dumps(message["data"], indent = 4))
                dataRows.extend(message["data"]["results"])
                log.debug(dataRows)
    
        # When the query is finished, countdown the latch so the program can continue when everything is done
        if query.finished(): queryLatch.countdown()
    
    for q in queries:
        io.query(q, callback)
    queryLatch.await()
    return dataRows
    