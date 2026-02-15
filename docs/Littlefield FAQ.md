# FAQ for Littlefield Simulation

### 1. At the time when our simulation starts, do we still have the original equipment configuration, i.e. 3 stuffers, 2 testers, and 1 tuner?

Yes, everything stays the same. The simulation has already started and paused at day 50.

### 2. How soon do new machines go online?

Immediately.

### 3. Is inventory paid for when it is ordered, or when it is received?

When it is ordered.

### 4. How long do the stations run each day?

The stations run continuously — 24 hours per day.

### 5. Can we edit parameters before the system opens?

You cannot change anything until the system opens.

### 6. Will the choice of contract affect the number of orders coming in? (i.e., is there any elasticity in demand?)

Demand is perfectly inelastic — the choice of contract will have no impact on the number of orders arriving or leaving the plant.

### 7. How should we treat Station 2, since all jobs have to pass through it twice? Should we consider it as two separate stations?

It is not helpful to think of the second time through as a separate station since it is not. The only difference between station 2 and the other stations is that jobs go through twice. There is an average service time for the first test and an average service time for the second test. The average service time at station 2 is the average of two. It is not necessary to find the average for the first test and the average for the second test separately.

### 8. If the current inventory is below the reorder point, will it reorder or does it only reorder when hitting the exact reorder point?

Yes it will reorder at any point below the reorder point (providing you have enough money and there is no outstanding order).

### 9. If we set the reorder quantity to zero, will we still be charged for a reorder when the inventory falls below the reorder point?

No, a reorder will not be placed so long as the reorder quantity is set to zero.

### 10. Are we expected to sell off the machines or will they automatically be counted for $10K each at the end of the simulation?

Machines will not be sold automatically. You lose control on day 385 and the factory will run by itself until day 485. You can only sell machines up to day 385 (but then there won't be machines to run for extra 100 days). You'll have to compare your savings with lost profit.

### 11. During the period from day 386 to day 485 when we've lost the ability to change anything, the simulation will still continue to re-order inventory based on our re-order quantity and point, correct?

Customer demand arrives at random intervals, but the long-run average demand will not change over the product's 485-day lifetime. At the end of this lifetime, demand will end abruptly and factory operations will be terminated. At this point, all capacity and remaining inventory will be useless, and thus have no value. That means demands keep coming. You need to forecast the demand and manage your inventory. But the demand will stop immediately after day 485, so pay attention to that to set up the inventory reorder point and quantity.

### 12. How is the final rank calculated?

Your final rank is calculated as operating cash minus debt. You can't win the game just by borrowing money. Also, paying off debt will not change your rank. However, it reduces the daily interest expense from financing (and hence it can potentially impact your rank in the long-term).

### 13. How is interest on loans and cash treated?

Interest is calculated and accrued daily, so you will see increases in both your operating cash and your debt daily due to accrued interest.

### 14. Regarding the scheduling policies: are there different scheduling policies for each station or are they all FIFO?

During simulation you may change the scheduling policy only at the Testing Station. In other stations, the scheduling rule is set to FIFO. At the Testing Station, you will be given three options:
1. FIFO
2. Priority to Step 2
3. Priority to Step 4

### 15. Is it possible to change contract offerings by revising the quoted lead-time requirements on certain contracts?

You will be given three options: Contract 1, Contract 2, and Contract 3. Each contract comes with distinct quoted lead time. You cannot revise a quoted lead time of a given contract. The only way you can switch to a different quoted lead time (for future orders) is via choosing one of the three contracts.

### 16. For each of the lateness penalties, is it done through a straight line depreciation (fractional) or is it done by larger time increments?

It's linear from the quoted lead time to maximum lead time. Fraction is allowed, so you can calculate according to a straight line depreciation.

### 17. There are 40 orders undelivered at the end of day 50. If I choose to enter a new contract term, will the prices for those orders change accordingly?

From the Overview document: "A contract is assigned to an order as soon as it arrives at the factory, and that contract cannot be changed afterward for that order."

So even though these orders are undelivered, they have already been assigned the original contract term. Changing the contract term will only affect orders that arrive at the factory (regardless of whether there is inventory to actually process these orders) from that point onwards.

### 18. Equipment purchase is blocked — "cash balance resulting from purchase would be insufficient to pay for a single order of kits." What is happening?

The simulation only allows you to buy machines if it does not prevent you from buying raw material in the future. Hence, the simulation helps you by ensuring that you can continue to produce and to serve your customers after you ordered the new machine. However, the simulation bases the estimated cash needed for raw material purchases on the reorder point and reorder quantity currently set by you. Hence, you may experiment (carefully) with adjusting reorder point and reorder quantity.

### 19. Can we set the price to be different for different orders?

You can change the contract price (750, 1000, or 1250) at any time, and the change will affect all future orders from the time you change it until you change it again. Orders still in the system will be paid at whichever contract rate was in effect when they were received, so if you want to have one price for X orders then switch to another price you'd have to predict/estimate that and change it at the appropriate time.

### 20. What happens if I run out of inventory before the end and never reorder, but there are contracts that never got fulfilled?

You won't receive payment for any unfulfilled contracts, but there also wouldn't be any penalty. So without any inventory you would just stop making money until the simulation ends.

### 21. What does splitting an order into lots do mechanically? What would be the benefits?

The factory receives (input) jobs in the form of orders (each order of 60 receivers), while the actual processing on a machine happens in the form of lots. If you don't split the order then the lot and order can be treated as the same. However, if you split an order into 2/3/5 lots then it allows you to process the same order in parallel depending on how many machines you have. This helps you to process an order faster at a particular station.

From the Overview document: "Hence splitting an order into lots would increase the fraction of time each stuffer and the tester spends on setups."

The other thing to remember is that the flow from one station to another is also in the form of lots. So if you split the order into, let's say 2 lots, then after the first lot of 30 is processed at Station 1, it will move to Station 2 while the 2nd lot of the same order will still be at Station 1. Compare that to no splitting — all the processed orders at Station 1 will wait until all 60 are processed.
