# sc_ptech
Web scraped all available abstracts from The Journal of Petroleum Technology 

# Create the environment
conda env create -f sc_ptech_env.yml

# Update the environment
conda env update -f sc_ptech_env.yml

# Activate the environment
conda activate sc_ptech_env
# Deactivate the environment
conda deactivate

conda remove --name sc_ptech_env --all