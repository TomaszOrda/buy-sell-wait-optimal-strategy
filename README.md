# Introduction

Let's say we are involuntary time travelers. Somehow landed in the 1950s. It just so happens that we remember every day exchange rates starting on the current date all the way to 1985. Perhaps it was a graph on a newspaper we were holding at the moment of time travel. Or maybe we just have a good memory. Splendid idea, but there is one problem. We are starting with only a few dollars to spare. Far fewer to make this idea worthwhile, unless we make every trade optimally.

That represents our problem. Knowing a chronological collection of exchange rates, what is the optimal strategy of exchanging our currency (let's say it is dollar) with another (again, for the sake of presentation call in a yen). There is also a margin — a fraction that is deduced from our money after every exchange.

## A note about machine learning and other ai approaches

It is tempting to use any machine learning approach here. After all, we have a huge array of data we can train on. And in the worst case scenario we overfit the data. And yes, this approach would work. However there are simpler algorithms. Especially algorithms that we can show give optimal answer.

# Functionality

## Brute force

Have I just said there are simpler algorithms with proof of optimality? Well, it is true brute force is extremely rudimentary and will indeed give us optimal answer. Naturally the time complexity would be abysmal. The only reason brute force appears here, is because we will need it in a moment.

Idea is simple. As seen in the code, we are iterating over all possible subsets of points. Each subset represents buy/sell strategies. Which of them are buy, and which are sell is just up to the currency we are starting with.

## Divide and Conquer

The algorithm used is simple Divide and Conquer. It works as follows:

1. If the problem is small, solve it naively (Brute force);
2. Otherwise divide the problem in half, and solve the halves recursively;
3. Knowing all the optimal strategies for each halve we are trying to combine them and picking the best one.

That itself is enough. There is just one subtlety. Our DnC algorithm always returns 4 different strategies. Each with different opening or closing currencies. Why is it so, will be easily visible in the proof.

### Sketch of a proof of correctness

Let's say now that we have a problem as above. But we can calculate left and right halfs optimal strategy (strategies). Now without loss of generality, assume that we want to calculate a full strategy opening with dollar, and closing with yen. There are two ways we can do that.

First possibility is that we take the left strategy that is dollar -> dollar; we also take right strategy that is dollar -> yen. Combining them we will attain a proper strategy. And assuming that, during the middle day we have dollar in our pocket, it is an optimal strategy.

To show that we assume that it is not. Which means that there is a **better strategy** that is more optimal than **our strategy**. So the better strategy will diverge from our strategy on at least one decision. This decision has to be in either left or right strategy — assume it is left. If we divide the better strategy we will get halves, where the left part is different from our. Notice that the right strategy gets no benefit from starting with less dollars, so the left part of the better strategy has to be strictly better than the left part of our strategy. But our left strategy was assumed optimal. Thus there can not be a better strategy. That finishes the proof by contradiction.

Second possibility follows the same way, but with left strategy being dollar -> yen, and right being yen -> dollar.

For everything to work every step of the algorithm (apart from the outermost) must calculate all four opening and closing variations. But all of them go, as the above.

Naturally we should not omit, that the last recursive call of DnC asks brute force for the left and right strategy. But those are optimal, as stated earlier.

### Time complexity

Each function call, calls another two on input that is half the size of the original one. Then we combine the results in constant time. Let's represent that as a recursive function.

$$T(n) = 2T(\frac{n}{2}) + O(1)$$

Now using the master theorem of divide-and-conquer algorithms we get:

$$T(n) \in O(n) \text{.}$$

Or we could argue that we need to run the function on each of the $n$ input variables. Those were run by $\frac{n}{2}$ function calls as each calls for exactly two new functions. Then those were called by $\frac{n}{4}$ functions etc. We get $n + \frac{n}{2} + \frac{n}{4} + \frac{n}{8} + \ldots + 2 + 1 = 2n - 1$ function calls, each running in constant time. One can imagine that as a binary tree of function calls. Of course here we omit the optimization of using brute force for any $n<4$, however that has no impact on the asymptotic time complexity.

## Scanning

There should be a faster algorithm. Let us assume now that we have a partial optimal strategy — that up until a certain day we have made all the perfect decisions. How would we expand that strategy by one more day? 

Assume that We start with dollar and end with dollar. So any partial strategy will buy, then sell, then buy, sell, finally ending on sell. Starting from the day of last sell, for each following day we are going to:
 1. check if it is a good place to buy — we will remember the lowest price since the last sell
 2. check if we can delay our last sell to that day — that is if the price i higher than the last sell
 3. or check if we make a profit if we buy on the day from the 1. and then sell on this day

On top of that, if the opening and closing currency does not match, we need to adjust our final strategy slightly. Here at the end we are either removing the last buy-sell pair and adding the highest buy we can (it will be the buy from buy-sell pair or the next potential buying day), or we just append a buy from after the last pair.

When the currencies are reversed from what the algorithm thinks they are, it is sufficient to reverse every rate and run the algorithm as is.

### Proof of correctness and time complexity

Time complexity is naturally O(n), as any natural scanning algorithm.

Proof of correctness is... tedious. But doable? I suppose?

Let us notice that in optimal solution any buy has the lowest rate among its neighbours up until the two sells that envalop it. Same with sell days — they are the highest among their neighbours. If it was not true, then we could shift the buy (sell) towards that value and get a better solution.

Now assume that our algorithm found the previous buy-sell pairs just fine. We have a few cases to consider:

 - It would not find a new buy-sell pair before the next optimal-buy, because that pair could get introduced to the optimal solution making it better.
 - We cant find an earlier buy and sell that is after that buy, beause the optimal-buy is smaller than any buy we could choose, our algorithm would choose it as its buy.
 - Our algorithm cannot choose a buy that is after the optimal-sell, because the optimal pair would trigger it to remember that buy and search for another pair or a better sell.
Let us stop for a brief moment and notice that our algorithm already finds optimal buy days.
 - If our algorithm choose an earlier sell, then it would naturally keep on updating the sell up untill the optimal one. That is unless it finds another pair before it considers the optimal sell.
   - If it touches the optimal sell, it will choose better option between updating sell and creating a new pair. And updating sell is optimal, as we assumed.
   - If it finds a buy-sell pair before it touches the optimal-sell, then we already found a non-zero profit pair that is better than postponing sell. That pair with sell updated to the optimal-sell would generate a better income than the one optimal buy-sell pair, which creates a contradiction. (Lemma required.)
 - And naturally we cannot update optimal-sell to anything better because we could optimize the optimal solution, which we can not do.

This proof is... less than pretty. It likely has some holes, but the general idea holds. If tried to write a full proof, it would likely take a few pages more.

### Why choose DnC over scanning?

It seems that scanning would be the simpler algorithm of the two. It should be enough to walk the list just once. With perfect control over what we consider a good move and what to discard. No recursion or complicated ideas.

Reality is a presented. Plenty special cases. Other opening and closing combinations which we did not even try to discuss. Writing that algorithm took way longer, and there were countless bugs to be dealt with.

Whereas DnC approach is cleverly simple as soon as one understands the idea behind all of the Divide and Conquer algorithms.
