# Littlefield Technologies: Overview and Assignment

> Based on the instruction written by Sunil Kumar and Samuel C. Wood at the Stanford University Graduate School of Business. Copyright 1998. No part of this document may be reproduced without permission from Responsive Learning Technologies, Inc., at info@responsive.net.

## Simulation Overview

Littlefield Technologies assembles Digital Satellite System (DSS) receivers. These receivers are assembled from kits of electronic components procured from a single supplier. The assembly process consists of four steps carried out at three stations: Board Stuffing, Testing, and Tuning.

1. **Step 1** — Components are mounted onto PC boards and soldered at the **Board Stuffing station (Station 1)**.
2. **Step 2** — The digital components are briefly tested at the **Testing station (Station 2)**.
3. **Step 3** — Key components are tuned at the **Tuning station (Station 3)**.
4. **Step 4** — The boards undergo exhaustive "final testing" at the **Testing station (Station 2)** before delivery to the customer.

Every receiver passes the final test. All stations consist of automated machines that perform the operations.

### Machine Costs

You may purchase additional machines during the simulation.

| Station | Machine | Buy Price | Sell Price |
|---------|---------|-----------|------------|
| S1 | Board Stuffer | $90,000 | $10,000 |
| S2 | Tester | $80,000 | $10,000 |
| S3 | Tuner | $100,000 | $10,000 |

You can sell any machine at a retirement price of $10,000, provided at least one other machine remains at that station. Operators are paid a fixed salary, and increasing the number of machines at a station does not require additional operators.

### Orders & Lots

Customer orders arrive randomly at the factory, with each order consisting of **60 receivers**. If an order arrives and there are fewer than 60 raw kits in the materials buffer, the order is placed in the customer order queue, pending the arrival of raw kits. Additionally, **orders are not accepted if the total number of orders in the system (either waiting for kits or in process) exceeds 100**.

You may choose to release each order into the factory as:
- **1 lot of 60** receivers
- **2 lots of 30** receivers
- **3 lots of 20** receivers
- **5 lots of 12** receivers

Processing a lot on each machine entails performing a setup on the machine, processing each kit in the lot (one at a time), and then sending the completed lot to the next station. Once all the receivers in an order are completed, the order is shipped immediately. **An order is not shipped to the customer until all its lots have been completed.**

Management has resisted splitting a customer order of 60 receivers into multiple manufacturing lots in the past because each lot requires setup time at both the stuffer and the tester. Thus, splitting an order into lots would increase the fraction of time each stuffer and tester spends on setups.

### Raw Materials & Inventory

- Raw kits cost **$10 per kit**
- Fixed cost of **$1,000 per shipment**, regardless of shipment size
- Supplier requires **4 days** to deliver any quantity of raw kits
- Kits are purchased in multiples of 60

An order for new raw kits is placed with the supplier only when **all three criteria** are met:
1. The inventory of raw kits is below the material reorder point
2. There are no outstanding orders for raw kits
3. The factory has sufficient cash to purchase the specified order quantity

No order is placed if any of these three criteria are not met. You may set the reorder point and order quantity independently, in multiples of 60 kits, including zero.

Management considers the physical cost of holding inventory negligible.

### Contracts & Revenue

The current pricing contract: an order does not leave the factory until all 60 receivers in the order are completed. Revenue decreases linearly from full price at the quoted lead time to $0 at the maximum lead time. Orders taking longer than the maximum lead time generate no revenue.

| Contract | Price | Quoted Lead Time | Maximum Lead Time |
|----------|-------|------------------|-------------------|
| C1 (default) | $750 | 7 days | 14 days |
| C2 | $1,000 | 1 day | 2 days |
| C3 | $1,250 | 0.5 days | 1 day |

**A contract is assigned to an order as soon as it arrives at the factory, and that contract cannot be changed afterward for that order.**

### Cash & Interest

You will have some cash on hand when the assignment begins. This amount will decrease as you purchase machines and raw kits from the supplier. Revenue earned from filled orders will increase the cash balance.

- **Positive cash interest:** 10% per year, compounded every simulated day
- **No taxes**
- All fixed overhead costs (salaries, rent, utilities) are ignored

**Machine purchase restriction:** You are not allowed to purchase a machine if doing so would leave the cash balance too low to cover the cost of a raw materials order at the current order quantity.

### Loans

Once the market matures on **Day 100**, a bank will extend a line of credit to Littlefield Technologies at:
- **Annual interest rate:** 20%, compounded daily
- **Loan processing fee:** 5% (incurred when the loan is issued)

### Winning Condition

The winning team is the one with the highest cash balance at the end of the game. **Cash balance = cash on hand minus any outstanding debt.**

## Playing the Simulation Game

The simulator runs continuously. **24 hours of real time = 67 days of simulated time** (about 2.8 simulated days per actual hour). You have no control over the simulator's clock.

The product lifetime is **485 days**. After 485 days of operation, the plant ceases production. Remaining equipment and inventory is worthless.

**Demand is random but stable over the entire 485 days.** Even though orders arrive randomly, long-run average demand will not change.

### Timeline

- **Day 0:** Factory starts with 3 stuffers, 2 testers, 1 tuner, 9,600 kits inventory, no cash on hand
- **Day 50:** You gain control (50 days of history available)
- **Day 50–385:** Your management window (335 simulated days = 5 real days, 67 sim days per real day)
- **Day 385:** You lose control; factory runs on autopilot
- **Day 385–485:** Final 100 days run automatically over a few minutes
- **Day 485:** Simulation ends, demand stops abruptly, remaining inventory worthless

### Changeable Parameters

- **Stations:** Buy/sell machines (enter total number of machines)
- **Station 2:** Change scheduling policy (FIFO, Priority to Step 2, Priority to Step 4)
- **Orders:** Set lot size and select contract for future orders
- **Material:** Change reorder point and/or order quantity (set ROQ to 0 to stop ordering)
- **Cash:** Borrow and repay loans starting on Day 100

Data points are recorded at the start of each day.

## Your Task

The Littlefield factory began production by investing most of its cash in capacity and inventory:
- **Day 0 starting state:** 3 stuffers, 2 testers, 1 tuner, 9,600 kits, no cash
- Management currently quotes 7-day lead times (Contract 1)
- Your goal: manage capacity, scheduling, purchasing, lot sizing, and contracts to **maximize cash generated over the factory's lifetime**
- No operating budget beyond cash generated by the factory itself
- When you lose control on Day 385, leave factory parameters set to maximize the cash balance at Day 485
- **Team scores = cash on hand minus debt**
