import torch
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM
from optimum.bettertransformer import BetterTransformer

from llmpool.model import LLModel
from transformers import GenerationConfig

class LocalAlpaca(LLModel):
    def __init__(self, name, base):
        super().__init__(name)

        self.tokenizer = LlamaTokenizer.from_pretrained(base)
        self.tokenizer.pad_token_id = 0
        self.tokenizer.padding_side = "left"

        self.model = LlamaForCausalLM.from_pretrained(
            base,
            load_in_8bit=False if multi_gpu else True,
            device_map="auto",
        )
        
        if multi_gpu:
            self.model.half()
        # model = BetterTransformer.transform(model)

    def stream_gen(self, gen_config: GenerationConfig):
        pass

    def batch_gen(self, gen_config: GenerationConfig):
        pass
    

class LocalAlpacaLoRA(LocalAlpaca):
    def __init__(self, name, base, ckpt):
        super().__init__(name, base)

        self.model = PeftModel.from_pretrained(
            self.model, ckpt, 
            device_map={'': 0}
        )