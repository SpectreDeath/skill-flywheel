"""
Auction Strategy Optimizer

Optimizes bidding strategies for various auction types:
- English (ascending) auctions
- Dutch (descending) auctions
- First-price sealed-bid
- Second-price sealed-bid (Vickrey)
- All-pay auctions
"""

from typing import Dict, List, Any, Optional
import math


def auction_strategy_optimizer(
    auction_type: str,
    num_bidders: int,
    your_valuation: float,
    common_value: Optional[float] = None,
    private_values: Optional[List[float]] = None,
    reserve_price: Optional[float] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Optimize bidding strategy for different auction types.

    Args:
        auction_type: Type of auction (english, dutch, first_price, second_price, all_pay)
        num_bidders: Number of competing bidders
        your_valuation: Your true valuation of the item
        common_value: For common value auctions, the underlying value
        private_values: List of other bidders' private value estimates
        reserve_price: Auction reserve price (if any)
        **kwargs: Additional parameters

    Returns:
        Optimal bidding strategy and expected outcomes
    """

    auction_type = auction_type.lower().replace("-", "_").replace(" ", "_")

    strategies = {
        "english": _english_auction_strategy,
        "dutch": _dutch_auction_strategy,
        "first_price": _first_price_strategy,
        "second_price": _second_price_strategy,
        "vickrey": _second_price_strategy,
        "all_pay": _all_pay_strategy,
    }

    if auction_type not in strategies:
        return {
            "status": "error",
            "error": f"Unknown auction type: {auction_type}",
        }

    strategy_func = strategies[auction_type]
    result = strategy_func(
        num_bidders=num_bidders,
        your_valuation=your_valuation,
        common_value=common_value,
        private_values=private_values,
        reserve_price=reserve_price,
    )

    result["auction_type"] = auction_type
    result["status"] = "success"

    return result


def _english_auction_strategy(
    num_bidders: int,
    your_valuation: float,
    common_value: Optional[float],
    private_values: Optional[List[float]],
    reserve_price: Optional[float],
) -> Dict[str, Any]:
    """English (ascending) auction strategy"""

    # In English auction, bid up to your valuation
    # With private values, bid your valuation
    # With common value, be cautious of winner's curse

    strategy = {
        "optimal_bid": your_valuation,
        "bid_increment": "Raise by minimum increment until others drop",
        "stop_condition": "Drop out when price exceeds your valuation",
    }

    expected_winner_curse = 0
    if common_value and private_values:
        # Winner's curse: you likely overestimated if you win
        avg_others = sum(private_values) / len(private_values)
        expected_winner_curse = your_valuation - avg_others
        strategy["adjustment"] = (
            f"Reduce bid by ~{expected_winner_curse:.2f} for winner's curse"
        )

    return {
        "strategy": "Bid your valuation (or valuation minus winner's curse for common value)",
        "details": strategy,
        "expected_payment": your_valuation
        - (expected_winner_curse if expected_winner_curse > 0 else 0),
        "winning_probability": _estimate_win_prob(
            num_bidders, your_valuation, private_values
        ),
    }


def _dutch_auction_strategy(
    num_bidders: int,
    your_valuation: float,
    common_value: Optional[float],
    private_values: Optional[List[float]],
    reserve_price: Optional[float],
) -> Dict[str, Any]:
    """Dutch (descending) auction strategy"""

    # In Dutch auction, be ready to bid quickly at your threshold
    # Time pressure favors decisive action

    optimal_jump = your_valuation * 0.95

    return {
        "strategy": "Wait until price drops to your threshold, then bid immediately",
        "details": {
            "optimal_jump_price": optimal_jump,
            "reasoning": "Pre-commit to a price to avoid hesitation",
            "risk": "If you wait too long, someone else may bid first",
        },
        "expected_payment": optimal_jump,
        "winning_probability": _estimate_win_prob(
            num_bidders, your_valuation, private_values
        ),
    }


def _first_price_strategy(
    num_bidders: int,
    your_valuation: float,
    common_value: Optional[float],
    private_values: Optional[List[float]],
    reserve_price: Optional[float],
) -> Dict[str, Any]:
    """First-price sealed-bid strategy"""

    # In first-price, shade your bid below valuation
    # With symmetric bidders, optimal bid = valuation * (n-1)/n
    # More bidders = less shading

    n = num_bidders
    shaded_factor = (n - 1) / n if n > 1 else 1.0

    # Adjust for private information
    if private_values:
        avg_competing = sum(private_values) / len(private_values)
        if your_valuation > avg_competing * 1.2:
            shaded_factor *= 1.1  # Bid more aggressively if you have advantage
        elif your_valuation < avg_competing * 0.8:
            shaded_factor *= 0.9  # Bid more conservatively if behind

    optimal_bid = your_valuation * shaded_factor

    return {
        "strategy": f"Shade bid by factor ~{shaded_factor:.2f}",
        "details": {
            "optimal_bid": optimal_bid,
            "shade_factor": shaded_factor,
            "logic": f"With {n} bidders, shade by {(1 - shaded_factor) * 100:.1f}%",
        },
        "expected_payment": optimal_bid,
        "expected_profit": your_valuation - optimal_bid,
        "winning_probability": _estimate_win_prob(
            num_bidders, your_valuation, private_values
        ),
    }


def _second_price_strategy(
    num_bidders: int,
    your_valuation: float,
    common_value: Optional[float],
    private_values: Optional[List[float]],
    reserve_price: Optional[float],
) -> Dict[str, Any]:
    """Second-price sealed-bid (Vickrey) strategy"""

    # In second-price, truthful bidding is dominant strategy
    # Bid your valuation

    reserve_impact = 0
    if reserve_price:
        if your_valuation > reserve_price:
            reserve_impact = (reserve_price - your_valuation) / num_bidders

    return {
        "strategy": "Truthful bidding is dominant - bid your valuation",
        "details": {
            "optimal_bid": your_valuation,
            "logic": "In Vickrey, your payment determined by 2nd highest bid",
            "reserve_handling": "If reserve > your valuation, bid 0; else bid valuation",
        },
        "expected_payment": reserve_price
        if reserve_price and reserve_price < your_valuation
        else your_valuation * 0.5,
        "expected_profit": your_valuation * 0.5
        if not reserve_price or reserve_price < your_valuation
        else 0,
        "winning_probability": _estimate_win_prob(
            num_bidders, your_valuation, private_values
        ),
    }


def _all_pay_strategy(
    num_bidders: int,
    your_valuation: float,
    common_value: Optional[float],
    private_values: Optional[List[float]],
    reserve_price: Optional[float],
) -> Dict[str, Any]:
    """All-pay auction strategy"""

    # In all-pay, everyone pays their bid regardless of winning
    # Very different incentives - consider expected value carefully

    # Optimal bid depends on your value and probability of winning
    prob_win = _estimate_win_prob(num_bidders, your_valuation, private_values)

    # Expected value = prob(win) * your_valuation - bid
    # Optimal balance requires calculation
    optimal_bid = prob_win * your_valuation * 0.8

    return {
        "strategy": "Balance winning probability against guaranteed payment",
        "details": {
            "recommended_bid": optimal_bid,
            "logic": "All-pay favors underdog - high valuation bidders disadvantaged",
            "caution": "Every bid is lost regardless of outcome",
        },
        "expected_payment": optimal_bid,
        "expected_profit": (prob_win * your_valuation) - optimal_bid,
        "winning_probability": prob_win,
    }


def _estimate_win_prob(n: int, your_val: float, others: Optional[List[float]]) -> float:
    """Estimate probability of winning"""

    if others:
        # Simple estimate based on relative valuations
        all_vals = [your_val] + others
        sorted_vals = sorted(all_vals, reverse=True)
        your_rank = sorted_vals.index(your_val) + 1
        # P(winning) = number of bidders you beat / total comparisons
        wins = sum(1 for v in others if your_val > v)
        return wins / len(others) if others else 0

    # With no info, assume uniform distribution
    return 1.0 / n


def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "optimize")
    auction_type = payload.get("auction_type", "first_price")
    num_bidders = payload.get("num_bidders", 2)
    your_valuation = payload.get("your_valuation", 100)
    common_value = payload.get("common_value")
    private_values = payload.get("private_values")
    reserve_price = payload.get("reserve_price")

    result = auction_strategy_optimizer(
        auction_type=auction_type,
        num_bidders=num_bidders,
        your_valuation=your_valuation,
        common_value=common_value,
        private_values=private_values,
        reserve_price=reserve_price,
    )

    return {"result": result}


def register_skill():
    """Return skill metadata"""
    return {
        "name": "auction-strategy-optimizer",
        "description": "Optimize bidding strategies for English, Dutch, sealed-bid, and all-pay auctions",
        "version": "1.0.0",
        "domain": "STRATEGY",
    }
