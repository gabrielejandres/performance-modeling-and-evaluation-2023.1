from scipy.stats import norm
from math import *
import numpy as np
 
# Given information
mean = 0
std_dev = sqrt(100/3)
total_sources = 100
score = 10
 
# Calculate z-score for 10
z_score = (score - mean) / std_dev
 
# Calculate the probability of getting a noise less than 10
probability = norm.cdf(z_score)
 
# Print the result
print(f"P(|S| < 10) = {round(probability * 100, 2)}%")