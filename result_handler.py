from services import get_wikipedia_info, get_facts, get_youtube_videos

def handle_vqa_result(answer):
    extra_info = []
    extra_facts = []
    source_url = None
    info_videos = []
    fact_videos = []

    if answer.lower() in ['yes', 'no']:
        # For yes/no answers, keep everything empty
        pass
    elif answer.isnumeric():
        # For numeric answers, get Wikipedia info and facts, no videos
        extra_info = get_wikipedia_info(answer)
        facts_result = get_facts(answer)
        extra_facts = facts_result['facts']
        source_url = facts_result['source_url']
    else:
        # For other text answers, get full information including videos
        extra_info = get_wikipedia_info(answer)
        facts_result = get_facts(answer)
        extra_facts = facts_result['facts']
        source_url = facts_result['source_url']
        embedded_videos = get_youtube_videos(answer)
        
        # Split videos for two different sections
        info_videos = embedded_videos[:2]
        fact_videos = embedded_videos[2:4]

    return extra_info, extra_facts, source_url, info_videos, fact_videos