import openai
from typing import List, Optional
from config import settings
import asyncio

class LLMProcessor:
    def __init__(self):
        self.client = None
        self.groq_client = None
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize OpenAI and Groq clients"""
        try:
            # Try Groq first (faster)
            if settings.groq_api_key:
                try:
                    import groq
                    self.groq_client = groq.Groq(api_key=settings.groq_api_key)
                    print("✅ Groq client initialized successfully (Primary)")
                except Exception as e:
                    print(f"Groq initialization failed: {e}")
                    self.groq_client = None
            
            # Try OpenAI as fallback
            if settings.openai_api_key:
                try:
                    import httpx
                    http_client = httpx.Client()
                    self.client = openai.OpenAI(
                        api_key=settings.openai_api_key,
                        http_client=http_client
                    )
                    print("✅ OpenAI client initialized successfully (Fallback)")
                except Exception as e:
                    print(f"OpenAI initialization failed: {e}")
                    self.client = None
            
            if not self.client and not self.groq_client:
                print("Warning: No LLM service available")
                
        except Exception as e:
            print(f"Warning: LLM client initialization failed: {e}")
            self.client = None
            self.groq_client = None
    
    async def generate_answer(self, question: str, context: str) -> str:
        """Generate answer using LLM with optimized prompt"""
        try:
            # Create optimized prompt for faster response
            prompt = f"""Answer this question based on the context. Be concise and accurate.

Context: {context[:1500]}  # Limit context length for speed

Question: {question}

Answer:"""
            
            # Try Groq first (faster)
            if self.groq_client:
                try:
                    response = self.groq_client.chat.completions.create(
                        model="llama3-8b-8192",  # Fast model
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant. Answer questions accurately and concisely."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1000,  # Reduced for speed
                        temperature=0.1
                    )
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    print(f"Groq generation failed: {e}")
            
            # Try OpenAI as fallback
            if self.client:
                try:
                    response = self.client.chat.completions.create(
                        model=settings.llm_model,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant. Answer questions accurately and concisely."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=settings.max_tokens,
                        temperature=settings.temperature
                    )
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    print(f"OpenAI generation failed: {e}")
            
            return "LLM service not available. Please check configuration."
            
        except Exception as e:
            print(f"Warning: LLM generation failed: {e}")
            return f"Error generating answer: {str(e)}"
    
    async def generate_answers_batch(self, questions: List[str], contexts: List[str]) -> List[str]:
        """Generate answers for multiple questions with parallel processing"""
        try:
            if not self.client and not self.groq_client:
                return ["LLM service not available. Please check configuration."] * len(questions)
            
            # Process in parallel for speed
            tasks = []
            for question, context in zip(questions, contexts):
                task = self.generate_answer(question, context)
                tasks.append(task)
            
            answers = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle any exceptions
            processed_answers = []
            for answer in answers:
                if isinstance(answer, Exception):
                    processed_answers.append(f"Error: {str(answer)}")
                else:
                    processed_answers.append(answer)
            
            return processed_answers
            
        except Exception as e:
            print(f"Warning: Batch LLM generation failed: {e}")
            return [f"Error generating answers: {str(e)}"] * len(questions) 