"""Demo news stories based on real City Information Office posts.

The text is plain, accessible copy rewritten from the city's own published
stories. Dates match the original posts. Photos live under ``static/img/news``
and are resolved by :mod:`content.article_images`.
"""

from datetime import date

NEWS_ARTICLES = [
    {
        "slug": "subaraw-festival-queen-2026",
        "category": "Festival",
        "title": "Angela Joyce Tabago crowned Subaraw Festival Queen 2026",
        "summary": (
            "The Camarines Norte candidate won the crown at the Edward S. Hagedorn "
            "Coliseum, closing a festival that celebrated beauty, talent, and care "
            "for the environment."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 12),
        "body": [
            "Angela Joyce Tabago of Camarines Norte is the Subaraw Festival Queen 2026. She was crowned during the coronation night on November 10 at the Edward S. Hagedorn Coliseum.",
            "Aliya Clemeña Rohilla of Manila was first runner-up, while Faith Dweyne Villanueva of Sorsogon placed second runner-up. Special awards recognized evening gown, swimsuit, photogenic, and community impact.",
            "In his message, Mayor Lucilo R. Bayron said the pageant was not only about choosing a queen but also about celebrating the intelligence, confidence, and environmental awareness of the candidates.",
            "The city thanked the organizers, sponsors, judges, and residents who supported the 30 candidates from Puerto Princesa, Palawan, and other parts of the country.",
        ],
    },
    {
        "slug": "subaraw-biodiversity-festival-2026-success",
        "category": "City government",
        "title": "Mayor Bayron: Subaraw Biodiversity Festival 2026 is a great success",
        "summary": (
            "The city closed this year's festival with a grand parade and awarding "
            "ceremony, with the mayor crediting residents, performers, and organizers "
            "for its success."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 12),
        "body": [
            "Mayor Lucilo R. Bayron declared the Subaraw Biodiversity Festival 2026 a success during the closing program and awarding ceremony on November 11 at the Edward S. Hagedorn Coliseum.",
            "The day began with a grand parade from Robinsons Mall Palawan to the coliseum in observance of Puerto Princesa Underground River Day. City officials, employees, and sector representatives joined the procession.",
            "The mayor thanked participants, spectators, judges, the City Events Team, and the PPSRNP team for the activities held in the city proper and in Sitio Sabang.",
            "He said the festival continues to grow and that the city will use this year's experience to make Subaraw 2027 even bigger. He also reminded residents that protecting the environment is a shared responsibility.",
        ],
    },
    {
        "slug": "subaraw-national-hiphop-dance-competition-2026",
        "category": "Festival",
        "title": "Twelve teams compete in Subaraw National Hiphop Dance Competition 2026",
        "summary": (
            "Astrophile of Ormoc City won the national title, besting teams from "
            "Palawan and other provinces at the Edward S. Hagedorn Coliseum."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 12),
        "body": [
            "Twelve dance teams from Puerto Princesa, Palawan, and other provinces competed in the Subaraw National Hiphop Dance Competition 2026 on November 9.",
            "Astrophile from Ormoc City, Leyte took the championship and a PHP 150,000 cash prize. KNGS of Puerto Princesa placed second, while Hype Impact of Olongapo City finished third.",
            "OBS Palawan of Narra won the special showdown. Teams outside the top three received a PHP 25,000 consolation prize.",
            "The city congratulated all dancers for their preparation, teamwork, and energy, and thanked the audience who filled the coliseum.",
        ],
    },
    {
        "slug": "city-peso-bread-making-training",
        "category": "Livelihood",
        "title": "City Peso runs bread-making training for women in Barangay Masikap",
        "summary": (
            "Around 25 women, including solo parents, completed a five-day skills "
            "training aimed at opening new livelihood opportunities."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 10),
        "body": [
            "The City Public Employment Service Office (PESO) organized a five-day bread-making skills training for about 25 women in Barangay Masikap, including young mothers and solo parents.",
            "The training ran from November 5 to 9, 2026 at the barangay covered gym under PESO manager Demetrio Lopez.",
            "Participants learned practical techniques for preparing different kinds of bread and discussed how to turn the skills into a small household business.",
            "The city continues to bring livelihood programs closer to barangays as part of its employment and enterprise support efforts.",
        ],
    },
    {
        "slug": "subaraw-drum-and-lyre-competition",
        "category": "Festival",
        "title": "San Jose NHS and Francisco Ubay Elementary win Subaraw drum and lyre contest",
        "summary": (
            "The two schools topped their divisions in a competition that filled the "
            "festival with music, color, and school pride."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 10),
        "body": [
            "San Jose National High School and Francisco Ubay Memorial Elementary School won their respective divisions in the Subaraw Drum and Lyre Competition.",
            "The high school division also recognized excellence in keyboard percussion, drum line, music, color guard, baton twirling, drill design, and visual performance.",
            "In the elementary division, Sta. Monica Elementary School and Sicsican Elementary School received special awards for conductor, uniform, and general effects.",
            "The city praised the students and their coaches for the discipline and teamwork they showed during the festival.",
        ],
    },
    {
        "slug": "subaraw-national-music-championship-2027",
        "category": "Festival",
        "title": "Puerto Princesa to host Subaraw National Music Championship in 2027",
        "summary": (
            "The championship will serve as a qualifier for the Asian Music Games and "
            "is expected to bring more than 60 ensembles to the city."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 10),
        "body": [
            "Puerto Princesa will host the Subaraw National Music Championship in 2027, an official qualifying event for the Asian Music Games.",
            "The Philippine Drum and Lyre Associates Inc. said the championship may draw more than 60 ensembles and over 2,400 participants from cities, provinces, and its chapters nationwide.",
            "A local drum and lyre competition will be held a day before the national event so local groups can still compete and showcase their talents.",
            "The announcement supports Mayor Bayron's goal of expanding Subaraw into an international event and giving Filipino performers a larger stage.",
        ],
    },
    {
        "slug": "subaraw-festival-grows-as-national-event",
        "category": "Festival",
        "title": "Mayor Bayron: Subaraw Festival continues to grow as a national event",
        "summary": (
            "From a local celebration in Sabang, the festival now draws candidates, "
            "dancers, and designers from across the Philippines."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 10),
        "body": [
            "Mayor Lucilo R. Bayron said the Subaraw Biodiversity Festival has grown from a local celebration in Sabang into a national event.",
            "Speaking at SM City Puerto Princesa on November 6, the mayor noted that 22 of the 30 festival queen candidates came from outside Palawan, representing Luzon, Visayas, and Mindanao.",
            "The national hiphop competition and the Philippine Designers Competition also brought participants from other provinces.",
            "The mayor encouraged residents to watch and support the performers, and thanked SM management, organizers, sponsors, and partners for their help.",
        ],
    },
    {
        "slug": "new-school-stage-tagburos-elementary",
        "category": "Education",
        "title": "Tagburos Elementary School opens new stage under Bayanihan Program",
        "summary": (
            "The newly built stage will host school programs and give students a "
            "space to showcase their talents."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 9),
        "body": [
            "A new stage at Tagburos Elementary School was inaugurated on November 6, 2026 under the city's Bayanihan Program.",
            "Mayor Lucilo R. Bayron led the inauguration. The city said the stage will be used for school programs, performances, and community activities.",
            "The project is part of the city's continuing effort to address the needs of public schools and provide students with better spaces for learning and creative expression.",
        ],
    },
    {
        "slug": "subaraw-biodiversity-festival-grand-opening",
        "category": "Festival",
        "title": "Mayor Bayron leads Subaraw Biodiversity Festival 2026 grand opening",
        "summary": (
            "The festival opened with a parade, the sashing of 30 queen candidates, "
            "and the banging of the Subaraw gong."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 9),
        "body": [
            "Mayor Lucilo R. Bayron led the grand opening of the Subaraw Biodiversity Festival 2026 at the Edward S. Hagedorn Coliseum on November 7.",
            "The program opened with a drum and lyre parade from Robinsons Mall Palawan and continued with the sashing ceremony for the 30 festival queen candidates.",
            "The mayor also announced that Puerto Princesa will host a national drum and lyre competition in 2027.",
            "Festival activities included the elementary drum and lyre competition, hiphop eliminations, the Philippine Designers Competition, and a national go-kart race.",
        ],
    },
    {
        "slug": "subaraw-2026-preserving-nature",
        "category": "Environment",
        "title": "Mayor Bayron at Subaraw 2026: preserving nature is everyone's responsibility",
        "summary": (
            "The festival opened in Sitio Sabang with a thanksgiving mass, a community "
            "parade, and a call to protect the city's biodiversity."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 9),
        "body": [
            "Mayor Lucilo R. Bayron opened the Subaraw Biodiversity Festival 2026 in Sitio Sabang, Barangay Cabayugan on November 5 with a call for unity in protecting the environment.",
            "The celebration began with a thanksgiving mass at Santuario de San Jose Marello Parish and a community parade along Sabang Beach.",
            "The mayor said the festival is a reminder that preserving nature is the responsibility of every resident and that government cannot do it alone.",
            "Tourism officials and biodiversity advocates also visited the Puerto Princesa Subterranean River National Park and stressed that healthy forests and seas support both wildlife and livelihoods.",
        ],
    },
    {
        "slug": "bfp-courtesy-call-mayor-bayron",
        "category": "Public safety",
        "title": "BFP Puerto Princesa personnel pay courtesy call ahead of ASEAN deployment",
        "summary": (
            "The city fire team will join the BFP contingent providing fire safety "
            "and emergency response at the 49th ASEAN Summit."
        ),
        "author": "City Information Office",
        "date": date(2026, 11, 4),
        "body": [
            "Personnel of the Bureau of Fire Protection Puerto Princesa City Fire Station paid a courtesy call on Mayor Lucilo R. Bayron on November 4.",
            "The team, led by City Fire Marshal Angel Lynn B. Salvador, will join the BFP contingent deployed for the 49th ASEAN Summit and Related Summits in Pasay City.",
            "Their mission covers fire safety, emergency response, and hazardous materials services during the international gatherings.",
            "Mayor Bayron recognized the professionalism of the city's uniformed personnel and wished them a safe and successful deployment.",
        ],
    },
]
