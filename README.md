# Interactive Prompt Playground

An interactive tool for experimenting with OpenAI API parameters in real-time. Test different parameter combinations, observe their effects on product descriptions, and keep track of your experiments.

## ⚠️ Important Notes for Free Tier Users

Before using this playground, please be aware:

1. **Model Availability**:
   - Free tier only has access to `gpt-3.5-turbo`
   - `gpt-4` requires special access from OpenAI
   - The playground will automatically show only available models

2. **API Rate Limits**:
   - Free tier is limited to 3 requests per minute (RPM)
   - Each experiment counts as one request
   - The script includes automatic error handling

3. **Cost Information**:
   - Free tier starts with $5 worth of credits
   - Each `gpt-3.5-turbo` request costs about $0.0015 per 1K tokens
   - Average experiment uses 100-200 tokens ($0.0002-0.0003)
   - Cost is shown before each request

## Features

- **Interactive Parameter Selection**:
  - Model selection (based on your API access)
  - Temperature (0.0 - 2.0)
    - Lower: More focused/deterministic
    - Higher: More creative/random
  - Max tokens (1 - 4096)
    - Controls response length
  - Presence penalty (-2.0 to 2.0)
    - Controls topic repetition
  - Frequency penalty (-2.0 to 2.0)
    - Controls vocabulary diversity
  - Stop sequences
    - Customize where the response ends
    - Add multiple stop sequences
    - Examples: ".", "!", "\n"

- **Real-time Testing**:
  - Immediate response preview
  - Cost estimation before sending request
  - Clear display of current parameters
  - Error handling and feedback

- **Results Tracking**:
  - Automatic logging of all experiments
  - Parameter comparison grid
  - Output comparison table
  - Automatic parameter effect analysis
  - Timestamp for each test

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/interactive-prompt-playground.git
cd interactive-prompt-playground
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Unix/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

## Usage

1. Start the playground:
```bash
python prompt_playground.py
```

2. Enter a product name when prompted
   - Example: "Tesla Model 3" or "iPhone 15 Pro"

3. Select your parameters:
   - Choose the available model
   - Set temperature
   - Adjust max tokens
   - Configure penalties
   - Add stop sequences

4. Review and send:
   - Check estimated cost
   - Confirm parameters
   - Send request

5. Analyze results:
   - View generated description
   - Compare with previous results
   - See parameter comparison grid
   - Results automatically saved to log

## Understanding the Results

Each experiment is logged with:
- Timestamp
- Model used
- All parameter values
- Generated output
- Cost and token usage

Results are saved in a markdown file (`results_[timestamp].md`) containing:
1. Parameter comparison table
2. Grid view of outputs
3. Complete test history
4. AI-generated analysis of parameter effects (after 2+ experiments)

## Tips for Effective Testing

1. **Start Simple**:
   - Begin with default parameters
   - Change one parameter at a time
   - Note the effects of each change

2. **Cost Management**:
   - Check estimated cost before sending
   - Monitor total usage
   - Start with small max_tokens values
   - Increase gradually as needed

3. **Parameter Guidelines**:
   - Temperature: Start at 0.7
   - Max tokens: Start at 50-100
   - Penalties: Start at 0.0
   - Stop sequences: Test with and without

4. **Rate Limit Handling**:
   - Wait a few seconds between requests
   - If you hit rate limits, the script will notify you
   - Consider spacing out your experiments

## License

MIT License - feel free to use and modify as needed. 