mkdir model
mkdir audio
wget /model https://huggingface.co/balacoon/tts/resolve/main/en_us_hifi92_light_cpu.addon
# wget /model https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/ggml-model-q4_k.gguf
wget /model https://huggingface.co/TheBloke/orca_mini_v3_7B-GGUF/resolve/main/orca_mini_v3_7b.Q4_K_M.gguf

wget https://huggingface.co/stabilityai/stablelm-2-zephyr-1_6b/blob/main/stablelm-2-zephyr-1_6b-Q5_K_M.gguf