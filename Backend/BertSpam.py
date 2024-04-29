from transformers import BertTokenizer, BertModel
import torch


def BertSpam(data):
    # Load pre-trained BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    # Example input text
    input_texts = data

    # Initialize list to store sentence embeddings
    sentence_embeddings = []

    # Iterate over each input text
    for input_text in input_texts:
        # Tokenize input text
        tokens = tokenizer.tokenize(input_text)
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        token_ids = torch.tensor(token_ids).unsqueeze(0)  # Add batch dimension

        # Forward pass through BERT model
        outputs = model(token_ids)

        # Extract embeddings
        last_hidden_states = outputs.last_hidden_state
        # Take the mean of embeddings across all tokens
        # mean_embedding = torch.mean(last_hidden_states, dim=1).squeeze(0)

        mean_embedding = torch.mean(last_hidden_states).item()

        # Append mean embedding to sentence_embeddings list
        sentence_embeddings.append(mean_embedding)
    return sentence_embeddings


