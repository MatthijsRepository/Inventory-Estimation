import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

import numpy as np
import matplotlib.pyplot as plt

##############################################################################################################
##############################################################################################################
##############################################################################################################

def add_buyer(period, weight, deviation):
    """ Adds a buyer to the list of buyers """
    global periods, weights, deviations
    periods = np.append(periods, period*4*7)
    weights = np.append(weights, weight)
    deviations = np.append(deviations, deviation)
    pass

def calculate_best_subscription(sub_period):
    """ Calculates the expected amount of supplies required in the subscription period """
    global sub_volume
    avg_daily_volume = np.sum(weights / periods)
    
    sub_volume = int(np.round(avg_daily_volume * sub_period, decimals=1))
    pass

def calculate_orders():
    """ Defines the placement of the orders of all the buyers over the total timeperiod """
    orders = np.zeros((len(periods),days))
    for i in range(len(periods)):
        day_count = offsets[i]
        orders[i, day_count] = weights[i]
        
        while day_count < days:
            shift = np.random.normal(0, deviations[i])
            day_count += int(np.round(periods[i], decimals=0)) + int(np.round(shift,decimals=0))
            if day_count>=days:
                break
            orders[i, day_count] = weights[i]
    return orders

def calculate_stock_normal(delivery_time, orders):
    """ Given the regular model of 'relaying placed orders', calculates the surgical instruments stock of the NGO """
    stock = np.zeros(days)
    #Orders by hospitals
    out = np.cumsum(orders, axis=1)
    out_sum = np.sum(out, axis=0)
    stock = stock - out_sum
    
    incoming_order_days = np.nonzero(np.sum(orders, axis=0))
    for i in incoming_order_days[0]:
        #Add delivery at 'delivery_time' days after placing order
        stock[i+delivery_time:] += np.sum(orders[:,i])
    return stock

def calculate_stock_sub(sub_period, sub_volume, delivery_time, orders, allow_add_orders):
    """ Calculates the surgical supply stock in the case of the subscription model """
    stock = np.zeros(days)
    additional_order_count = 0
    
    #Orders by hospitals
    out = np.cumsum(orders, axis=1)
    out_sum = np.sum(out, axis=0)
    stock = stock - out_sum
    
    #Income of equipment by subscription
    for i in sub_delivery_days:
        stock[i:] += sub_volume
    
    #Stock on hand + stock that has been ordered
    phantom_stock = stock.copy()
    
    for i in range(days):
        if phantom_stock[i] < 0:
            #Calculate days until the next subscription is delivered
            next_delivery_day = sub_delivery_days[np.where((sub_delivery_days-i)>0)[0][0]]
            days_to_delivery = next_delivery_day-i
            
            #Order additional stock if time until next subscription delivery exceeds time required to place additional delivery 
            if days_to_delivery>delivery_time:
                stock[i+delivery_time:] += -1*phantom_stock[i]
                phantom_stock[i:] += -1*phantom_stock[i]
                additional_order_count += 1
            #Order additional stock if the projected medical equipment stock is lower than what a subscription normally supplies
            if phantom_stock[i]<-1*sub_volume:
                stock[i+delivery_time:] += int(np.round(-0.8 * (stock[i] + sub_volume),decimals=0)) #order twice the deficit for new buffer
                phantom_stock[i:] += int(np.round(-0.8 * (stock[i] + sub_volume),decimals=0)) #Update phantom stock such that no new order is placed the next day
                additional_order_count += 1
    return stock, additional_order_count

def calculate_stock_surplus(stock):
    """ Calculates the number of days the NGO has a surplus stock of equipment, and the average amount of surplus the NGO has to store """
    surplus = np.delete(stock, np.where(stock<=0))
    return len(surplus), np.average(surplus)
    
def calculate_wait_times(stock):
    """ Calculates the average time the NGO has to wait before an order can be delivered """
    #Calculate wait times in case of stock deficit
    in_deficit = stock<0
    wait_times = np.array([])
    count=0
    for i in range(len(in_deficit)):
        if in_deficit[i] == True:
            count += 1
        elif (in_deficit[i]==False and count>0):
            wait_times = np.append(wait_times, count)
            count = 0
    
    total_reqs = len(np.nonzero(orders)[0]) #Total number of orders placed
    
    #Count number of times requests cannot be delivered immediately
    wait_reqs = len(wait_times)
    immediate_reqs = total_reqs - wait_reqs
    
    #calculate the fraction of requests that can be delivered immediately
    fraction = immediate_reqs/total_reqs
    wait_times_total = np.append(wait_times, np.zeros(immediate_reqs))
    return wait_times, wait_times_total, fraction

##############################################################################################################
##############################################################################################################
##############################################################################################################

def parse_value(key, value):
    if key in ['simulation_time', 'num_simulations', 'delivery_time', 'sub_period']:
        return int(value)
    elif key in ['plot_results']:
        return value.lower() == 'true'
    elif key in ['periods', 'weights', 'deviations']:
        return np.array(list(map(float, value.split(','))))
    else:
        return value
    
def read_variables_from_file(filename):
    variables = {}
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            # Remove whitespace and split by the first colon
            key, value = map(str.strip, line.split(':', 1))
            variables[key] = parse_value(key, value)
    
    return variables

filename = 'simulation_variables.txt'
variables = read_variables_from_file(filename)

simulation_time = variables['simulation_time']
num_simulations = variables['num_simulations']
periods = variables['periods']
periods *= 30 #Convert periods to months
weights = variables['weights']
deviations = variables['deviations']
delivery_time = variables['delivery_time']
sub_period = variables['sub_period']
plot_results = variables['plot_results']    


if (len(periods)!= len(weights) or len(periods) != len(deviations)):
    print("Periods, Weigths and Deviations do not have the same length, please check.")
    print(f"Length of periods: {len(periods)}")
    print(f"Length of weights: {len(weights)}")
    print(f"Length of deviations: {len(deviations)}")
    print()



"""
print("simulation_time:", simulation_time)
print("num_simulations:", num_simulations)
print("periods:", periods)
print("weights:", weights)
print("deviations:", deviations)
print("delivery_time:", delivery_time)
print("sub_period:", sub_period)
print("plot_results:", plot_results)
"""



days = simulation_time * num_simulations
padding_days = 2*sub_period #Padding in future
offsets         = np.random.randint(0,120,len(periods))  #time from day 0 to first request
sub_delivery_days = np.arange(0,days + padding_days, sub_period)
allow_additional_orders = True  #Allow the NGO to place additional orders


calculate_best_subscription(sub_period)
orders = calculate_orders()
stock_sub, additional_order_count = calculate_stock_sub(sub_period, sub_volume, delivery_time, orders, allow_additional_orders)
stock_normal = calculate_stock_normal(delivery_time, orders)
days_with_surplus, average_surplus = calculate_stock_surplus(stock_sub)
wait_times, wait_times_total, fraction = calculate_wait_times(stock_sub)




print(f"Subscription volume of :                                                    {sub_volume} units each {sub_period} days")
print(f"Average wait time for delivery with subscription:                           {np.round(np.average(wait_times_total),decimals=1)} days")
print(f"Average wait time for delivery with subscription if no stock is on-hand:    {np.round(np.average(wait_times), decimals=1)} days")
print(f"Total percentage of deliveries that can be delivered immediately:           {np.round(fraction*100,decimals=0)}%")
print(f"Fraction of days NGO has surplus stock:                                     {np.round(days_with_surplus/days *10,decimals=2)} out of 10 days")
print(f"Average surplus stock NGO has:                                              {np.round(average_surplus, decimals=3)} units")
#if allow_additional_orders:
#    print(f"Additional orders placed: {additional_order_count}")
print()
print(f"Wait time between deliveries using normal method:                           {delivery_time} days")



def plot_requests():
    for i in range(len(periods)):
        plt.plot(orders[i, simulation_time:2*simulation_time])
    
    plt.xlim(0, simulation_time)
    
    plt.xlabel("Days")
    plt.ylabel("Relative volume of requested equipment")
    plt.show()
    pass

def plot_stock():
    plt.figure(dpi=200)
    plt.plot(np.arange(0,simulation_time), stock_normal[simulation_time:2*simulation_time], label="Normal")
    
    plt.plot(np.arange(0,simulation_time), stock_sub[simulation_time:2*simulation_time], label="Subscription")
    
    #plt.xlim(0,len(stock_normal))
    plt.xlim(0,simulation_time)
    plt.hlines(0,0,simulation_time, color="grey",linewidth=0.5)
    
    plt.xlabel("Days")
    plt.ylabel("Stock")
    plt.legend()
    plt.show()
    pass

if plot_results:
    plot_requests()
    plot_stock()        
    pass