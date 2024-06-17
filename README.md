# Inventory-Estimation
## Small probabilistic model of the inventory given a randomized demand.

### About the model
This model considers an organisation which distributes some good, in this case surgical supplies, to a certain number of customers. When a customer needs a good, it asks the organisation for a certain amount of supplies. The organisation relays this order to the manufacturer or in this case the company in contact with the manufacturer. The manufacturer then produces the supplies and sends them to the organisation, a process which may take multiple weeks. In this model the standard time between a request and a delivery is set to 21 days, but this can be set to any desired variable as described in the next section. This means that it takes 2 days before an order by a customer can be delivered. This delivery time can be drastically reduced if the organisation has an agreement with the manufacturer that a certain amount of surgical supplies to be delivered at regular intervals, such that when a customer places an order it can be delivered immediately, which comes at a tradeoff that the organisation has to store some surplus stock. This is the subscription model, regarding which more can be read in the report.

This model has been made to numerically determine the effect a given subscription model has on both the expected delivery time to the customers, and the surplus stock needed to be stored by the organisation. It works as follows. The user can add a customer to the model that is characterised by three variables: the customer period P, customer weight W and customer variance V. This means a customer places an order of W units of surgical equipment each P months, with a probabilistic variance of V days between orders. Specifically, this means a customer will on average order supplies each P months + or - V days, according to an N(P,V) Gaussian distribution. the amount of surgical equipment ordered, W, is to be considered as an abstraction of real-world quantities (i.e. kg, boxes, etc.). There is no limit to the amount of customers that can be added.

An important point that must be mentioned here is the fact that all months are assumed to be 30 days for code convenience and scaleability.

Next, the user specifies the amount of time that a simulation covers in days, standard is set to 4 years (1460 days). Then, using the (P, W, V) of all customers, a randomized demand is generated over the time period as follows: each customer will place its first order at a randomized point in the first 4 months, after which each P months with standard deviation of V days a new order is placed by this customer until the simulation ends. Each order is of weight W.

Given this randomized 'demand profile', the code will now calculate the differences between the 'normal' model and the 'subscription' model. The normal model assumes that the organisation places an order the moment a customer asks for supplies. Hence, the customers will always have to wait 21 days for delivery of their request.

The subscription model works as follows. The user specifies the interval at which subscription deliveries are made in days, the default is set to 30 days (1 month). The code then calculates the ideal volume of a subscription delivery. This is done by calculating the expected demand per day per customer, summing over all customers, multiplying by the delivery interval and rounding to the nearest integer value, effectively calculating the expected demand each delivery interval. Naturally, this calculation only depends on the variables (P, W, V) of all customers, and does not include the actual randomized demand profile.

After calculating subscription size, the model calculates the inventory profiles of the two methods. The inventory is the amount of supplies that the organisation has in store or that has yet to deliver on a given day. To illustrate how this works, let us assume that on a given day the organisation has a certain amount of inventory. An order is placed by a customer, which means the amount of inventory decreases. If the total inventory remains positive or goes to 0 this means the order can be delivered immediately. If the inventory goes to a negative value due to the order, it means additional supplies need to be ordered. Inventory goes up by the ordered amount after the delivery time, allowing the order to be delivered.

In the normal model, the invenotry is standard at 0 and goes below 0 upon the placement of an order. It goes up once each order has been delivered, and back to 0 if all pending orders are delivered. In the subscription model the inventory is usually standard above 0 and decreases with orders placed. If the inventory has a negative value this means an order cannot be delivered. The model then checks if it is faster to order additional supplies directly or to wait for the subscription delivery. This is especially relevant in the case there are long intervals between subscription deliveries. Also, in the case that the invenotry assumes a negative value lower than the amount a subscription will provide (that is, there total volume of pending orders is not covered by a subscription delivery) an additional order will be placed also.

This concludes the workings of the simulation. The user can specify the length of a simulation, the regular delivery time, the subscription delivery time, and the (P,W,V) values of any desired number of customers. Lastly, the number of iterations the model averages over can be specified. Standard is set to 40.

The results the model returns are of the following form.

Subscription volume of :                                                    8 units each 30 days
Average wait time for delivery with subscription:                           1.7 days
Average wait time for delivery with subscription if no stock is on-hand:    10.8 days
Total percentage of deliveries that can be delivered immediately:           84.0%
Fraction of days NGO has surplus stock:                                     7.58 out of 10 days
Average surplus stock NGO has:                                              5.609 units

Wait time between deliveries using normal method:                           21 days

Let us briefly go through this information before concluding this section. First the subscription volume and period are listed. Next, the average wait time for subscription in case the subscription model is used is listed. This is the average over all customer requests, where immediate delivery means that it takes 0 days for the request to be delivered, hence why the average can assume such low values. Next, the average delivery time of the subscription model in case the customer has to wait is listed. Naturally, sometimes the organisation will not have sufficient supplies in store to satisfy an order and has to place additional orders. However, in this situation it is likely that stock is low since the last subscription delivery has been a long time ago, and hence a new subscription delivery is coming soon. If this is the case no additional order needs to be placed and hence the waiting time is also lower than the standard order delivery time. For very long subscription intervals this benefit decreases until this time is equal to that of the normal method.

Next, the percentage of orders that can be immediately delivered is listed. Then, some information is given on the amount of surplus inventory the organisation has to store is given. Naturally, once a subscription delivery is made the NGO has to store these supplies until an order is placed by the customers. In this case, the organisation has to store 75.8% of the time (given 1000 days, the NGO has surplus inventory on 758 out of the 1000 days). Also the average amount of surplus invenotry is listed, in this case 5.609 units (for example boxes of supplies).

Lastly, the wait time for customers in the normal model is listed. This wait time is equal to the time it takes between the organisation ordering the supplies and the manufacturer delivering them.

Additionally, the user can choose to plot the demand profiles and inventory profiles of a simulation.


### How to use this model
The model consists of a single python script and a .txt file which specifies the model parameters. These two files should be stored in the same directory.

To run this model, the user needs to have python 3.6 or higher installed on their computer. Moreover, the code depends on the 'numpy' and 'matplotlib' calculation and visualisation packages. To verify installation of python, open the command line and run the command 'python --version'. If a version higher than 3.6 is printed, the code can be run. Upon running the code. If this results in error messages of the form 'ImportError', this means that the packages numpy or matplotlib are not yet installed. This can be done by returning to the command line and running the commands 'pip install numpy' and 'pip install matplotlib'. The code can now be run.

Simulation specifications are stored in the text file simulation variables.txt. This file looks as follows:

simulation_time: 1460
num_simulations: 40
periods: 2, 1.5, 4.5, 4.5, 3, 3, 4.5, 4
weights: 3, 2, 3, 2, 3, 3, 4, 5
deviations: 7, 7, 21, 18, 7, 7, 28, 7
delivery_time: 21
sub_period: 30
plot_results: True

Simulation_time specifies the length of a single simulation in days.
Num_simulations is the number of simulations the code averages over. This number should always be greater than or equal to at least 2, but it is recommended to be a higher value.
The periods, weights and deviations list contain the specifications of each customer. In this example these three lists all have a length of 8, which means there are 8 customers. The first entry in each of the lists corresponds to the first customer, the second entry to the second, et cetera.
Delivery_time specifies the regular delivery time in days between the placement of an order and the delivery by the manufacturer.
Sub_period is the specified delivery interval between subscription deliveries in days
Plot_results can assume values True or False, and decides if you want example results to be plotted or not.



