# Littlefield Technologies: Complete Strategy Guide & Walkthrough

## Quick Reference Card

| Parameter | Value |
|---|---|
| **Simulation Duration** | Day 0-485 (you control Day 50-385) |
| **Starting Equipment** | 3 stuffers, 2 testers, 1 tuner |
| **Starting Inventory** | 9,600 kits (depleting since Day 0) |
| **Starting Cash** | ~$0 (all invested in equipment + inventory) |
| **Machine Costs** | Stuffer $90K, Tester $80K, Tuner $100K |
| **Machine Sell Price** | $10K each (must keep at least 1 per station) |
| **Kit Cost** | $10/kit + $1,000 fixed per shipment |
| **Supplier Lead Time** | 4 days |
| **Order Size** | 60 receivers per customer order |
| **Interest on Cash** | 10%/year compounded daily |
| **Loan Interest** | 20%/year compounded daily + 5% processing fee (available Day 100+) |
| **Goal** | Maximize cash balance (cash - debt) at Day 485 |

---

## Part 1: Understanding the Factory (The "What")

### The Assembly Process (4 Steps, 3 Stations)

Think of it like an assembly line with 4 stops:

```
Customer Order (60 kits)
        |
        v
  [STATION 1: Board Stuffing] -- Step 1: Mount components onto PC boards
        |
        v
  [STATION 2: Testing] -------- Step 2: Brief initial test
        |
        v
  [STATION 3: Tuning] --------- Step 3: Tune key components
        |
        v
  [STATION 2: Testing] -------- Step 4: Exhaustive final test
        |
        v
  Ship to Customer --> Earn Revenue
```

**Key insight**: Station 2 (Testing) is used TWICE -- for Step 2 AND Step 4. This means it handles double the traffic of the other stations. This is critical for capacity planning.

### The Three Contracts

| Contract | Price | Quoted Lead Time | Max Lead Time | Revenue if Late |
|---|---|---|---|---|
| 1 (Default) | $750 | 7 days | 14 days | Linear decline $750 -> $0 |
| 2 | $1,000 | 1 day | 2 days | Linear decline $1,000 -> $0 |
| 3 | $1,250 | 0.5 days | 1 day | Linear decline $1,250 -> $0 |

**Key insight**: Contract 3 pays 67% more than Contract 1, but you need VERY fast throughput (under 0.5 days). Contract 2 is a good middle ground -- 33% more revenue with a 1-day target.

### How Revenue Works (Important!)

For each contract, revenue decreases linearly if you're late:

- **Contract 1**: Full $750 if done in <= 7 days. At 10.5 days, you earn $375. At 14+ days, you earn $0.
- **Contract 2**: Full $1,000 if done in <= 1 day. At 1.5 days, you earn $500. At 2+ days, you earn $0.
- **Contract 3**: Full $1,250 if done in <= 0.5 days. At 0.75 days, you earn $625. At 1+ day, you earn $0.

**Formula**: Revenue = Price x max(0, (MaxLT - ActualLT) / (MaxLT - QuotedLT))

---

## Part 2: Analyzing the First 50 Days (The "Where Are We Now")

When you log in, you'll see 50 days of historical data. Here's what to look for and how to interpret it:

### Step-by-Step Data Analysis

#### 1. Estimate Demand Rate
- Go to **Consolidated Daily Data** (download the Excel spreadsheet)
- Look at "Jobs Completed" or "Jobs Arrived" columns
- Calculate the average number of orders per day
- **Typical finding**: Demand is roughly 12 orders/day (meaning 12 x 60 = 720 kits consumed per day)
- Demand is random but STABLE -- the long-run average never changes over 485 days

#### 2. Check Station Utilizations
- Click on each station thumbnail and look at the utilization plots
- **Utilization** = fraction of time the machines are busy
- If utilization > 80-85%, expect significant queuing delays
- If utilization > 95%, the station is severely bottlenecked

**What you'll likely see**:
- Station 1 (3 stuffers): Moderate utilization (~50-70%) -- probably NOT the bottleneck
- Station 2 (2 testers, used twice): HIGH utilization (~85-100%) -- likely THE bottleneck
- Station 3 (1 tuner): Variable -- could be bottleneck depending on processing times

#### 3. Check Lead Times
- Look at the "Average Lead Time" plot in Finished Orders
- If lead times are well under 7 days with Contract 1, you have room to switch to a more profitable contract
- If lead times are near or above 7 days, you're losing money on late orders

#### 4. Check Inventory Levels
- Look at the Material section's "Inventory level in kits" plot
- Starting inventory was 9,600 kits
- Calculate daily consumption rate to estimate when you'll run out
- **Example**: If using ~720 kits/day, initial stock lasts about 13 days. By Day 50, you may have already needed reorders.

#### 5. Check Cash Position
- Look at Cash on Hand
- You started with $0 but have been earning revenue from completed orders
- Note your current balance -- this determines what machines you can afford

### Identifying the Bottleneck (Most Important Analysis!)

The **bottleneck** is the station with the highest utilization. It limits your entire factory's throughput.

**How to calculate capacity at each station:**

From the historical data, you can find average processing times per lot. Let's work with typical values:

Suppose from the data:
- Station 1 avg processing time per lot of 60: ~roughly X hours
- Station 2 avg processing time per lot of 60: ~roughly Y hours (remember: jobs go through TWICE)
- Station 3 avg processing time per lot of 60: ~roughly Z hours

**Utilization formula**: u = (arrival rate x processing time) / number of machines

The station with the highest utilization is your bottleneck. **Station 2 is almost always the bottleneck** because every job passes through it twice.

---

## Part 3: The Strategy (The "What to Do")

### Phase 1: Immediate Actions (Day 50-60) -- "Stabilize"

**Priority order:**

1. **Download and analyze the data spreadsheet** (Consolidated Daily Data)
   - Calculate average demand rate (orders/day)
   - Calculate utilization at each station
   - Identify the bottleneck

2. **Buy machines for the bottleneck station**
   - If Station 2 is the bottleneck (most likely): Buy 1-2 additional testers ($80K each)
   - This immediately reduces lead times
   - **Important**: The system won't let you buy a machine if it leaves you with insufficient cash to cover your next material order. If blocked, temporarily reduce your reorder quantity first.

3. **Adjust inventory policy**
   - Check current reorder point (ROP) and order quantity
   - Initial settings may be too high (tying up cash) or too low (risking stockouts)
   - A reasonable starting point:
     - **Reorder Point**: ~3,600-4,200 kits (enough to cover ~5-6 days of demand at ~720 kits/day, which gives buffer over the 4-day lead time)
     - **Order Quantity**: ~3,600-7,200 kits (balance between ordering costs and not tying up too much cash)

4. **Keep Contract 1 ($750/7 days) initially**
   - Don't switch contracts until you've reduced lead times
   - Switching to Contract 2 or 3 while lead times are high = $0 revenue on many orders

### Phase 2: Optimize (Day 60-150) -- "Speed Up and Earn More"

1. **Add capacity strategically** as cash allows
   - Keep monitoring utilization at each station
   - Buy machines at whichever station has the highest utilization
   - **Typical target configuration**: 3 stuffers, 3-4 testers, 1-2 tuners

2. **Switch to Contract 2 ($1,000/1 day) when ready**
   - Switch ONLY when average lead times are consistently well below 1 day
   - Check that utilization at all stations is below ~80%
   - **This is the single biggest revenue lever in the game**
   - Going from $750 to $1,000 per order is a 33% revenue increase with NO additional cost

3. **Consider Contract 3 ($1,250/0.5 days) if capacity allows**
   - Only switch if lead times are very consistently under 0.5 days
   - This is risky -- if demand spikes even briefly, you earn $0 on those orders
   - Contract 2 is often the safer, better choice

4. **Use a loan (available Day 100+) if it makes sense**
   - If buying another machine will let you switch from Contract 1 to Contract 2
   - The extra $250/order will easily pay back a loan
   - Be cautious: 20% interest + 5% processing fee is expensive
   - Calculate: Will the extra revenue from a better contract exceed the loan cost?

### Phase 3: Optimize Lot Size (Ongoing)

**Lot sizing options**: 1 lot of 60, 2 lots of 30, 3 lots of 20, or 5 lots of 12.

**Tradeoff**:
- Smaller lots = faster flow through the system (a lot of 30 finishes at Station 1 and moves to Station 2 while the second lot is still being processed at Station 1) = LOWER lead times
- Smaller lots = more setups = more time spent on setups instead of processing = REDUCED effective capacity

**Recommendation**:
- If you have plenty of capacity (low utilization), smaller lots help reduce lead times
- If stations are near capacity, keep larger lots to minimize setup overhead
- **With enough machines, splitting into 2 lots of 30 is often optimal** -- it significantly reduces lead time without too much setup overhead

### Phase 4: Station 2 Scheduling Policy

Station 2 offers three scheduling options:
1. **FIFO** (First-In, First-Out) -- default
2. **Priority to Step 2** (initial testing gets priority)
3. **Priority to Step 4** (final testing gets priority)

**Recommendation**: Generally stick with **FIFO** or try **Priority to Step 4**.
- Priority to Step 4 means orders that are almost done get finished faster, reducing their lead time
- This can help ensure orders are completed within the contract window
- But test and monitor -- if it causes Step 2 items to back up, it could make things worse

### Phase 5: End-Game (Day 350-385) -- "Prepare for Autopilot"

You lose control at Day 385 and the factory runs by itself until Day 485. Plan ahead:

1. **Stop buying unnecessary inventory**
   - Calculate how many kits you need for the remaining ~100 days (Day 385-485)
   - Remaining demand = ~100 days x average daily demand in kits
   - Example: 100 days x 720 kits/day = 72,000 kits needed
   - Factor in the 4-day lead time and set your reorder point/quantity so you'll have EXACTLY enough
   - Any leftover inventory at Day 485 is worthless

2. **Consider setting reorder quantity to 0 near the end**
   - If you have enough kits to last until Day 485, stop ordering
   - This saves the $1,000 fixed cost per shipment AND the $10/kit cost
   - More cash on hand earns interest at 10%/year

3. **Consider selling machines near Day 385**
   - Each machine sells for $10K
   - But selling machines reduces capacity, which means longer lead times and less revenue during Days 385-485
   - **Only sell if**: The factory still has enough capacity to fulfill orders during the last 100 days
   - Usually it's NOT worth selling machines because the lost revenue from longer lead times exceeds $10K

4. **Set the best contract for the final 100 days**
   - Leave whichever contract will maximize revenue given the capacity you're leaving in place
   - If you've been running Contract 2 comfortably, leave it on Contract 2

5. **Pay off any debt before Day 385**
   - Debt accrues 20% interest daily
   - Cash on hand earns 10% interest
   - Paying off debt saves you the 10% net interest difference

---

## Part 4: Key Formulas and Calculations

### Utilization at Each Station
```
Utilization = (Demand Rate x Processing Time per Order) / Number of Machines

Example for Station 2 (handles each order TWICE):
If demand = 12 orders/day
Processing time per pass = 0.04 days (total for both passes = 0.08 days per order)
Number of testers = 2

Utilization = (12 x 0.08) / 2 = 0.48 --> 48% (looks good!)

But if processing time per pass = 0.08 days each (total 0.16):
Utilization = (12 x 0.16) / 2 = 0.96 --> 96% (BOTTLENECK! Buy more testers!)
```

### Revenue Calculation
```
For Contract 2 ($1,000, 1-day quoted, 2-day max):

If order completed in 0.8 days: Revenue = $1,000 (within quoted lead time)
If order completed in 1.5 days: Revenue = $1,000 x (2 - 1.5)/(2 - 1) = $500
If order completed in 2.5 days: Revenue = $0 (exceeds max lead time)
```

### Inventory Reorder Math
```
Daily demand in kits = orders/day x 60 kits/order
Lead time demand = daily demand x 4 days (supplier lead time)

Reorder Point (ROP) should be >= Lead time demand + safety buffer
  Example: 720 kits/day x 4 days = 2,880 kits minimum
  With safety buffer: Set ROP = 3,600 kits (covers ~5 days)

Order Quantity: Balance cost vs. cash tied up
  Each order costs: $1,000 fixed + ($10 x quantity)
  Bigger orders = fewer $1,000 fees, but more cash tied up in inventory
```

### Should I Take a Loan? (Quick Decision Framework)
```
Cost of loan = Loan Amount x 5% fee + daily interest at 20%/year

Benefit = Extra revenue from improved operations

Example: Borrow $80K to buy a tester
  Loan cost: $80K x 5% = $4K fee + ~$80K x (20%/365) per day = ~$44/day interest
  If switching from Contract 1 to Contract 2 earns extra $250/order x 12 orders/day = $3,000/day
  Payback: The machine pays for itself in about 28 days ($80K / $2,956 net daily gain)
  --> ABSOLUTELY worth it!
```

---

## Part 5: Day-by-Day Action Checklist

### When Simulation Opens (Day 50)
- [ ] Download Consolidated Daily Data spreadsheet
- [ ] Calculate average demand rate (orders per day)
- [ ] Calculate utilization at each station
- [ ] Identify bottleneck station
- [ ] Note current cash balance
- [ ] Note current inventory level
- [ ] Note current ROP and order quantity settings

### First 2 Hours (Day 50-56, since ~2.8 sim days/real hour)
- [ ] Buy 1 machine for bottleneck station (most likely 1 extra tester for Station 2)
- [ ] Adjust reorder point to ~3,600-4,200 kits
- [ ] Adjust order quantity to ~3,600-7,200 kits
- [ ] Keep Contract 1 for now
- [ ] Monitor lead times

### Day 1 of Real Time (Day 50-117)
- [ ] Check lead times -- are they dropping?
- [ ] Buy additional machines as cash allows
- [ ] When lead times are consistently < 1 day with margin, switch to Contract 2
- [ ] On Day 100+: Consider taking a loan if it enables a profitable machine purchase

### Days 2-3 of Real Time (Day 117-251)
- [ ] Fine-tune: monitor utilizations, buy/adjust as needed
- [ ] Experiment with lot sizes if lead times need further reduction
- [ ] Experiment with Station 2 scheduling policy
- [ ] Consider Contract 3 if lead times are < 0.5 days consistently
- [ ] Pay down any loans with excess cash

### Days 4-5 of Real Time (Day 251-385)
- [ ] Calculate remaining inventory needs for Days 385-485
- [ ] Start reducing reorder quantity to avoid excess inventory at end
- [ ] Pay off all debt
- [ ] Set final contract, lot size, and scheduling for the autopilot period
- [ ] Consider setting order quantity to 0 if you have enough stock to last

---

## Part 6: Common Mistakes to Avoid

1. **Switching to Contract 2 or 3 too early**: If your lead times are too high, you earn $0 instead of $750. Always make sure capacity is sufficient FIRST.

2. **Ignoring Station 2's double duty**: Station 2 handles both Step 2 and Step 4. It needs proportionally more machines.

3. **Running out of raw materials**: If inventory hits zero and there's no outstanding order (or you don't have cash), the factory stops. Dead time = zero revenue.

4. **Ordering too much inventory near the end**: Kits cost $10 each and are worthless after Day 485. Don't waste money on kits you'll never use.

5. **Not using loans when profitable**: A loan at 20% that lets you earn thousands more per day is worth it. Do the math.

6. **Selling machines too early**: You might think selling a machine near Day 385 for $10K is free money, but if it causes longer lead times during Days 385-485, you lose much more in reduced revenue.

7. **Forgetting that contracts are locked to orders**: If you switch from Contract 2 to Contract 1, orders already in the system stay at Contract 2 pricing. Only NEW orders get the new contract.

---

## Part 7: Theoretical Frameworks from Class (For the Write-Up)

When writing the Action Plan and Summary Report, reference these concepts:

### Queuing Theory (Lectures 5-6)
- **Utilization and waiting time**: As utilization approaches 100%, waiting time (and thus lead time) goes to infinity. The Tq formula shows this: Tq = (p/m) x [u^(sqrt(2(m+1)-1)) / (1-u)] x [(CVa^2 + CVp^2)/2]
- **Bottleneck analysis**: The station with the highest utilization determines the factory's throughput limit
- **Little's Law**: Inventory = Flow Rate x Flow Time. More WIP = longer lead times.

### Inventory Management (Lectures 7-8)
- **EOQ Model**: Q* = sqrt(2AK/H). Balances ordering costs vs. holding costs.
- **Reorder Point with Lead Time**: ROP = Lead Time Demand + Safety Stock
- In Littlefield, holding cost is negligible per the assignment, but the opportunity cost of cash IS significant (10% interest). So don't over-order.

### Capacity Planning
- Adding capacity (buying machines) reduces utilization, which dramatically reduces waiting time
- The relationship is nonlinear -- going from 95% to 80% utilization is far more impactful than going from 60% to 45%

### Contract Selection as a Revenue Optimization Problem
- Higher contracts are like selling a premium product -- you need operational excellence to deliver
- The decision mirrors a newsvendor problem: the "cost of underage" is lost premium revenue; the "cost of overage" is earning $0 on late orders

---

## Quick-Reference Decision Tree

```
START: Day 50
  |
  v
Is any station utilization > 85%?
  |          |
  YES        NO
  |          |
  v          v
Buy machine  Check lead times
at that      |
station      Are lead times < 1 day consistently?
  |          |          |
  |          YES        NO
  |          |          |
  |          v          v
  |     Switch to    Keep Contract 1,
  |     Contract 2   optimize capacity
  |          |
  |          v
  |     Are lead times < 0.5 days?
  |          |          |
  |          YES        NO
  |          |          |
  |          v          v
  |     Consider     Stay on Contract 2
  |     Contract 3   (safer)
  |
  v
Repeat: Monitor -> Adjust -> Monitor
```

---

*Remember: The winning team has the highest (Cash on Hand - Debt) at Day 485. Every decision should be evaluated through the lens of: "Does this increase my final cash balance?"*
