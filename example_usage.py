# -*- coding: utf-8 -*-
from client import OpenClawGenParkLeadNexus

nexus = OpenClawGenParkLeadNexus()

enterprise_graph = {
    "Stripe": ["Vercel", "Supabase", "OpenAI"],
    "Vercel": ["Stripe", "NextJS_Hub", "Supabase"],
    "Supabase": ["Postgres_Org", "Stripe"],
    "OpenAI": ["Microsoft", "Stripe", "Vercel"],
    "Microsoft": ["OpenAI", "Enterprise_Client_A"],
    "Enterprise_Client_A": ["Microsoft"],
    "NextJS_Hub": ["Vercel"],
    "Postgres_Org": ["Supabase"]
}

# 1. PageRank Centrality
pr = nexus.calculate_pagerank_influence(enterprise_graph)
print(f"Top Influencer: {pr['rankings'][0]['account_id']} (Score: {pr['rankings'][0]['influence_score']})")

# 2. Adamic-Adar Link Prediction
links = nexus.predict_adamic_adar_links(enterprise_graph, source_node="Stripe", top_k=3)
print(f"\nTop Expansion Link for Stripe:")
for l in links['top_expansion_opportunities']:
    print(f"  Target: {l['candidate_account']} (AA Index: {l['adamic_adar_index']}, via {l['shared_enterprise_hubs']})")

# 3. Champion Mobility Model
mob = nexus.evaluate_champion_mobility(past_account="Stripe", new_account="Fintech_Unicorn_X", tenure_months=36.0, previous_satisfaction_score=0.95)
print(f"\nChampion Transition Conversion: {mob['conversion_probability']*100:.1f}% -> {mob['recommended_engagement_strategy']}")
