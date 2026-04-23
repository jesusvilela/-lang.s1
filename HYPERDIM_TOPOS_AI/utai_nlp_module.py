import requests
import json

class UTAINLPModule:
    def __init__(self, base_url="http://192.168.56.1:1234/v1"):
        self.base_url = base_url

    def query(self, prompt, system_prompt="You are a Topos AI researcher specializing in hyperdimensional geometry."):
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }
        try:
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Exception: {str(e)}"

    def get_geometric_tendril(self, association):
        """Recover a geometric section from a symbolic association via LLM knowledge."""
        prompt = f"Map the following concept to an 8D coordinate vector (norm < 0.999): '{association}'"
        result = self.query(prompt, system_prompt="Output ONLY a JSON list of 8 floats.")
        try:
            return json.loads(result)
        except:
            # Fallback to random section if parsing fails
            return [0.1] * 8

if __name__ == "__main__":
    nlp = UTAINLPModule()
    print("Testing UTAI NLP Module...")
    print(nlp.query("What is the stability condition for a Z/k graded sheaf?"))
