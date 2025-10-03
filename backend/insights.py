from fastapi import FastAPI

insight_router = FastAPI()

@insight_router.get("/gaps")
def fetch_gaps():
    return [
        {
            "severity": "HIGH",
            "number_of_papers": 3,
            "title": "Bone loss vs density paradox",
            "analysis": "Multiple studies report clear micro- and nanoscale structural degradation after spaceflight or high-LET irradiation (decreased BV/TV, thinner trabeculae, enlarged osteocyte lacunae, increased osteoclast surface), yet bulk bone mineral density or total bone volume measures are sometimes reported as unchanged. Gene-expression data simultaneously show up-regulation of matrix-degrading MMPs and elevations in some mineralization-related transcripts, producing inconsistent interpretations about whether bone is being primarily resorbed, remodeled into a different geometry, or subject to localized mineral retention. These divergent readouts (µCT vs nanoCT vs histology vs transcriptomics) create a major conflict about the true nature and clinical significance of space- or radiation-induced bone change."
        },
        {
            "severity": "HIGH",
            "number_of_papers": 3,
            "title": "Oxidative stress response direction",
            "analysis": "Across cardiac, bone marrow and osteoprogenitor studies there are inconsistent findings about antioxidant status: some assays show acute depletion of antioxidant capacity after irradiation (marrow ECF), others report up- or down-regulation of specific antioxidant genes (e.g., Nfe2l2 down but Catalase/CuZnSOD/other antioxidants up in certain contexts). Functional outcomes (cell survival, differentiation) and timing (1 day vs 7 days vs weeks) also differ, so it is unclear whether spaceflight/radiation provokes net oxidative damage because defenses fail, or a compensatory upregulation that is insufficient or maladaptive. The direction, timing and tissue specificity of the redox response are therefore in conflict."
        },
        {
            "severity": "MEDIUM",
            "number_of_papers": 4,
            "title": "Method-driven result variability",
            "analysis": "Several papers demonstrate that experimental methods strongly influence outcomes: a new K_FEA fatigue protocol dramatically reduces variability compared with older loading methods; microgravity qPCR runs are noisier and affected by bubble formation and cap design yet report Ct values comparable to 1 g; microsphere (microgravity-mimic) culture markedly changes stemness marker expression versus dish culture. These discrepancies highlight a cross-cutting conflict—are observed biological effects genuine or artifacts of differing hardware, sealing, culture format or analysis pipelines—and complicate cross-study comparisons."
        }
    ]


@insight_router.get("/projects")
def fetch_gaps():
    return [
  {
    "title": "Martian Microbial Resilience Study",
    "description": "A mission combining orbital spectrometry, robotic surface labs, and simulated analog chambers to resolve conflicting evidence on microbial survival in Martian radiation, perchlorate-rich soil, and fluctuating hydration cycles.",
    "cost": "$1.8B",
    "risk_level": "High",
    "potential_roi": "Revolutionary",
    "expected_discoveries": "Definitive constraints on microbial viability under Martian surface and subsurface conditions, clarifying habitability potential."
  },
  {
    "title": "Spaceflight Muscle Mechanobiology Mission",
    "description": "An integrated rodent and organoid study aboard the ISS to reconcile conflicting findings about mechanotransduction, calcium handling, and muscle atrophy pathways under microgravity and mechanical loading conditions.",
    "cost": "$950M",
    "risk_level": "Medium",
    "potential_roi": "High",
    "expected_discoveries": "Novel insights into muscle atrophy mechanisms and therapeutic countermeasures critical for astronaut health on long-duration missions."
  },
  {
    "title": "Microgravity Plant Adaptation Lab",
    "description": "A long-term ISS-based greenhouse project to resolve contradictions in plant gravitropism, root signaling, and nutrient uptake under microgravity and variable light cycles.",
    "cost": "$1.2B",
    "risk_level": "Medium",
    "potential_roi": "Moderate",
    "expected_discoveries": "Clear mechanisms of plant stress adaptation, enabling reliable space agriculture and closed-loop life support systems."
  }
]
