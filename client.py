# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Lead Nexus - Graph PageRank Influence & Adamic-Adar Enterprise Relationship Engine
Standard Library only: math, typing.
Calculates power-iteration PageRank centrality across enterprise account networks,
computes Adamic-Adar link prediction scores for buyer account expansion, and models
champion mobility re-engagement conversion probability.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkLeadNexus:
    def __init__(self, default_damping: float = 0.85):
        self.default_damping = default_damping

    def calculate_pagerank_influence(self, graph: Dict[str, List[str]],
                                     damping: float = None,
                                     max_iter: int = 50,
                                     tol: float = 1e-6) -> Dict[str, Any]:
        """
        Calculates stationary distribution of enterprise influence via power-iteration PageRank.
        r_i^(k+1) = (1 - d)/N + d * sum_{j in M(i)} (r_j^(k) / out_deg(j))
        """
        d = damping if damping is not None else self.default_damping
        nodes = sorted(list(graph.keys()))
        N = len(nodes)
        if N == 0:
            return {"rankings": [], "iterations": 0}

        # Initialize uniform distribution
        ranks = {node: 1.0 / N for node in nodes}
        out_degrees = {node: len(graph.get(node, [])) for node in nodes}

        iterations_run = 0
        for it in range(max_iter):
            iterations_run += 1
            new_ranks = {}
            # Base probability from random jump
            base_prob = (1.0 - d) / N

            # Distribute dangling node mass
            dangling_sum = sum(ranks[n] for n in nodes if out_degrees[n] == 0)
            dangling_contrib = d * dangling_sum / N

            for node in nodes:
                rank_sum = 0.0
                # Incoming links to node
                for j in nodes:
                    if node in graph.get(j, []):
                        rank_sum += ranks[j] / max(1, out_degrees[j])
                new_ranks[node] = base_prob + dangling_contrib + d * rank_sum

            # Check convergence L1-norm
            diff = sum(abs(new_ranks[n] - ranks[n]) for n in nodes)
            ranks = new_ranks
            if diff < tol:
                break

        sorted_ranks = sorted(
            [{"account_id": n, "influence_score": round(ranks[n], 5), "degree": out_degrees[n]} for n in nodes],
            key=lambda x: x["influence_score"],
            reverse=True
        )

        return {
            "total_accounts": N,
            "damping_factor": d,
            "iterations_converged": iterations_run,
            "rankings": sorted_ranks
        }

    def predict_adamic_adar_links(self, graph: Dict[str, List[str]],
                                  source_node: str,
                                  top_k: int = 5) -> Dict[str, Any]:
        """
        Predicts prospective enterprise expansion ties using the Adamic-Adar index:
        AA(u, v) = sum_{z in Neighbors(u) cap Neighbors(v)} (1 / ln(deg(z)))
        """
        if source_node not in graph:
            return {"error": f"Source node '{source_node}' not in graph"}

        source_neighbors = set(graph.get(source_node, []))
        all_nodes = set(graph.keys())
        # Candidates are nodes not directly connected to source
        candidates = all_nodes - source_neighbors - {source_node}

        node_degrees = {n: len(graph.get(n, [])) for n in all_nodes}
        scores = []

        for cand in candidates:
            cand_neighbors = set(graph.get(cand, []))
            common = source_neighbors.intersection(cand_neighbors)
            if not common:
                continue

            aa_score = 0.0
            for z in common:
                deg_z = max(2, node_degrees.get(z, 2))
                aa_score += 1.0 / math.log(deg_z)

            scores.append({
                "candidate_account": cand,
                "adamic_adar_index": round(aa_score, 4),
                "shared_enterprise_hubs": list(common),
                "shared_hubs_count": len(common)
            })

        scores.sort(key=lambda x: x["adamic_adar_index"], reverse=True)

        return {
            "source_account": source_node,
            "candidate_evaluations_count": len(scores),
            "top_expansion_opportunities": scores[:top_k]
        }

    def evaluate_champion_mobility(self, past_account: str,
                                   new_account: str,
                                   tenure_months: float,
                                   previous_satisfaction_score: float) -> Dict[str, Any]:
        """
        Models conversion probability when an executive/champion moves from a satisfied customer
        account to a prospective target account:
        P = 1 / (1 + exp(-(beta_0 + beta_1 * satisfaction + beta_2 * ln(tenure))))
        """
        # Baseline log-odds
        beta_0 = -2.5
        beta_1 = 3.2  # Satisfaction weight (normalized 0-1)
        beta_2 = 0.4  # Tenure impact
        
        tenure_term = math.log(max(1.0, tenure_months))
        sat_term = max(0.0, min(1.0, previous_satisfaction_score))
        
        logit = beta_0 + beta_1 * sat_term + beta_2 * tenure_term
        prob = 1.0 / (1.0 + math.exp(-logit))

        if prob >= 0.70:
            urgency = "IMMEDIATE_EXECUTIVE_WARM_OUTREACH"
        elif prob >= 0.40:
            urgency = "SCHEDULE_CONGRATULATORY_NOTE"
        else:
            urgency = "MONITOR_ACCOUNT_TRANSITION"

        return {
            "past_account": past_account,
            "new_account": new_account,
            "tenure_months": tenure_months,
            "previous_satisfaction": sat_term,
            "conversion_probability": round(prob, 4),
            "expected_pipeline_multiplier": round(prob * 4.5, 2),
            "recommended_engagement_strategy": urgency
        }
