from data.storage import get_last_messages
from analysis.analyzer import analyze_conversation


BATCH_SIZE = 20



def process_batch_if_needed(message_count):
    if message_count % BATCH_SIZE != 0:
        return
    
    messages = get_last_messages(BATCH_SIZE)

    if not messages:
        return
    
    analyze_conversation(messages)