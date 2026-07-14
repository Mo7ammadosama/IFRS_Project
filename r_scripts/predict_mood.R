# ============================
# R Script: predict_mood.R
# Input : JSON list of answers from Django
# Output: Mood string (Excited / Neutral / Sad)
# ============================

library(jsonlite)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  stop("No JSON data passed from Django")
}

# Convert JSON array to R list
answers <- fromJSON(args[1])

# Count positive answers
positive <- sum(answers == "yes")

# Mood logic
if (positive >= 5) {
  mood <- "Excited"
} else if (positive >= 3) {
  mood <- "Neutral"
} else {
  mood <- "Sad"
}

cat(mood)
