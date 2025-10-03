from fastapi import APIRouter, Body

router = APIRouter(prefix="/api") 


@router.get("/")
def hello_world():
    return {"message": "welcome from api"}



@router.post("/search")
async def search_publications(search_filters: dict = Body(...)):
    # You can inspect search_filters for filtering if you want
    # e.g., q = search_filters.get("query")
    response = {
        "publications": [
            {
                "paperName": "Microbial Life Detection in Martian Subsurface Ice",
                "numberOfScientists": 80,
                "viewPaperURL": "https://nasa.gov/papers/mars-microbial-detection-2024",
                "paperSummary": "This blah blah blah groundbreaking study presents compelling evidence for potential microbial biosignatures in Martian subsurface ice, utilizing advanced spectrometry and DNA sequencing techniques. The research represents a collaborative effort involving multiple NASA centers and provides critical insights for future Mars sample return missions.",
                "tags": ["Mars", "Astrobiology", "Subsurface", "Biosignatures", "Ice"],
                "scientistSummary": {
                    "header": "Breakthrough Discovery in Mars Astrobiology",
                    "body": "Our research team successfully identified potential biosignatures in subsurface ice samples from the Martian polar regions. Using advanced spectrometry and DNA sequencing techniques, we detected organic compounds consistent with extremophile microorganisms similar to those found in Earth's Antarctic ice sheets.",
                    "conclusion": "These findings suggest a high probability of past or present microbial life on Mars, warranting immediate follow-up missions for sample return and further analysis."
                },
                "managerSummary": {
                    "header": "Mission-Critical Astrobiology Results",
                    "body": "This study represents a significant milestone in our Mars exploration program. The research leveraged $15M in advanced instrumentation and involved collaboration between JPL, Ames Research Center, and international partners. The results directly support our 2028 Mars Sample Return mission objectives.",
                    "conclusion": "Recommend immediate funding allocation for expanded research and acceleration of sample return timeline based on these promising results."
                },
                "missionArchSummary": {
                    "header": "Technical Architecture for Mars Life Detection",
                    "body": "The mission utilized the Mars Reconnaissance Orbiter's advanced spectrometers in conjunction with ground-penetrating radar to identify optimal drilling sites. Our distributed sensor network architecture enabled real-time data collection and analysis across multiple subsurface locations.",
                    "conclusion": "The technical approach validates our multi-platform architecture design for future Mars missions and provides blueprint for Europa and Enceladus exploration."
                }
            },
            {
                "paperName": "Atmospheric Methane Variations and Seasonal Patterns on Mars",
                "numberOfScientists": 12,
                "viewPaperURL": "https://nasa.gov/papers/mars-methane-atmospheric-2023",
                "paperSummary": "An 18-month comprehensive atmospheric monitoring study revealing seasonal methane emission patterns on Mars. The research demonstrates coordinated observations across multiple orbital and surface assets, providing crucial data for understanding active geological and potentially biological processes on the Red Planet.",
                "tags": ["Mars", "Atmosphere", "Methane", "Seasonal", "Monitoring"],
                "scientistSummary": {
                    "header": "Seasonal Methane Cycles Confirm Active Geological Processes",
                    "body": "Our 18-month atmospheric monitoring campaign revealed consistent seasonal methane emissions patterns, with peak concentrations occurring during Martian summer in the northern hemisphere. The methane plumes correlate strongly with known geological fault systems and potential hydrothermal activity zones.",
                    "conclusion": "The data strongly suggests active subsurface processes, potentially including both geological and biological methane production mechanisms."
                },
                "managerSummary": {
                    "header": "Strategic Implications for Mars Exploration",
                    "body": "This comprehensive atmospheric study utilized resources from three active Mars orbiters and the Perseverance rover, representing excellent ROI on our existing mission infrastructure. The findings have immediate implications for site selection for the Mars Sample Return mission and future human exploration.",
                    "conclusion": "Recommend prioritizing methane source regions for upcoming landing site selections and consider dedicated atmospheric monitoring satellite for continuous observation."
                },
                "missionArchSummary": {
                    "header": "Multi-Platform Atmospheric Monitoring System",
                    "body": "The research successfully demonstrated coordinated observations between orbital and surface assets, with real-time data fusion from Mars Reconnaissance Orbiter, MAVEN, ExoMars TGO, and Perseverance rover. Our atmospheric modeling pipeline processed over 2TB of spectroscopic data using machine learning algorithms.",
                    "conclusion": "The integrated monitoring architecture serves as a proven framework for future planetary atmospheric studies across the solar system."
                }
            },
            {
                "paperName": "Lunar Water Ice Distribution and Accessibility Analysis",
                "numberOfScientists": 6,
                "viewPaperURL": "https://nasa.gov/papers/lunar-water-ice-mapping-2024",
                "paperSummary": "A comprehensive mapping study of water ice deposits at the lunar south pole, identifying approximately 600 million tons of accessible water ice reserves. This research provides critical data for the Artemis program and future sustainable lunar operations, with significant cost-saving implications for space exploration.",
                "tags": ["Moon", "Water", "Ice", "Artemis", "Resources"],
                "scientistSummary": {
                    "header": "Comprehensive Lunar Water Resource Assessment",
                    "body": "Using data from the Lunar Reconnaissance Orbiter and recent impact missions, we've created the most detailed map of water ice deposits at the lunar south pole. Our analysis indicates accessible water ice reserves totaling approximately 600 million tons within permanently shadowed regions, with concentrations reaching 20% by mass in optimal locations.",
                    "conclusion": "These water ice reserves represent a game-changing resource for sustainable lunar operations and future Mars missions, with sufficient quantities to support decades of human presence."
                },
                "managerSummary": {
                    "header": "Lunar Resource Utilization Strategic Assessment",
                    "body": "This research directly supports the Artemis program's sustainability objectives and provides critical data for site selection of the lunar Gateway and surface habitats. The identified water reserves could reduce mission costs by $2-5 billion over 10 years by enabling in-situ resource utilization instead of Earth-based supply missions.",
                    "conclusion": "Recommend immediate development of water extraction and processing technologies, with prototype deployment targeted for Artemis IV mission in 2028."
                },
                "missionArchSummary": {
                    "header": "Advanced Lunar Mapping and Resource Assessment Systems",
                    "body": "The study integrated multi-spectral imaging, neutron spectroscopy, and ground-penetrating radar data through our advanced planetary mapping pipeline. The system successfully processed petabytes of orbital data and generated 3D subsurface models with meter-scale resolution across 15,000 km² of lunar surface.",
                    "conclusion": "The mapping architecture and data processing pipeline can be directly adapted for asteroid mining assessments and Mars resource surveys in future missions."
                }
            }
        ]
    }
    return response