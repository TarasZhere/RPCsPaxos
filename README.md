# RPCsPaxos

This is an implementation mean to work on google cloud of a simple Paxos algorithm

## important implementation

during the development some important implementation were done

-   creating a simple RPC module that uses sockets and JSON to communicate
-   threading.Thread
-   Implementation of threading class with a return in Thread.join()

### Open a port to allow TCP requests

Before running Paxos in Google Cloud open a port to allow TCP:

1. Go to cloud.google.com
2. Go to my Console
3. Choose your Project
4. Choose Networking > VPC network
5. Choose "Firewall"
6. Choose "Create Firewall Rule"
7. To apply the rule to select VM instances, select Targets > "Specified target tags", and enter into "Target tags" the name of the tag. This tag will be used to apply the new firewall rule onto whichever instance you'd like. Then, make sure the instances have the network tag applied.
8. Set Source IP ranges to allow traffic from all IPs: 0.0.0.0/0
9. To allow incoming TCP connections to port 9090, in "Protocols and Ports", check “tcp” and enter 9090
10. Click Create (or click “Equivalent Command Line” to show the gcloud command to create the same rule)

# Start a server

`python server/server.py [instance number] [google cloud of IP if instance #1] [google cloud of IP if instance #2] [google cloud of IP if instance #3]`

Example:

```python
# This is an example

python server/server.py 0 0.0.0.0 0.0.0.0 0.0.0.0
```
