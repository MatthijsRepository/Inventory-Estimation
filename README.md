# Inventory-Estimation
## Small probabilistic model of the inventory given a randomized demand.

### About the model
This model considers an organisation which distributes some good, in this case surgical supplies, to a certain number of customers. When a customer needs a good, it asks the organisation for a certain amount of supplies. The organisation relays this order to the manufacturer or in this case the company in contact with the manufacturer. The manufacturer then produces the supplies and sends them to the organisation, a process which may take multiple weeks. In this model the standard time between a request and a delivery is set to 21 days, but this can be set to any desired variable as described in the next section. This means that it takes 2 days before an order by a customer can be delivered. This delivery time can be drastically reduced if the organisation has an agreement with the manufacturer that a certain amount of surgical supplies to be delivered at regular intervals, such that when a customer places an order it can be delivered immediately, which comes at a tradeoff that the organisation has to store some surplus stock. This is the subscription model, regarding which more can be read in the report.

This model has been made to numerically determine the effect a given subscription model has on both the expected delivery time to the customers, and the surplus stock needed to be stored by the organisation. It works as follows. The user can add a customer to the model that is characterised by three variables: the customer period P, customer weight W and customer variance V. This means a customer places an order of W units of surgical equipment each P months, with a probabilistic variance of V days between orders. Specifically, this means a customer will on average order supplies each P months + or - V days, according to an N(P,V) Gaussian distribution. the amount of surgical equipment ordered, W, is to be considered as an abstraction of real-world quantities (i.e. kg, boxes, etc.).

First, the normal duration of a delivery from the manufacturer to the organisation is specified. This is the time it takes between the organisation places the order and the order is delivered. The 'normal' model assumes that the organisation places an order the moment a customer asks for supplies. Hence, the customers have to wait 21 days for delivery of their request.

Second, the customers are


### How to use this model
The model consists of a single python script and a .txt file which specifies the model parameters.


